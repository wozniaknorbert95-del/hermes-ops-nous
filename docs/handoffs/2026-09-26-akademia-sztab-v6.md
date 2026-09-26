# Handoff — Akademia sztab v6 (8 tabów)

**Data:** 2026-09-26  
**Gałąź:** `feat/academy-sztab-v6`  
**Zakres:** UI Akademii wg `docs/ops/PLAN-AKADEMIA-SZTAB-2026-09-25.md`. Zero `/ops` poza linkiem. **Nie deploy.**

## Zrobione

- 8 tabów: TERAZ · WORKFLOW · NARZĘDZIA · DSAAS · MONETYZACJA · ŹRÓDŁA · NOTATKI · DZIEŃ
- Chrome kill: brak hero.sub, sync-bar, paska „Postęp studiów”, legendy, tty-left/right
- Mapa A–H (`#course-map`) — klik → tab + dział
- DSAAS: werdykt + 1 mermaid z 7 chipami + B–G; biblia plik→obowiązek; H poza DSAAS
- MONETYZACJA: H1–H4 LEARN+DO (lis). Zero 10 maili / EUR w labie
- ŹRÓDŁA: 3 karty + archiwum
- Guardy ux-v6 + `mutation-test-fala-o.py` w CI i `testy:`

## Testy

Pełna linia `testy:` z AGENTS.md — PASS (Fala 0–O, w tym O1–O6). Smoke 360px: mapa 4×2, taby 2 rzędy × 4, `min-height: 44px`.

Po drodze: extra `}` w `renderTools()` (martwy UI) + litery A–H na mapie były `--ink` na `--card` (niewidoczne) → `color: var(--txt)`.

## Stop

Deploy VPS tylko po GO Dowódcy (Zasada 11). Commit/PR — osobne GO.
