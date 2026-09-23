# Handoff — awaria Hermes Ops: plan + fix deploy/tick (2026-09-23)

**Run Cloud Agent:** `bc-db1ab4b8` · **Repo:** akademia + workflow-lab (path unit)  
**Main po merge:** `c13c346` (PR #54) · **Deploy-ready:** PASS · **Deploy VPS:** DONE 2026-09-23T18:21Z (handoff: `2026-09-23-cloud-triage-deploy.md`)

## Werdykt root cause (najbardziej prawdopodobne)

| Priorytet | Ogniwo | Dowód | Fix |
| --- | --- | --- | --- |
| P0 | **Deploy Akademii nie dojechał** | `DEPLOY-READY-QUI-70.md`: deploy ręczny; main @ `29cd270` (#52) — brak smoke z tego agenta na VPS (brak SSH) | `bash scripts/deploy-akademia-vps.sh` z czystego `main` |
| P0 | **`ops-cmd.json` = katalog** | Runbook + #52: Docker/systemd trap → `409`, Start martwy | `ensure_hermes_ops_cmd_file` w `setup-akademia-vps.sh` (ten PR) |
| P1 | **Tick martwy (E2)** | `/ops/diag` → `tick_alive: false`, hint runbook A | VPS: `install-hermes-ops-vps.sh`, `systemctl is-active hermes-ops.timer hermes-ops-cmd.path` |
| P1 | **Path unit `MakeDirectory=true`** | workflow-lab: tworzy katalog zamiast pliku | lab PR: `MakeDirectory=false` + sed w install |

Lokalnie (agent): **PASS** — `test_progress_vault.py`, `validate-academy-export.py`, `test_hermes_ops.py` (lab).

## Plan działania (Dowódca / VPS)

1. **Diagnoza bez zgadywania** (5 min): `curl -fsS -u academy:*** https://akademia…/ops/diag | python3 -m json.tool` — odczytaj `hint`, `dispatch.state`, `tick_alive`.
2. **Deploy Akademii** (Zasada 11): `git checkout main && git pull` → `bash scripts/deploy-akademia-vps.sh` — setup teraz naprawia `ops-cmd.json` i smoke `/ops/diag`.
3. **Lab path unit** (jeśli katalog wraca): w `/opt/workflow-lab` pull + `bash scripts/install-hermes-ops-vps.sh`.
4. **Telefon:** Start → **QUEUED** (nie RUNNING) → po ticku ack / REFUSED z powodem (E1/E3).

## Komendy weryfikacji (copy-paste)

```bash
# Lokalnie (repo akademia)
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py

# VPS (po deploy)
curl -fsS http://127.0.0.1:8097/health
curl -fsS http://127.0.0.1:8097/ops/diag | python3 -m json.tool
ls -la /opt/akademia/data/ops-cmd.json /opt/akademia/data/ops-status.json
systemctl is-active hermes-ops.timer hermes-ops-cmd.path
```

## Pliki dotknięte (akademia)

- `scripts/setup-akademia-vps.sh` — preflight ops-cmd + smoke Hermes Ops
- `scripts/validate-academy-export.py` — guard deploy smoke
- `docs/ops/RUNBOOK-OPS-WIRING.md` — wiersz katalog ops-cmd

## Pliki dotknięte (workflow-lab, osobny PR — bot bez push)

- `docs/ops/hermes-ops-cmd.path.example` — `MakeDirectory=false`
- `scripts/install-hermes-ops-vps.sh` — wymuszenie przy instalacji

## Uzupełnienie sesji 2 (bez skrótów)

- `scripts/deploy-ready-hermes-ops.sh` — pełna bramka AGENTS.md + git
- `scripts/smoke-hermes-ops-vps.sh` — smoke na VPS (setup kończy fail-closed)
- `host/systemd/hermes-ops-cmd.path.snippet` — SoT MakeDirectory=false
- `fix_hermes_ops_systemd` w setup — patch path unit bez czekania na lab PR
- `deploy-akademia-vps.sh` woła deploy-ready przed tar
- `docs/ops/DEPLOY-READY-HERMES-OPS.md`
