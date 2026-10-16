# Handoff — deploy HON-CHAT-01 / F4 (2026-10-16)

**GO Dowódcy:** pełna zgoda (weryfikacja → merge #11 → deploy)  
**SHA:** `9a2632ecc581193cef46ce44211e705b2d617690` (`origin/main`)  
**Komenda:** `bash scripts/deploy-akademia-vps.sh`

## Preflight

| Check | Wynik |
| --- | --- |
| Review + harden refuse (deploy/merge/ssh) | PASS |
| `validate_todo_nous.py` | PASS |
| `test_progress_vault.py` | PASS (incl. `/ops/chat`) |
| PR [#11](https://github.com/wozniaknorbert95-del/hermes-ops-nous/pull/11) | **MERGED** |
| HEAD == origin/main | PASS |

## Deploy

| Check | Wynik |
| --- | --- |
| Pack + upload `/opt/akademia` | PASS |
| `akademia-vault` recreate | PASS → healthy |
| nginx + HTTPS smoke | PASS |
| public `GET /ops` | HTTP 200 |
| timer + path | active |
| Conductor image | nietknięty |

## DoD live

| Kryterium | Wynik |
| --- | --- |
| MD5 `OPS.html` VPS == laptop | **PASS** `6519f193bf7322aec6aad8514416020a` |
| Fold Zapytaj / `/ops/chat` w HTML | PASS |
| `POST /ops/chat` „co robić” | 200 `ops_facts` |
| `POST /ops/chat` „deploy vps” | 200 `ZASADA_11` |
| `POST /hermes/chat` | **410** |
| `/ops/diag` tick_alive | true · idle |

## NEXT

- F5 polish — **BLOCKED** do osobnego GO.
- Product Autopilot — Linear (poza tym repo).
