# Handoff — Hermes Ops live: sterowanie martwe — 2026-10-01

**Status:** ZAMKNIĘTE W KODZIE 2026-10-03 na `feat/ops-steer-hud` — [`2026-10-03-ops-steer-hud.md`](2026-10-03-ops-steer-hud.md). Live VPS nadal stary aż do GO deploy.

`git status` (akademia, koniec sesji):

```
* main eef0996 [origin/main] feat(ops): fail-closed Hermes Ops HUD (no fake green) (#90)
?? docs/handoffs/2026-10-01-ops-ghost-active-slot.md
?? docs/handoffs/2026-10-01-ops-steer-live-bugs.md
```

## Co zrobione

Fala HUD fail-closed zmergowana i wdrożona (GO z tej sesji):

- PR [akademia#90](https://github.com/wozniaknorbert95-del/akademia/pull/90) squash → `eef0996`.
- `bash scripts/deploy-ready-hermes-ops.sh` **DEPLOY READY PASS** (`HEAD == origin/main`).
- `bash scripts/deploy-akademia-vps.sh` exit 0. Smoke: vault health, public `/ops` 200, `/ops/diag` `tick_alive: true`, tick idle.
- Lab lokalnie zsynchronizowany do `origin/main` `0f5d65b` (#97 tick adapter). Ponowny install ticka nie był w tej fali.

Lokalny browser 360/1200 na `python -m http.server` (bez vaulta): chipy `DoR brak` / `lane ?` / `todo —`, preflight `3 ✗ · 1 ?`, Run next disabled. To **nie** jest ten sam tor co live z hasłem.

## Co live

- Akademia: `https://akademia.quietforge.flexgrafik.nl/ops` — HUD #90 + vault. Credentials: VPS `CREDENTIALS.local.txt`.
- `/ops/diag` po deploy: `tick_alive: true`, `dispatch.state: idle`, `ops_cmd_state: file`.
- Tick labu: już na `main` `0f5d65b` (Nous-copy, nie `@cursor`). **Nous / `ENGINEER_LOOP_E2E` = WAITING-GO.**
- Dowódca na live: sterowanie nie działa (poniżej). To jest prawda produktu, nie „HUD ładny lokalnie”.

## Co zablokowane

**Sterowanie `/ops` — właściciel: następna sesja na `feat/` (nie `main`).** Dowódca zgłosił:

1. **Buduj / Testuj / Ulepszaj** — tap nie zmienia trybu (wraca albo nic nie robi).
2. **Run next** — nie rusza pętli.
3. **Pause → FAIL.** **Stop → FAIL.** Pauza i stop to nie jest porażka runu.

Podejrzenie w kodzie (nie naprawiane dziś — nie zgadywać na live bez `/ops/status`):

- Chip trybu: `paintWorkMode` woła `workModeOf(s)` które **nadpisuje** `selectedWorkMode` polem `s.work_mode` z cache. Klik ustawia lokalnie, `loadStatus` co 15 s / ten sam `paint()` zrzuca z powrotem na `buduj`. `OPS.html` `workModeOf` + `paintWorkMode` + klik `#work-mode`.
- Run next: `#90` fail-closed — `btn-run.disabled` gdy preflight ma ✗ (DoR/lane/tick) albo `status=UNKNOWN`. Click guard: `disabled` / `aria-disabled`. Może być za ciasne na idle z żywym tickiem; albo POST `/ops/run` 400 (DoR vault).
- Pause/Stop = FAIL: `paint()` stawia pigułkę **FAIL** gdy `run.verdict==='failed'` **zanim** uszanuje `PAUSED`/`STOPPED`. Vault `derive_run`: gałąź `fail_step` przy leftover `live.issue` wygrywa nad Pause/Stop. Dodatkowo `pillClass('STOPPED')` = `bad` (czerwone jak FAIL).

Nie ruszać: Nous, `ENGINEER_LOOP_E2E`, `CURSOR_API_KEY`, ghost handoff `2026-10-01-ops-ghost-active-slot.md`.

## Następny krok

**Jedna gałąź `feat/ops-steer-hud`:** chipy trybu zostają po tapnięciu; Run next rusza gdy tick żywy i jest Autopilot; Pause = PAUSED, Stop = STOPPED — nigdy FAIL.

## Komendy weryfikacji

```
python scripts/validate-academy-export.py
python scripts/test_progress_vault.py
python scripts/mutation-test-fala-q.py
python scripts/mutation-test-fala-s.py
bash scripts/deploy-ready-hermes-ops.sh
```

Live (hasło z VPS, nie z repo): `GET /ops/status` + tap Buduj/Testuj/Ulepszaj (chip zostaje) + Pause (pigułka PAUSED) + Stop (STOPPED) + Run next (QUEUED, nie FAIL).

## Pliki dotknięte

Ta sesja (już na `main` / VPS): `OPS.html`, `scripts/validate-academy-export.py`, `scripts/mutation-test-fala-q.py`, `scripts/test_progress_vault.py`, `docs/ops/UX-SPEC-HERMES-OPS-ENTERPRISE.md`, `docs/handoffs/2026-10-01-ops-hud-fail-closed.md`.

Ten handoff: `docs/handoffs/2026-10-01-ops-steer-live-bugs.md` (nie commituj bez GO).
