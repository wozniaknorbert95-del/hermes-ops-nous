# Handoff — Audyt trybów + UI polish + deploy (2026-09-21)

**Repo:** `akademia` PR [#42](https://github.com/wozniaknorbert95-del/akademia/pull/42) · `workflow-lab` PR [#68](https://github.com/wozniaknorbert95-del/workflow-lab/pull/68)
**Status:** **ZMERGOWANE + WDROŻONE.** HEAD akademia `5f66bcb`, lab `1caec4e`.

## Werdykt

Zakładki Manual / Autopilot / Supervised **działały logicznie**, ale HUD lagował (Docker vault ≠ host systemd). Path unit + optimistic patch = instant feedback.

## Live smoke (po deploy)

```
immediate SUPERVISED queued_mode_supervised
after_2s   SUPERVISED mode_supervised
restored   AUTOPILOT PAUSED
hermes-ops-cmd.path: active
```

## UI

**Ops:** pending tryb, focus toru, Live wymaga `issue`, bez duplikatu Start, Plex, captions.
**Akademia:** hero CTA Hermes Ops, safe-area, Plex, mniej chipów na mobile.

## Testy

- validate + vault + Fala M PASS (CI academy-gate zielony)
