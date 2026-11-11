#!/bin/bash
set -euo pipefail
# Launch from the user's local WSL terminal. No system proxy, TUN or firewall edits.
vpn_repo=$(cd "$(dirname "$0")/.." && pwd)
vpn_root=$(cd "$vpn_repo/.." && pwd)
export VPN_TEST_ROOT
VPN_TEST_ROOT=$(wslpath -w "$vpn_root")
export WSLENV="${WSLENV:+$WSLENV:}VPN_TEST_ROOT"
powershell.exe -NoProfile -NonInteractive -Command - < "$vpn_repo/scripts/test-windows.ps1"
