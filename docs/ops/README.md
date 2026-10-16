# Hermes Ops — dokumentacja (Control Plane)

**UI:** [`/ops`](../../OPS.html) — osobne repo `hermes-ops-nous`.  
**Ekosystem:** [`docs/OPERATING-MODEL-HERMES-OPS.md`](../OPERATING-MODEL-HERMES-OPS.md) — role, przepływy, zakazy.  
**SoT zadań inżynieryjnych tego repo:** [`../../todo.json`](../../todo.json) (`HON-*`). Kolejka Autopilot = Linear.

Orchestrator (tick, merge): repozytorium **`workflow-lab`**, pakiet `scripts/hermes_ops/`. Ten katalog opisuje tylko UI vault i kontrakt.

## Stan żywy (2026-10-16)

| Fakt | Źródło |
| --- | --- |
| T1c PASS (3× Start→https `run_url`) + T3 `run_all` | [`DIRECTION-LOCK-2026-10-13.md`](DIRECTION-LOCK-2026-10-13.md), [`../handoffs/2026-10-16-conductor-t1c-pass.md`](../handoffs/2026-10-16-conductor-t1c-pass.md) |
| Merge + deploy verify | [`../handoffs/2026-10-16-verify-merge-deploy.md`](../handoffs/2026-10-16-verify-merge-deploy.md) |
| Freeze polish HUD (F5) | ON do osobnego GO; **F4 chat GO** (`/ops/chat` facts) |
| NEXT | tor `NOUS-PRODUCT-LOOP` — `todo.json` → `HON-OPS-PROD-01` (produktowy Start ≤3 min) |

**Handoff = append-only** (dowód sesji). Stan żywy = Direction Lock + `todo.json`, nie najnowszy czat ani stary PLAN z WAITING-GO.

## Hierarchia prawdy

1. [`DIRECTION-LOCK-2026-10-13.md`](DIRECTION-LOCK-2026-10-13.md)  
2. [`../../todo.json`](../../todo.json)  
3. [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md) + [`CONTRACT-OPS-STATUS.md`](CONTRACT-OPS-STATUS.md)  
4. Handoff dnia w `docs/handoffs/`  
5. Historyczne PLAN-/AUDYT- — kontekst; przy sprzeczności ze (1)–(2) nie są SoT

## Czytaj w tej kolejności (żywe)

0. [`../../todo.json`](../../todo.json) — aktywne `HON-*` + NEXT sesji.  
1. [`DIRECTION-LOCK-2026-10-13.md`](DIRECTION-LOCK-2026-10-13.md) — freeze, KPI `run_url`, NEXT produktu.  
2. [`PLAN-HERMES-CONDUCTOR-2026-10-01.md`](PLAN-HERMES-CONDUCTOR-2026-10-01.md) — kontrakt Nous+Cloud (**slice/T1c WYKONANY**). Lab e2e = [`conductor-slice-e2e.json`](conductor-slice-e2e.json).  
3. [`HERMES-OPS-HOWTO.md`](HERMES-OPS-HOWTO.md) — 30 sekund: Linear, Start, brak merge z telefonu.  
4. [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md) — role, routing etykiet, S0–S6.  
5. [`RUNBOOK-OPS-WIRING.md`](RUNBOOK-OPS-WIRING.md) — tick, timer, awaria HUD.  
6. [`CONTRACT-OPS-STATUS.md`](CONTRACT-OPS-STATUS.md) — `ops-status.json` / `ops-cmd.json`.  
7. [`DEPLOY-READY-HERMES-OPS.md`](DEPLOY-READY-HERMES-OPS.md) — checklist przed deployem vault + `/ops`.

## Historyczne (kontekst, nie SoT stanu)

- [`AUDYT-WYNIK-DIRECTION-LOCK-2026-10-13.md`](AUDYT-WYNIK-DIRECTION-LOCK-2026-10-13.md) — T0 (conductor halted = historyczny STOP).  
- [`AUDYT-WYNIK-HERMES-OPS-2026-10-11.md`](AUDYT-WYNIK-HERMES-OPS-2026-10-11.md) · [`AUDYT-WYNIK-HERMES-OPS-2026-10-03.md`](AUDYT-WYNIK-HERMES-OPS-2026-10-03.md) · [`AUDYT-UX-HERMES-OPS-LIVE-2026-10-03.md`](AUDYT-UX-HERMES-OPS-LIVE-2026-10-03.md)  
- [`PLAN-UX-POLISH-2026-10-03.md`](PLAN-UX-POLISH-2026-10-03.md) · [`PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md`](PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md) — polish **BLOCKED** do GO unfreeze.  
- Split Academy/Ops: [`../handoffs/2026-09-21-split-academy-ops.md`](../handoffs/2026-09-21-split-academy-ops.md)  
- Awaria tick/deploy: [`../handoffs/2026-09-23-hermes-ops-awaria-plan.md`](../handoffs/2026-09-23-hermes-ops-awaria-plan.md)  
- [`LOCAL-GATE.md`](LOCAL-GATE.md) — merge bez płatnego GitHub Actions (laptop = bramka).

## FUTURE / PARKED (nie aktywny tor)

- [`../ops/workflow-marzen/`](../ops/workflow-marzen/) — workflow marzeń / GitLab CE self-hosted; wymaga osobnego GO VPS. Nie bierz jako NEXT sesji.

```bash
curl -fsS http://127.0.0.1:8097/health
curl -fsS http://127.0.0.1:8097/ops/status
curl -fsS http://127.0.0.1:8097/ops/diag | python3 -m json.tool
python scripts/validate_todo_nous.py
```

Publicznie (Basic Auth): zamień host i `-u academy:HASLO` — patrz `AGENTS.md` § smoke.

Orchestrator tick: repozytorium **`workflow-lab`**, nie ten katalog.

**Heartbeat:** tylko tick pisze `ops-status.json.updated_at`. Pause / Stop na telefonie **nie** udają żywego timera. Brak `ops-cmd.json` po ACK = idle.
