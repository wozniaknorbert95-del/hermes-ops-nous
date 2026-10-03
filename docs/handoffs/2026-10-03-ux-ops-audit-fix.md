# Handoff — UX/UI post-audit fix — 2026-10-03

**Status:** kod + guardy PASS. Re-walk lokalny: `/ops` leftover PAUSED = `Ostatni run` (nie Live); Retry hidden na cold load; TERAZ 375px = brief + B1, rytuał w zamkniętym `Ręcznie / wieczór`; `host/auth-gate.html` branded, bez formularza.

## Co weszło

- `OPS.html`: `Live` tylko przy `RUNNING`; leftover PAUSED/STOPPED → `Ostatni run`; `#btn-retry` `hidden` + `body.booting`; `h1.sr-only`; skip 44px.
- `host/auth-gate.html` + nginx `error_page 401 =401` (TLS i HTTP).
- `DASHBOARD.html`: wieczór + rytuał w jednym zamkniętym `<details>`.
- Guardy: validate, vault, Fala S16 `live-eyebrow-not-fake`.

## Poza tym MR

- Live 401 na VPS jest nagi dopóki ten MR nie wyleci deployem (nginx na VPS czyta repo).
- Rotacja kluczy Cursor/Basic — osobna decyzja ops.

## Następny krok

1. Merge `feat/ux-ops-audit-fix`.
2. `bash scripts/deploy-akademia-vps.sh` (GO Dowódcy już było).
3. Anon GET `https://akademia.quietforge.flexgrafik.nl/ops` → body ma „Akademia”, status 401.
