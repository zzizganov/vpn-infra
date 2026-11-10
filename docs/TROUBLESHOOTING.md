# Troubleshooting

SSH permission denied: check agent (`ssh-add -l`), identity and username; use `-F /dev/null` if host system SSH configuration has incorrect permissions. Never disable StrictHostKeyChecking. Verify a changed host key through the provider after reinstall before editing known_hosts.

Xray not starting: run systemctl status, restricted journal and config test. Check binary architecture, config file group, systemd capability to bind 443, and listener conflicts. Do not increase logging to debug on production without reviewing sensitive data exposure.

443 reachable but tunnel fails: compare client UUID, public key, shortId, SNI, flow and time synchronization. Verify target from VPS with scripts/check-target.py. A port probe alone is not a VPN test. Try another network to distinguish routing/DPI from configuration.

DNS failures: SOCKS must use remote resolution (`socks5h`, not local socks5 resolution). In TUN configure remote DNS and interception; inspect direct fallback and IPv6 bypass. Device DNS leak checks must run on that device, not solely on the VPS.

APT on this VPS originally used an unreachable provider mirror. It was replaced with official archive/security Ubuntu endpoints. The aborted release upgrade stopped during downloads; focal package sources and clean dpkg state were verified before VPN deployment.
