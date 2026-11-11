# Troubleshooting

SSH permission denied: check agent (`ssh-add -l`), identity and username; use `-F /dev/null` if host system SSH configuration has incorrect permissions. Never disable StrictHostKeyChecking. Verify a changed host key through the provider after reinstall before editing known_hosts.

Xray not starting: run systemctl status, restricted journal and config test. Check binary architecture, config file group, systemd capability to bind 443, and listener conflicts. Do not increase logging to debug on production without reviewing sensitive data exposure.

443 reachable but tunnel fails: compare client UUID, public key, shortId, SNI, flow and time synchronization. Verify target from VPS with scripts/check-target.py. A port probe alone is not a VPN test. Try another network to distinguish routing/DPI from configuration.

DNS failures: SOCKS must use remote resolution (`socks5h`, not local socks5 resolution). In TUN configure remote DNS and interception; inspect direct fallback and IPv6 bypass. Device DNS leak checks must run on that device, not solely on the VPS.

APT on this VPS originally used an unreachable provider mirror. It was replaced with official archive/security Ubuntu endpoints. The aborted release upgrade stopped during downloads; focal package sources and clean dpkg state were verified before VPN deployment.

## Desktop fails while phone works on the same Wi-Fi

This is not enough evidence for blanket IP blocking. First compare client/core versions, selected profile, REALITY fingerprint, proxy/TUN mode and DNS behavior. The server was rechecked after this report: config valid, service active without restarts, no warning journal entries, two real tunnel requests passed. A 1 MB Cloudflare test took 0.078 s from VPS directly and 2.280 s through the controller's tunnel; these are single small-file observations, not measurements from the affected device or a reliable throughput benchmark.

An alternative local Firefox fingerprint profile was prepared without changing server credentials or the original Chrome profile. Both real tunnel checks passed with Firefox. This does not prove connectivity from the affected device. Use `python3 scripts/smoke-test.py SERVER_IP /absolute/path/to/client-firefox.json` to test a local alternative JSON. Device credentials remain excluded from Git.

Use a current client/core from its official vendor. Xray 26.11.9 changed the default Chrome fingerprint; this is client-side behavior and upgrading the server does not upgrade the fingerprint emitted by an old app. See [official release notes](https://github.com/XTLS/Xray-core/releases/tag/v26.11.9) and [REALITY documentation](https://xtls.github.io/en/config/transports/reality.html). Obtain Happ through [its official site](https://happ.info/), not similarly named third-party download sites.

Comparison with a working reference URI found the same VLESS/TCP/443, Vision, REALITY, mirror.init7.net SNI and Chrome fingerprint. The sole visible non-credential option missing locally was spx=/; it has been added to exported profiles and reference JSON. This is not evidence that spiderX caused the failure. Both local tunnel tests still pass; affected Windows/provider connectivity remains unconfirmed. For Windows read-only TCP and unauthenticated TLS comparison, scripts/diagnose-path.ps1 accepts an optional -ReferenceIP argument. Run with all VPNs disconnected. Its outputs contain no VLESS credentials; the script has not been executed in Windows by the automation environment because WSL interop is unavailable.

When unauthenticated TLS succeeds for all compared servers, full IP/port unreachability is excluded for that test; authenticated REALITY and traffic-specific filtering remain untested. A local Windows test is provided by scripts/test-windows.sh, launched from the user's WSL terminal with Happ/other VPNs disconnected. It uses the checksum-verified official Windows Xray 26.11.9 binary in the ignored .artifacts directory and per-host local configs in .secrets/<site>/windows-client.json. It listens only on loopback SOCKS/10818, makes an explicit SOCKS5h HTTPS request, and stops only its own process. It does not change system proxy settings, routes, TUN, firewall or services. Windows execution must be performed on the affected machine; it was not possible through the restricted WSL interop in the automation session. Test files contain the user's existing credentials and must remain local.
