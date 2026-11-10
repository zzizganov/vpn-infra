# Verification scope

This document is updated with the observed deployment checks. An open TCP port is not proof of VLESS functionality. A workstation SOCKS test proves REALITY authentication and tunnel forwarding for those requests only. Actual Android/iOS/Windows/macOS TUN routing, IPv6 behavior, DNS leakage and kill-switch behavior require tests on those devices.

Initial audit: Ubuntu 20.04.6 amd64, 1 GB RAM, 20 GB disk, only TCP/22 listening, no VPN/web packages, UFW inactive, no Fail2ban, root/password SSH enabled. NTP synchronized. Ubuntu Pro not attached. Upgrade to 22.04 was canceled during downloads; no 22.04 package installation occurred, focal sources and clean dpkg audit verified.

REALITY target www.microsoft.com: certificate hostname/trust validation, TLS 1.3 and ALPN h2 passed from VPS before deployment.

Artifact: Xray 26.11.9 from XTLS/Xray-core, archive SHA256 matched GitHub release asset digest and official .dgst. No independent publisher signature/attestation has been verified. Local gh version lacks attestation verification.

Deployment observations (2026-11-10):

- Independent vpnadmin SSH key session and passwordless sudo passed before and after SSH hardening.
- Effective SSH config: PermitRootLogin=no, PasswordAuthentication=no, KbdInteractiveAuthentication=no, MaxAuthTries=3.
- UFW active: deny incoming / allow outgoing; only 22/TCP and 443/TCP rules for IPv4/IPv6. Listener audit found no other public services.
- Fail2ban running with sshd jail. NTP synchronized. Unattended-upgrades dry-run exit 0; apt security timers active. This does not extend 20.04 support without Pro.
- Xray systemd service active; config validated as the xray account. Config root:xray 0640; secrets/client root:root 0600; directory root:xray 0750.
- Two independent HTTPS requests from the local Xray SOCKS client over actual VLESS+REALITY/Vision succeeded; api.ipify.org and icanhazip.com both returned the expected VPS egress IP. socks5h ensured proxy-side resolution for those requests.
- Local Gitleaks working-tree and full-history scans found no leaks. Ansible syntax, YAML lint, Python compilation and Bash syntax checks passed.
- Client URI, QR and reference JSON were created locally in ignored .secrets/ with directory 0700 and files 0600. No server private key was exported.

Pending external checks: real Android/iOS/Windows/macOS app imports, device-wide TUN routing, IPv6 bypass, DNS leaks and kill switch. No such device test is claimed. This temporary installation is not a completed production security acceptance on a supported OS.

Final Ansible verify: 9 successful tasks, zero changes/failures/unreachable hosts. Repeated xray deployment: 9 successful tasks, changed=0; no secret rotation or service restart. Initial GitHub Actions run completed successfully, including complete-history Gitleaks scan.
