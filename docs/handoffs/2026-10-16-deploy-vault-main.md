# Handoff — deploy vault HTML z main (2026-10-16)

**GO Dowódcy:** tak (chat)  
**SHA:** `6a6d2f48aed461ae347121b701e704f3c2227db3` (`origin/main`)  
**Komenda:** `bash scripts/deploy-akademia-vps.sh`

## Preflight

| Check | Wynik |
| --- | --- |
| Working tree clean · HEAD == origin/main | PASS |
| `validate_todo_nous.py` | PASS |
| `test_progress_vault.py` | PASS |
| deploy-ready gate (w skrypcie) | PASS |

## Deploy

| Check | Wynik |
| --- | --- |
| Pack + upload `/opt/akademia` | PASS |
| `akademia-vault` recreate | PASS → healthy |
| nginx reload + HTTPS smoke | PASS |
| public `GET /ops` | HTTP 200 |
| `hermes-ops.timer` + `path` | active |
| Conductor image | nietknięty (poza zakresem) |

## DoD

| Kryterium | Wynik |
| --- | --- |
| MD5 `OPS.html` VPS == laptop | **PASS** `e7628adbf5d584c1f3c64692d979afd9` |
| `paintHudDecision` / baner Nous na VPS | PASS (grep) |
| `smoke-hermes-ops-vps.sh` (na VPS) | **SMOKE PASS** |
| `/ops/diag` tick_alive | true · idle |

## Drift zamknięty

Przed: VPS `OPS.html` z 2026-10-11.  
Po: ten sam plik co `main` (product-loop Teraz: + SoT docs w pakiecie).

## NEXT

- `HON-OPS-ORPHAN` — obserwacja create-spam przy kolejnym Start.
- F4/F5 chat/polish — BLOCKED do GO.
