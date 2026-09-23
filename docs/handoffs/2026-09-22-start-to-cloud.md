# Handoff — Start telefonu → Cursor Cloud (fail-closed)

**Data:** 2026-09-22  
**Repo:** akademia `#52` + workflow-lab `#85` (merged, deployed)

## Co

Jedno tapnięcie **Start** tworzy/wybiera GitHub issue, pisze komentarz `@cursor` tokenem `GITHUB_OPS_COMMENT`, a RUNNING jest legalne dopiero po ACK + comment 2xx + numerze issue.

## Dowód E2E (VPS, 2026-09-22T20:20Z)

- POST `/ops/run` start → 200 QUEUED → tick → **RUNNING**
- Linear `QUI-88` → GitHub [workflow-lab#86](https://github.com/wozniaknorbert95-del/workflow-lab/issues/86)
- Komentarz `@cursor`: `.../issues/86#issuecomment-5783514453`
- `cursor[bot]`: **Taking a look!** (~7 s później), agent `bc-aef864fd-8f9e-489f-8f5e-4ee596be910c`
- Canary `GITHUB_OPS_COMMENT` dry HTTP **404** (Issues write OK, nie 403)
- `OPS_MAX_RUNS_PER_DAY=32` (udokumentowany sufit smoke)

## UI

REFUSED mapuje: `lock` / `cap_*` / `cursor_wake_*` / `ops_cmd_path_is_directory` — bez kłamliwego „napraw token E1” na locku. Live: `Wake: issue #N · comment sent` tylko po realnym URL.

## VPS

- workflow-lab HEAD `590e1ec`
- akademia HEAD `29cd270`
- `ops-cmd.json` jest **plikiem**, nie katalogiem
- lock po Pause: absent; busy() nie blokuje Start gdy PAUSED

## Next

Obserwuj agenta QUI-88 na issue #86 (Cloud już wstał). Nie ruszaj tokenów. Merge z telefonu nadal zabroniony (Zasada 11).
