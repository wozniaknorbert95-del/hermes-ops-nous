# Handoff — Real Autopilot Brief (zamknięcie sesji 2026-10-16)

**Rola:** Control Plane / Dowódca  
**GO:** pełne zamknięcie (merge + deploy conductor + dogfood)

## Werdykt

**PASS.** Conductor nie wkleja już lab-probe dla QUI-43. Default = real Autopilot + `/autopilot`; smoke = `lab_probe`.

## Linki

| Artefakt | URL / SHA |
| --- | --- |
| Lab PR | https://github.com/wozniaknorbert95-del/workflow-lab/pull/112 → `65f771b` |
| Nous PR (docs) | https://github.com/wozniaknorbert95-del/hermes-ops-nous/pull/23 → `b157fb7` |
| Lab handoff | `workflow-lab/docs/handoffs/2026-10-16-real-autopilot-brief.md` + `-deploy.md` |
| Image VPS | `hermes-conductor:local` `90e149ecc633` |

## Co było złe (dziecko)

Start odpalał Cloud, ale prompt mówił „dopisz linijkę do conductor-lab-probe” zamiast robić issue z Linear. Naprawione w `workflow-lab` `_brief()` + handoff AC.

## Co nie ruszaliśmy

- OPS.html polish / meta PWA deprecation (szum)
- Auto-merge platformy / deploy z telefonu
- F9 reject list

## NEXT

1. Jeden żywy Start QUI-43 z `/ops` — sprawdź prompt w Cloud (bez probe).
2. SoT `todo.json` tego repo: IDLE (F5 + real brief shipped).
3. Sesja zamknięta — nowa sesja = `/ops-audit` + Linear IP.
