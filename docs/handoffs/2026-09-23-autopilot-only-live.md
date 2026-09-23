# Handoff — Autopilot-only live + cap unblocked (2026-09-23)

**GO Dowódcy:** dokończyć Cloud (#55) + naprawić pętlę capu.

## Co zrobione

- Akademia [#57](https://github.com/wozniaknorbert95-del/akademia/pull/57) merged `b955469` — Manual/Supervised **usunięte** z `/ops` (przywrócony Cloud #55).
- Lab [#90](https://github.com/wozniaknorbert95-del/workflow-lab/pull/90) / [#89](https://github.com/wozniaknorbert95-del/workflow-lab/issues/89) merged `0191226` — `tick()` po stale lock **nie** woła `run_next`.
- Ledger: backup + usunięte 32× dzisiejsze `run_next` QUI-88. `today.runs=0`.
- VPS: akademia deploy + lab pull + `OPS_MODE=AUTOPILOT` + PAUSED.

## Live (2026-09-23T18:42Z)

| Check | Wynik |
| --- | --- |
| `data-mode=MANUAL/SUPERVISED` | **brak** |
| vault `mode` | AUTOPILOT |
| `today.runs / cap` | **0 / 32** |
| `tick_alive` | true |
| lab HEAD | `0191226` |

## Następny krok

Telefon: twarde odświeżenie `/ops` (PWA cache) → **Start**. Oczekuj QUEUED, nie fałszywego RUNNING. Cap już nie blokuje.
