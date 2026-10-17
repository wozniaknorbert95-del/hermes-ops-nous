# DIRECTION LOCK — Hermes Ops (2026-10-13)

**Status:** OBOWIĄZUJE · GO Dowódcy  
**Plan:** `audyt_pivot_hermes` v2  
**Rytuał startu:** `/vibeinit` → `/ops-audit` (ten repo) · praca mózgu = `workflow-lab` (inny workspace)

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

**T1c = PASS (2026-10-16)** odblokował kill-switch (golden path ×3 + T3).  
**GO F4 chat (2026-10-16):** cienki ask na `/ops` (`POST /ops/chat`, fold Zapytaj) — fakty `ops-status`, 0 tokenów, bez MCP. `/hermes/chat` = 410.  
**GO F5 polish (2026-10-16):** cienka polerka `/ops` (atomy A/B/C) — gęstość telefonu, nie przebudowa.  
**Nadal zakaz (F9):** klon Agents Window / cost HUD / Snowflake CP / tick-S2 / todo→Start.

**KPI tygodnia:** po Start widać https `run_url` w &lt;3 min albo jasny refuse. Reszta = hałas.  
Zadania inżynieryjne tego repo: korzeń [`../../todo.json`](../../todo.json) (nie kolejka Linear, nie todo platformy).

## Kill-switch

- **T1c PASS:** spełnione 2026-10-16 → T2 **N/A**. F4 chat + F5 polish = GO 2026-10-16.
- **T1 FAIL (historyczny tor):** park custom conductor → OpenHands PoC 48h → `/ops` read-only. **Zakaz** „jeszcze trochę HUD”.

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
| Automatyczny zapis live po `create` | **PASS** (2026-10-16) — early live; timeout 25s; recovery |
| Issue change ⇒ create (nie followup trupa) | **PASS** (2026-10-16) — obraz `cf32acb` / PR #104 |

## T1c = PASS (2026-10-16)

3/3 Start→https `run_url` ≤3 min bez ręcznego bind: QUI-126 / QUI-127 / QUI-128.  
Handoff: [`../handoffs/2026-10-16-conductor-t1c-pass.md`](../handoffs/2026-10-16-conductor-t1c-pass.md).

## T3 status (2026-10-16)

| Check | Wynik |
| --- | --- |
| `OPS_RUN_ALL=1` | PASS |
| run_all → create QUI-129 + URL | PASS |
| OPS.html freeze | PASS (zero polish) |

**NEXT:** `IDLE` — F3 product loop DONE · F4/F5 DONE · Real Brief `#112` · DOGFOOD QUI-43 PASS · **HON-AGENT-LOCK** + **HON-SOT-TRUTH** (docs sync 2026-10-17). T2 **N/A**. Kolejne HON-* tylko po nowym GO.  
**F5 PASS:** viewport + Czekaj/sesja + folds (handoff [`../handoffs/2026-10-16-hon-ux-unfreeze.md`](../handoffs/2026-10-16-hon-ux-unfreeze.md)).  
**URL-LAG PASS:** dogfood-2 view URL @9s — handoff [`../handoffs/2026-10-16-url-lag-remediation.md`](../handoffs/2026-10-16-url-lag-remediation.md) · nous #18 · lab #111.  
**DISPATCH-LIVE PASS:** RUNNING+https bez `ops-cmd` → `dispatch.running` (handoff [`../handoffs/2026-10-16-hon-ops-dispatch-live.md`](../handoffs/2026-10-16-hon-ops-dispatch-live.md)).  
**Deploy HTML:** PASS dispatch-live 2026-10-16 — `main` `eac896c`; `hermes-ops-conductor.path` active.  
**DOGFOOD:** QUI-43 → create_ms=3343; URL lag zamknięty dogfood-2 (handoff dogfood + url-lag).  
**TRUTH-WAIT:** RUNNING/QUEUED bez `run_url` → `#hud-truth` Czekaj (handoff [`../handoffs/2026-10-16-hon-truth-wait.md`](../handoffs/2026-10-16-hon-truth-wait.md)).  

**PROD PASS:** QUI-41 Start → https `run_url` (handoff [`../handoffs/2026-10-16-hon-ops-prod-01.md`](../handoffs/2026-10-16-hon-ops-prod-01.md)).  
**ORPHAN PASS:** QUI-43 → 1× `conductor created` (handoff [`../handoffs/2026-10-16-hon-ops-orphan.md`](../handoffs/2026-10-16-hon-ops-orphan.md)).  
**CHAT PASS:** `POST /ops/chat` ops_facts (handoff [`../handoffs/2026-10-16-hon-chat-01.md`](../handoffs/2026-10-16-hon-chat-01.md)).  
**AGENT-LOCK PASS:** alwaysApply scope-lock + `/vibeinit` AI Engineer (handoff [`../handoffs/2026-10-17-hon-sot-truth.md`](../handoffs/2026-10-17-hon-sot-truth.md)).  
SoT: [`../../todo.json`](../../todo.json) tor `NOUS-SOT-HYGIENE` → `IDLE` (F10 open_tasks=0; F9 reject nadal).  
Pętla operatora: HOWTO § „Pętla operatora” (+ lag URL ≤30s + Zapytaj). Hierarchia: ten plik > `todo.json` > kontrakty > handoffy > historyczne PLAN-.  
Reject F9: Agents Window / cost / tick-S2 / todo→Start. Linear ≠ SoT zadań tego workspace.
