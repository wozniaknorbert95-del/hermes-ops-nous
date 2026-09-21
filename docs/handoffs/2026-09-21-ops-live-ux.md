# Handoff — Hermes Ops live + polerka /ops (2026-09-21)

**Repo:** `akademia` + `workflow-lab`  
**Status:** kod na feat. Deploy Akademii + timer VPS po merge.

## Co dowiezione

1. **Timer `hermes-ops`** (osobny od read-only `hermes-phone-loop`):
   - `scripts/install-hermes-ops-vps.sh`
   - cache → `/opt/akademia/data/ops-status.json`
   - komenda z telefonu → `/opt/akademia/data/ops-cmd.json`
   - Pause **przetrwa** tick (state file).
2. **Linear fail-closed:** brak `LINEAR_OPS_READ` = `UNKNOWN`, nie pusta zieleń. Query po **nazwie projektu** (`workflow-lab` / `dsaas-platform-main`), nie po fałszywym UUID.
3. **Vault** czyta ten sam plik (`HERMES_OPS_STATUS` w compose).
4. **UX `/ops`:** sticky stan, banner UNKNOWN, karty issue 44px, Live = krok S n (nie JSON), safe-area, Run next z pierwszego toru Manual.

## Tokeny (nie w git)

`/etc/workflow-lab/hermes-engineer.env`:
- `LINEAR_OPS_READ` — bez tego kolejka UNKNOWN
- `GITHUB_OPS_WRITE` — bez tego Run next/merge nie ruszy
- `OPS_MODE=MANUAL` (Autopilot tylko świadomie)

Na VPS przed tą sesją był **tylko** `GITHUB_ENGINEER_TOKEN`.

## Testy

- lab: `python scripts/test_hermes_ops.py`
- akademia: validator + vault + Fala M **7/7** (M7 = 44px)

## Świadomie nie

- Autonomiczny deploy platformy
- Wklejanie sekretów Linear/GitHub write z czatu
