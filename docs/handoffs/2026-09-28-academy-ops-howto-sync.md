# Handoff — instrukcja Hermes Ops w Akademii — 2026-09-28

**Status:** Kod na `fix/academy-ops-howto-sync`. Nie deployowano. `/ops` nadal live `b3287a3`.

## Co zrobione

Werdykt planu: Control Plane `/ops` zgadza się z HOWTO. Szczegółowa lekcja **tylko** na NARZĘDZIA (karta Engineer), nie na TERAZ.

- TERAZ: `refreshOpsLine()` czyta `report.queue_auto`; pill `PASS|FAIL|UNKNOWN` przez `opsLinePill` (fail-closed — nie `engine` IDLE).
- NARZĘDZIA: `renderOpsCta()` — kolejka pierwsza, Kolejka nie udaje Run, Użyj tego, Take over = confirm. Stringi `id="ops-howto"`, Autopilot, Approval ≠ Merge zostają.
- Callout Engineer: Start jest na `/ops`, nie na karcie Akademii.
- INSTRUKCJA „Chcę zlecić kod”: jedno zdanie o kolejce i confirm.
- `TOOL-MASTERY.md` Hermes Engineer — ten sam gotcha.
- PLAN-UX-NAV: `select_next` na liście allowed; Take over ma confirm.
- **Nie ruszane:** 6 pathów `workflow-lab/…` w `TOOL_DATA.kroki` (guard hermes-dual + Fala L).

Guardy: walidator v7 linia kolejki + P6 (queue_len).

## Co live

Nie deployowano. Produkcja `/ops` = HUD/queue z `b3287a3`. Akademia na VPS **bez** tej lekcji aż do merge + GO.

## Co zablokowane

Deploy — Zasada 11, osobne GO po merge. Pełna pętla Linear → `@cursor` → CI nie była odpalana. `ENGINEER_LOOP_E2E=false` → karta Engineer zostaje PARTIAL / SETUP.

## Następny krok

Review + merge `fix/academy-ops-howto-sync`, potem GO na `bash scripts/deploy-akademia-vps.sh`.

## Komendy weryfikacji (copy-paste)

```
python scripts/validate-academy-export.py
python scripts/mutation-test-fala-p.py
python scripts/mutation-test-fala-l.py
python scripts/mutation-test-fala-q.py
python scripts/test_progress_vault.py
python scripts/test_hermes_intent.py
```

Oczekiwane: validate PASS · P 6/6 · L 6/6 · Q 15/15 · vault PASS · hermes-intent PASS.

## Pliki dotknięte

- `DASHBOARD.html`
- `docs/ops/TOOL-MASTERY.md`
- `docs/ops/PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md`
- `scripts/validate-academy-export.py`
- `scripts/mutation-test-fala-p.py`
- `docs/handoffs/2026-09-28-academy-ops-howto-sync.md`

`git status` w chwili zapisu: gałąź `fix/academy-ops-howto-sync`, niecommitowane (handoff nie commituje). Zero sekretów.
