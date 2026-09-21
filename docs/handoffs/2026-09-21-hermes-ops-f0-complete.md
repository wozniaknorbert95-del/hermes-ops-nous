# Handoff — Hermes Ops F0 complete (queue bootstrap + Supervised push) 2026-09-21

**Status:** kod na `feat/hermes-ops-f0-complete` → PR → merge → **GO deploy** (Zasada 11).

## Co dowiezione w tym kroku

1. **F0 prawda bez tokenu Linear:** `LINEAR_OPS_QUEUE_FILE` (`data/linear-queue.json`). Brak `LINEAR_OPS_READ` ≠ UNKNOWN, jeśli plik ma issues. Fixture MCP: `scripts/fixtures/hermes-ops/linear-queue-open.json` (QUI-61 + Ready).
2. **Seed VPS:** `scripts/push-linear-queue-to-vps.ps1` — scp + tick albo fallback status `reason=queue_file`.
3. **Active agents + lane progress** w cache `/ops/status` + UI `OPS.html`.
4. **SUPERVISED → Web Push:** `hermes_ops/notify.py` → `ops-push-pending.json` → `push-send.py --ops` (cooldown 1h).
5. **Waiting** = max(ledger, local HITL count).

## Tokeny (nadal docelowo)

```powershell
cd workflow-lab
$lin = Read-Host -AsSecureString "LINEAR_OPS_READ"
$gh  = Read-Host -AsSecureString "GITHUB_OPS_WRITE"
.\scripts\push-ops-tokens-to-vps.ps1 -SecureLinear $lin -SecureGithub $gh
```

Po `LINEAR_OPS_READ` plik kolejki jest tylko awaryjnym bootstrapem — API wygrywa.

## Testy

- lab: `python scripts/test_hermes_ops.py` → PASS
- akademia: walidator + vault + Fala M 8/8 → PASS

## Świadomie nie

- Deploy bez GO Dowódcy.
- Merge z telefonu, fałszywy $.
