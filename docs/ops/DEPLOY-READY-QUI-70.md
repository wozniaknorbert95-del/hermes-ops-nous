# Deploy-ready — QUI-70 (Akademia)

> Status Części 1 planu: **GOTOWE** (T1–T8). Część 2 (E1–E5) = poza tym repo.

## Werdykt

| Warstwa | Stan |
| --- | --- |
| Kod T1–T8 | ✅ w `feat/ops-wiring-qui-70` / PR #49 |
| Testy lokalne + Fala N | ✅ (linia `testy:` w AGENTS.md) |
| CI `academy-gate` | ✅ wymagane zielone przed merge |
| Deploy VPS | ⛔ dopiero po **merge do `main`** (Zasada 11 + bramka `deploy-akademia-vps.sh`) |
| Agent Cursor realnie rusza | ⛔ wymaga E1–E5 (workflow-lab / VPS) |

## Checklist przed `bash scripts/deploy-akademia-vps.sh`

1. [ ] PR #49 zmergowany do `main`
2. [ ] Lokalnie: `git checkout main && git pull` — working tree czysty
3. [ ] `HEAD == origin/main` (inaczej skrypt odmówi bez `--force`)
4. [ ] Smoke po deploy: `curl -fsS http://127.0.0.1:8097/health`
5. [ ] Public: `curl -fsS -u academy:HASLO https://…/ops/diag` → `tick_alive` / `dispatch` czytelne
6. [ ] Telefon: Start → QUEUED (nie RUNNING); przy starym ticku → STALLED

## Po deploy — zewnętrzne (E1–E5)

Patrz [`PLAN-OPS-WIRING-QUI-70.md`](PLAN-OPS-WIRING-QUI-70.md) § Część 2 oraz [`RUNBOOK-OPS-WIRING.md`](RUNBOOK-OPS-WIRING.md).
Bez E1/E2 telefon będzie uczciwie pokazywał QUEUED/STALLED — agent i tak nie wystartuje.
