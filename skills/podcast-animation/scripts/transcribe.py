#!/usr/bin/env python3
"""Optional local timed transcription; uses FFmpeg to avoid container-decoder differences."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--language', help='Known source language; omit for detection')
    parser.add_argument('--model', default='small', help='Multilingual faster-whisper model; downloaded on first use')
    parser.add_argument('--ffmpeg', default=shutil.which('ffmpeg'))
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; choose a new filename')
    if not args.ffmpeg or not args.input.is_file():
        parser.error('A local input and FFmpeg are required')
    try:
        import numpy as np
        from faster_whisper import WhisperModel
    except ImportError:
        parser.error('Install faster-whisper in your project environment first')
    model = WhisperModel(args.model, device='cpu', compute_type='int8', cpu_threads=4)
    raw = subprocess.check_output([args.ffmpeg, '-v', 'error', '-i', str(args.input), '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'])
    segments, info = model.transcribe(np.frombuffer(raw, dtype='<f4'), language=args.language, word_timestamps=True)
    result = {'source': str(args.input.resolve()), 'language': info.language, 'language_probability': info.language_probability,
              'segments': [{'start': s.start, 'end': s.end, 'text': s.text,
                            'words': [{'start': w.start, 'end': w.end, 'word': w.word} for w in s.words or []]} for s in segments]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as output:
        json.dump(result, output, ensure_ascii=False, indent=2)
    print(args.output)


if __name__ == '__main__':
    main()
