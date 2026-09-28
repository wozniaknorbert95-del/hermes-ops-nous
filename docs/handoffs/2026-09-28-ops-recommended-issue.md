# Handoff — atom P0 #2 recommended_issue + Użyj tego — 2026-09-28

**Status:** Lokalnie zielono. Nie deployowano.

## Co zrobione

P0 #2 ze specu nawigacji `/ops`: payload `recommended_issue` + przycisk **Użyj tego** ustawia Next i **nie** startuje pętli.

- `host/progress_vault.py`: `_recommended_issue` (głowa Autopilot + powód DoR), `_https_url` fail-closed, `POST /ops/run` action `select_next` (nie pisze `ops-cmd.json`, nie QUEUED).
- `OPS.html`: `#rec-why`, `#btn-use-rec` (`data-ops="select_next"`). 400 na select_next nie maluje REFUSED.
- `scripts/test_progress_vault.py`: unit + HTTP (head vs stale next, queued=None, QUI-404 → `qui_not_in_queue`).
- Guard: walidator + mutacja Q6.
- Docs: CONTRACT, UX-SPEC, HOWTO, PLAN (atom 2 WYKONANE).

## Co live

Nie deployowano. VPS bez zmian.

## Co zablokowane

Brak. Backlog P1 (IA/sticky/hierarchia przycisków) czeka na osobne GO.

## Następny krok

Deploy tego atomu (Zasada 11, Dowódca) **albo** GO na P1 IA.

## Komendy weryfikacji (copy-paste)

```
python scripts/test_progress_vault.py
python scripts/validate-academy-export.py
python scripts/mutation-test-fala-q.py
```

Oczekiwane: vault PASS · validate PASS · Q1–Q6 6/6 ZŁAPANE.

## Pliki dotknięte

- `host/progress_vault.py`
- `OPS.html`
- `scripts/test_progress_vault.py`
- `scripts/validate-academy-export.py`
- `scripts/mutation-test-fala-q.py`
- `docs/ops/CONTRACT-OPS-STATUS.md`
- `docs/ops/UX-SPEC-HERMES-OPS-ENTERPRISE.md`
- `docs/ops/HERMES-OPS-HOWTO.md`
- `docs/ops/PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md`
- `docs/handoffs/2026-09-28-ops-recommended-issue.md`
