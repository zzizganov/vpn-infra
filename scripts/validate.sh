#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
yamllint playbooks .github/workflows .yamllint.yml
for file in scripts/*.sh; do bash -n "$file"; done
python3 -m compileall -q scripts
for name in bootstrap security xray verify; do
  ansible-playbook -i inventories/production.example.ini --syntax-check "playbooks/$name.yml"
done
python3 scripts/scan-secrets.py
