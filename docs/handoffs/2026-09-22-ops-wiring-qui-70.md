# Handoff — QUI-70 ops wiring (Akademia)

**Data:** 2026-09-22  
**Gałąź:** `feat/ops-wiring-qui-70`  
**PR:** https://github.com/wozniaknorbert95-del/akademia/pull/49 (draft)

## Werdykt planu

| Zakres | Stan |
| --- | --- |
| **Część 1 T1–T8** (to repo) | **DONE** + polerka enterprise (Fala N, BOM, diag thresholds) |
| **Część 2 E1–E5** (VPS / workflow-lab) | **NIE** — poza Akademią, celowo |

## Deploy-ready

Patrz `docs/ops/DEPLOY-READY-QUI-70.md`. Deploy VPS **dopiero po merge do main** (Zasada 11). Bez E1/E2 agent nie ruszy — telefon już nie kłamie RUNNING.

## Polerka enterprise

- `utf-8-sig` na odczycie ops JSON (BOM z Windows)
- `/ops/diag`: `last_cmd.age_sec` + `thresholds`
- Guardy walidatora `ops-qui70:*` + `mutation-test-fala-n.py` (CI + AGENTS.md)
