import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from array import array

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills' / 'podcast-animation' / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import settings
import doctor
import finalize_versions as delivery

spec = importlib.util.spec_from_file_location('public_installer', ROOT / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
FFMPEG, FFPROBE = shutil.which('ffmpeg'), shutil.which('ffprobe')


class SetupTests(unittest.TestCase):
    def test_install_is_isolated_and_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = installer.install(Path(tmp) / 'skills')
            self.assertTrue((target / 'SKILL.md').is_file())
            self.assertTrue((target / 'scripts' / 'finalize_versions.py').is_file())
            sentinel = target / 'my-local-note'
            sentinel.write_text('keep me')
            with self.assertRaises(FileExistsError):
                installer.install(Path(tmp) / 'skills')
            self.assertEqual(sentinel.read_text(), 'keep me')

    def test_private_key_storage_and_environment_precedence(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {}, clear=True):
            path = Path(tmp) / 'private' / 'fal.json'
            with patch.object(settings, 'credentials_path', return_value=path):
                self.assertIsNone(settings.load_key())
                settings.save_key('fixture-local-value')
                self.assertEqual(settings.load_key(), 'fixture-local-value')
                if os.name != 'nt':
                    self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
                    self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)
                with patch.dict(os.environ, {'FAL_KEY': 'fixture-environment-value'}):
                    self.assertEqual(settings.load_key(), 'fixture-environment-value')
                with self.assertRaises(ValueError):
                    settings.save_key('line one\nline two')

    def test_doctor_does_not_reveal_key(self):
        with patch.object(doctor, 'load_key', return_value='fixture-not-for-logs'):
            result = doctor.check()
        self.assertTrue(result['local_fal_key_present'])
        self.assertNotIn('fixture-not-for-logs', json.dumps(result))
        self.assertFalse(result['network_checked'])

    def test_configure_refuses_noninteractive_secret_input(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / 'configure.py')], input='', text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('interactive terminal', result.stderr)

    def test_skill_references_and_metadata(self):
        skill = ROOT / 'skills' / 'podcast-animation'
        import re
        for document in [skill / 'SKILL.md', *list((skill / 'references').glob('*.md'))]:
            for link in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                if '://' not in link and not link.startswith('#'):
                    self.assertTrue((document.parent / link.split('#')[0]).exists(), (document, link))
        self.assertIn('name: podcast-animation', (skill / 'SKILL.md').read_text())
        self.assertIn('$podcast-animation', (skill / 'agents' / 'openai.yaml').read_text())


@unittest.skipUnless(FFMPEG and FFPROBE, 'FFmpeg and ffprobe required for media fixtures')
class MediaTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source.mp4'
        # A complete tone, quiet pause, then an unwanted trailing tone.
        subprocess.run([
            FFMPEG, '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=160x90:rate=24:duration=4',
            '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=4',
            '-af', "volume=enable='between(t,1.8,2.8)':volume=0",
            '-c:v', 'libx264', '-preset', 'ultrafast', '-c:a', 'aac', '-shortest', str(self.source)
        ], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def manifest(self, **changes):
        data = {'original': {'source': 'source.mp4', 'filename': '01-original.mp4', 'language': 'en', 'mute_from': 2.5},
                'versions': [{'source': 'source.mp4', 'filename': '02-dub.mp4', 'language': 'hi', 'mute_from': 2.4}],
                'extras': [{'source': 'source.mp4', 'filename': '00-source.mp4', 'language': 'en', 'mute_from': None}]}
        data.update(changes)
        p = self.root / 'delivery.json'
        p.write_text(json.dumps(data))
        return p

    def amplitude(self, path, start, duration):
        samples = array('f')
        samples.frombytes(subprocess.check_output([FFMPEG, '-v', 'error', '-ss', str(start), '-i', str(path), '-t', str(duration), '-vn', '-ac', '1', '-f', 'f32le', '-']))
        if sys.byteorder != 'little':
            samples.byteswap()
        return max(map(abs, samples))

    def test_delivery_mutes_audio_and_preserves_original_video(self):
        dest = self.root / 'final'
        before = delivery.sha256(self.source)
        result = delivery.finalize(self.manifest(), dest, FFMPEG, FFPROBE, make_zip=True)
        self.assertEqual(len(result['files']), 3)
        self.assertEqual(result['status'], 'complete')
        self.assertEqual(delivery.sha256(self.source), before)
        self.assertEqual(delivery.sha256(dest / '00-source.mp4'), before)
        self.assertGreater(self.amplitude(dest / '01-original.mp4', .2, .5), .01)
        self.assertGreater(self.amplitude(self.source, 3, .5), .01)
        self.assertLess(self.amplitude(dest / '01-original.mp4', 3, .5), .0001)
        self.assertTrue(all(x['video_unchanged'] for x in result['files']))
        self.assertTrue(Path(result['zip']).is_file())
        with self.assertRaises(FileExistsError):
            delivery.finalize(self.root / 'delivery.json', dest, FFMPEG, FFPROBE)

    def test_invalid_cutoffs_do_not_create_output(self):
        for cutoff in [-1, 0, 5, float('nan'), True]:
            p = self.manifest(original={'source': 'source.mp4', 'filename': 'original.mp4', 'language': 'en', 'mute_from': cutoff})
            dest = self.root / 'invalid'
            with self.assertRaises(ValueError):
                delivery.finalize(p, dest, FFMPEG, FFPROBE)
            self.assertFalse(dest.exists())

    def test_duplicate_and_traversal_names_rejected(self):
        for name in ['01-ORIGINAL.mp4', '../escape.mp4', 'a\\b.mp4']:
            p = self.manifest(versions=[{'source': 'source.mp4', 'filename': name, 'language': 'hi'}])
            with self.assertRaises(ValueError):
                delivery.prepare(p, FFPROBE)

    def test_original_is_required(self):
        p = self.root / 'missing-original.json'
        p.write_text('{"versions": []}')
        with self.assertRaises(ValueError):
            delivery.prepare(p, FFPROBE)

    def test_assembly_keeps_source_audio(self):
        manifest = self.root / 'assembly.json'
        manifest.write_text(json.dumps({'source': 'source.mp4', 'width': 160, 'height': 90, 'fps': 24,
                                        'shots': [{'path': 'source.mp4', 'start': 0, 'end': 4, 'duration': 4}]}))
        out = self.root / 'assembled.mp4'
        subprocess.run([sys.executable, str(SCRIPTS / 'assemble.py'), str(manifest), str(out), '--ffmpeg', FFMPEG], check=True, capture_output=True)
        self.assertGreater(self.amplitude(out, .2, .5), .01)
        self.assertTrue(out.with_suffix('.probe.json').is_file())


if __name__ == '__main__':
    unittest.main()
