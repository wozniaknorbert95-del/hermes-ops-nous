# Handoff — audyt + plan naprawczy Hermes Ops (2026-10-11)

**Repo:** `hermes-ops-nous`  
**Branch:** `main` @ `9d71b06` (PR #1 merged)  
**Deploy:** **LIVE** 2026-10-11 ~09:14 CEST — SMOKE PASS (`tick_alive: true`, public `/ops` 401 = Hermes Ops)

## Zrobione

1. **Fala 1 UX** — `OPS.html`: Otwórz Linear przy zablokowanym Start (DoR-aware copy), PL, Zatrzymaj i przejmij, Jak zacząć, refuse-aware Retry; `host/auth-gate-ops.html` + nginx `/ops`.
2. **Fala 2 vault** — `scripts/test_progress_vault.py`; AGENTS + deploy-ready.
3. **Fala 3 docs** — AUDYT-WYNIK 2026-10-11, DEPLOY-READY, HOWTO.
4. **Ship** — PR [#1](https://github.com/wozniaknorbert95-del/hermes-ops-nous/pull/1) → main → deploy VPS.

## Live proof

- Public 401 `/ops`: H1 **Hermes Ops** + „Pokaż okno logowania”
- Vault HTML: `Wymagania przed startem`, `run-linear`, `refuseRetryable`, `Zatrzymaj i przejmij`
- `/ops/diag`: `ok:true`, `tick_alive:true`, dispatch `idle`

## NEXT (najsensowniejsze)

**Telefon 30 s — ścieżka Start:** otwórz live `/ops` → jeśli Start disabled: tap **Otwórz Linear**, domknij DoR Next, wróć, **Run next** → oczekuj **QUEUED** (nie RUNNING bez ack). To domyka audyt C2 na produkcji.

Potem (osobne GO / lab): conductor Nous + `CURSOR_API_KEY` na hoście — dziś `llm:false`, WAITING-GO.
