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
python3 scripts/export-client.py 185.247.117.108 ~/.ssh/id_ed25519 ../.secrets/185.247.117.108 "Амстердам"
python3 scripts/smoke-test.py 185.247.117.108 ../.secrets/185.247.117.108/client.json
```

The new server generates its own UUID, REALITY keypair and shortId. Never copy credentials from the original server. Export to a separate directory so the original QR/profile remain available. Test both servers from the affected home connection; a success from the automation environment alone cannot establish that the provider permits the new path.

Status: deployment and automated verification passed.

Audit on 2026-11-10: Ubuntu 24.04.5 amd64, approximately 1 GB RAM and 16 GB free disk. Only SSH/22 publicly listening before deployment; port 443 free, no dpkg audit errors. Chrony was already running and synchronized. The branch preserves Chrony rather than adding a competing time daemon. Profile display name requested by owner: «Амстердам». This is a user-selected label; physical location is not independently established by the audit.

Provider SSH configuration had no Include directive. The hardening playbook now explicitly includes its policy first and asserts effective root/password restrictions before reloading SSH; administrator access is independently rechecked afterward.

The «Амстердам» client profile uses credentials distinct from the original VPS. Two real VLESS/REALITY HTTPS requests returned egress 185.247.117.108. The existing server and its client files were not changed. Actual reachability from the affected provider and device TUN/DNS leak tests remain pending.

Final checks: security rerun 17 tasks changed=0; verify 11 tasks passed; Xray rerun 9 tasks changed=0. Unattended-upgrades dry-run exit 0; Chrony synchronized. Public listener audit found only SSH/22 and Xray/443. Server secret file root:root 0600, config root:xray 0640, config directory root:xray 0750. Local per-host credential directory 0700, files 0600. No credentials were published.

## Shared REALITY target update

At the owner's request both VPS instances now use `mirror.init7.net` for REALITY target and client SNI. The hostname's certificate, TLS 1.3 and ALPN H2 were verified independently from both VPS instances before applying changes. Keypairs, UUIDs and shortIds are preserved. New client links/QR must be imported after changing the target; old Microsoft-SNI profiles are no longer applicable. The ignored inventory-both.ini allows applying the same target to both hosts. Example inventory uses the new hostname, but each new VPS must independently pass the compatibility check.
