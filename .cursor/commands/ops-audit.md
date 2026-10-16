---
description: Audyt Hermes Ops — UX/UI, HUD, vault, tick
---

Jesteś agentem w repo **hermes-ops-nous** (Control Plane). Komenda **`/ops-audit`**.

To **nie** jest `akademia` ani `workflow-lab`. Nie ładuj palety komend akademii (`/vibeinit`, `/auditread`, `/rootcause`, `/handoff`).

## Krok 0 — SoT (obowiązkowy przed raportem)

1. Odczytaj korzeń [`todo.json`](../../todo.json): `meta.aktywny_tor`, `meta.aktywne_zadanie`, `meta.nastepne_todo`, fazę `ACTIVE`.
2. Odczytaj [`docs/ops/DIRECTION-LOCK-2026-10-13.md`](../../docs/ops/DIRECTION-LOCK-2026-10-13.md) § FREEZE + § NEXT.
3. Hierarchia przy konflikcie: Direction Lock > `todo.json` > Role Contract / CONTRACT-OPS-STATUS > handoff > historyczne PLAN-/AUDYT-.
4. **Nie** bierz SoT z `dsaas-platform-main/todo.json`. Kolejka Autopilot = Linear.

Uruchom: `python scripts/validate_todo_nous.py` (oczekiwane PASS).

## Zakres

- TAK: audyt UX/UI (`OPS.html`), HUD, vault (`host/`), tick, dokumentacja (`docs/ops/`), zgodność z `todo.json`.
- NIE: deploy VPS bez GO, SSH z hasłem, sekrety, edycja `workflow-lab`, **F5 polish** bez GO (F4 chat = GO; `/ops/chat` facts OK).

## Raport

```
REPO: hermes-ops-nous
TODO: <aktywne_zadanie> | <nastepne_todo>
AUDYT: <HUD | UX/UI | vault | tick | docs | SoT>
PLIK: <jeden plik>
GATE: <PASS | FAIL | SKIP>
STOP: <brak albo blocker>
NEXT: <jeden krok — zgodny z todo.json / Direction Lock>
```
