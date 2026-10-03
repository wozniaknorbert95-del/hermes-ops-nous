# Raport audytu — Hermes Ops (`/ops`)

**Data:** 2026-10-03  
**Plan:** [`AUDYT-PLAN-HERMES-OPS-2026-09-24.md`](AUDYT-PLAN-HERMES-OPS-2026-09-24.md) (re-run O1–O8)  
**Gałąź:** `feat/ops-steer-hud`  
**Kontrakt:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md) · [`CONTRACT-OPS-STATUS.md`](CONTRACT-OPS-STATUS.md)  
**Deploy tej sesji:** **nie** (Zasada 11 — brak GO)

---

## Executive summary

Faza 1 (sterowanie HUD) jest **domknięta w kodzie**: Pause/Stop nie malują FAIL, chipy `buduj/testuj/ulepszaj` zostają po tapnięciu, `derive_run` honoruje operator halt nad leftover `fail_step` na ghost `live.issue`. UI P0–P3 z 2026-09-28 zostaje. Slice Nous + Cursor Cloud API = **WAITING-GO** ([`conductor-slice-e2e.json`](conductor-slice-e2e.json)).

Live VPS (`https://akademia.quietforge.flexgrafik.nl/ops`) **nie** weryfikowano w tej sesji — wymaga deploy po GO.

---

## Metody

| Faza | Wynik | Dowód |
| --- | --- | --- |
| **O1** docs | **PASS** | HOWTO = `Cloud: /autopilot`; ROLE: stary e2e ≠ AKTYWNY; conductor slice JSON = WAITING-GO |
| **O2** vault API | **PASS** | `test_progress_vault.py` PASS — PAUSED/STOPPED + leftover S5 FAIL → `paused`/`stopped`; T1.1 DONE nadal wygrywa |
| **O3** OPS UI | **PASS lokalnie** | `operator-halt-wins-fail`; `pillClass` STOPPED = warn; `ops-work-mode` + `workModeTouched`; safe-area + 44px |
| **O4** ops-cmd.json | **SKIP live** | Bez SSH/deploy; kontrakt I3 bez zmian |
| **O5** tick_alive | **SKIP live** | Bez `/ops/diag` na VPS w tej sesji |
| **O6** e2e Linear | **SKIP** | Conductor slice WAITING-GO; legacy [`engineer-loop-e2e.json`](engineer-loop-e2e.json) = era `@cursor` |
| **O7** smoke | **PARTIAL** | `validate` + vault + Fala Q 18/18 + Fala S 12/12 + Fala L 6/6 PASS. `deploy-ready-hermes-ops.sh` git-check = FAIL na feature branch (oczekiwane: HEAD ≠ origin/main) |
| **O8** mutacje | **PASS** | Fala S S10–S12 łapią regresję persistencji / STOPPED / paint FAIL |

`ENGINEER_LOOP_E2E` w `DASHBOARD.html` = **false**.

---

## Findingi zamknięte w kodzie (były live 2026-10-01)

| Objaw | Naprawa |
| --- | --- |
| Chip trybu wraca do buduj | `localStorage['ops-work-mode']` + `workModeTouched` — serwer nie nadpisuje do Run |
| Pause/Stop → pigułka FAIL | `paint()`: dispatch → PAUSED/STOPPED → dopiero leftover FAIL; STOPPED = warn |
| Vault `derive_run` failed przy Pause | operator halt wygrywa nad ghost `fail_step` gdy brak dispatch queued/running/picked_up |

## Świadomie poza zakresem

- Deploy VPS i smoke publiczny — GO Dowódcy.
- Nous na VPS + adapter ticka w `workflow-lab` — osobne GO Fazy 3.
- Cursor Projects jako UI w `/ops`.
- `DASHBOARD.html` 7 tabów — nietknięte.

---

## Werdykt

**KOD Fazy 1+2: PASS.** **PRODUKT live: WAITING-GO deploy.** **Conductor: WAITING-GO.**
