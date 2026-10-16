# Handoff — todo.json + porządek SoT (2026-10-16)

**Repo:** `hermes-ops-nous` · gałąź `chore/todo-nous-sot`  
**Plan:** audyt + `todo.json` + higiena SoT (bez platformy QUI, bez unfreeze polish)

## Zrobione

| Atom | Wynik |
| --- | --- |
| HON-TODO-01 | `todo.json` 1.0.0-nous — F0–F8, reguły, hierarchia |
| HON-SOT-01 | Direction Lock: T1c odblokował kill-switch; freeze polish/chat ON |
| HON-SOT-02 | PLAN-CONDUCTOR = WYKONANY (slice+T1c); Projects PARKED |
| HON-SOT-03 | `docs/ops/README.md` — stan żywy T1c; żywe vs historyczne; workflow-marzen FUTURE |
| HON-SOT-04 | `AGENTS.md` §0 SoT + §1a freeze po T1c + `validate_todo_nous.py` |
| HON-SOT-05 | `/ops-audit` krok 0 = todo + Direction Lock |
| HON-VAL-01 | `scripts/validate_todo_nous.py` |
| HON-TRUTH-01 | OPS.html: baner „brak sesji” ≠ WAITING-GO mózgu; refuse `qui_todo_mismatch` = todo platformy |
| HON-F7-MARZEN | kotwica FUTURE w README |

## S1–S10

| ID | Stan |
| --- | --- |
| S1 freeze wording | DONE |
| S2 README create-hang | DONE |
| S3 PLAN WAITING-GO | DONE |
| S4 baner prawdy | DONE (wąska korekta copy) |
| S5 qui_todo_mismatch copy | DONE (HUD + CONTRACT + HOWTO) |
| S6 ops-audit SoT | DONE |
| S7 hierarchia | DONE (todo.reguly + README + AGENTS) |
| S8 workflow-marzen | DONE (F8 PARKED + README) |
| S9 handoffy historyczne | DONE (polityka: append-only; żywe = DL + todo) |
| S10 walidator | DONE |

## Granice

- **Nie** ruszano `dsaas-platform-main/todo.json` ani `load_todo_active` → lokalny todo.
- Mózg conductor = `workflow-lab` (OUT_OF_SCOPE w F2).
- F4 chat / F5 unfreeze = BLOCKED do GO.

## Aktywne

- `meta.aktywne_zadanie`: **HON-OPS-PROD-01** — produktowa kolejka Autopilot (operacja Linear).
- `meta.nastepne_todo`: produktowa kolejka; cienki chat po GO; freeze polish ON.

## Verify

```bash
python scripts/validate_todo_nous.py
python scripts/test_progress_vault.py
```
