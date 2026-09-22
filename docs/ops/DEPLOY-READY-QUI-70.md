# Deploy-ready — QUI-70 (Akademia)

> Status Części 1: **DONE** (T1–T8, PR #49 → `main`). Część 2 E1–E5: **DONE** na VPS (`workflow-lab@5378d85`).

## Werdykt

| Warstwa | Stan |
| --- | --- |
| Kod T1–T8 | ✅ `main` @ `7c4b7fd` (PR #49) |
| Testy lokalne + Fala N | ✅ |
| CI `academy-gate` | ✅ |
| E1–E5 (lab/VPS) | ✅ smoke QUI-88 → RUNNING + GH #80 |
| Deploy VPS Akademia | ⛔ ręcznie (Zasada 11) |
| `agent.run_url` | ⏳ wypełni się gdy Cursor Cloud skomentuje run URL |

## Checklist przed `bash scripts/deploy-akademia-vps.sh`

1. [x] PR #49 zmergowany do `main`
2. [ ] Lokalnie: `git checkout main && git pull` — working tree czysty
3. [ ] `HEAD == origin/main` (inaczej skrypt odmówi bez `--force`)
4. [ ] Smoke po deploy: `curl -fsS http://127.0.0.1:8097/health`
5. [ ] Public: `curl -fsS -u academy:HASLO https://…/ops/diag` → `tick_alive` / `dispatch` czytelne
6. [ ] Telefon: Start → QUEUED; po ticku → RUNNING dopiero z `ack` (nie optimistic)

## Po deploy

Runbook: [`RUNBOOK-OPS-WIRING.md`](RUNBOOK-OPS-WIRING.md).  
Handoff E1–E5: [`../handoffs/2026-09-22-ops-wiring-qui-70.md`](../handoffs/2026-09-22-ops-wiring-qui-70.md).
