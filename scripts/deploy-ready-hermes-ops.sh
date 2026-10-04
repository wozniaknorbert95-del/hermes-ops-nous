#!/usr/bin/env bash
# Bramka przed deploy Akademii + Hermes Ops (AGENTS.md + integralność git).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

FAIL=0
step() {
  echo ""
  echo "==> $*"
  if ! "$@"; then
    echo "FAIL: $*" >&2
    FAIL=1
  fi
}

step bash -n scripts/smoke-hermes-ops-vps.sh

echo ""
echo "==> git integralność (deploy pakietuje working copy)"
if [[ -n "$(git status --porcelain)" ]]; then
  git status --short
  echo "FAIL: working copy nie jest czysty" >&2
  FAIL=1
fi

git fetch --quiet origin main 2>/dev/null || echo "UWAGA: fetch origin/main nieudany" >&2
HEAD_SHA="$(git rev-parse HEAD)"
MAIN_SHA="$(git rev-parse origin/main 2>/dev/null || echo missing)"
echo "    HEAD=${HEAD_SHA}"
echo "    origin/main=${MAIN_SHA}"
if [[ "${MAIN_SHA}" != "missing" && "${HEAD_SHA}" != "${MAIN_SHA}" ]]; then
  echo "FAIL: HEAD != origin/main — merge PR albo checkout main przed deploy" >&2
  FAIL=1
fi

for f in scripts/setup-akademia-vps.sh scripts/smoke-hermes-ops-vps.sh scripts/deploy-akademia-vps.sh; do
  if [[ ! -f "${f}" ]]; then
    echo "FAIL: brak ${f}" >&2
    FAIL=1
  fi
done

echo ""
if [[ "${FAIL}" -eq 0 ]]; then
  echo "DEPLOY READY: Hermes Ops + akademia gate PASS"
  echo "Następny krok (GO Dowódcy): bash scripts/deploy-akademia-vps.sh"
  exit 0
fi
echo "NOT DEPLOY READY — napraw powyższe przed VPS" >&2
exit 1
