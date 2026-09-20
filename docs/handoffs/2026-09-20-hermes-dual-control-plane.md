# Handoff — Hermes Dual-Control Plane (2026-09-20)

## Zrobione (z weryfikacją)

| # | Zadanie | Dowód |
|---|---------|--------|
| 1 | Merge **#27** dual-control (Akademia UI + Fala L/B) | `main` @ `0e82cda` |
| 2 | Deploy Akademii VPS | health OK, HTTPS smoke, Hermes LLM on |
| 3 | **#28** vault router + **#29** docker mount `hermes_router.py` | deploy `b2a7d89` |
| 4 | Live **hermes-eval** B3 | VPS: `FAIL=0/7` (artefakt `/tmp/hermes-eval.json`) |
| 5 | **workflow-lab #60** merged | `phone-loop-status.py`, CI `phone-loop-guard` |

## Nie zrobione (wymaga Dowódcy / telefonu)

| # | Zadanie | Blocker |
|---|---------|---------|
| C2 | PAT read-only + `/etc/workflow-lab/hermes-engineer.env` | Brak pliku env na VPS (sprawdzone 2026-09-20) |
| C4 | E2e Telefon loop W-06 | Issue syntetyczne + kroki z telefonu |
| C4→A3 | `ENGINEER_LOOP_E2E=true` | Dopiero po C4 PASS |
| D1 | Draft platformy | Po C4 + HITL |

## Następny plan (▶ TERAZ)

1. **C2 (30 min):** Utwórz fine-grained PAT → `/etc/workflow-lab/hermes-engineer.env` (chmod 600) wg `workflow-lab/docs/ops/HERMES-ENGINEER-SECRETS.md`. Kanarek: `gh pr merge` → 403.
2. **C4 (1 sesja, telefon):** Issue lab `agent` + `@cursor` → PR → CI → review → merge. Log Engineera S1–S6 vs GitHub.
3. **PR akademia:** Po C4 — `ENGINEER_LOOP_E2E=true` + karta **AKTYWNY W LABIE**.
4. **D1:** Draft issue/PR platformy z checklistą R7 — bez merge bez GO.

## Komendy kontrolne

```bash
# Akademia (lokalnie)
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py

# Live eval (na VPS)
cd /opt/akademia && python3 scripts/hermes-eval.py --url https://akademia.quietforge.flexgrafik.nl ...

# Lab
python scripts/test_phone_loop_status.py
```
