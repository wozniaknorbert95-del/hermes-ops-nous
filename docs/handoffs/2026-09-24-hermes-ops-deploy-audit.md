# Handoff — audyt Hermes Ops O1–O8 (2026-09-24)

**Repo:** akademia · **Strefa:** `/ops`, vault, VPS smoke (read-only)  
**Main:** `5c955f7` (PR #63) · **Deploy:** brak (Zasada 11 — nie było GO)

## Co zrobione (fakty)

- Sync `main`, lektura kontraktów (`docs/ops/README` → ROLE → HOWTO → RUNBOOK → CONTRACT → DEPLOY-READY).
- Audyt O1–O8 wg [`docs/ops/AUDYT-PLAN-HERMES-OPS-2026-09-24.md`](../ops/AUDYT-PLAN-HERMES-OPS-2026-09-24.md).
- Raport: [`docs/ops/AUDYT-WYNIK-HERMES-OPS-2026-09-24.md`](../ops/AUDYT-WYNIK-HERMES-OPS-2026-09-24.md).
- Zaktualizowano `DEPLOY-READY-HERMES-OPS.md` (SHA, smoke, brak deploy).
- `DASHBOARD.html` / welcome / plan audytu Akademii — **nietknięte**.

| Faza | Werdykt |
| --- | --- |
| O1 docs | PASS |
| O2 vault + 410 | PASS (`test_progress_vault.py`; VPS chat 410) |
| O3 UI 360px | PASS (Autopilot, QUEUED, Take over, STALLED copy, Approval ≠ Merge) |
| O4 ops-cmd.json | PASS z P2 (nie katalog; plik nie istnieje; MakeDirectory=false) |
| O5 tick_alive | PASS (`true`, timer+path active) |
| O6 e2e Linear | SKIP (brak issue test; nie Start QUI-92) |
| O7 smoke | PASS lokalnie deploy-ready + VPS smoke (bez `deploy-akademia-vps.sh`) |
| O8 Fala M/N | PASS, 0 PRZEPUSZCZONE |

## Co live

- `/ops` na VPS: HUD Autopilot + Take over + refuse 403; `tick_alive: true`; public GET `/ops` 200.
- Dispatch: `idle` (uczciwe, nie RUNNING).
- Engine: `PAUSED` / `AUTOPILOT` / `reason=vps_timer`.

## Co zablokowane

- Deploy VPS — czeka na GO Dowódcy.
- O6 S0–S6 — czeka na issue testowe labu (nie produkcyjne).
- `ops-cmd.json` nie leży na dysku (P2; smoke WARN).

## Następny krok (jeden TERAZ)

**Nie Startuj QUI-92 z `/ops`; przy następnym GO deploy dociągnij pusty plik `ops-cmd.json` (`ensure_hermes_ops_cmd_file`) razem z Akademią 6 zakładek.**

## Komendy weryfikacji

```bash
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
python scripts/mutation-test-fala-m.py && python scripts/mutation-test-fala-n.py
bash scripts/deploy-ready-hermes-ops.sh
# na VPS (read-only):
bash /opt/akademia/scripts/smoke-hermes-ops-vps.sh
curl -fsS http://127.0.0.1:8097/ops/diag
# deploy tylko po GO:
# bash scripts/deploy-akademia-vps.sh
```

## Pliki dotknięte

- `docs/ops/AUDYT-WYNIK-HERMES-OPS-2026-09-24.md` (nowy)
- `docs/ops/AUDYT-PLAN-HERMES-OPS-2026-09-24.md` (checkbox GO)
- `docs/ops/DEPLOY-READY-HERMES-OPS.md`
- `docs/ops/README.md` (link do wyniku)
- `docs/handoffs/2026-09-24-hermes-ops-deploy-audit.md` (ten plik)
