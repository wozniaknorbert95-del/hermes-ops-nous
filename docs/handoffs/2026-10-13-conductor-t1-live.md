# Handoff — T1 conductor live (2026-10-13)

**Repo pracy (Cursor):** `hermes-ops-nous`  
**Branch:** `feat/conductor-t1-live`  
**Rytuał:** `/ops-audit` → Direction Lock → T1 VPS  
**Deploy HTML:** nie wymagany (baner chowa się gdy jest `run_url`)

## Dowód (HUD / vault)

| Pole | Wartość |
| --- | --- |
| status | `RUNNING` |
| live.issue | `QUI-33` |
| run_url | `https://cursor.com/agents/bc-f6717be0-eba7-4ed9-9748-2dbbb26dc7e6` |
| tick_alive | true |
| cmd_id handoff | `afbd6e2461494100` |

## Co zrobiono z tego repo

1. Workspace = **hermes-ops-nous** (bez skoku product work do workflow-lab UI).
2. DoR QUI-33 uzupełnione w Linear (brakujące pola platformy).
3. Clear halt / ghost QUI-113; Start QUI-33 → tick napisał handoff (wcześniej QUI-113 = `empty_queue`).
4. Cloud API **działa** (`CURSOR_API_KEY` SET; GET agents 200).
5. Live HUD podpięty do najnowszej sesji QUI-33.

## STOP / bugi (kod conductora = obraz z workflow-lab)

1. **`cli.create` wisi** (>45–60s) — sesje Cloud powstają, ale pętla nie zapisuje `live` (stąd ręczne bind).
2. **Zmiana issue przy leftover `agent_id`** → follow-up na trupie → `cursor_api_busy` zamiast `create`.
3. Autopilot kolejka bez DoR → Start 400; QUI-113 poza kolejką → `refuse_empty_queue`.
4. Duplikaty create (4× RUNNING QUI-33) — archive częściowo; pilnować kosztów Cloud.

## NEXT

1. Fix w obrazie `hermes-conductor` (źródło: `workflow-lab/scripts/hermes_conductor/`): timeout create + **nowe issue ⇒ create, nie followup**; po create zawsze write live.
2. Powtórz golden path 2× (T1c = 3/3) bez ręcznego bind.
3. Potem T3 (run_all / push) — nie polish `/ops`.

## Zakaz

Polish `OPS.html`. Product = żywy `run_url`, nie copy HUD.
