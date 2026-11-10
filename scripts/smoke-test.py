#!/usr/bin/env python3
"""Use actual VLESS REALITY outbound; verify egress and proxy-side DNS."""
import os
from pathlib import Path
import subprocess
import sys
import time
os.umask(0o077)
root = Path(__file__).resolve().parent.parent
expected = sys.argv[1]
config = root / '.secrets/client.json'
subprocess.run([str(root / '.artifacts/xray'), 'run', '-test', '-config', str(config)],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
with open(root / '.secrets/client-test.log', 'w') as log:
    process = subprocess.Popen([str(root / '.artifacts/xray'), 'run', '-config', str(config)], stdout=log, stderr=log)
    try:
        time.sleep(2)
        assert process.poll() is None, 'Local Xray exited'
        for url in ['https://api.ipify.org', 'https://icanhazip.com']:
            response = subprocess.check_output(['curl', '--fail', '--silent', '--show-error', '--max-time', '35',
                '--noproxy', '', '--proxy', 'socks5h://127.0.0.1:10808', url], text=True).strip()
            assert response == expected, 'Unexpected tunnel exit IP'
            print('PASS real VLESS+REALITY: HTTPS request, proxy-side DNS, exit IP ' + response)
    finally:
        process.terminate()
        process.wait(timeout=10)
