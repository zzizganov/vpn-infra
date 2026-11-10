#!/usr/bin/env python3
"""Fetch only pinned official release bytes, verify SHA256, extract binary."""
import hashlib
import json
import os
from pathlib import Path
import urllib.request
import zipfile
root = Path(__file__).resolve().parent.parent
pin = json.loads((root / 'xray-release.json').read_text())
url = pin['url']
assert url.startswith('https://github.com/XTLS/Xray-core/releases/download/')
cache = root / '.artifacts'
cache.mkdir(mode=0o700, exist_ok=True)
archive = cache / 'xray.zip'
if not archive.exists() or hashlib.sha256(archive.read_bytes()).hexdigest() != pin['sha256']:
    with urllib.request.urlopen(url, timeout=90) as response:
        archive.write_bytes(response.read())
assert hashlib.sha256(archive.read_bytes()).hexdigest() == pin['sha256'], 'Checksum mismatch'
with zipfile.ZipFile(archive) as z:
    (cache / 'xray').write_bytes(z.read('xray'))
os.chmod(cache / 'xray', 0o755)
print('Pinned official release checksum verified')
