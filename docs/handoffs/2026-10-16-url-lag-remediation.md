# Handoff — URL lag remediation (A0 + Tor B + Tor A)

**Data:** 2026-10-16  
**GO:** plan naprawczy (dogfood URL lag)  
**Repos:** `hermes-ops-nous` #18 → `2134e37` · `workflow-lab` #111 → `e724a3f`

## A0 diagnose (root cause)

| Event | Latency |
| --- | --- |
| conductor created + live https URL | ~11s |
| ops-status `run_url` (before fix) | empty until next tick (cmd.path / up to **5min** timer) |

**H1 confirmed:** Nous writes URL fast; tick did not re-merge until `ops-cmd` change or `OnUnitActiveSec=5min`.

## Fix

| Tor | Change |
| --- | --- |
| **B (nous)** | `overlay_conductor_run_url` on `/ops/status` view; HUD Live only with https URL; setup/smoke conductor path |
| **A (lab)** | `hermes-ops-conductor.path` → kick `hermes-ops.service` on live JSON write |

## Prove

- Vault tests: PASS (picked_up + overlay)
- Deploy akademia: SMOKE PASS · `conductor_path=active`
- **Dogfood-2:** Start QUI-43 → view/file/live URL @ **9s** · `DOGFOOD2_URL_LAG=PASS` (≤30s)

## NEXT

- Product loop: continue Autopilot DoR / Linear queue (F5 polish still BLOCKED)
- Optional: dispatch may show `idle` briefly after ack unlink even with URL — secondary, not dogfood blocker
