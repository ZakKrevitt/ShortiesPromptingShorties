#!/usr/bin/env python3
"""Assemble generated shots over original podcast audio. No network or generation calls."""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile


def positive(value, label, allow_zero=False):
    n = float(value)
    if not math.isfinite(n) or n < 0 or (n == 0 and not allow_zero):
        raise ValueError(f'{label} must be a finite positive number')
    return n


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--ffmpeg', default=shutil.which('ffmpeg'))
    args = parser.parse_args()
    if not args.ffmpeg:
        parser.error('FFmpeg is required; use --ffmpeg /path/to/ffmpeg')
    output = args.output.resolve()
    if output.exists():
        parser.error('Output already exists; choose a new filename')
    manifest = args.manifest.resolve()
    data = json.loads(manifest.read_text())
    root = manifest.parent
    source = (root / data['source']).resolve(strict=True)
    shots = data['shots']
    if not shots or len(shots) > 30:
        raise ValueError('Provide 1 to 30 shots')
    width, height, fps = (int(data.get(k, v)) for k, v in [('width', 720), ('height', 1280), ('fps', 24)])
    if not (16 <= width <= 3840 and 16 <= height <= 3840 and width % 2 == height % 2 == 0 and 1 <= fps <= 60):
        raise ValueError('Use even output dimensions from 16 to 3840 and 1 to 60 fps')
    cmd = [args.ffmpeg, '-n', '-v', 'error']
    filters, total = [], 0.0
    for i, shot in enumerate(shots):
        path = (root / shot['path']).resolve(strict=True)
        start = positive(shot.get('start', 0), 'shot start', True)
        end = positive(shot['end'], 'shot end')
        duration = positive(shot['duration'], 'shot duration')
        if end <= start:
            raise ValueError('Each shot end must follow its start')
        cmd += ['-i', str(path)]
        filters.append(f'[{i}:v]trim=start={start}:end={end},setpts=(PTS-STARTPTS)*{duration}/{end-start},scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1,fps={fps},tpad=stop_mode=clone:stop_duration={duration},trim=duration={duration},setpts=PTS-STARTPTS[v{i}]')
        total += duration
    audio_start = positive(data.get('audio_start', 0), 'audio start', True)
    cmd += ['-ss', str(audio_start), '-i', str(source)]
    filters.append(''.join(f'[v{i}]' for i in range(len(shots))) + f'concat=n={len(shots)}:v=1:a=0,format=yuv420p[joined]')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='podcast-assembly-') as tmp:
        video_label = '[joined]'
        if data.get('captions'):
            shutil.copyfile((root / data['captions']).resolve(strict=True), Path(tmp) / 'captions.ass')
            filters.append('[joined]ass=captions.ass[captioned]')
            video_label = '[captioned]'
        cmd += ['-filter_complex', ';'.join(filters), '-map', video_label, '-map', f'{len(shots)}:a:0',
                '-t', str(total), '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
                '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', str(output)]
        subprocess.run(cmd, cwd=tmp, check=True)
    ffprobe = str(Path(args.ffmpeg).resolve().with_name('ffprobe'))
    if not Path(ffprobe).exists():
        ffprobe = shutil.which('ffprobe')
    if ffprobe:
        probe = subprocess.check_output([ffprobe, '-v', 'error', '-show_entries',
            'format=duration,size:stream=codec_name,width,height,r_frame_rate', '-of', 'json', str(output)], text=True)
        output.with_suffix('.probe.json').write_text(probe)
    print(output)


if __name__ == '__main__':
    main()
