#!/usr/bin/env python3
"""Fetch client-only credentials through SSH and write local private artifacts."""
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.parse
import qrcode
os.umask(0o077)
host = sys.argv[1]
key = os.path.expanduser(sys.argv[2] if len(sys.argv) > 2 else '~/.ssh/id_ed25519')
ssh = ['ssh', '-F', '/dev/null', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
       '-o', 'UpdateHostKeys=no', '-i', key, 'vpnadmin@' + host]
client = json.loads(subprocess.check_output(ssh + ['sudo -n cat /etc/xray/client.json']))
root = (Path(sys.argv[3]).expanduser().resolve() if len(sys.argv) > 3
        else Path(__file__).resolve().parent.parent / '.secrets')
root.mkdir(mode=0o700, parents=True, exist_ok=True)
params = {'encryption': 'none', 'flow': 'xtls-rprx-vision', 'security': 'reality',
          'sni': client['serverName'], 'fp': 'chrome', 'pbk': client['publicKey'],
          'sid': client['shortId'], 'type': 'tcp', 'spx': '/'}
uri = 'vless' + '://' + client['uuid'] + '@' + host + ':443?' + urllib.parse.urlencode(params) + '#' + urllib.parse.quote(sys.argv[4] if len(sys.argv) > 4 else 'VPS-' + host)
(root / 'connection.txt').write_text(uri + '\n')
qrcode.make(uri).save(root / 'connection.png')
config = {'log': {'loglevel': 'warning', 'access': 'none'},
          'inbounds': [{'listen': '127.0.0.1', 'port': 10808, 'protocol': 'socks', 'settings': {'udp': True}}],
          'outbounds': [{'protocol': 'vless', 'settings': {'vnext': [{'address': host, 'port': 443,
              'users': [{'id': client['uuid'], 'encryption': 'none', 'flow': 'xtls-rprx-vision'}]}]},
              'streamSettings': {'network': 'raw', 'security': 'reality', 'realitySettings': {
                  'serverName': client['serverName'], 'fingerprint': 'chrome',
                  'password': client['publicKey'], 'shortId': client['shortId'], 'spiderX': '/'}}}]}
(root / 'client.json').write_text(json.dumps(config, indent=2) + '\n')
for path in root.iterdir():
    if path.is_file():
        path.chmod(0o600)
print('Client config, URI and QR written under .secrets/; credentials not printed')
