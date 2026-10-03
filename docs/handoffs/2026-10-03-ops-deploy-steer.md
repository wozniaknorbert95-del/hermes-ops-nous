# Handoff — deploy Hermes Ops steer HUD — 2026-10-03

**Status:** LIVE. `main` `35f80b5` (#91) na VPS. SMOKE PASS.

## Co

- Merge [akademia#91](https://github.com/wozniaknorbert95-del/akademia/pull/91) squash.
- `deploy-ready-hermes-ops.sh` PASS (`HEAD == origin/main`).
- `deploy-akademia-vps.sh` exit 0. `/ops/diag` `tick_alive: true`, dispatch idle, public `/ops` 200.

## DoD live (telefon)

1. Chip Testuj zostaje do Run.
2. Pause = PAUSED (żółty), nie FAIL.
3. Stop = STOPPED, nie FAIL.
4. Retry niewidoczny na idle.
5. Pusty Wynik schowany.
6. WAITING-GO widoczny bez sesji Cloud.

## NEXT

Zrobione w [`2026-10-03-conductor-slice.md`](2026-10-03-conductor-slice.md). Ten plik zostaje zapisem deployu #91.
