# Project state — 2026-11-11

## Repository and workspace

- Private GitHub repository: https://github.com/zzizganov/singapore-vpn-infra
- Active work branch: deploy/185-247-117-108. Changes for both hosts are on this branch; branch name does not restrict host scope. Main has not been merged automatically.
- Logical project name: vpn-infra. GitHub repository rename was not requested.
- Current workspace: /home/zizganov/projects/singapore-vpn-infra; canonical Git checkout: repository/ inside it.
- Requested outer-folder rename to /home/zizganov/projects/vpn-infra is pending: the session cannot write to the parent projects directory (read-only filesystem). Rename locally after this session, then reopen the renamed workspace. Avoid absolute project paths in new scripts. Recreate the local virtual environment after moving because launchers embed absolute paths.

## Servers

| Site/profile | IP | OS observed | NTP | SSH | VPN |
| --- | --- | --- | --- | --- | --- |
| Singapore | 45.130.165.105 | Ubuntu 20.04.6 LTS | systemd-timesyncd | vpnadmin, key, TCP/22 | TCP/443 |
| Амстердам | 185.247.117.108 | Ubuntu 24.04.5 LTS | Chrony | vpnadmin, key, TCP/22 | TCP/443 |

Xray-core 26.11.9, official XTLS/Xray-core archive checked against GitHub asset SHA256 and official .dgst. No independent publisher attestation was verified. Version is deliberately pinned, not a claim about the latest release today.

Shared production configuration: VLESS + REALITY over RAW/TCP, flow xtls-rprx-vision; target mirror.init7.net:443 and matching SNI, client fingerprint chrome. URI spx=/ and JSON spiderX=/ are required by the project's working baseline. Each server has an independent UUID, REALITY keypair and shortId, preserved across reruns.

## Security and recovery

Both hosts have key-tested vpnadmin with sudo, PermitRootLogin=no, PasswordAuthentication=no, KbdInteractiveAuthentication=no, MaxAuthTries=3, UFW denying incoming except SSH/22 and TCP/443, Fail2ban SSH jail, security update timers, bounded journald, synchronized time, and an unprivileged hardened Xray systemd service. Config root:xray 0640, server secrets root:root 0600, directory root:xray 0750. Server secrets remain under /etc/xray; no server private key was exported. Passwords previously posted in chat must not be copied here; replacement through a local interactive mechanism remains recommended.

Singapore has no Ubuntu Pro entitlement. Enabling unattended-upgrades does not extend 20.04 security support. An attempted 20.04 → 22.04 upgrade was canceled during download before installing 22.04 packages; focal sources and clean dpkg state were restored. The unavailable provider mirror was replaced by official Ubuntu endpoints. No OS upgrade is currently running.

Amsterdam's provider sshd_config lacked Include. Fixed by including the managed hardening policy first, asserting effective settings, then rechecking independent administrator access. Keep this compatibility fix.

## Local layout — secret content never committed

```text
hosts/singapore/       README.md, inventory.example.ini, ignored inventory.ini
hosts/amsterdam/       README.md, inventory.example.ini, ignored inventory.ini
inventories/          production.example.ini, ignored production.ini
.secrets/singapore/    client.json, connection.txt, connection.png, optional diagnostics
.secrets/amsterdam/    client.json, connection.txt, connection.png, optional diagnostics
.artifacts/           verified binaries and release metadata, ignored
```

The enclosing workspace .secrets and .artifacts paths are compatibility symlinks to this checkout. No duplicated credential store is maintained. Old root-level credential paths no longer apply; select the site directory.

## Verified observations and diagnosis

- Automated checks passed on both hosts: independent admin SSH/sudo, effective SSH restrictions, service-account Xray config validation, systemd services, UFW, Fail2ban, time synchronization, automatic-update dry run, public listener audit, and actual tunneled HTTPS egress using two endpoints.
- Security and Xray reruns completed with changed=0. Identity comparison before/after target changes confirmed UUID/public key/shortId preservation.
- Original www.microsoft.com target was replaced by mirror.init7.net at the owner's request, after certificate/TLS 1.3/H2 tests from both VPSs.
- The initial report that a friend could use our profile was retracted. Do not use that report as evidence.
- A different friend's credential worked in the user's Windows 11 / Happ 4.7.2 / same Wi-Fi conditions. No third-party credential is stored in this repository.
- Windows unauthenticated HTTPS with mirror.init7.net SNI returned HTTP 200 through all three compared IPs; this ruled out complete TCP/443 unreachability for that test, not selective filtering or authentication failure.
- After spx=/ was added to our exported profiles, the user reported: everything worked. Treat this as the key user-observed result; the exact mechanism was not proven. No further Windows standalone test was required.
- Real device TUN coverage, IPv6 bypass, DNS leaks, kill-switch behavior, and sustained throughput were not verified. Do not claim these passed.
- Prior code CI/Gitleaks checks passed. Run checks again for each new commit; no status from a prior commit proves the current commit.

## Operations

From this checkout use inventories/production.ini for both hosts, or hosts/<site>/inventory.ini for one. Normal access uses an already-loaded local SSH agent; its socket path may change or expire. Do not assume the earlier temporary agent socket will persist across sessions.

Use playbooks/verify.yml for server checks and scripts/smoke-test.py with a server IP for real tunnel egress. Client export and smoke-test defaults select the matching site directory. The optional Windows test does not change system proxy, routes, firewall or TUN; its execution was not verified in the restricted automation environment.

See docs/OPERATIONS.md and docs/RECOVERY.md for upgrade, backup and rollback procedures. Next priorities: verify current profiles on actual devices, move Singapore to a supported OS when appropriate, and finish the requested local outer-folder rename.
