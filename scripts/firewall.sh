#!/bin/bash
set -euo pipefail
port=${1:?SSH port required}
[[ $port =~ ^[0-9]+$ ]] && ((port > 0 && port < 65536))
changed=0
for rule in "$port/tcp" 443/tcp; do
  result=$(ufw allow "$rule")
  [[ $result == *"Skipping"* ]] || changed=1
done
before=$(ufw status verbose)
ufw default deny incoming >/dev/null
ufw default allow outgoing >/dev/null
ufw --force enable >/dev/null
after=$(ufw status verbose)
[[ $before == "$after" ]] || changed=1
((changed == 0)) || echo CHANGED
