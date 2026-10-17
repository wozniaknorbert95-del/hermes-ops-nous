# Handoff — HON-DOGFOOD-REAL-43 PASS (2026-10-17)

**Atom:** żywy Start QUI-43 po Real Autopilot Brief  
**Image:** `hermes-conductor:local` `90e149ecc633`  
**Lab:** `main` (PR #112)

## Preflight

| Check | Wynik |
| --- | --- |
| conductor / timer / ops-cmd.path | active |
| CURSOR_API_KEY | SET |
| Leftover | PAUSED QUI-43 + stary `bc-8499…` → take_over + stop |

## Start

| Pole | Wartość |
| --- | --- |
| Issue | **QUI-43** brand-kit (`dsaas-platform-main`) |
| work_mode | buduj |
| cmd_id | `3e2e1e9bb6f64f82` |
| Conductor | `created` http=201 **create_ms=2867** |
| agent_id | `bc-fb9361ea-ad1a-44f7-8574-dd0035699a9b` |
| run_url | https://cursor.com/agents/bc-fb9361ea-ad1a-44f7-8574-dd0035699a9b |
| ≠ stary agent | PASS (nie `bc-8499…`) |

## Dowód real brief

| Check | Wynik |
| --- | --- |
| handoff `brief_kind` | **real** |
| handoff `repo` | `dsaas-platform-main` |
| handoff `ac` | **3** |
| `_brief(handoff)` | `real Autopilot` + `autopilot.md` + brand-kit |
| `conductor-lab-probe` w brief | **BRAK** |
| PROVE | **PASS** |

## Po dogfood

- `stop` → STOPPED (slot nie zostaje RUNNING bez kontroli).
- Cloud sesja może dalej żyć pod URL — to OK; nie spamować create.

## NEXT

1. Produkt: Cloud Agent może domknąć brand-kit (osobna sesja / obserwacja URL) — nie Control Plane polish.
2. SoT `todo.json`: IDLE (check prompt zamknięty).
3. F9 reject nadal.
