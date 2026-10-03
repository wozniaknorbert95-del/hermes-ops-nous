# Handoff — polerka UX A+B+C — 2026-10-03

**Status:** kod na `chore/ux-polish-plan`. Gate lokalny PASS (validate, vault, Fala 0–S w tym S17).

## Co zrobione

- A: brief poranka bez `eRows`; fold = sam `renderDay()`; brief wieczoru wraca na TERAZ dopiero po `ranoDone()`.
- B: skip „Przejdź do runu”; `#live-heading` = Live / Ostatni run / Run; banner JSON nie na static 404.
- C: mapa A–H w `<details>` na ≤560px gdy welcome widoczne; linia NARZĘDZIA w welcome (nie 4. krok).

## Co live

Deploy w tej sesji po merge (GO Dowódcy).

## Co zablokowane

Rotacja kluczy, Nous LLM, redesign kart NARZĘDZIA — parked.

## Następny krok

Merge + `bash scripts/deploy-akademia-vps.sh`.

## Komendy

```
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py && python scripts/mutation-test-fala-s.py
```

## Pliki

`DASHBOARD.html` · `OPS.html` · `scripts/validate-academy-export.py` · `scripts/mutation-test-fala-s.py` · `scripts/test_progress_vault.py` · `docs/ops/PLAN-UX-POLISH-2026-10-03.md`
