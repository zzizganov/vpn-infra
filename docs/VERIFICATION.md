# Verification scope

This document is updated with the observed deployment checks. An open TCP port is not proof of VLESS functionality. A workstation SOCKS test proves REALITY authentication and tunnel forwarding for those requests only. Actual Android/iOS/Windows/macOS TUN routing, IPv6 behavior, DNS leakage and kill-switch behavior require tests on those devices.

Initial audit: Ubuntu 20.04.6 amd64, 1 GB RAM, 20 GB disk, only TCP/22 listening, no VPN/web packages, UFW inactive, no Fail2ban, root/password SSH enabled. NTP synchronized. Ubuntu Pro not attached. Upgrade to 22.04 was canceled during downloads; no 22.04 package installation occurred, focal sources and clean dpkg audit verified.

REALITY target www.microsoft.com: certificate hostname/trust validation, TLS 1.3 and ALPN h2 passed from VPS before deployment.

Artifact: Xray 26.11.9 from XTLS/Xray-core, archive SHA256 matched GitHub release asset digest and official .dgst. No independent publisher signature/attestation has been verified. Local gh version lacks attestation verification.
