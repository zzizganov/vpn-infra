# vpn-infra

Shared Ansible/Bash infrastructure for two independent VLESS + REALITY servers: **Singapore** and **Амстердам**. Read [PROJECT_STATE.md](PROJECT_STATE.md) for deployed state and [AGENTS.md](AGENTS.md) for agent instructions. The GitHub repository remains private under its existing name.

```text
hosts/
  singapore/   README.md, inventory.example.ini, local inventory.ini
  amsterdam/   README.md, inventory.example.ini, local inventory.ini
inventories/   production.example.ini, local production.ini
.secrets/      singapore/, amsterdam/ — local credentials and QR, never in Git
playbooks/     bootstrap.yml, security.yml, xray.yml, verify.yml
scripts/       shared export, validation and diagnostics
```

Working baseline: TCP/443, VLESS, REALITY, Vision, mirror.init7.net SNI/target, chrome fingerprint, **spx=/ and spiderX=/**. The user reported successful connectivity after spx was added. Each host retains its own UUID and keypair. Device TUN/DNS leak testing remains outstanding.

## Use

Run from this Git checkout. Install requirements in a local virtual environment. Copy inventories/production.example.ini to inventories/production.ini and review host/key settings; optionally use hosts/<site>/inventory.ini for a single host. Verify SSH host fingerprints independently and unlock the local key through ssh-agent. Credentials must never enter inventory or command arguments.

```bash
python3 scripts/prepare-artifacts.py
ansible-playbook playbooks/verify.yml
ansible-playbook playbooks/xray.yml --limit singapore
ansible-playbook playbooks/xray.yml --limit amsterdam
python3 scripts/export-client.py 45.130.165.105
python3 scripts/export-client.py 185.247.117.108
python3 scripts/smoke-test.py 45.130.165.105
python3 scripts/smoke-test.py 185.247.117.108
```

Exports default to .secrets/singapore/ or .secrets/amsterdam/. Keep the Amsterdam display name when exporting explicitly:

```bash
python3 scripts/export-client.py 185.247.117.108 ~/.ssh/id_ed25519 .secrets/amsterdam 'Амстердам'
```

Fresh-server provisioning: run bootstrap.yml as the initial administrator, independently verify the created vpnadmin key and sudo access, switch the selected inventory to vpnadmin, then run security.yml, xray.yml and verify.yml. Existing servers already use vpnadmin; do not re-enable root/password SSH.

CI only validates syntax and scans for secrets; it has no production access. Singapore's Ubuntu 20.04 without Pro is an accepted temporary experiment; use Ubuntu 24.04 for persistent new installations.

[Setup](docs/SETUP.md) · [Security](docs/SECURITY.md) · [Clients](docs/CLIENTS.md) · [Operations](docs/OPERATIONS.md) · [Recovery](docs/RECOVERY.md) · [Troubleshooting](docs/TROUBLESHOOTING.md) · [Amsterdam history](docs/ALTERNATE-VPS.md)
