# Alternate VPS deployment

Branch: deploy/185-247-117-108. Target: 185.247.117.108, initial user root, SSH port 22. Deployment is explicitly authorized; audit the OS, listeners and existing services first. Keep the original VPS unchanged for provider/network comparison. Location and OS of the new VPS have not yet been verified.

Initial SSH requires a verified host fingerprint and the existing administrator public key appended through local ssh-copy-id. Never pass a password as a command argument or store it in inventory.

Use ignored inventory-alt.ini. Initially ansible_user=root. After bootstrap passes a fresh vpnadmin SSH/sudo check, change this inventory user to vpnadmin.

```bash
python3 scripts/prepare-artifacts.py
ansible-playbook -i inventory-alt.ini playbooks/bootstrap.yml
# Change ansible_user to vpnadmin in inventory-alt.ini.
ansible-playbook -i inventory-alt.ini playbooks/security.yml
ansible-playbook -i inventory-alt.ini playbooks/xray.yml
ansible-playbook -i inventory-alt.ini playbooks/verify.yml
python3 scripts/export-client.py 185.247.117.108 ~/.ssh/id_ed25519 ../.secrets/185.247.117.108
python3 scripts/smoke-test.py 185.247.117.108 ../.secrets/185.247.117.108/client.json
```

The new server generates its own UUID, REALITY keypair and shortId. Never copy credentials from the original server. Export to a separate directory so the original QR/profile remain available. Test both servers from the affected home connection; a success from the automation environment alone cannot establish that the provider permits the new path.

Status: branch prepared; production audit/deployment pending initial SSH access.
