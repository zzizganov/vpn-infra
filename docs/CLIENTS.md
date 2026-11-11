# Clients

Sensitive local files: `.secrets/<site>/connection.txt` (import URI), `.secrets/<site>/connection.png` (QR), `.secrets/<site>/client.json` (Xray SOCKS reference config). Never upload them to GitHub, public QR generators, issue trackers or chat. QR is equivalent to the credential.

| OS | Client option | Import and full-device traffic |
| --- | --- | --- |
| Android | v2rayNG, official 2dust/v2rayNG releases | Scan QR/import clipboard, select profile, enable VPN service and approve Android VPN permission. Enable always-on VPN and block connections without VPN in Android settings for a kill switch. |
| iOS | Streisand, official App Store listing | Import URI or scan QR, select profile, approve VPN configuration and connect; choose global routing for the experiment. |
| Windows | v2rayN, official 2dust/v2rayN releases | Import URI, select server, use TUN mode with requested administrator privileges; set global routing. System proxy alone does not cover all applications. |
| macOS | v2rayN, official macOS release | Import URI, select server, enable TUN and authorize the helper/network permissions requested by the client; use global routing. |

Names/menu positions depend on client version. Use a current core supporting VLESS, REALITY, TCP, Vision. Server port 443; encryption none; flow xtls-rprx-vision; fingerprint chrome; SNI, public key and shortId come from the local credential. On current Xray JSON the public key field is named `password`; URI clients normally use `pbk`.

DNS: enable remote/encrypted DNS in the client's VPN/TUN settings and route resolver traffic through the proxy. Prefer DoH such as https://dns.google/dns-query or https://cloudflare-dns.com/dns-query; ensure bootstrap resolution does not cause a direct DNS path. Enable DNS interception/hijack for port 53 where supported. Avoid direct resolver fallback. iOS/Android VPN DNS settings and Windows/macOS TUN implementation differ; confirm on the actual device.

For a complete test: compare public IP before/after, check multiple DNS-leak test services, check both IPv4 and IPv6, and inspect physical-interface traffic for direct DNS (UDP/TCP 53 and DoT 853). Disable IPv6 in the client's routing policy or tunnel it; do not assume an IPv4-only profile covers IPv6. Disconnect the tunnel to test the kill switch. Browser secure DNS must also travel through the tunnel. Success through local SOCKS is not proof of TUN coverage or device-wide leak prevention.

Official sources: [v2rayNG](https://github.com/2dust/v2rayNG/releases), [v2rayN](https://github.com/2dust/v2rayN/releases), [Streisand](https://apps.apple.com/us/app/streisand/id6450534064), [REALITY fields](https://xtls.github.io/en/config/transports/reality.html).
