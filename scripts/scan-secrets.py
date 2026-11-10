#!/usr/bin/env python3
"""Scan explicit tracked/staged repository content, never print offending lines."""
import pathlib
import re
import subprocess
import sys
repo = pathlib.Path.cwd()
paths = subprocess.check_output(['git', 'ls-files', '-z'], text=True).split('\0')
patterns = [r'-----BEGIN (?:OPENSSH|RSA|EC|PRIVATE).*?KEY-----',
            r'\b[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}\b',
            r'vless' + r'://[^\s]+', r'gh[pousr]_[A-Za-z0-9]{20,}',
            r'"privateKey"\s*:\s*"[A-Za-z0-9_-]{30,}"']
failed = []
for path in filter(None, paths):
    if path.startswith(('.secrets/', '.artifacts/', '.venv/')) or path == 'inventory.ini':
        failed.append(path)
        continue
    text = (repo / path).read_text(errors='replace')
    if any(re.search(pattern, text) for pattern in patterns):
        failed.append(path)
if failed:
    print('Potential secrets in files: ' + ', '.join(failed), file=sys.stderr)
    sys.exit(1)
print('Tracked content secret checks passed')
