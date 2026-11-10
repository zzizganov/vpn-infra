# Security

Admin SSH key and sudo are verified in a distinct session before root/password authentication is disabled. KbdInteractiveAuthentication=no, MaxAuthTries=3. Existing authorized keys are retained. Root account itself is retained for provider-console recovery.

UFW denies incoming by default, permits outgoing, allows actual SSH TCP port and TCP/443. Existing rules are not reset: audit additional rules on nonempty servers. IPv6 firewall rules are retained; no public SOCKS or DNS listener is installed. Fail2ban SSH jail uses systemd journal, five failures per ten minutes and one-hour bans.

Security update timers and unattended-upgrades are enabled. This cannot create Ubuntu Pro entitlement: 20.04 without ESM is a temporary accepted risk. The existing Chrony service is retained when installed; otherwise systemd-timesyncd maintains time. Journald is capped to 100 MB persistent, 30 MB runtime, seven days. Existing rsyslog/logrotate policy should be inspected separately.

Xray has only CAP_NET_BIND_SERVICE, no writable system/home directories, no API or access log. Errors/warnings go to a bounded journal. Config root:xray 0640, directory 0750; server keys and client export root-only 0600. Client artifacts are sensitive and ignored locally. REALITY secrets are generated once; reruns do not rotate them. Config is tested before replacement; previous config is retained for rollback.

Private/loopback/link-local outbound destinations are blocked, including cloud metadata. No general-purpose open SOCKS proxy is exposed. Each device should eventually receive a separate UUID; the initial single-client credential is for a compatibility test.

Published passwords should be changed through `sudo passwd root` interactively; root password authentication over SSH is disabled by the playbook. Do not record the replacement in logs. No code automatically changes account passwords or rotates keys.
