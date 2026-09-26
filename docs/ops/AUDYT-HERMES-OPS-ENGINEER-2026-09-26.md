# Audyt Hermes Ops — dwa runy Cloud 3290 (2026-09-26)

**Werdykt:** Hermes Ops **budzi** Cursor Cloud na `dsaas-platform-main`. **Nie** dociąga QUI do Done (komendy Cursor → testy → CI → EV → Linear). Budzik + sekretarz, nie strażnik.

**Werdykt (po weryfikacji 26.09):** kod bramki i HUD są w `feat/hermes-ops-engineer`. Deploy akademii = osobne GO. `LINEAR_OPS_READ` na VPS obowiązkowy.

## Workspace `*-3290`

| Run | QUI | PR | Branch | Stan 26.09 wieczór |
| --- | --- | --- | --- | --- |
| A | [QUI-93](https://linear.app/quietforge/issue/QUI-93) | [#115](https://github.com/wozniaknorbert95-del/dsaas-platform-main/pull/115) | `cursor/nightly-heavy-prod14-diag-3290` | open, **dirty** vs `main`; `gates` + `spa-ui-e2e` **failure** (~3 s, billing) |
| A' | ten sam epic | [#116](https://github.com/wozniaknorbert95-del/dsaas-platform-main/pull/116) | `cursor/nightly-park-main-3290` | open, dirty; bez `@cursor` 26.09 |
| B | [QUI-83](https://linear.app/quietforge/issue/QUI-83) | [#117](https://github.com/wozniaknorbert95-del/dsaas-platform-main/pull/117) | `cursor/qui-83-finanse-ksiega-3290` | Linear **Done**; PR **draft**, stale; kod na `main` przez #118 |

Cloud IDs: `bc-7651bd58-…` (25.09 kod) · `bc-18111eed-…` (26.09 ~16:53 UTC, telefon).

## Co potrafi (zmierzone)

- Etykieta `agent` → GitHub twin + `@cursor` z bootstrapem (`AGENTS.md`, `.cursor/README.md`, `session-preflight.py QUI-xx`).
- Zakaz deploy / merge z telefonu — trzyma się.
- Cloud czyta pakiet, preflight, komentarz Linear + PR.
- QUI-93: **1** test AC (`test_nightly_heavy_schedule_is_parked`) PASS; zero nowego kodu (park już na branchu).
- QUI-83 (25.09): potrafi napisać produkt (księga + 12 pytest).

## Czego nie potrafi

- Pętli `/vibeinit` → `/plan` → `/gate` → `/verify` → `/evidence` → `/handoff`.
- Fałszywy `LANE=LOCAL`: słowo `workflow_dispatch` / `production-ready` w AC (QUI-93).
- Ochrony `todo.json` `aktywne_zadanie` (inne QUI niż 93).
- Rebase dirty; zakaz draft (#117).
- Strażnika CI: Ready-for-review przy czerwonym `gates` (billing ≠ PASS).
- HUD: DoR, lane, nazwa joba, „napraw albo powiedz”.

## P0 do naprawy (ten program)

1. Vault: Linear READ + 400 przed `@cursor` (DoR / HITL / LOCAL prawdziwy / todo / dirty).
2. HUD `/ops`: 3 strefy, chipy, pulse.
3. Platforma: markery preflight + session-entry wymusza `/gate`+`/verify`; billing ≠ automerge.

Szczegóły runów: komentarz Linear QUI-93 (16:54 UTC) · PR #115 comment `cursor[bot]`.
