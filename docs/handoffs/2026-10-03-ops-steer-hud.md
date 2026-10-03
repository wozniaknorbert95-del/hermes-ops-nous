# Handoff — Hermes Ops steer HUD + plan finalizacji — 2026-10-03

**Status:** Kod na `feat/ops-steer-hud`. Merge i deploy = GO Dowódcy. Slice Nous = osobne GO.

## Co zrobione

Zamknięcie live-bugów z [`2026-10-01-ops-steer-live-bugs.md`](2026-10-01-ops-steer-live-bugs.md):

1. **Pigułka** — `paint()`: dispatch → PAUSED/STOPPED (`operator-halt-wins-fail`) → dopiero leftover FAIL. STOPPED = `warn`, nie `bad`.
2. **Chipy work_mode** — `localStorage['ops-work-mode']` + `workModeTouched`. Serwer nie zrzuca chipa do `buduj` co 15 s. Po udanym Run flaga pada (komenda już ma `work_mode`).
3. **Vault** — `derive_run`: PAUSED/STOPPED bez dispatch active wygrywa nad leftover `fail_step` na ghost issue. T1.1 (6/6 + PR = DONE) zostaje.
4. **Faza 2** — HOWTO = linia `Cloud: /autopilot`; [`engineer-loop-e2e.json`](../ops/engineer-loop-e2e.json) oznaczony legacy `@cursor`; [`conductor-slice-e2e.json`](../ops/conductor-slice-e2e.json) = WAITING-GO; Cursor Projects PARKED w planie conductor.
5. **Guardy** — Fala S S10–S12; audyt [`AUDYT-WYNIK-HERMES-OPS-2026-10-03.md`](../ops/AUDYT-WYNIK-HERMES-OPS-2026-10-03.md).

## Gate lokalny

```
python scripts/validate-academy-export.py
python scripts/test_progress_vault.py
python scripts/mutation-test-fala-q.py
python scripts/mutation-test-fala-s.py
```

PASS. `deploy-ready-hermes-ops.sh` pełny = FAIL na tej gałęzi (`HEAD != origin/main`, dirty aż do commita) — to bramka **przed deployem z main**, nie przed merchem PR.

## Polish (ten sam PR)

- WAITING-GO zostaje aż do https `run_url` (nie chowa się przy zdrowym ticku).
- Live pokazuje DoD / `local_remaining` / follow-up z conductora.
- Retry ukryty na idle (nie trup).
- Hint trybu: „wejdzie w następnym Start”.
- GET `/ops/status` na fixture Pause+S5 FAIL = `paused`. Fala S 15/15.

## Live /ops

**WAITING-GO deploy** (Zasada 11). Po GO:

- tap Testuj → chip zostaje
- Run next → QUEUED albo REFUSED z powodem
- Pause → PAUSED (nie FAIL)
- Stop → STOPPED (nie FAIL)

## Faza 3 (osobne GO)

Nous Docker + `HERMES_HOME` + tick adapter w `workflow-lab`. Dopiero po dowodzie uzupełnić `conductor-slice-e2e.json` (`github_pr`) i `ENGINEER_LOOP_E2E=true`.

## Czego nie ruszano

DASHBOARD 7 tabów. Paleta 38. Sekrety. Deploy. Tick w labie.
