# Handoff — Hermes prowadzący + Cursor Cloud API — 2026-10-01

**Status:** Kod na `feat/hermes-conductor-cloud-api`. Nie commituj / nie deploy. Slice live (Nous na VPS) = **WAITING-GO**.

## Co zrobione

Werdykt planu: jeden mózg. **Nous** woła Cursor Cloud Agents API. Tick/vault = heartbeat + HUD. Zero drugiego S2 w Pythonie Akademii (`api.cursor.com` w vault = FAIL).

Akademia dostarcza kontrakt HUD + szablony conductor + baner prawdy. Nie udaje, że sesja już prowadzi.

- Kontrakt: zdania kanoniczne `Tick nie woła POST /v1/agents`, `S2 = Cursor Cloud Agents API`. `ENGINEER_LOOP_E2E=false` aż `conductor-slice-e2e.json`. Stary `engineer-loop-e2e.json` nie zapala AKTYWNY.
- `/ops`: chipy `buduj/testuj/ulepszaj`, `live.tests[]` + UNKNOWN gdy puste w RUNNING, AC/raport, refuse `missing_CURSOR_API_KEY` / `cursor_api_busy` / `conductor_timeout`. Take over = zero follow-up do Cursora.
- Vault: `work_mode`, `_sanitize_tests`, `_sanitize_conductor`, `tests_verdict`. RUNNING nie wymaga komentarza GitHub — sesja = `live.agent.run_url`.
- PWA: fingerprint `ops-report.py` obejmuje `line` (raport po runie, nie tylko 07:00). Telegram = P1 (TOOLSET).
- Karty/HOWTO: baner `Prowadzenie sesji = WAITING-GO (lab+Nous). To nie jest @cursor.` 6 pathów labu zostaje; label W2 = Cloud API.
- Szablony VPS (zero kluczy): `docs/ops/hermes-conductor/{SOUL,CONDUCTOR,TOOLSET}.md`.
- Polish Atom 1: `dispatch.running` tylko przy https `live.agent.run_url`; bez URL = `picked_up`. HUD: **brak sesji Cloud API**, chip testów nie zielony. Guard Fala S9.
- Guardy: Fala L3 → `conductor-slice-e2e.json`. Fala S 9/9. Fala J: `mutation-test-fala-s.py` w `academy-gate.yml` + `AGENTS.md` `testy:`.

Lokalnie: `validate-academy-export.py` PASS · `test_progress_vault.py` PASS · Fala N 13/13 · S 9/9. Smoke `/OPS.html`: chipy work_mode (Testuj `on`), baner WAITING-GO, linia `brak sesji Cloud API`, confirm Take over w źródle. Zero deploy.

## Co live

Nie deployowano. Produkcja nie ma tej maszyny. Baner WAITING-GO jest prawdą.

## Co zablokowane

Slice P0: Nous na VPS obok vault + adapter ticka w `workflow-lab` (Nous → `ops-status.json`). Właściciel: Dowódca (GO lab+Nous).  
`ENGINEER_LOOP_E2E=true` zabronione bez `docs/ops/conductor-slice-e2e.json`.  
Deploy Akademii — Zasada 11, osobne GO. Auto-merge `dsaas-platform-main` nie w tym splicie.

## Następny krok

**Atom 2 = WAITING-GO (nie w tym merge).** GO Dowódcy: Nous conductor na VPS (Docker, `HERMES_HOME` poza repo, kopia szablonów) + tick w `workflow-lab` tylko zapisuje `run_url` / `live.tests[]` / `live.conductor` — pierwsze issue labu `agent` ze Start na `/ops`. Potem `conductor-slice-e2e.json` i dopiero `ENGINEER_LOOP_E2E=true`.

## Komendy weryfikacji

```
python scripts/validate-academy-export.py
python scripts/test_progress_vault.py
python scripts/mutation-test-fala-l.py
python scripts/mutation-test-fala-q.py
python scripts/mutation-test-fala-s.py
python scripts/mutation-test-fala-j.py
```

## Pliki dotknięte

- `DASHBOARD.html` `OPS.html` `host/progress_vault.py`
- `docs/ops/HERMES-ROLE-CONTRACT.md` `CONTRACT-OPS-STATUS.md` `HERMES-OPS-HOWTO.md` `TOOL-MASTERY.md` `PLAN-HERMES-CONDUCTOR-2026-10-01.md` `README.md` `UX-SPEC-HERMES-OPS-ENTERPRISE.md`
- `docs/ops/hermes-conductor/SOUL.md` `CONDUCTOR.md` `TOOLSET.md`
- `docs/SLOWNIK-HERMESA.md` `docs/ACADEMY-UX-SPEC.md`
- `scripts/validate-academy-export.py` `test_progress_vault.py` `ops-report.py` `mutation-test-fala-l.py` `mutation-test-fala-q.py` `mutation-test-fala-s.py` `deploy-ready-hermes-ops.sh`
- `AGENTS.md` `.github/workflows/academy-gate.yml`

Nie ruszane: 7 tabów, `/hermes/chat` 410, sekrety, deploy VPS, archiwalne handoffy.
