# Recovery

Before SSH/firewall changes keep an existing session and verify provider-console availability. A config archive is not a VM snapshot and cannot undo an OS release upgrade. The owner explicitly allowed subsequent OS upgrade work without additional backups; that exception does not suppress configuration rollback copies.

SSH lockout: use provider console, run `/usr/sbin/sshd -t`, inspect `sshd -T`, authorized_keys ownership/modes and `/etc/ssh/sshd_config.d/00-vpn-hardening.conf`. Restore the timestamped Ansible backup if needed, validate and reload ssh. Re-enable root/password SSH only temporarily with operator authorization. For firewall mistakes allow the correct SSH port from console; avoid a global firewall reset.

Xray config rollback: inspect `/etc/xray/config.previous.json`, validate it with `sudo /usr/local/bin/xray run -test -config /etc/xray/config.previous.json`, copy it over config.json, set root:xray 0640, restart and repeat the real client test. Binary rollback: restore the timestamped Ansible copy under /usr/local/bin or prepare the previous pinned official release; validate config against that binary before restarting. Unit backups are alongside the unit file.

Secret backup: over verified SSH export `/etc/xray/secrets.json`, `/etc/xray/config.json` and `/etc/xray/client.json` directly into a local encrypted backup using an independently supplied age/GPG recipient. For example, locally:

```bash
set -o pipefail
ssh -F /dev/null -o StrictHostKeyChecking=yes vpnadmin@SERVER_IP \
  'sudo tar -C /etc -czf - xray' | age -r YOUR_AGE_RECIPIENT -o xray-backup.tar.gz.age
```

Do not store the encrypted backup or decryption key in this repository. On restore, decrypt in a private directory, inspect archive paths, restore /etc/xray with root ownership, secrets/client 0600, config root:xray 0640 and directory root:xray 0750. Test before restarting. Preserve existing keys/UUID; never regenerate on restore unless intentional rotation is authorized. Provider reinstall erases server secrets: save the encrypted backup first if credentials must survive.
