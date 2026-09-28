# Handoff — cienka paczka Cursor — 2026-09-28

**Status:** Lokalnie zielono. Nie deployowano. 4 slash-komendy akademii + 3 glob-rules + Cloud env.

## Co zrobione

Cienka paczka `.cursor/` na rootcie akademii (wcześniej folder nie istniał). Palety 38 komend platformy **nie** skopiowano.

- `.cursor/commands/`: `/vibeinit` `/rootcause` `/auditread` `/handoff` — ciała procedur (SoT).
- `.cursor/rules/`: `ui-dashboard.mdc`, `python-scripts.mdc`, `ops-surface.mdc` — `alwaysApply: false`.
- `.cursor/environment.json`: `install` = `python3 --version`, terminal `dev` = `python3 -m http.server 8765`.
- `AGENTS.md`: rytuały jako slash + sekcja Cursor Cloud.
- `docs/CURSOR-WORKFLOW.md`: indeks (bez zduplikowanych wklejek).

## Co live

Nie deployowano. VPS bez zmian.

## Co zablokowane

Brak blockerów tej paczki. Atom 2 (skills, hook deny-deploy) świadomie poza zakresem.

## Następny krok

Commit + PR na prośbę Dowódcy. W Cursor: paleta ma pokazać 4 komendy; `/vibeinit` ładuje procedurę akademii, nie platformy.

## Komendy weryfikacji (copy-paste)

```
python scripts/validate-academy-export.py
python scripts/test_progress_vault.py
```

Oczekiwane: `PASS: academy export contract` i `PASS: progress vault tests`.

## Pliki dotknięte

- `.cursor/commands/vibeinit.md` (added)
- `.cursor/commands/rootcause.md` (added)
- `.cursor/commands/auditread.md` (added)
- `.cursor/commands/handoff.md` (added)
- `.cursor/rules/ui-dashboard.mdc` (added)
- `.cursor/rules/python-scripts.mdc` (added)
- `.cursor/rules/ops-surface.mdc` (added)
- `.cursor/environment.json` (added)
- `AGENTS.md` (modified)
- `docs/CURSOR-WORKFLOW.md` (modified)
- `docs/handoffs/2026-09-28-cursor-pack-thin.md` (added)
