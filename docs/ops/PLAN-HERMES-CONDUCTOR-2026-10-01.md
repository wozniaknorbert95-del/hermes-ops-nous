# PLAN — Hermes prowadzący + Cursor Cloud API

**Status:** slice + T1c/T3 = **WYKONANY** (2026-10-03 slice · 2026-10-16 T1c×3 + run_all)  
**Data:** 2026-10-01 (plan) · rewizja statusu 2026-10-16  
**DoD Dowódcy:** z `/ops` Start widać URL sesji Cursora, testy w trakcie (albo UNKNOWN), raport zrobione/lokalnie/padło, follow-up na **tej samej** sesji przy FAIL AC — **spełnione** ([`conductor-slice-e2e.json`](conductor-slice-e2e.json), handoff T1c). NEXT produktu: kolejka Autopilot (nie polish HUD). SoT zadań tego repo: [`../../todo.json`](../../todo.json).

## Maszyna (jeden mózg)

Linear (pin + `agent` + 6 pól) → `/ops` Start → vault `ops-cmd.json` (w tym `work_mode`) → **Nous** (profil conductor, VPS) woła [Cursor Cloud Agents API](https://cursor.com/docs/cloud-agent/api/overview) → strumień testów → skrypt D (AC × DoD × CI) → follow-up albo HITL → `ops-status.json` → HUD. Deploy = Dowódca (Zasada 11).

**Tick w `workflow-lab` nie implementuje S2.** Jest adapterem: heartbeat + zapis statusu z wyjścia Nousa. Drugi `POST /v1/agents` w Pythonie = zakaz.

## Warstwy

| Warstwa | Kto | Werdykt |
| --- | --- | --- |
| C — sesja | Nous + Cloud API | jedna durable sesja / issue (`agentId`), follow-up = to samo `id` |
| D — skrypt | mandatory tool | DoR, lista AC, required checks, dirty PR, R7; FAIL D ⇒ zakaz PASS J |
| J — lead | Nous po D | treść AC, artefakt UX w trybie testuj, jedna sugestia w ulepszaj |

UNKNOWN nigdy nie jest zielone. Puste `live.tests[]` przy RUNNING = **UNKNOWN testów**.

## Tryby (`work_mode` w `ops-cmd.json`)

- `buduj` — wdróż issue (domyślny).
- `testuj` — udowodnij; **nie** merge.
- `ulepszaj` — jedna propozycja Linear; **nie** kod.

## Slice P0 — WYKONANY

1. Issue labu `agent` (nie prod platformy).
2. Nous na VPS (Docker), `HERMES_HOME` poza repo, szablony z [`hermes-conductor/`](hermes-conductor/).
3. Adapter ticka: Nous → `ops-status.json` (`live.agent.run_url`, `live.tests[]`, `live.conductor`).
4. FAIL AC → follow-up na tym samym `agentId`.
5. Dowód → [`conductor-slice-e2e.json`](conductor-slice-e2e.json) · T1c: [`../handoffs/2026-10-16-conductor-t1c-pass.md`](../handoffs/2026-10-16-conductor-t1c-pass.md).

**Nie w P0 (nadal):** auto-merge `dsaas-platform-main`, Nous z `patch` na platformie, Telegram (P1).

## Budżet i lock

- Max follow-up / issue: `OPS_CONDUCTOR_MAX_FOLLOWUPS` (domyślnie 3), potem HITL.
- `OPS_MAX_RUNS_PER_DAY` bez zmian. QUI-88: brak auto-chain po stale lock / PAUSED.
- Take over = Pause + cancel run Cloud + archive; zero follow-up.
- 409 `agent_busy` = refuse `cursor_api_busy` na HUD.

## Szablony Nous (kopia na VPS, zero kluczy)

[`hermes-conductor/SOUL.md`](hermes-conductor/SOUL.md) · [`CONDUCTOR.md`](hermes-conductor/CONDUCTOR.md) · [`TOOLSET.md`](hermes-conductor/TOOLSET.md)

## Cursor Projects (P1 po slice, PARKED)

[Cursor Projects](https://prod.cursor.com/changelog/projects) (beta): coordinator planuje i deleguje do Cloud Agents; projekt ma własny komputer w chmurze i shared context.

Mapowanie — **nie** drugi kokpit w Akademii:

| Projects | Hermes |
| --- | --- |
| Coordinator | Nous (ten profil) |
| Cloud Agent | jedna sesja / issue (`agentId`) |
| Shared context | `HERMES_HOME` na VPS + docs; tick nie kopiuje orchestratora do akademii |
| Subscriptions | Linear-first już jest; Slack/schedule = P1 po slice |

Po slice (WYKONANY): ręcznie Project per repo (`akademia`, `workflow-lab`) jako shared context — **PARKED** do osobnego GO. Zero nowego tabu w `DASHBOARD.html`. Dowód e2e: [`conductor-slice-e2e.json`](conductor-slice-e2e.json).
