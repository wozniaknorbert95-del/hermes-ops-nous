# Handoff — polerka UX A+B+C — 2026-10-03

**Status:** LIVE. `main` `39d9995` na VPS 2026-10-03. Gate: validate + vault + Fala 0–S PASS (S17). Zagnieżdżony deploy-ready na Windows: OSError 22 przy restore — Fala N dowieziona solo, pack `--force` (handoff 2026-09-26).

## Co zrobione

- A: brief poranka bez `eRows`; fold = sam `renderDay()`; brief wieczoru wraca na TERAZ dopiero po `ranoDone()`.
- B: skip „Przejdź do runu”; `#live-heading` = Live / Ostatni run / Run; banner JSON nie na static 404.
- C: mapa A–H w `<details>` na ≤560px gdy welcome widoczne; linia NARZĘDZIA w welcome (nie 4. krok).

## Co live

`39d9995` na `/opt/akademia`. Smoke: vault health, `/ops/diag` idle, HTTPS progress, public `/ops` 200, PWA 200/200/401. Kotwice na VPS: skip „Przejdź do runu”, `#live-heading`, `json-banner-not-static`, `#course-map-fold`.

## Co zablokowane

Rotacja kluczy, Nous LLM, redesign kart NARZĘDZIA — parked.

## Następny krok

Parked: rotacja kluczy Cursor/Basic, redesign NARZĘDZIA, Nous LLM. Nie deployuj z brudnym drzewem.

## Komendy

```
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py && python scripts/mutation-test-fala-s.py
```

## Pliki

`DASHBOARD.html` · `OPS.html` · `scripts/validate-academy-export.py` · `scripts/mutation-test-fala-s.py` · `scripts/test_progress_vault.py` · `docs/ops/PLAN-UX-POLISH-2026-10-03.md`
