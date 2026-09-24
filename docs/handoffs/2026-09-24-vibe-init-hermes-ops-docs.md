# Handoff — vibe-init: dokumentacja Hermes Ops (komplet 2026-09-24)

## Co zrobione

- Plan rozszerzony (diagram, SSoT, utrzymanie) — `docs/ops/PLAN-AKTUALIZACJI-DOKUMENTACJI-HERMES-2026-09-24.md` → **WYKONANE**
- **Fala 0–4:** README, OPERATING-MODEL v1.4, AGENTS smoke ops, CURSOR-WORKFLOW, runbook VPS §10, cursor-kurs, AKADEMIA-INSTRUKCJA, workflow-marzen, DEPLOY-READY link
- Guard: `validate-academy-export.py` — README + `docs/ops/README.md` + OPERATING-MODEL muszą wspominać Hermes Ops

## Co live

Bez deploy VPS — wyłącznie pliki markdown w repo. Produkcja bez zmian do merge + ewentualnego deploy Dowódcy (Zasada 11).

## Co zablokowane

- Drift UI (panel INSTRUKCJA vs 4 zakładki) — osobny ticket jeśli Dowódca chce zsynchronizować copy w `DASHBOARD.html`

## Następny krok (jeden)

Merge PR docs; opcjonalnie deploy docs-only nie wymaga VPS — przy następnej zmianie vault/UI uruchomić `bash scripts/smoke-hermes-ops-vps.sh`.

## Komendy weryfikacji

```bash
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
# pełna bramka: linia testy: w AGENTS.md
```

## Pliki dotknięte

- `README.md`, `AGENTS.md`, `docs/OPERATING-MODEL.md`, `docs/CURSOR-WORKFLOW.md`
- `docs/runbooks/AKADEMIA-VPS.md`, `docs/ops/*` (plan, README, AKADEMIA-INSTRUKCJA, DEPLOY-READY)
- `cursor-kurs/00-START-TUTAJ.md`, `cursor-kurs/05-Profesjonalny-workflow-autonomia.md`
- `ops/workflow-marzen/README.md`, `ops/workflow-marzen/00-PLAN-DZIALANIA.md`
- `scripts/validate-academy-export.py`
