# Setup

1. Use a provider console to record the host fingerprint. Connect with strict host checking. Append the public key using ssh-copy-id; do not overwrite authorized_keys.
2. Inspect OS, listening ports, users, SSH settings, active units, firewall and apt sources before deployment. Resolve port 443 conflicts with the owner. Do not stop arbitrary services.
3. Install controller requirements and fill inventories/production.ini from the example. Production inventory is ignored. The administrator defaults to vpnadmin and needs a key; sudo is passwordless because automation uses an unlocked SSH agent rather than stored passwords.
4. Run prepare-artifacts.py: version and SHA256 are pinned in xray-release.json from the official GitHub release API over TLS. This is integrity and source verification, not a detached publisher signature or independent reproducible-build attestation. Never accept an unexplained checksum change.
5. Execute bootstrap, change inventory user to vpnadmin, execute security, xray, verify. Bootstrap/security independently test fresh admin SSH and sudo before restricting authentication. Keep provider console available.
6. Export credentials and perform smoke-test. The private key is not exported. Run an actual device/TUN test separately.

Dry runs: `ansible-playbook playbooks/bootstrap.yml --check` and `ansible-playbook playbooks/security.yml --check`. Fresh-machine security --check cannot predict packages/commands not yet installed. Xray --check can compare artifacts/unit files after preparation but skips secret generation, runtime validation and restarts. Always run verify after application.

Changing SSH rules, firewall policy or keys requires operator review; do not use automatic deployments. This session's requested deployment was explicitly authorized. OS upgrades are intentionally separate from playbooks. No service minimization happens blindly.
