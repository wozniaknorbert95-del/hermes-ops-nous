# Handoff — ghost slot PAUSED blokował Start — 2026-10-01

**Status:** Zmergowane i wdrożone. Tick `97e0623` (#96). Akademia `0327750` (#88). VPS zweryfikowany.

## Diagnoza (klasa A)

Przed fixem, VPS ~04:25Z: `engine PAUSED reason vps_timer`, brak locków, `live.issue=QUI-93` w cache, `agents_n=1`. HUD slot = `active_agents.length===0` → Start zablokowany. Autopilot nie bierze następnego (anti QUI-88: tick pomija gdy PAUSED).

S5 FAIL na QUI-93 to osobny stary run (CI nie domknięte). Ten atom **nie** obiecuje e2e Cloud. `ENGINEER_LOOP_E2E` nadal false.

## Co zrobione

### workflow-lab PR #96 → main `97e0623`

`active_agents_from` zajmuje slot tylko przy lock + `RUNNING`. PAUSED/STOPPED, `take_over`, brak locka, ghost `live.issue` po TTL/S6 → `[]`.

Testy lokalne: `python scripts/test_hermes_ops.py` · `npm run lint` · `npm test` · `npm run build`. CI PR: validate/execute/phone-loop-guard PASS. Automerge squash.

Deploy tick: `bash /opt/workflow-lab/scripts/install-hermes-ops-vps.sh` na `root@185.243.54.115`. HEAD VPS = `97e0623`.

### akademia PR #88 → main `0327750`

HUD `slotOccupying(s)`: RUNNING/QUEUED albo dispatch queued/running/picked_up. PAUSED+ghost nie blokuje Start. Chip agentów ukryty gdy slot wolny.

Guardy: walidator `function slotOccupying(` + zakaz `ok:agents.length===0`. Fala Q16.

Lokalnie: `validate-academy-export.py` PASS · Fala Q 16/16. `bash scripts/deploy-ready-hermes-ops.sh` PASS (wszystkie fale). Deploy: `bash scripts/deploy-akademia-vps.sh`. SMOKE PASS (vault + `/ops/diag`).

## Dowód na VPS po deploy (04:34Z)

```
engine PAUSED
status PAUSED
live.issue QUI-93          # ghost w cache zostaje
agents_n 0                 # było 1
agent_ids []
lock_payload None
dispatch idle
slotOccupying False
Start enabled True
tick_alive true (age 2s)
OPS.html slotOccupying: 1
```

Tick SoT czyści `active_agents`. HUD belt broni przypadku vault-only PAUSED bez konsumowania ticka.

## Czego nie ruszano

DASHBOARD 7 tabów. Paleta 38. Secrets. QUI-93 S5. Cloud e2e. `ENGINEER_LOOP_E2E`.

## Następny krok

Na `/ops`: Start nowej karty Autopilot (HUD slot wolny). QUI-93 zostaje w `live` jako historia — nie zajmuje slotu. Nie startuj Cloud e2e bez osobnego GO.

## Komendy weryfikacji

```
python scripts/validate-academy-export.py
python scripts/mutation-test-fala-q.py
```

Lab: `python scripts/test_hermes_ops.py`

VPS: `curl -fsS http://127.0.0.1:8097/ops/status` → `active_agents: []` przy PAUSED.

## Pliki

- `workflow-lab/scripts/hermes_ops/router.py`
- `workflow-lab/scripts/hermes_ops/orchestrator.py`
- `workflow-lab/scripts/test_hermes_ops.py`
- `akademia/OPS.html`
- `akademia/scripts/validate-academy-export.py`
- `akademia/scripts/mutation-test-fala-q.py`

Zero sekretów. Handoff nie commituje.
