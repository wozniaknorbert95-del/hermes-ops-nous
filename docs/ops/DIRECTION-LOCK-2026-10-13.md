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

**T1c = PASS (2026-10-16)** odblokował kill-switch (golden path ×3 + T3).  
**GO F4 chat (2026-10-16):** cienki ask na `/ops` (`POST /ops/chat`, fold Zapytaj) — fakty `ops-status`, 0 tokenów, bez MCP. `/hermes/chat` = 410.  
**Freeze polish nadal ON** do osobnego GO F5:

- zakaz: polish copy, nowe chipy, audyty UX, auth-gate, „Jak zacząć”, klon Agents Window / cost HUD
- dozwolone: docs kierunku, SoT (`todo.json`), smoke/vault, linia prawdy HUD, **cienki chat F4** (już GO)

**KPI tygodnia:** po Start widać https `run_url` w &lt;3 min albo jasny refuse. Reszta = hałas.  
Zadania inżynieryjne tego repo: korzeń [`../../todo.json`](../../todo.json) (nie kolejka Linear, nie todo platformy).

## Kill-switch

- **T1c PASS:** spełnione 2026-10-16 → T2 **N/A**. Cienki chat / unfreeze polish = osobne GO (nie automat).
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

**NEXT:** `IDLE` — DOGFOOD PASS (3 bóle UX w handoffie). F5 polish BLOCKED. T2 **N/A**.  
**Deploy HTML:** PASS 2026-10-16 — `main` `260369d` (MD5 OPS.html `d294e71a…`); `select_next` + `/ops/chat` live.  
**DOGFOOD:** QUI-43 → create_ms=3343; URL w statusie lagował ~3 min (handoff [`../handoffs/2026-10-16-hon-ops-dogfood.md`](../handoffs/2026-10-16-hon-ops-dogfood.md)).  

**PROD PASS:** QUI-41 Start → https `run_url` (handoff [`../handoffs/2026-10-16-hon-ops-prod-01.md`](../handoffs/2026-10-16-hon-ops-prod-01.md)).  
**ORPHAN PASS:** QUI-43 → 1× `conductor created` (handoff [`../handoffs/2026-10-16-hon-ops-orphan.md`](../handoffs/2026-10-16-hon-ops-orphan.md)).  
**CHAT PASS:** `POST /ops/chat` ops_facts (handoff [`../handoffs/2026-10-16-hon-chat-01.md`](../handoffs/2026-10-16-hon-chat-01.md)).  
SoT: [`../../todo.json`](../../todo.json) tor `NOUS-PRODUCT-LOOP` → `IDLE` (F4 DONE; F5 BLOCKED).  
Pętla operatora: HOWTO § „Pętla operatora” (+ lag URL + Zapytaj). Hierarchia: ten plik > `todo.json` > kontrakty > handoffy > historyczne PLAN-.  
Reject F9: Agents Window / cost / chat bez GO / tick-S2 / todo→Start.
