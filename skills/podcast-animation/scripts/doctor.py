#!/usr/bin/env python3
"""Report local prerequisites, without exposing credentials or contacting providers."""
import importlib.util
import json
import shutil
import sys
from settings import load_key


def check():
    try:
        key_present = bool(load_key())
        key_error = None
    except (ValueError, OSError):
        key_present, key_error = False, 'Local credential file could not be read.'
    return {
        'python_supported': sys.version_info >= (3, 10),
        'ffmpeg': bool(shutil.which('ffmpeg')),
        'ffprobe': bool(shutil.which('ffprobe')),
        'local_fal_key_present': key_present,
        'credential_error': key_error,
        'optional_fal_client': importlib.util.find_spec('fal_client') is not None,
        'optional_faster_whisper': importlib.util.find_spec('faster_whisper') is not None,
        'network_checked': False,
        'note': 'Presence does not verify account access or balance. Connected fal tools may supply credentials instead.',
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
