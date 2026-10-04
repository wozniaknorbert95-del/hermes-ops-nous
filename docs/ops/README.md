# Hermes Ops — dokumentacja (Control Plane)

**UI:** [`/ops`](../../OPS.html) na tym samym hoście co Akademia (`/`).  
**Nauka kursu:** [`DASHBOARD.html`](../../DASHBOARD.html) — to **inny** produkt.  
**Mapa repo:** [`README.md`](../../README.md) · **ekosystem:** [`OPERATING-MODEL.md`](../OPERATING-MODEL.md) §1.1

Orchestrator (tick, merge): repozytorium **`workflow-lab`**, pakiet `scripts/hermes_ops/`. Ten katalog opisuje tylko UI vault i kontrakt.

## Czytaj w tej kolejności

0. [`PLAN-HERMES-CONDUCTOR-2026-10-01.md`](PLAN-HERMES-CONDUCTOR-2026-10-01.md) — Nous prowadzi, Cursor Cloud API buduje, tick = status. Lab e2e = [`conductor-slice-e2e.json`](conductor-slice-e2e.json). Deploy HTML = Zasada 11.
1. [`HERMES-OPS-HOWTO.md`](HERMES-OPS-HOWTO.md) — 30 sekund: Linear, Start, brak merge z telefonu.
2. [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md) — role, routing etykiet, S0–S6, zdania guard CI.
3. [`RUNBOOK-OPS-WIRING.md`](RUNBOOK-OPS-WIRING.md) — tick, timer, awaria HUD.
4. [`CONTRACT-OPS-STATUS.md`](CONTRACT-OPS-STATUS.md) — `ops-status.json` / `ops-cmd.json`.
5. [`DEPLOY-READY-HERMES-OPS.md`](DEPLOY-READY-HERMES-OPS.md) — checklist przed deployem vault + `/ops`.

## Plan i audyt repo

- [`PLAN-UX-POLISH-2026-10-03.md`](PLAN-UX-POLISH-2026-10-03.md) — polerka po audycie: brief bez dubli (Fala A), etykiety `/ops` (B), chrome 360 (C). P0 audytu = live `#93`.
- [`PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md`](PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md) — katalog `/ops`; **P0 live**, **P1–P3 kod** (IA, hierarchia, dispatch, confirm, fold, skróty); deploy P1–P3 po GO.
- [`PLAN-AKADEMIA-START-2026-09-26.md`](PLAN-AKADEMIA-START-2026-09-26.md) — **aktualny SoT reguł Akademii** (7 tabów, TERAZ wchłania DZIEŃ, DSAAS = 18 DoD). HTML v7 WYKONANE. Deploy = WAITING-GO.
- [`UI-GO-AKADEMIA-V7.md`](UI-GO-AKADEMIA-V7.md) — HTML WYKONANE; deploy zablokowany.
- [`../ACADEMY-UX-SPEC.md`](../ACADEMY-UX-SPEC.md) — kontrakt v7.
- [`TOOL-MASTERY.md`](TOOL-MASTERY.md) — karty narzędzi (pełne vs PARKED).
- [`PLAN-AKADEMIA-SZTAB-2026-09-25.md`](PLAN-AKADEMIA-SZTAB-2026-09-25.md) — historia v6 (live HTML 8 tabów).
- [`PLAN-AKTUALIZACJI-DOKUMENTACJI-HERMES-2026-09-24.md`](PLAN-AKTUALIZACJI-DOKUMENTACJI-HERMES-2026-09-24.md) — dokumentacja (WYKONANE).
- [`AUDYT-PLAN-HERMES-OPS-2026-09-24.md`](AUDYT-PLAN-HERMES-OPS-2026-09-24.md) — plan O1–O8.
- [`AUDYT-WYNIK-HERMES-OPS-2026-10-03.md`](AUDYT-WYNIK-HERMES-OPS-2026-10-03.md) — re-audyt sterowania HUD + vault (Faza 1).
- [`AUDYT-UX-HERMES-OPS-LIVE-2026-10-03.md`](AUDYT-UX-HERMES-OPS-LIVE-2026-10-03.md) — live Fail: Start martwy, Retry ukryty, 401 gate.
- [`conductor-slice-e2e.json`](conductor-slice-e2e.json) — slice Nous/Cloud API = **WYKONANY** (QUI-113, ten sam `agentId`, follow-up). Handoff: [`../handoffs/2026-10-03-conductor-slice.md`](../handoffs/2026-10-03-conductor-slice.md). Merge labu #98 i deploy HTML = osobne GO.
- [`AUDYT-HERMES-OPS-ENGINEER-2026-09-26.md`](AUDYT-HERMES-OPS-ENGINEER-2026-09-26.md) — dwa runy Cloud 3290 (QUI-93/#115, QUI-83/#117) + program prawnej ręki.
- [`../AUDYT-PLAN-AKADEMIA-2026-09-24.md`](../AUDYT-PLAN-AKADEMIA-2026-09-24.md) — plan audytu kursu (osobna sesja).

## Historyczne plany (kontekst)

Split Academy/Ops: [`../handoffs/2026-09-21-split-academy-ops.md`](../handoffs/2026-09-21-split-academy-ops.md)  
Awaria tick/deploy: [`../handoffs/2026-09-23-hermes-ops-awaria-plan.md`](../handoffs/2026-09-23-hermes-ops-awaria-plan.md)

- [`LOCAL-GATE.md`](LOCAL-GATE.md) — merge bez płatnego GitHub Actions (laptop = bramka).

```bash
curl -fsS http://127.0.0.1:8097/health
curl -fsS http://127.0.0.1:8097/ops/status
curl -fsS http://127.0.0.1:8097/ops/diag | python3 -m json.tool
```

Publicznie (Basic Auth): zamień host i `-u academy:HASLO` — patrz `AGENTS.md` § smoke.

Orchestrator tick: repozytorium **`workflow-lab`**, nie ten katalog.

**Heartbeat:** tylko tick pisze `ops-status.json.updated_at`. Pause / Stop na telefonie **nie** udają żywego timera. Brak `ops-cmd.json` po ACK = idle.
