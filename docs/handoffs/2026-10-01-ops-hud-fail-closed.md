# Handoff — Hermes Ops HUD fail-closed — 2026-10-01

**Status:** `feat/ops-hud-fail-closed`. Merge + deploy Akademii = GO Dowódcy z tej sesji. Nous / `ENGINEER_LOOP_E2E` = nadal WAITING-GO.

## Co zrobione

`/ops` nie maluje zieleni bez dowodu.

- Chip `todo zgodny` tylko gdy `todo_match===true` **i** jest `todo_active`. Pusty Linear ≠ ok.
- Preflight: Tick ✗ przy UNKNOWN/brak cache; CI bez dowodu = `?` (nie ✓); lane UNKNOWN = ✗.
- `#btn-run:disabled` = ciemny dashed, nie wyciszony cyan. Hint: `Zablokowane: … To nie jest merge.`
- Jeden baner przy UNKNOWN (WAITING-GO w health). Approval HITL tylko `httpsUrl`.
- Tryby Buduj/Testuj/Ulepszaj `max-width:420px` na desktopie. Deploy panel `aria-hidden` gdy pusty.
- Guardy: Fala Q17–Q18. Validator: fail-open todo, `tick_alive`, HTTP w Approval.

Browser 360 + 1200: chipy `DoR brak` / `lane ?` / `todo —`; preflight `3 ✗ · 1 ?`; Run next zablokowany; Testuj `aria-pressed`; Take over → error vault na static server (uczciwy, nie 200).

## Co nie ruszane

- `ENGINEER_LOOP_E2E=false`. Zero Nous. Zero `CURSOR_API_KEY`.
- workflow-lab tick (już na `main` `0f5d65b`) bez nowej fali.
- `docs/handoffs/2026-10-01-ops-ghost-active-slot.md` — osobny temat, nie w tym PR.

## Weryfikacja

```
python scripts/validate-academy-export.py
python scripts/test_progress_vault.py
python scripts/mutation-test-fala-q.py   # 18/18
python scripts/mutation-test-fala-s.py   # 9/9
```

Pełna linia `testy:` z AGENTS.md PASS na feat. `deploy-ready-hermes-ops.sh` na feat **musi** FAIL (`HEAD != origin/main`) — bramka po merge na `main`.

## Następny krok

Po merge: czyste drzewo (park ghost handoff) → `bash scripts/deploy-ready-hermes-ops.sh` → `bash scripts/deploy-akademia-vps.sh`. Lab VPS tick bez reinstall, chyba że smoke `/ops/diag` padnie.
