# PLAN — Hermes prowadzący + Cursor Cloud API

**Status:** kontrakt Akademii WYKONANY · slice live (Nous na VPS + tick adapter) = **WAITING-GO**  
**Data:** 2026-10-01  
**DoD Dowódcy:** z `/ops` Start widać URL sesji Cursora, testy w trakcie (albo UNKNOWN), raport zrobione/lokalnie/padło, follow-up na **tej samej** sesji przy FAIL AC. Dopóki tego nie ma — karta Engineer = PARTIAL + baner WAITING-GO.

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

## Slice P0 (WAITING-GO, poza tym merge)

1. Issue labu `agent` (nie prod platformy).
2. Nous na VPS (Docker), `HERMES_HOME` poza repo, szablony z [`hermes-conductor/`](hermes-conductor/).
3. Adapter ticka: Nous → `ops-status.json` (`live.agent.run_url`, `live.tests[]`, `live.conductor`).
4. FAIL AC → follow-up na tym samym `agentId`.
5. Dowód → nowy `docs/ops/conductor-slice-e2e.json` → dopiero wtedy `ENGINEER_LOOP_E2E=true`.

**Nie w P0:** auto-merge `dsaas-platform-main`, Nous z `patch` na platformie, Telegram (P1; P0 = raport na `/ops` + istniejący PWA push po runie).

## Budżet i lock

- Max follow-up / issue: `OPS_CONDUCTOR_MAX_FOLLOWUPS` (domyślnie 3), potem HITL.
- `OPS_MAX_RUNS_PER_DAY` bez zmian. QUI-88: brak auto-chain po stale lock / PAUSED.
- Take over = Pause + cancel run Cloud + archive; zero follow-up.
- 409 `agent_busy` = refuse `cursor_api_busy` na HUD.

## Szablony Nous (kopia na VPS, zero kluczy)

[`hermes-conductor/SOUL.md`](hermes-conductor/SOUL.md) · [`CONDUCTOR.md`](hermes-conductor/CONDUCTOR.md) · [`TOOLSET.md`](hermes-conductor/TOOLSET.md)
