# Handoff — Nous + Cursor Cloud API (P0) — 2026-10-03

**Status:** slice e2e = **WYKONANY**. `ENGINEER_LOOP_E2E=true` po [`conductor-slice-e2e.json`](../ops/conductor-slice-e2e.json). Tick **nie** woła `POST /v1/agents`. Merge labu #98 i deploy HTML Akademii = osobne GO (Zasada 11). Cursor Projects = **PARKED P1**.

## CO

| Zadanie | Stan |
| --- | --- |
| T0 tick #97 + zero Cloud API w `hermes_ops` | PASS |
| T1 QUI-113 `agent` + 6 pól + projekt `workflow-lab` | PASS |
| T2 `HERMES_HOME` + ścieżki `/data` + unit | PASS; `CURSOR_API_KEY=SET` (tylko host, awk) |
| T3 Docker `hermes-conductor` + idle + refuse bez klucza | PASS |
| T4 adapter `ac`/`dod`/`local_remaining`/`followups_used` | PASS — [workflow-lab#98](https://github.com/wozniaknorbert95-del/workflow-lab/pull/98) |
| T5 https `run_url` po Start | PASS — HUD RUNNING, [sesja](https://cursor.com/agents/bc-c2ddd959-9623-4413-a849-747051f32f25) |
| T6 follow-up ten sam `agentId` | PASS — `followups_used=1`, AC-1 PASS, id `bc-c2ddd959-9623-4413-a849-747051f32f25` |
| T7 `conductor-slice-e2e.json` + flaga | PASS |

Halt: Nous archiwizuje sesję **tylko** przy operator Pause/Stop/Take over, nie przy idle PAUSED. Follow-up robi unarchive.

## DLACZEGO

Jeden mózg: Nous woła Cloud API, tick kopiuje JSON. Karta Engineer zapala AKTYWNY W LABIE dopiero po https `run_url` + tym samym `agentId` + `github_pr` (maszyna = #98).

## NASTĘPNY KROK

1. **Rotacja klucza** — User API key był wklejony na czacie. Odwołaj w Cursor Dashboard → Keys, wklej nowy tylko do `/etc/workflow-lab/hermes-engineer.env` (chmod 600). Zero gita.
2. Merge [workflow-lab#98](https://github.com/wozniaknorbert95-del/workflow-lab/pull/98) = osobne GO.
3. Deploy HTML Akademii = Zasada 11, osobne GO.
4. Cursor Projects = PARKED (nie UI, nie 8. tab).

## Weryfikacja (bez sekretów)

```
curl -fsS http://127.0.0.1:8097/ops/diag
systemctl is-active hermes-conductor.service
awk -F= '/^CURSOR_API_KEY=/{print $1"="(($2==""||$2=="CHANGE_ME")?"EMPTY":"SET")}' /etc/workflow-lab/hermes-engineer.env
```
