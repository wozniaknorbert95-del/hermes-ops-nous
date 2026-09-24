# Hermes Ops — dokumentacja (Control Plane)

**UI:** [`/ops`](../../OPS.html) na tym samym hoście co Akademia (`/`).  
**Nauka kursu:** [`DASHBOARD.html`](../../DASHBOARD.html) — to **inny** produkt.  
**Mapa repo:** [`README.md`](../../README.md) · **ekosystem:** [`OPERATING-MODEL.md`](../OPERATING-MODEL.md) §1.1

Orchestrator (tick, merge): repozytorium **`workflow-lab`**, pakiet `scripts/hermes_ops/`. Ten katalog opisuje tylko UI vault i kontrakt.

## Czytaj w tej kolejności

1. [`HERMES-OPS-HOWTO.md`](HERMES-OPS-HOWTO.md) — 30 sekund: Linear, Start, brak merge z telefonu.
2. [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md) — role, routing etykiet, S0–S6, zdania guard CI.
3. [`RUNBOOK-OPS-WIRING.md`](RUNBOOK-OPS-WIRING.md) — tick, timer, awaria HUD.
4. [`CONTRACT-OPS-STATUS.md`](CONTRACT-OPS-STATUS.md) — `ops-status.json` / `ops-cmd.json`.
5. [`DEPLOY-READY-HERMES-OPS.md`](DEPLOY-READY-HERMES-OPS.md) — checklist przed deployem vault + `/ops`.

## Plan i audyt repo

- [`PLAN-AKTUALIZACJI-DOKUMENTACJI-HERMES-2026-09-24.md`](PLAN-AKTUALIZACJI-DOKUMENTACJI-HERMES-2026-09-24.md) — dokumentacja (WYKONANE).
- [`AUDYT-PLAN-HERMES-OPS-2026-09-24.md`](AUDYT-PLAN-HERMES-OPS-2026-09-24.md) — plan O1–O8.
- [`AUDYT-WYNIK-HERMES-OPS-2026-09-24.md`](AUDYT-WYNIK-HERMES-OPS-2026-09-24.md) — **WYKONANE** (2026-09-24, SHA `5c955f7`, bez deploy).
- [`../AUDYT-PLAN-AKADEMIA-2026-09-24.md`](../AUDYT-PLAN-AKADEMIA-2026-09-24.md) — plan audytu kursu (osobna sesja).

## Historyczne plany (kontekst)

Split Academy/Ops: [`../handoffs/2026-09-21-split-academy-ops.md`](../handoffs/2026-09-21-split-academy-ops.md)  
Awaria tick/deploy: [`../handoffs/2026-09-23-hermes-ops-awaria-plan.md`](../handoffs/2026-09-23-hermes-ops-awaria-plan.md)

## Smoke (bez sekretów w git)

```bash
curl -fsS http://127.0.0.1:8097/health
curl -fsS http://127.0.0.1:8097/ops/status
curl -fsS http://127.0.0.1:8097/ops/diag | python3 -m json.tool
```

Publicznie (Basic Auth): zamień host i `-u academy:HASLO` — patrz `AGENTS.md` § smoke.

Orchestrator tick: repozytorium **`workflow-lab`**, nie ten katalog.

**Heartbeat:** tylko tick pisze `ops-status.json.updated_at`. Pause / Stop na telefonie **nie** udają żywego timera. Brak `ops-cmd.json` po ACK = idle.
