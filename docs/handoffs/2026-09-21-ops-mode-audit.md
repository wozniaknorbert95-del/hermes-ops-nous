# Handoff — Audyt trybów Manual / Autopilot / Supervised (2026-09-21)

**Repo:** `akademia` (`fix/ops-mode-instant`) + `workflow-lab` (`fix/ops-cmd-path-unit`)
**Status:** root cause potwierdzony w przeglądarce + API. Path unit **już live na VPS**. Optymistyczny vault/UI czeka na merge+deploy Akademii (Zasada 11).

## Werdykt eksperta

Zakładki **nie są zepsute logicznie** — `POST /ops/run` kolejuje `set_mode`, tick Hermesa przepisuje `ops-status.json` i **przestawia tory** (MANUAL ↔ AUTOPILOT ↔ SUPERVISED).

To, co wygląda jak „nie działa”, to **lag HUD**:
1. Vault w Dockerze **nie może** `systemctl` kicknąć hosta → wcześniej czekanie na timer (minuty).
2. UI odświeżał `mode` dopiero po ticku → tap Manual wygląda jak „nic” (przycisk zostaje na Autopilot).

## Dowód (live)

| Krok | Wynik |
|---|---|
| Path unit `hermes-ops-cmd.path` | **enabled + active** na VPS (20:52) |
| API latency po path | `immediate` = stary mode; `after_2s` = nowy mode (MANUAL / SUPERVISED / AUTOPILOT) |
| Browser (tunel `18097→8097`) | Manual → 8 w Manual; Supervised → 8 w Autopilot; Autopilot OK; Pause → `reason=paused` |
| Lokalny `:8765` | `/ops/status` 404 — statyczny serwer, nie vault |

## Fix (kod)

**workflow-lab**
- `docs/ops/hermes-ops-cmd.path.example`
- `scripts/install-hermes-ops-vps.sh` instaluje + enable path

**akademia** (jeszcze nie na produkcji)
- `host/progress_vault.py` — `patch_ops_status` zaraz po `set_mode` / pause / start / stop
- `OPS.html` — optymistyczny `setModes` + `burstPoll`
- test + guard walidatora (`burstPoll`)

## Następny krok Dowódcy

1. **GO** merge PR obu gałęzi + deploy Akademii (vault optimistic).
2. Lab: po merge odpalić `install-hermes-ops-vps.sh` (path unit już jest; skrypt utrwala).
3. Nie startuj Autopilot Run next bez świadomego GO — kolejka ma QUI-61.

## Świadomie nieruszone

- Autonomiczny deploy platformy / merge z telefonu
- Tokeny / sekrety w chacie
