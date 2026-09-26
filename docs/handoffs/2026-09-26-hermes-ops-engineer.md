# Handoff — Hermes Ops engineer (audyt 3290 + Fale 1–3 + Cloud)

**Data:** 2026-09-26  
**Repo:** akademia `main` `c7a7a4a` (PR #71) · platforma `main` (PR #124)  
**Nie:** `workflow-lab` · plan file · QUI-102 · merge z telefonu

## Co

Audyt dwóch runów Cloud 3290 (QUI-93 #115, QUI-83 #117) + HUD 3 strefy + bramka DoR przed `@cursor` + pętla Cloud `/vibeinit→/gate→/verify` + strażnik check_runs + pulse 3 issue.

## Dowód

- `docs/ops/AUDYT-HERMES-OPS-ENGINEER-2026-09-26.md`
- `/ops`: chipy DoR/lane/testy/CI/todo, fold 360px, kolejka nie-Run, pulse, zero Tokens/Cost
- `POST /ops/run` 400: `qui_dor_not_ready` · `qui_hitl` · `qui_blocked` · `qui_lane_local` · `qui_todo_mismatch` · `qui_dirty_pr` · `missing_LINEAR_OPS_READ`
- Platforma: `session-preflight.py` nie spycha QUI-93 na LOCAL przez słowo `workflow_dispatch` w AC; `ci_check_guardian.py` (billing ≠ automerge)

## Testy

Pełna linia `testy:` w `AGENTS.md` (Fala Q + R) PASS. Platforma: `tests/test_session_preflight.py` + `tests/test_ci_check_guardian.py` + `tests/test_cursor_pack.py` PASS.

Weryfikacja 26.09 wieczór: Linear lookup = team+number (nie UUID); `run.dor` na GET `/ops/status`; linia `Cloud: /gate` na foldzie.

## NEXT

**ZAMKNIĘTE.** Deploy + Linear SET: `docs/handoffs/2026-09-26-hermes-ops-vps-deploy.md`.

Nie budź Cloud z telefonu. Nie ruszaj QUI-102. Merge z telefonu = nie.
