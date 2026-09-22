# Handoff — QUI-70 ops wiring (Akademia + VPS E1–E5)

**Data:** 2026-09-22  
**Akademia:** PR [#49](https://github.com/wozniaknorbert95-del/akademia/pull/49) → `main` @ `7c4b7fd`  
**Lab:** `workflow-lab@5378d85` (PR #69/#71/#76/#78/#79) wdrożone na VPS `/opt/workflow-lab`

## Werdykt planu

| Zakres | Stan |
| --- | --- |
| **Część 1 T1–T8** (akademia) | **DONE** — zmergowane do `main` |
| **Część 2 E1–E5** (VPS / workflow-lab) | **DONE** — smoke poniżej |

## Smoke E1–E5 (VPS 2026-09-22 ~21:20 CEST)

| ID | Dowód |
| --- | --- |
| E1 | `LINEAR_OPS_READ=SET`, `GITHUB_OPS_WRITE=SET` |
| E2 | `hermes-ops.timer` + `hermes-ops-cmd.path` = `active` |
| E3 | Start QUI-SMOKE → `ack` + `refuse=empty_queue`; Start przy cap → `refuse=cap_OPS_MAX_RUNS_PER_DAY` |
| E4 | Start QUI-88 → `RUNNING` + issue [workflow-lab#80](https://github.com/wozniaknorbert95-del/workflow-lab/issues/80) z `@cursor` w body (`environment.json` obecny) |
| E5 | `live.repo=workflow-lab`, `github_issue=80`, `pr_url=null` (uczciwie), `agent.run_url=""` do czasu komentarza Cursor Cloud |

## Token caveat

Fine-grained `GITHUB_OPS_WRITE` **tworzy** issue, ale **403 na comments**. Trigger: `@cursor` w body + fallback create na `workflow-lab` gdy dsaas create 403. Dla niezawodniejszego `@cursor` dodaj *Issues: Write* (komentarze) na PAT.

## Deploy Akademia

Zasada 11 — ręcznie po merge: `bash scripts/deploy-akademia-vps.sh`  
Checklist: `docs/ops/DEPLOY-READY-QUI-70.md`
