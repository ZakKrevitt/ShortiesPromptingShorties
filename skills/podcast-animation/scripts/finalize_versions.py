#!/usr/bin/env python3
"""Deliver original and dubs; optionally silence a measured audio tail, never shorten video."""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile


def probe(path, ffprobe):
    return json.loads(subprocess.check_output([
        ffprobe, '-v', 'error', '-show_entries',
        'format=duration:stream=codec_type,width,height,r_frame_rate,duration,nb_frames',
        '-of', 'json', str(path)], text=True))


def video_hash(path, ffmpeg):
    return subprocess.check_output([
        ffmpeg, '-v', 'error', '-i', str(path), '-map', '0:v:0',
        '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-'], text=True).strip()


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{name} must be a finite number')
    return float(value)


def prepare(manifest, ffprobe):
    data = json.loads(manifest.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or not isinstance(data.get('original'), dict):
        raise ValueError('A source-language original is required')
    versions, extras = data.get('versions', []), data.get('extras', [])
    if not isinstance(versions, list) or not isinstance(extras, list):
        raise ValueError('versions and extras must be lists')
    raw = [('original', data['original'])] + [('dub', x) for x in versions] + [('extra', x) for x in extras]
    if len(raw) > 100:
        raise ValueError('Use at most 100 versions per delivery')
    names, languages, prepared = set(), set(), []
    for role, item in raw:
        if not isinstance(item, dict):
            raise ValueError('Each entry must be an object')
        name = item.get('filename', '')
        if (not isinstance(name, str) or Path(name).name != name or '/' in name or '\\' in name
                or name.startswith('.') or not name.lower().endswith('.mp4')
                or any(ord(c) < 32 for c in name)):
            raise ValueError('Use plain MP4 filenames without directories or control characters')
        if name.casefold() in names:
            raise ValueError('Duplicate output filename')
        names.add(name.casefold())
        language = item.get('language', '')
        if not isinstance(language, str) or not re.fullmatch(r'[a-zA-Z0-9-]{2,20}', language):
            raise ValueError('Give each entry a language code')
        if role != 'extra':
            if language.casefold() in languages:
                raise ValueError('Duplicate original/dub language')
            languages.add(language.casefold())
        source_name = item.get('source')
        if not isinstance(source_name, str) or not source_name:
            raise ValueError('Each entry needs a local source path')
        source = (manifest.parent / source_name).resolve(strict=True)
        if not source.is_file() or source.suffix.lower() != '.mp4':
            raise ValueError('Inputs must be final local MP4 files')
        info = probe(source, ffprobe)
        video = [s for s in info['streams'] if s['codec_type'] == 'video']
        audio = [s for s in info['streams'] if s['codec_type'] == 'audio']
        if len(video) != 1 or len(audio) != 1:
            raise ValueError('Each input must have exactly one video and one audio stream')
        duration = number(float(info['format']['duration']), 'duration')
        if duration <= 0:
            raise ValueError('Input duration must be positive')
        cutoff = item.get('mute_from')
        fade = number(item.get('fade_seconds', 0.02), 'fade_seconds')
        if not 0 < fade <= 1:
            raise ValueError('Use a fade longer than zero and no longer than one second')
        if cutoff is not None:
            cutoff = number(cutoff, 'mute_from')
            if not fade <= cutoff < duration:
                raise ValueError('Mute cutoff must leave the complete phrase and lie inside the video')
        prepared.append({'role': role, 'language': language, 'source': source, 'filename': name,
                         'mute_from': cutoff, 'fade_seconds': fade, 'probe': info})
    return prepared


def finalize(manifest, destination, ffmpeg, ffprobe, make_zip=False):
    manifest = Path(manifest).resolve(strict=True)
    destination = Path(destination).expanduser().resolve()
    report_path = Path(str(destination) + '.manifest.json')
    zip_path = Path(str(destination) + '.zip')
    for path in [destination, report_path] + ([zip_path] if make_zip else []):
        if path.exists() or path.is_symlink():
            raise FileExistsError(f'Existing output preserved: {path}')
    entries = prepare(manifest, ffprobe)  # Validate every input before creating output.
    destination.mkdir(parents=True)
    report = {'folder': str(destination), 'status': 'in_progress', 'files': []}
    def save():
        report_path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    save()
    for item in entries:
        source, output = item['source'], destination / item['filename']
        cutoff = item['mute_from']
        if cutoff is None:
            shutil.copy2(source, output)
        else:
            subprocess.run([
                ffmpeg, '-n', '-v', 'error', '-i', str(source), '-map', '0:v:0', '-map', '0:a:0',
                '-c:v', 'copy', '-af', f"afade=t=out:st={cutoff-item['fade_seconds']:.9f}:d={item['fade_seconds']:.9f}",
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(output)], check=True)
        after = probe(output, ffprobe)
        before_video = next(s for s in item['probe']['streams'] if s['codec_type'] == 'video')
        after_video = next(s for s in after['streams'] if s['codec_type'] == 'video')
        if before_video != after_video or video_hash(source, ffmpeg) != video_hash(output, ffmpeg):
            raise RuntimeError('Video stream changed; do not deliver this output')
        if abs(float(after['format']['duration']) - float(item['probe']['format']['duration'])) > 0.05:
            raise RuntimeError('Output duration changed unexpectedly')
        subprocess.run([ffmpeg, '-v', 'error', '-i', str(output), '-f', 'null', '-'], check=True)
        peak = None
        if cutoff is not None:
            margin = min(0.05, (float(after['format']['duration']) - cutoff) / 2)
            raw = subprocess.check_output([
                ffmpeg, '-v', 'error', '-ss', str(cutoff + margin), '-i', str(output),
                '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'])
            samples = array('f')
            samples.frombytes(raw)
            if sys.byteorder != 'little':
                samples.byteswap()
            peak = max(map(abs, samples), default=None)
            if peak is None or peak > 0.0001:
                raise RuntimeError('Tail silence could not be verified')
        report['files'].append({
            'role': item['role'], 'language': item['language'], 'file': output.name,
            'source': str(source), 'mute_from': cutoff,
            'fade_seconds': item['fade_seconds'] if cutoff is not None else None,
            'duration_seconds': float(after['format']['duration']), 'video_unchanged': True,
            'full_decode': 'passed', 'silent_tail_peak': peak, 'sha256': sha256(output)})
        save()
    if make_zip:
        with zipfile.ZipFile(zip_path, 'x', compression=zipfile.ZIP_STORED) as archive:
            for item in report['files']:
                archive.write(destination / item['file'], arcname=destination.name + '/' + item['file'])
        with zipfile.ZipFile(zip_path) as archive:
            if archive.testzip() is not None:
                raise RuntimeError('ZIP verification failed')
        report['zip'] = str(zip_path)
    report['status'] = 'complete'
    save()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--ffmpeg', default=shutil.which('ffmpeg'))
    parser.add_argument('--ffprobe', default=None)
    parser.add_argument('--zip', action='store_true')
    args = parser.parse_args()
    if not args.ffmpeg:
        parser.error('FFmpeg is required')
    sibling = Path(args.ffmpeg).resolve().with_name('ffprobe')
    ffprobe = args.ffprobe or (str(sibling) if sibling.is_file() else shutil.which('ffprobe'))
    if not ffprobe:
        parser.error('ffprobe is required')
    try:
        result = finalize(args.manifest, args.destination, args.ffmpeg, ffprobe, args.zip)
    except (ValueError, OSError, RuntimeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'{error}\nInputs were preserved. Inspect any partial delivery before retrying in a new folder.\n')
    print(json.dumps({'folder': result['folder'], 'files': len(result['files']), 'status': result['status']}))


if __name__ == '__main__':
    main()
