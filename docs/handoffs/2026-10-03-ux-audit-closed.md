# Handoff — UX audit zamknięty (live) — 2026-10-03

**Status:** P0/P1 z audytu Conditional Pass są na `main` (`0d88bf0`, PR #93) i na VPS.

## Co zrobione

- HUD `/ops`: `Live` tylko przy `RUNNING`; leftover `PAUSED`/`STOPPED` = `Ostatni run`; Retry `hidden` + CSS boot; `h1.sr-only`; skip 44px.
- Bramka 401: `host/auth-gate.html` + nginx `error_page 401 =401`. Anon HTTPS trzyma `WWW-Authenticate: Basic realm="Akademia OS"`.
- TERAZ: wieczór + rytuał w jednym zamkniętym `<details>` `Ręcznie / wieczór`.
- Guardy: validate, vault, Fala S16. Deploy-ready + `deploy-akademia-vps.sh` PASS.

## Co live

- `https://akademia.quietforge.flexgrafik.nl/ops` anon → **401** + body „Akademia” + „Przeglądarka poprosi”.
- `/auth-gate.html` publiczne **200** (bez hasła, bez formularza).
- Manifest/ikony 200, HTML bez hasła 401 (smoke deploy).
- `/ops/diag` po deploy: `ok: true`, `tick_alive: true`.

`git status` przy zamknięciu: `main...origin/main` czyste (`0d88bf0`).

## Co zablokowane

- Rotacja kluczy Cursor / Basic Auth — decyzja ops, nie ten MR. Właściciel: Dowódca.
- Nous LLM na VPS — `.env` bez mózgu; czat Akademii = silnik lokalny. Osobne GO.

## Następny krok

Jeden TERAZ: **Fala A planu polerki** — brief poranka bez listy wieczoru i bez drugiego `renderDay()` w foldzie (`docs/ops/PLAN-UX-POLISH-2026-10-03.md`).

## Komendy weryfikacji

```
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py && python scripts/mutation-test-fala-s.py
curl -s -o NUL -w "%{http_code}" https://akademia.quietforge.flexgrafik.nl/ops
# oczekiwane: 401 + body zawiera Akademia
```

## Pliki dotknięte (MR #93)

`OPS.html` · `DASHBOARD.html` · `host/auth-gate.html` · `host/nginx-akademia.conf` · `host/nginx-akademia-http.conf` · `scripts/validate-academy-export.py` · `scripts/test_progress_vault.py` · `scripts/mutation-test-fala-s.py` · `scripts/setup-akademia-vps.sh` · `docs/handoffs/2026-10-03-ux-ops-audit-fix.md`
