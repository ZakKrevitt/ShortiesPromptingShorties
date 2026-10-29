#!/usr/bin/env python3
"""Collect a user's fal key locally without echoing it or making a network request."""
import argparse
import getpass
import sys
from settings import save_key


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    if not sys.stdin.isatty():
        raise SystemExit('Run this command in your own interactive terminal. Do not send a key through chat or stdin automation.')
    print('The key will be stored outside the repository in a private local plaintext file.')
    key = getpass.getpass('Your fal API key (hidden; empty cancels): ').strip()
    if not key:
        print('Cancelled; no credentials changed.')
        return
    try:
        path = save_key(key)
    except (ValueError, OSError):
        raise SystemExit('Could not save the credential. Check the key format and local file permissions.') from None
    print(f'Credential saved at {path}. No API request was made.')


if __name__ == '__main__':
    main()
