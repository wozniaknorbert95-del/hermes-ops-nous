#!/usr/bin/env bash
# Smoke Hermes Ops na VPS (uruchamiaj NA hoście lub: ssh root@VPS 'bash -s' < scripts/smoke-hermes-ops-vps.sh)
set -euo pipefail

TARGET="${AKADEMIA_TARGET:-/opt/akademia}"
HOST="${ACADEMY_HOST:-akademia.quietforge.flexgrafik.nl}"
USER="${ACADEMY_BASIC_USER:-academy}"
VAULT="http://127.0.0.1:8097"

fail() { echo "SMOKE FAIL: $*" >&2; exit 1; }
warn() { echo "SMOKE WARN: $*" >&2; }

echo "==> Hermes Ops smoke (target=${TARGET})"

curl -fsS "${VAULT}/health" >/dev/null || fail "vault /health"

DIAG="$(curl -fsS "${VAULT}/ops/diag")"
echo "    /ops/diag: ${DIAG}"
case "${DIAG}" in
  *'"ok":true'*|*'"ok": true'*) ;;
  *) fail "/ops/diag brak ok=true" ;;
esac

curl -fsS "${VAULT}/ops/status" >/dev/null || fail "/ops/status"

CMD_PATH="${TARGET}/data/ops-cmd.json"
if [[ -d "${CMD_PATH}" ]]; then
  fail "ops-cmd.json jest katalogiem — napraw ensure_hermes_ops_cmd_file"
fi

if [[ -f "${CMD_PATH}" ]]; then
  echo "    ops-cmd.json: plik OK"
else
  echo "    ops-cmd.json: missing — idle (legal after tick ACK; vault recreates on Start/restart)"
fi

if command -v systemctl >/dev/null 2>&1; then
  T="$(systemctl is-active hermes-ops.timer 2>/dev/null || echo inactive)"
  P="$(systemctl is-active hermes-ops-cmd.path 2>/dev/null || echo inactive)"
  echo "    systemd: timer=${T} path=${P}"
  if [[ "${T}" != "active" || "${P}" != "active" ]]; then
    warn "tick nie active — /ops/diag tick_alive moze byc false (runbook A)"
  fi
  UNIT="/etc/systemd/system/hermes-ops-cmd.path"
  if [[ -f "${UNIT}" ]] && grep -qE '^MakeDirectory=true' "${UNIT}"; then
    fail "hermes-ops-cmd.path ma MakeDirectory=true — uruchom setup-akademia-vps.sh ponownie"
  fi
fi

if [[ -f "${TARGET}/CREDENTIALS.local.txt" ]] && grep -q '^password=' "${TARGET}/CREDENTIALS.local.txt"; then
  PASS="$(grep '^password=' "${TARGET}/CREDENTIALS.local.txt" | cut -d= -f2-)"
  PUB_CODE="$(curl -s -o /dev/null -w '%{http_code}' -u "${USER}:${PASS}" "https://${HOST}/ops")"
  echo "    public GET /ops: HTTP ${PUB_CODE}"
  [[ "${PUB_CODE}" == "200" ]] || fail "public /ops nie 200"
  PUB_DIAG="$(curl -fsS -u "${USER}:${PASS}" "https://${HOST}/ops/diag")"
  echo "    public /ops/diag: ${PUB_DIAG}"
fi

echo "SMOKE PASS: Hermes Ops (vault + diag)"
