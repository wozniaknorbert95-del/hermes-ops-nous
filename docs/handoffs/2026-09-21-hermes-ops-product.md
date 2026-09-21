# Handoff — Hermes Ops product (F0–F3 vs takiego.txt) 2026-09-21

**Status:** kod na feat → PR → merge → deploy Akademii + `install-hermes-ops-vps.sh`.

## Co dowiezione

### F0 — prawda na VPS
- S1–S6 z `phone-loop-status` → `live.steps[]` w `hermes-ops` ticku.
- `push-ops-tokens-to-vps.ps1` — LINEAR_OPS_READ + GITHUB_OPS_WRITE (interaktywnie).
- `KEEP_PHONE_LOOP=1` — stary timer zostaje jako watchdog logu.

### F1 — tożsamość PWA
- `manifest-ops.webmanifest` + ikony `icon-ops-*` (ciemny theme).
- `OPS.html`: sticky HUD, progress S n/6, tryby, footer Akademia (bez hero „Ucz się”).

### F2 — Live + Approval + telemetry
- Live: checks, PR, duration, steps; cost/tokens = null aż będzie źródło.
- Approval: karty `hitl_local` + `ci_green_waiting` (bez Merge z telefonu).
- Ledger: pełny schemat wydarzenia (null ≠ 0).

### F3 — tryby
- MANUAL | AUTOPILOT | SUPERVISED.
- Take over → Pause + local.
- Run all tylko przy `OPS_RUN_ALL=1`.
- Worker v1 = cursor.

## Tokeny (Dowódca)

```powershell
cd workflow-lab
$lin = Read-Host -AsSecureString "LINEAR_OPS_READ"
$gh  = Read-Host -AsSecureString "GITHUB_OPS_WRITE"
.\scripts\push-ops-tokens-to-vps.ps1 -SecureLinear $lin -SecureGithub $gh
```

## Świadomie nie
- Merge z telefonu, natywna apka, Codex/Claude dropdown, fałszywy $.
