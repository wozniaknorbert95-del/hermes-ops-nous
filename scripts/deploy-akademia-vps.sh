#!/usr/bin/env bash
# Deploy Akademia to isolated VPS namespace (/opt/akademia).
set -euo pipefail

REMOTE="${AKADEMIA_REMOTE:-root@185.243.54.115}"
TARGET="${AKADEMIA_TARGET:-/opt/akademia}"
SRC="$(cd "$(dirname "$0")/.." && pwd)"
ARCHIVE="/tmp/akademia-deploy-$$.tar"

# Bramka integralnosci. Deploy pakuje WORKING COPY (tar -C "${SRC}" .), wiec bez tej
# kontroli na produkcje mogl trafic kod, ktorego nikt nie zrecenzowal i ktorego NIE MA
# w main. Zmierzone 2026-09-20: PR #17 byl OTWARTY, a jego 6 commitow juz zylo na VPS,
# a main byl 6 commitow za produkcja — czyli "prawda" nie odpowiadala rzeczywistosci.
# Obejscie: --force (swiadoma decyzja Dowodcy, nie przypadek).
FORCE=0
for _arg in "$@"; do
  case "${_arg}" in
    --force) FORCE=1 ;;
  esac
done

if [ "${FORCE}" -eq 0 ]; then
  # Fail-closed: jesli nie umiem POTWIERDZIC pochodzenia kodu, NIE deployuje.
  # Bez tego `git status` na katalogu, ktory nie jest repozytorium, zwraca puste
  # i bramka milczaco przepuszcza — czyli dokladnie ta falszywa zielen, ktorej
  # ten guard ma pilnowac.
  if ! git -C "${SRC}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "BLAD: ${SRC} nie jest repozytorium git — nie potwierdze, ze deploy idzie z main." >&2
    echo "Obejscie: --force" >&2
    exit 1
  fi
  if [ -n "$(git -C "${SRC}" status --porcelain 2>/dev/null)" ]; then
    echo "BLAD: working copy nie jest czysty — deploy pakuje to, co lezy na dysku." >&2
    git -C "${SRC}" status --short >&2
    echo "Commitnij i zmerguj do main ALBO uzyj --force (swiadoma decyzja)." >&2
    exit 1
  fi
  git -C "${SRC}" fetch --quiet origin main 2>/dev/null || echo "UWAGA: nie udalo sie odswiezyc origin/main" >&2
  HEAD_SHA="$(git -C "${SRC}" rev-parse HEAD)"
  MAIN_SHA="$(git -C "${SRC}" rev-parse origin/main 2>/dev/null || echo brak)"
  if [ "${HEAD_SHA}" != "${MAIN_SHA}" ]; then
    echo "BLAD: HEAD (${HEAD_SHA}) != origin/main (${MAIN_SHA})." >&2
    echo "Deploy tylko ze zmergowanego main (OPERATING-MODEL: deploy = zmergowany main)." >&2
    echo "Obejscie: --force" >&2
    exit 1
  fi
  echo "==> integralnosc OK: HEAD == origin/main (${HEAD_SHA})"
fi

if [[ "${FORCE}" -eq 0 ]]; then
  echo "==> deploy-ready (Hermes Ops gate)"
  bash "${SRC}/scripts/deploy-ready-hermes-ops.sh"
fi

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
