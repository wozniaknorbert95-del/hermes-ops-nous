# Handoff — 2026-10-01 Atom 2 tick adapter

## Zrobione

- Akademia: CONTRACT `picked_up` = ack bez pełnego `running` (RUNNING-slot bez https `run_url` zostaje `picked_up`). HUD `running` dopiero z URL.
- `workflow-lab` gałąź `feat/hermes-conductor-tick-adapter`: `run_next` nie woła `@cursor` / `ensure_cursor_trigger`. Tick zapisuje handoff JSON i kopiuje `hermes-conductor-live.json` → `ops-status.json`.
- Szablony Nous: `docs/ops/hermes-conductor/` + `scripts/install-hermes-conductor-docs.sh` (zero Docker / systemctl / sekretów).
- Testy: `test_hermes_ops.py` PASS; lab `npm run lint|test|build` PASS. Akademia vault + Fala S 9/9 + validate PASS.
- `ENGINEER_LOOP_E2E=false`. Brak `conductor-slice-e2e.json`. Brak deployu VPS.

## Nie zrobione (WAITING-GO)

- Nous na VPS + `CURSOR_API_KEY` + live Start z `/ops` z prawdziwym `run_url`.
- Commit / PR / pin / deploy — tylko na GO Dowódcy.

## Następny krok

GO: commit obu gałęzi, albo start Nous na VPS (Zasada 11 — nie agent).
