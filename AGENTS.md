# Instructions for this repository

This is `vpn-infra`: shared Ansible/Bash tooling for two independent VLESS + REALITY servers. Read PROJECT_STATE.md before production work. Canonical Git checkout is this directory; the enclosing workspace may contain historical generated copies. Run commands here.

## Production inventory

- Singapore: 45.130.165.105, Ubuntu 20.04.6, SSH/22, administrator vpnadmin.
- Amsterdam: 185.247.117.108, Ubuntu 24.04.5, SSH/22, administrator vpnadmin.
- Site-specific inventories are hosts/<site>/inventory.ini (ignored); combined inventory is inventories/production.ini (ignored).
- Use --limit singapore or --limit amsterdam for a single host; do not infer deployment scope from the current Git branch.
- Never assume a location from a profile label or IP alone. Ubuntu 20.04 is an accepted temporary experiment without Ubuntu Pro; a supported OS remains recommended.

## Secrets and working profiles

- Local credentials belong only in .secrets/singapore/ and .secrets/amsterdam/, directories 0700, files 0600. Artifacts in .artifacts/ are ignored. Do not commit, display, or paste credentials, QR content, UUIDs, passwords, tokens, private keys or actual connection URIs.
- Server /etc/xray/secrets.json is the source of truth. Generate secrets only on a server that lacks them; preserve all existing values on reruns and migration. Never copy one server's identity to the other or rotate without explicit authorization.
- Working settings: TCP/443, VLESS, xtls-rprx-vision, REALITY, mirror.init7.net target/SNI, chrome fingerprint, **spx=/ in URI and spiderX=/ in client JSON**. The user reported both profiles working after spx was added. Do not remove it as an allegedly irrelevant default.
- Verify target certificate, TLS 1.3 and H2 from each affected VPS before changing the target. An unauthenticated HTTPS success does not prove REALITY authentication, and an automation-environment test does not prove connectivity through a user's provider.

## Access and changes

- Use local SSH keys/agent; never request secrets in chat. StrictHostKeyChecking must stay enabled. Verify changed host keys through the provider.
- Before disabling root/password SSH, independently verify vpnadmin key access and sudo in a new connection. Keep SSH/22; preserve authorized_keys. Back up changed configuration files and validate effective sshd policy before reload.
- Provider images may omit Include directives; security.yml explicitly inserts its hardening include first. Keep the effective-policy assertions.
- Preserve the installed NTP implementation: Amsterdam uses Chrony, Singapore systemd-timesyncd. Do not install a second daemon blindly.
- Preserve firewall SSH access before enforcement. Open only the actual SSH port and TCP/443; do not reset unrelated existing rules blindly.
- Validate Xray config before restarting; preserve config.previous.json for rollback. Do not interrupt apt/dpkg or run competing release upgrades.
- The owner authorized operations in this project and dislikes redundant confirmations. Follow current scope; obtain explicit approval for new destructive work, secret rotation or credible lockout risks. Existing authorization does not authorize arbitrary future destructive changes.
- The owner waived additional backups for the earlier OS upgrade attempt, accepting provider reset as recovery. That waiver is not a blanket waiver of configuration backups or key preservation.

## Validation and Git

Use the pinned official release in xray-release.json. Verify artifact SHA256; do not use unreviewed curl-to-shell installers. No Docker is needed on production. CI runs validation only and has no production credentials.

Run scripts/validate.sh and Gitleaks with redaction before push. Scan the staged diff and Git history; scanning the whole local folder also finds intentionally ignored live credentials. Never upload a report containing those credentials. Update PROJECT_STATE.md when deployed state or verified user observations change. Never push secrets, force-push, or claim TUN/DNS leak testing that was not performed. Never access a third party's VPN using a provided comparison credential unless that use is authorized.
