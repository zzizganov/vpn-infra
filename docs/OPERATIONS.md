# Operations

From an SSH session as vpnadmin:

```bash
sudo systemctl status xray --no-pager
sudo systemctl restart xray
sudo /usr/local/bin/xray run -test -config /etc/xray/config.json
sudo journalctl -u xray --since '10 minutes ago' --no-pager
sudo ss -lntp
sudo ufw status verbose
sudo fail2ban-client status sshd
sudo systemctl list-timers 'apt-*'
timedatectl
```

Do not paste config or credentials into tickets/logs. Do not run key generation commands merely to inspect health.

Update: select an official stable Xray release, review release notes and support for installed clients, update xray-release.json version/URL/SHA256 using official release metadata, then run prepare-artifacts.py, xray.yml, verify.yml and smoke-test.py. Do not automatically trust a changed digest. The binary and config have backups; keep the previous known-working release. Updating the package pin alone does not deploy.

Periodic OS security updates: `sudo apt-get update` then inspect `apt list --upgradable`; planned maintenance may require reboot. Release upgrades are separate and not automated here. On this temporary 20.04 instance no Pro entitlement was attached.

Rerun playbooks using vpnadmin. Re-export local client files after intentional changes. Secret rotation is a separate manual change with explicit operator approval, and requires distributing a new client profile.
