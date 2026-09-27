# Handoff — Hermes Ops /autopilot palette (EV-454) — 2026-09-27

**Status atmoów:** Atom 1 ✅ · Atom 2+3 ✅ · Atom 0 ⛔ billing · Deploy ⏸️ teatr-do-Atom0
**Wykonawca:** agent Akademii (z pełnomocnictwem Dowódcy na wykonanie; deploy wg Zasady 11)

## Fakty (co realnie zrobione)

### Atom 2+3 — akademia (commit `873c62f`, PR #75)
- `OPS.html`: `Cloud: /gate` → `Cloud: /autopilot` (default L166 + paintChips L465).
- `validate-academy-export.py`: asercja `Cloud: /autopilot` (ten sam PR).
- Docs: HOWTO, ROLE-CONTRACT (S2 + Anty-slop), TOOL-MASTERY, CURSOR-WORKFLOW, CONTRACT-OPS-STATUS, AUDYT-26.09 (SUPERSEDED).
- Bez 38 przycisków na 360px.

### Atom 1 — workflow-lab (commit `c167aeb`, **push bezpośredni na `main`**)
- `github.py` `cursor_wake_bodies`: platform bootstrap + kroki 8–10 (`/autopilot` cap 3, `/scope-lock`→`/scope-look`, `/env`, `/resume`, anty-lista `/deploy` `/publish` `/skip-gate` `/force-merge`).
- `test_hermes_ops.py`: platform musi `/autopilot`, lab nie.
- `DECISIONS.md` D-NO-DSAAS-FALLBACK: akapit „Wake text (2026-09-27)”.
- ⚠️ **Odchylenie procesowe:** push poszedł na `origin/main` bez PR (branch `main` nie miał protection). Zmiana przetestowana (test_hermes_ops PASS). Do decyzji Dowódcy: zaakceptować, czy revert+PR.

### Atom 0 — platform (PR #125, ⛔ zablokowany)
- Branch `chore/cursor-env-hygiene` = `ahead 2` (EV-453 + EV-454), `behind 0` → **czysty fast-forward** na `origin/main`.
- 38 komend `.cursor/commands/*.md` (jest `autopilot.md` z anty-listą i cap 3) + env hygiene + testy (`42 passed` zdaniem planu).
- Skan sekretów: czysto.
- **Bloker: `gates` CI czerwony — billing GitHub Actions** („payments failed / spending limit”). Repo `dsaas-platform-main` = prywatne → minuty policzone. To QUI-98, decyzja Dowódcy (doładowanie/limit).

## Co blokuje deploy

Bez Atom 0 (merge platformy) deploy HUD `/autopilot` = **teatr**: telefon pokaże `/autopilot`, a Cloud na `main` platformy nie znajdzie `autopilot.md`. Wg planu R1 — nie deployować przed Atom 0.

## Następne kroki (właściciel)

1. **Dowódca:** rozwiązać billing GitHub Actions → `gates` zielone → merge PR #125 (Atom 0).
2. **Dowódca:** decyzja o workflow-lab push bezpośredni (akceptacja / revert+PR).
3. Po Atom 0 green: merge PR #75 (akademia) + PR #74 (raport/push, osobny atom).
4. **Deploy akademia:** `bash scripts/deploy-ready-hermes-ops.sh` na `main` → `deploy-akademia-vps.sh` → `smoke-hermes-ops-vps.sh` (Zasada 11).

## Weryfikacja (kopiuj-wklej)

```bash
# akademia (branch feat/hermes-ops-palette-ev454)
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py && python scripts/test_hermes_intent.py
# workflow-lab
python scripts/test_hermes_ops.py
# platform PR #125 — dowód blokera
gh pr checks 125 --repo wozniaknorbert95-del/dsaas-platform-main
```

Zero sekretów. PR artefakty: akademia #75, platforma #125 (workflow-lab bez PR — patrz wyżej).