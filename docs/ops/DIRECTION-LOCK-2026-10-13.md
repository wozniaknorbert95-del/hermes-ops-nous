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
**Freeze polish / chat nadal ON** do osobnego GO Dowódcy:

- zakaz: polish copy, chipy, audyty UX, auth-gate, „Jak zacząć”, nowe ekrany, chat
- dozwolone bez unfreeze: docs kierunku, SoT (`todo.json`), smoke/vault blocker, **jedna linia prawdy** HUD (np. baner: brak sesji ≠ WAITING-GO mózgu)

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

**NEXT:** Produktowy Start (Linear) → https `run_url` lub refuse ≤3 min. Chat/polish BLOCKED. T2 kill-switch **N/A**.  

SoT zadań: [`../../todo.json`](../../todo.json) tor `NOUS-PRODUCT-LOOP` → aktywne `HON-OPS-PROD-01`.  
Pętla operatora (5 kroków): HOWTO § „Pętla operatora”. Hierarchia: ten plik > `todo.json` > kontrakty > handoffy > historyczne PLAN-/AUDYT-.  
Reject (nie budujemy): F9 w todo — klon Agents Window, cost HUD, chat bez GO, tick-S2, wiring todo→Start.
