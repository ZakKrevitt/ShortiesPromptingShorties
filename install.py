#!/usr/bin/env python3
"""Install only the public skill; never read credentials or overwrite a skill."""
import argparse
import os
from pathlib import Path
import shutil


def install(skills_directory):
    source = Path(__file__).resolve().parent / 'skills' / 'podcast-animation'
    target = Path(skills_directory).expanduser().resolve() / source.name
    if target.exists() or target.is_symlink():
        raise FileExistsError(f'Existing skill preserved: {target}')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills'
    parser.add_argument('--dest', type=Path, default=default, help='Codex skills directory')
    args = parser.parse_args()
    try:
        target = install(args.dest)
    except FileExistsError as error:
        parser.exit(1, str(error) + '\n')
    print(f'Installed Podcast Animation at {target}. Available on your next Codex turn.')


if __name__ == '__main__':
    main()
