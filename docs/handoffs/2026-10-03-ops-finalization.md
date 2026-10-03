# Handoff — finalizacja Hermes Ops (Faza 1–4) — 2026-10-03

**Status:** Faza 1+2 w kodzie na `feat/ops-steer-hud`. Faza 3 conductor = WAITING-GO. Faza 4 audyt lokalny zapisany. Deploy = Zasada 11.

## Fazy

| Faza | Stan |
| --- | --- |
| 1 Sterowanie HUD | Kod PASS — Pause/Stop ≠ FAIL, work_mode persist, derive_run halt |
| 2 UX/docs | HOWTO = Cloud: /autopilot; e2e legacy note; PWA 44px/safe-area strzeżone |
| 3 Nous + Cloud API | [`conductor-slice-e2e.json`](../ops/conductor-slice-e2e.json) WAITING-GO — lab + VPS, nie ten PR |
| 4 Audyt O1–O8 | [`AUDYT-WYNIK-HERMES-OPS-2026-10-03.md`](../ops/AUDYT-WYNIK-HERMES-OPS-2026-10-03.md) — O4/O5/O6/O7 live SKIP |

## Następny krok Dowódcy

1. Review + merge `feat/ops-steer-hud`.
2. GO deploy Akademii → smoke live `/ops`.
3. Osobne GO: Nous na VPS + adapter ticka → uzupełnić conductor-slice JSON.
