# Handoff — T0 Direction Lock (2026-10-13)

**Repo:** `hermes-ops-nous`  
**Branch:** `chore/direction-lock-t0`  
**Rytuał:** `/ops-audit`  
**Deploy:** nie (docs only)

## Zrobione

1. SoT kierunku: [`docs/ops/DIRECTION-LOCK-2026-10-13.md`](../ops/DIRECTION-LOCK-2026-10-13.md) — freeze OPS.html, role Nous/Cloud/tick, kill-switch.
2. VPS readonly checklist (bez wartości sekretów): tick PASS, `CURSOR_API_KEY` SET, kontener conductor Up, **halted=true** na QUI-113.
3. Raport `/ops-audit`: [`AUDYT-WYNIK-DIRECTION-LOCK-2026-10-13.md`](../ops/AUDYT-WYNIK-DIRECTION-LOCK-2026-10-13.md).

## STOP

Conductor pętli w halt po Take over (Oct 3). Log: `conductor halted url=True`. Leftover `run_url` QUI-113 w `ops-status` ≠ żywa sesja.

## NEXT (T1 — `workflow-lab`)

1. Nowy `ops-cmd` / nowy `cmd_id` albo clear `halted` w live JSON wg `hermes_conductor/loop.py` (`same_cmd` guard).
2. Golden path: Start QUI labu → handoff → Cloud `run_url` &lt;3 min ×3.
3. Dopiero potem T1d baner w tym repo.

**Zakaz:** polish `/ops`.
