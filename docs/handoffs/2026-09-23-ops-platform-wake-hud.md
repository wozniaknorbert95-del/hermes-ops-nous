# Handoff — HUD prawdy: platform wake fail-closed (2026-09-23)

**Repo:** `akademia` (HUD) · live tick już na VPS z `workflow-lab` `71475ca` (#95)

## Fakty

- Tick: `/opt/workflow-lab` `71475ca` — `target_repo_create_forbidden`, bootstrap `@cursor`. `hermes-ops.timer` active. `python3 scripts/test_hermes_ops.py` PASS na VPS.
- HUD: `OPS.html` refuse copy dla 403 platformy. `DASHBOARD` karta Cloud: pack dsaas, nie „STOP NA PLATFORMIE”. HOWTO + kontrakt + S2 w role contract.

## Deploy Akademii

Po merge tego PR: `bash scripts/deploy-akademia-vps.sh` (HEAD == origin/main). Nie rusza ticka (tick = workflow-lab).

## Nie robione

- Deploy SPA QuietForge / dsaas runtime (osobny tor QUI-82, EV-427).
- Commit całego dirty QUI-92 poza `environment.json`.
