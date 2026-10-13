# DIRECTION LOCK — Hermes Ops (2026-10-13)

**Status:** OBOWIĄZUJE · GO Dowódcy  
**Plan:** `audyt_pivot_hermes` v2  
**Rytuał startu:** `/ops-audit` (ten repo) · praca mózgu = `workflow-lab` (nie polish HUD)

## Produkt (jedyna prawda)

| Rola | Kto | Uwagi |
| --- | --- | --- |
| Kolejka | Linear (`agent` + 6 pól) | SoT decyzji |
| Conductor | Hermes Nous na VPS | DeepSeek flash default / Pro gdy trudniej |
| Executor kodu | Cursor Cloud Agents API | jedyny S2; tick NIE woła Cloud |
| Status | tick `workflow-lab` | `ops-status.json` + `run_url` |
| Pilota | `/ops` (`OPS.html`) | Start/Pause/Stop — **nie** jest Hermesem |

Kontrakt: [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md) · [`PLAN-HERMES-CONDUCTOR-2026-10-01.md`](PLAN-HERMES-CONDUCTOR-2026-10-01.md).

## FREEZE — `OPS.html` / hermes-ops-nous UI

**Zakaz do T1 PASS** (żywy `run_url` ×3):

- polish copy, chipy, audyty UX, auth-gate, „Jak zacząć”, nowe ekrany, chat
- MR-y tylko: baner WAITING-GO (T1d, jedna linia) **po** dowodzie mózgu; docs kierunku; smoke/vault jeśli blocker T1

**KPI tygodnia:** po Start widać https `run_url` w &lt;3 min albo jasny refuse. Reszta = hałas.

## Kill-switch

- **T1 PASS (dzień ≤7):** golden path 3× QUI labu → T3 (run_all / push / cienki chat).
- **T1 FAIL:** park custom conductor → OpenHands PoC 48h → `/ops` read-only. **Zakaz** „jeszcze trochę HUD”.

## VPS checklist T0 (2026-10-13, readonly, zero wartości sekretów)

| Check | Wynik |
| --- | --- |
| `/ops/diag` tick_alive | **PASS** (`true`, age ~244s) |
| `hermes-ops.timer` + `path` | **PASS** active |
| `akademia-vault` docker | **PASS** healthy |
| `CURSOR_API_KEY` w `/etc/workflow-lab/hermes-engineer.env` | **PASS** SET |
| `LINEAR_OPS_READ` / GitHub ops tokens | **PASS** SET |
| Kontener `hermes-conductor` | **PASS** Up (10d) + loop Python |
| Szablony `/var/lib/hermes-conductor` | **PASS** SOUL/CONDUCTOR/TOOLSET |
| Academy `GET /hermes/status` `llm` | **N/A** `false` — czat akademii retired (410); to **nie** jest Nous conductor |
| Conductor live | **FAIL / STUCK** — `halted: true` na QUI-113 od 2026-10-03; log: `conductor halted url=True` (pętla) |
| `ops-status` leftover | QUI-113 + stary `run_url` Cursor; next QUI-33; status PAUSED |

**STOP T0 (historyczny):** conductor **halted** po Take over — odblokowane w T1 (2026-10-13).

## T1 status (2026-10-13, praca z `hermes-ops-nous`)

| Check | Wynik |
| --- | --- |
| Start QUI-33 (DoR uzupełnione) | PASS — handoff `afbd6e2461494100` |
| Cloud API klucz + GET agents | PASS |
| HUD `run_url` QUI-33 | **PASS** `https://cursor.com/agents/bc-f6717be0-eba7-4ed9-9748-2dbbb26dc7e6` |
| Automatyczny zapis live po `create` | **FAIL** — `create` wisi; bind ręczny z listy API |
| Issue change ⇒ create (nie followup trupa) | **FAIL** w obrazie conductor — wymaga fix źródła obrazu |

Handoff: [`../handoffs/2026-10-13-conductor-t1-live.md`](../handoffs/2026-10-13-conductor-t1-live.md).

**NEXT:** naprawa pętli `create`/followup w obrazie `hermes-conductor` (źródło dziś w `workflow-lab`, deploy obrazu na VPS) — Cursor workspace zostaje **hermes-ops-nous**; zero polish HUD.
