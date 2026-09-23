# Deploy-ready — Hermes Ops + Akademia

> Uruchom: `bash scripts/deploy-ready-hermes-ops.sh`  
> Deploy (GO Dowódcy): `bash scripts/deploy-akademia-vps.sh`

## Checklist (automatyczna bramka)

| # | Warunek | Skrypt |
| --- | --- | --- |
| 1 | Kontrakt UI + ops QUI-70 | `validate-academy-export.py` |
| 2 | Vault + dispatch/diag | `test_progress_vault.py` |
| 3 | Mutacje Fala 0,D,E,I,J,K,L,M,N | `mutation-test-fala-*.py` |
| 4 | Git clean + `HEAD == origin/main` | w `deploy-ready-hermes-ops.sh` |
| 5 | Pliki deploy/smoke obecne | setup + smoke + deploy scripts |

## Po deploy na VPS (setup robi automatycznie)

1. `ensure_hermes_ops_cmd_file` — plik, nie katalog
2. `fix_hermes_ops_systemd` — `MakeDirectory=false` na path unit
3. `scripts/smoke-hermes-ops-vps.sh` — health, `/ops/diag`, `/ops/status`, opcjonalnie public `/ops`

## Ręczna weryfikacja (Dowódca)

```bash
curl -fsS -u academy:HASLO https://akademia.quietforge.flexgrafik.nl/ops/diag | python3 -m json.tool
systemctl is-active hermes-ops.timer hermes-ops-cmd.path
```

Telefon: Start → **QUEUED** (nie RUNNING bez ack ticka).

Powiązane: [`DEPLOY-READY-QUI-70.md`](DEPLOY-READY-QUI-70.md) · [`RUNBOOK-OPS-WIRING.md`](RUNBOOK-OPS-WIRING.md)
