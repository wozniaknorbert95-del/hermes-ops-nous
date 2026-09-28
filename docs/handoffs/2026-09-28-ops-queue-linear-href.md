# Handoff — atom P0 #1 kolejka/pulse = link Linear — 2026-09-28

**Status:** Lokalnie zielono. Nie deployowano.

## Co zrobione

Atom P0 #1 ze specu nawigacji `/ops`: kolejka i Pulse wyglądają jak **linki Linear**, nie jak Run.

- `OPS.html`: `linearUrl()` — `it.url` jeśli `https://`, inaczej `https://linear.app/quietforge/issue/QUI-n`. `renderLane` → `<a class="issue">`. Pulse: id ↗. `canRun=false` zostaje. Hint „Kolejka nie udaje Run” zostaje.
- `scripts/validate-academy-export.py`: guard `function linearUrl` + `<a class="issue"`.
- `scripts/mutation-test-fala-q.py`: Q5 (button zamiast `<a>`).
- `docs/ops/PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md`: atom 1 = WYKONANE.

## Co live

Nie deployowano. VPS bez zmian.

## Co zablokowane

Brak. Następny atom specu (P0 #2 `recommended_issue`) nie ruszany.

## Następny krok

Po GO: atom P0 #2 — `recommended_issue` w vault + „Użyj tego” (nie startuje sam). Albo deploy tego atomu (Zasada 11, Dowódca).

## Komendy weryfikacji (copy-paste)

```
python scripts/validate-academy-export.py
python scripts/mutation-test-fala-q.py
python scripts/test_progress_vault.py
```

Oczekiwane: validate PASS · Q1–Q5 5/5 ZŁAPANE · vault PASS.

## Pliki dotknięte

- `OPS.html`
- `scripts/validate-academy-export.py`
- `scripts/mutation-test-fala-q.py`
- `docs/ops/PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md`
- `docs/handoffs/2026-09-28-ops-queue-linear-href.md`
