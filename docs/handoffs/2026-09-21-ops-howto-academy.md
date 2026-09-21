# Handoff — Hermes Ops howto w Akademii (2026-09-21)

**Repo:** `akademia`  
**PR:** [#44](https://github.com/wozniaknorbert95-del/akademia/pull/44) → `87cc9fa`  
**Status:** ZMERGOWANE + WDROŻONE na VPS.

## Plan (wykonany)

1. Instrukcja użycia `/ops` na zakładce **TERAZ** (nie nowa zakładka).
2. SoT markdown: `docs/ops/HERMES-OPS-HOWTO.md`.
3. Guardy walidatora + Fala M9.
4. Merge → deploy → handoff.

## Co dostał Dowódca na TERAZ

Rozwijane `#ops-howto`:
- Linear `agent` + 6 pól
- Manual / Autopilot / Supervised (+ Web Push)
- Approval ≠ Merge
- linki do HOWTO + kontraktu ról

## Testy

- `validate-academy-export.py` PASS  
- `mutation-test-fala-m.py` 9/9  
- CI `academy-gate` PASS  
- VPS: `HERMES-OPS-HOWTO.md` + `ops-howto` w DASHBOARD

## Git

- Gałąź `feat/ops-howto-academy` usunięta po squash-merge.
- Working tree `main` = `origin/main`.

## Świadomie nieruszone

- Nowa zakładka IA (zostały 4).
- Logika trybów / path unit (już live wcześniej).
