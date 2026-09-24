# Handoff — vault heartbeat (I1–I7) 2026-09-24

**Repo:** akademia · **Branch:** `feat/ops-vault-heartbeat`  
**Strefa:** `host/progress_vault.py` + kontrakt + testy. **Nie:** DASHBOARD.html, workflow-lab, deploy.

## Co zrobione (fakty)

- I1: `patch_ops_status(..., bump_updated=False)` default — Pause/Stop/Take over nie podszywają się pod tick.
- I3/I5: `ensure_ops_cmd_file()` w `main()`; `/health.ops_cmd_state`; brak pliku = idle, katalog = 409.
- I2: Start nadal QUEUED, nigdy RUNNING.
- Decision receipt: `POST /ops/run` → `{ queued, vault.patch_ok }`.
- Kontrakt §0 field ownership; HOWTO; RUNBOOK idle-after-ACK; smoke bez fałszywego WARN.
- Auth matrix w `docs/runbooks/AKADEMIA-VPS.md` §10.0 (bez breaking bearer na `/ops/status`).

## Invariants

| ID | Test / mutacja |
| --- | --- |
| I1 | pause nie bumpuje `updated_at`; N3 + N3b |
| I2 | start ≠ RUNNING (istniejące + N6) |
| I3 | directory → 409; N10/N11 |
| I4 | `queued.id` na POST start |
| I5 | empty cmd → idle, hint bez STALLED; N12 |
| I6 | stale + start cmd → stalled (istniejące) |
| I7 | deploy/merge 403 (istniejące) |

## Co live

Bez deploy. VPS nadal SHA sprzed igły aż do GO.

## Co zablokowane

- Deploy VPS — Zasada 11.
- O6 Linear e2e — issue testowe labu.
- Bearer na loopback `/ops/status` — osobny PR.

## Następny krok (▶ TERAZ)

**Merge PR → GO deploy → smoke VPS → opcjonalnie issue test lab (O6).**

## Komendy weryfikacji

```bash
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
python scripts/mutation-test-fala-n.py
# pełna linia testy: z AGENTS.md
- `bash scripts/deploy-ready-hermes-ops.sh` — po merge do `main` (skrypt wymaga `HEAD == origin/main`).
```

## Pliki dotknięte

- `host/progress_vault.py`
- `scripts/test_progress_vault.py`, `mutation-test-fala-n.py`, `validate-academy-export.py`, `smoke-hermes-ops-vps.sh`
- `docs/ops/CONTRACT-OPS-STATUS.md`, `HERMES-OPS-HOWTO.md`, `RUNBOOK-OPS-WIRING.md`, `README.md`, `DEPLOY-READY-HERMES-OPS.md`, `AUDYT-WYNIK-HERMES-OPS-2026-09-24.md`
- `docs/runbooks/AKADEMIA-VPS.md`
- `docs/handoffs/2026-09-24-ops-vault-heartbeat.md`
