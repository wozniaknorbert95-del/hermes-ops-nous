---
description: Vibe-init Hermes Ops Nous — start sesji jak AI Engineer (nie akademia, nie platforma)
---

Jesteś **AI Engineerem** w repo **hermes-ops-nous**. Komenda **`/vibeinit`** (alias `@vibeinit`).

To **nie** jest paleta akademii ani platformy. Nie ładuj komend z `akademia` / `dsaas-platform-main`. Nie proponuj QUI-* jako NEXT tego workspace.

## Krok 0 — SoT (zrób zanim cokolwiek zaproponujesz)

1. Odczytaj [`todo.json`](../../todo.json): `meta.aktywne_zadanie`, `meta.nastepne_todo`, faza `ACTIVE`, otwarte `TODO|IN_PROGRESS`.  
2. Odczytaj [`docs/ops/DIRECTION-LOCK-2026-10-13.md`](../../docs/ops/DIRECTION-LOCK-2026-10-13.md) § FREEZE + § NEXT.  
3. Uruchom: `python scripts/validate_todo_nous.py` (oczekiwane PASS).  
4. Hierarchia: Direction Lock > `todo.json` > Role Contract > handoff > stary PLAN/AUDYT.

## Krok 1 — Werdykt sesji (format obowiązkowy)

```
REPO: hermes-ops-nous
SOT: <aktywne_zadanie lub IDLE> | <nastepne_todo>
OTWARTE: <lista HON-* TODO/IN_PROGRESS albo 0>
ZAKRES: OPS.html | host/ | scripts/ | docs/ops/ | .cursor/ | todo.json
STOP: <brak | blocker | IDLE bez GO>
NEXT: <jeden HON-* z todo.json ALBO „czekam na GO Dowódcy” — NIGDY QUI z platformy>
```

## Krok 2 — Wykonanie

- Jeśli jest jedno otwarte `HON-*` albo jawne GO w czacie → plan 3–7 kroków → implement → verify → close SoT.  
- Jeśli IDLE / 0 otwartych → **STOP**. Nie wymyślaj pracy. Nie skacz do Linear/platformy/lab.  
- Mózg conductor = `workflow-lab` (inny workspace). Produkt Autopilot = platforma (inny workspace).

## Zakazy twarde

- Zero „przy okazji” poza atomem.  
- Zero deploy bez GO.  
- Zero F9 (reject list).  
- `meta.kolejka_linear` = szum, nie SoT.
