#!/usr/bin/env bash
# Deploy Akademia to isolated VPS namespace (/opt/akademia).
set -euo pipefail

REMOTE="${AKADEMIA_REMOTE:-root@185.243.54.115}"
TARGET="${AKADEMIA_TARGET:-/opt/akademia}"
SRC="$(cd "$(dirname "$0")/.." && pwd)"
ARCHIVE="/tmp/akademia-deploy-$$.tar"

echo "==> pack ${SRC}"
tar -cf "${ARCHIVE}" \
  --exclude='.git' \
  --exclude='.opencode' \
  --exclude='data/progress.json' \
  --exclude='data/progress.json.bak' \
  --exclude='CREDENTIALS.local.txt' \
  -C "${SRC}" .

echo "==> upload -> ${REMOTE}:${TARGET}"
ssh "${REMOTE}" "mkdir -p ${TARGET}"
scp "${ARCHIVE}" "${REMOTE}:/tmp/akademia-deploy.tar"
rm -f "${ARCHIVE}"

ssh "${REMOTE}" "tar -xf /tmp/akademia-deploy.tar -C ${TARGET} && rm -f /tmp/akademia-deploy.tar && chmod +x ${TARGET}/scripts/setup-akademia-vps.sh && bash ${TARGET}/scripts/setup-akademia-vps.sh"

echo "OK: deploy finished. Credentials on VPS: ${TARGET}/CREDENTIALS.local.txt"
