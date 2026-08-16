#!/usr/bin/env bash
set -euo pipefail

# Defense in depth, not a replacement for a full secret scanner.
# Report only file:line locations: if a real secret is ever committed by
# mistake, the scanner must not echo that secret into CI logs.

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

fail=0
check() {
  local label="$1"
  local pattern="$2"
  local hits

  hits="$(grep -RInE --exclude-dir=.git --exclude='public-safety-check.sh' "$pattern" . 2>/dev/null || true)"
  if [[ -n "$hits" ]]; then
    echo "[FAIL] $label"
    printf '%s\n' "$hits" | awk -F: '{print $1 ":" $2 " [redacted]"}'
    fail=1
  else
    echo "[ OK ] $label"
  fi
}

check "private overlay / CGNAT addresses" '100\.(6[4-9]|[7-9][0-9]|1[01][0-9]|12[0-7])\.[0-9]{1,3}\.[0-9]{1,3}'
check "absolute home-directory paths" '/home/[A-Za-z0-9._-]+/'
check "mesh DNS names" '(netbird\.cloud|ts\.net|tailscale\.net)'
check "GitHub tokens" '(ghp_|gho_|github_pat_)'
check "common LLM secret prefixes" '(sk-ant-|sk-or-v1-|sk-proj-)'
check "Telegram bot token shape" '[0-9]{7,12}:[A-Za-z0-9_-]{20,}'
check "private keys" 'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY'

if [[ $fail -ne 0 ]]; then
  echo
  echo "Public-safety checks failed. Fix every hit before publishing."
  exit 1
fi

echo
echo "Public-safety checks passed. Still review the diff manually before publishing."
