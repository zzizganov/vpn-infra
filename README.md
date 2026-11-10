# Singapore VLESS + REALITY infrastructure

Ansible + Bash, Xray-core on TCP/443, VLESS with `xtls-rprx-vision`, REALITY over RAW/TCP. No Docker or management API on the VPS. SSH remains on its existing port. Xray runs as an unprivileged service account; secrets originate on the server and survive reruns.

Architecture: device → encrypted REALITY connection → VPS:443 → Internet. REALITY target is independently checked for certificate validity, TLS 1.3 and H2 before deployment. Target/SNI defaults are examples and must pass this check from each new VPS.

## Quick start

Use Ubuntu 24.04 for persistent deployments. Ubuntu 20.04 here is an explicitly accepted temporary compatibility experiment; standard support has ended and Ubuntu Pro is not attached.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp inventory.example.ini inventory.ini
# Edit host, SSH identity, port and target. Verify host fingerprint independently.
python3 scripts/prepare-artifacts.py
ansible-playbook playbooks/bootstrap.yml
# Change ansible_user to vpnadmin in inventory.ini after bootstrap succeeds.
ansible-playbook playbooks/security.yml
ansible-playbook playbooks/xray.yml
ansible-playbook playbooks/verify.yml
python3 scripts/export-client.py SERVER_IP
python3 scripts/smoke-test.py SERVER_IP
```

If using an encrypted SSH key, load it into ssh-agent locally and export SSH_AUTH_SOCK. Never pass passwords, private keys or tokens in command arguments, repository files or CI variables. CI has no production credentials and cannot deploy.

See [setup](docs/SETUP.md), [security](docs/SECURITY.md), [clients](docs/CLIENTS.md), [operations](docs/OPERATIONS.md), [recovery](docs/RECOVERY.md), [troubleshooting](docs/TROUBLESHOOTING.md), and [verification results](docs/VERIFICATION.md).
