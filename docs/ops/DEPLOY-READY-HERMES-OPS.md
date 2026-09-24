# Deploy-ready — Hermes Ops + Akademia

> Mapa repo (Akademia + `/ops`): [`README.md`](../../README.md) · indeks docs: [`README.md`](README.md)  
> Uruchom: `bash scripts/deploy-ready-hermes-ops.sh`  
> Deploy (GO Dowódcy): `bash scripts/deploy-akademia-vps.sh`

## Status 2026-09-24 (vault heartbeat igła — bez deploy)

| Etap | Wynik |
| --- | --- |
| gałąź | `feat/ops-vault-heartbeat` (I1: Pause nie bumpuje `updated_at`) |
| `ensure_ops_cmd_file` w `main()` | ✅ plik `{}` albo diag `directory` |
| smoke missing cmd | idle PASS (nie WARN) |
| `bash scripts/deploy-akademia-vps.sh` | ⏸ **nie** — GO Zasada 11 |

## Status 2026-09-24 (audyt Ops, bez deploy)

| Etap | Wynik |
| --- | --- |
| `main` | ✅ `5c955f7` (PR #63 docs + IA Akademii) |
| `bash scripts/deploy-ready-hermes-ops.sh` | ✅ PASS (HEAD == origin/main) |
| `bash scripts/smoke-hermes-ops-vps.sh` na VPS | ✅ SMOKE PASS (read-only; WARN: brak `ops-cmd.json`) |
| `/ops/diag` | ✅ `tick_alive: true`, dispatch `idle`, `MakeDirectory=false` |
| `bash scripts/deploy-akademia-vps.sh` | ⏸ **nie** — brak GO Zasada 11 w tej sesji |

HUD `/ops` na VPS już zawiera Autopilot + Take over + STALLED + refuse 403 (#59–#61). Redeploy vault/`OPS.html` **nie jest wymagany** dla Ops. Raport: [`AUDYT-WYNIK-HERMES-OPS-2026-09-24.md`](AUDYT-WYNIK-HERMES-OPS-2026-09-24.md).

## Status 2026-09-23

| Etap | Wynik |
| --- | --- |
| PR #53 → `main` | ✅ `eb37d00` |
| PR #54 → `main` | ✅ `c13c346` |
| `bash scripts/deploy-ready-hermes-ops.sh` | ✅ PASS |
| `bash scripts/deploy-akademia-vps.sh` | ✅ VPS 2026-09-23T18:21Z — `tick_alive: true`, `ops-cmd.json` plik, `MakeDirectory=false`, SMOKE PASS |

Cloud Agent (`bc-db1ab4b8`) nie miał klucza SSH. Deploy zrobił laptop Dowódcy (GO Zasada 11). Szczegóły: [`docs/handoffs/2026-09-23-cloud-triage-deploy.md`](../handoffs/2026-09-23-cloud-triage-deploy.md).

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
