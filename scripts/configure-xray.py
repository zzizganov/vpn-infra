#!/usr/bin/env python3
"""Generate persistent server-side secrets and atomically validate/apply config."""
import json, os, pathlib, secrets, shutil, subprocess, sys, uuid
os.umask(0o077)
root = pathlib.Path('/etc/xray')
secret_path = root / 'secrets.json'
if secret_path.exists():
    secret = json.loads(secret_path.read_text())
else:
    result = subprocess.check_output(['/usr/local/bin/xray', 'x25519'], text=True)
    fields = dict(line.split(':', 1) for line in result.strip().splitlines())
    secret = {'uuid': str(uuid.uuid4()), 'shortId': secrets.token_hex(8),
              'privateKey': fields['PrivateKey'].strip(),
              'publicKey': fields.get('Password (PublicKey)', fields.get('Password', fields.get('PublicKey', ''))).strip()}
    assert secret['publicKey']
    fd = os.open(str(secret_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as out:
        json.dump(secret, out)
name = sys.argv[1]
config = {'log': {'loglevel': 'warning', 'access': 'none'}, 'inbounds': [{
    'listen': '0.0.0.0', 'port': 443, 'protocol': 'vless',
    'settings': {'clients': [{'id': secret['uuid'], 'flow': 'xtls-rprx-vision'}], 'decryption': 'none'},
    'streamSettings': {'network': 'raw', 'security': 'reality', 'realitySettings': {
        'show': False, 'target': name + ':443', 'xver': 0, 'serverNames': [name],
        'privateKey': secret['privateKey'], 'shortIds': [secret['shortId']]}}}],
    'outbounds': [{'protocol': 'freedom', 'tag': 'direct'}, {'protocol': 'blackhole', 'tag': 'block'}],
    'routing': {'rules': [{'type': 'field', 'ip': ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16',
        '127.0.0.0/8', '169.254.0.0/16', '::1/128', 'fc00::/7', 'fe80::/10'], 'outboundTag': 'block'}]}}
data = json.dumps(config, indent=2) + '\n'
dest = root / 'config.json'
if not dest.exists() or dest.read_text() != data:
    temp = root / 'config.pending.json'
    temp.write_text(data)
    try:
        subprocess.run(['/usr/local/bin/xray', 'run', '-test', '-config', str(temp)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if dest.exists():
            shutil.copy2(dest, root / 'config.previous.json')
        os.chmod(temp, 0o640)
        shutil.chown(temp, user='root', group='xray')
        os.replace(temp, dest)
    finally:
        temp.unlink(missing_ok=True)
    print('CHANGED')
# This file deliberately excludes the server private key; still a client credential.
client = {k: v for k, v in secret.items() if k != 'privateKey'}
client['serverName'] = name
(root / 'client.json').write_text(json.dumps(client))
os.chmod(root / 'client.json', 0o600)
