"""Local credential access. Never returns secret values in diagnostics."""
import json
import os
from pathlib import Path
import tempfile


def credentials_path():
    return Path.home() / '.config' / 'podcast-animation' / 'fal.json'


def load_key():
    value = os.environ.get('FAL_KEY', '').strip()
    if value:
        return value
    path = credentials_path()
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding='utf-8'))
    value = data.get('fal_key', '')
    return value.strip() if isinstance(value, str) and value.strip() else None


def save_key(value):
    if not isinstance(value, str) or not value.strip() or any(c.isspace() for c in value):
        raise ValueError('Enter a nonempty key without whitespace.')
    path = credentials_path()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.parent.chmod(0o700)
    name = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as output:
            name = Path(output.name)
            os.chmod(name, 0o600)
            json.dump({'fal_key': value}, output)
            output.write('\n')
            output.flush()
            os.fsync(output.fileno())
        os.replace(name, path)
    finally:
        if name is not None and name.exists():
            name.unlink()
    return path
