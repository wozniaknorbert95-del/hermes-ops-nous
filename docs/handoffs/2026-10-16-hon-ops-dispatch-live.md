# Handoff — HON-OPS-DISPATCH-LIVE

**Data:** 2026-10-16  
**Atom:** `HON-OPS-DISPATCH-LIVE`  
**Branch:** `fix/dispatch-live-running`

## Problem

Dogfood-2 residual: po tick ACK + unlink `ops-cmd.json` `/ops/status` miał https `run_url` i `RUNNING`, ale `run.dispatch.state` = `idle`.

## Fix

`derive_dispatch`: gdy brak worker cmd, a `status=RUNNING` + `live.issue` + https `run_url` → `running`. Bez URL → nadal `idle` (fail-closed).

## Prove

- `python scripts/test_progress_vault.py` — PASS (`running after cmd unlink`, `RUNNING without url stays idle`)
- `python scripts/validate_todo_nous.py` — PASS

## SoT

- `todo.json`: URL-LAG DONE; DISPATCH-LIVE → DONE w tym PR
- Direction Lock NEXT + HOWTO lag ≤30s zaktualizowane
