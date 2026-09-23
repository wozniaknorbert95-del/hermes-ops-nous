# Handoff — telefon Hermes Ops: pętla + HUD prawdy (2026-09-23)

**Repo:** `workflow-lab` + `akademia`  
**GO Dowódcy:** plan „telefon mówi prawdę” + handoff na GitHub

**Main lab:** `71475ca` ([#95](https://github.com/wozniaknorbert95-del/workflow-lab/pull/95))  
**Main akademia:** `cb3d74e` ([#61](https://github.com/wozniaknorbert95-del/akademia/pull/61))

Wcześniejszy stub `docs/handoffs/2026-09-23-ops-platform-wake-hud.md` wskazuje tutaj.

## Co zrobione (fakty)

### Fala 0 — obserwacja PR → DONE (`workflow-lab`)

[#94](https://github.com/wozniaknorbert95-del/workflow-lab/pull/94) squash `a955860` · VPS `/opt/workflow-lab` pulled.

- `find_agent_pull`: `Closes #tracking`, fallback tytuł Linear + `cursor/*`. Fail-closed `None`.
- `refresh_live` zapisuje `lock.pr`, potem S3–S6 z prawdziwego PR (w tym zmergowanego).
- S6 PASS: ledger `kind=merged`, lock clear, silnik **PAUSED**. Brak drugiego `PUT .../merge`.
- `tick()` przy PAUSED **nie** woła `run_next`.
- Scrape `cursor.com/agents` z body PR; HITL max 3 + karta `hitl_more`.

### Fala 1 — HUD (`akademia`)

[#60](https://github.com/wozniaknorbert95-del/akademia/pull/60) squash `a8cdcb3` · deployed na VPS (HEAD wtedy `a8cdcb3`).

- `derive_run`: 6/6 + `pr_number` → `done` także przy `engine=PAUSED`.
- PAUSED/STOPPED + live bez PR i bez 6/6 → `paused`/`stopped`, nie `running`.
- LIVE DONE: `DONE — PR #N · 6/6. Następne: QUI-xx. Start gdy chcesz.` Retry ukryty.
- Tokens/Cost: **brak źródła** (nie `—`, nie `$0.00`).
- LIVE pokazuje `live.repo`. `hitl_more` = reszta na laptopie.

### Fala 2

Weszła w #94 (URL agenta, cap HITL) i #60 (repo na karcie, etykieta reszty). Routing platformy = osobny epik.

### Faza draft / HUD FAIL (wcześniej tego dnia)

- Lab [#91](https://github.com/wozniaknorbert95-del/workflow-lab/pull/91): zakaz draft PR (D-AUTOMERGE).
- Lab [#88](https://github.com/wozniaknorbert95-del/workflow-lab/pull/88): QUI-88 team-desk — **merged** (draft zdjęty, squash).
- Lab [#87](https://github.com/wozniaknorbert95-del/workflow-lab/pull/87): draft Cloud — **closed, not merged** (superseded by #88).
- Akademia [#59](https://github.com/wozniaknorbert95-del/akademia/pull/59): pigułka FAIL + `ci_green_await_merge`.

### Platform wake (#95 / #61)

- Lab [#95](https://github.com/wozniaknorbert95-del/workflow-lab/pull/95): nie przenosić wake na lab, gdy Issues 403 na `dsaas-platform-main`.
- Akademia [#61](https://github.com/wozniaknorbert95-del/akademia/pull/61): refuse copy `target_repo_create_forbidden`. **Na `main`; deploy Akademii po #60 — potwierdź, czy VPS ma `cb3d74e`.**

## GitHub — porządki tej sesji

Otwarte PR-y `akademia` i `workflow-lab` przed sprzątaniem: **0**.

Zamknięte bez merge (nie re-open):

| PR | Akcja | Powód |
| --- | --- | --- |
| lab [#87](https://github.com/wozniaknorbert95-del/workflow-lab/pull/87) | closed, draft | Duplikat QUI-88; prawda = [#88](https://github.com/wozniaknorbert95-del/workflow-lab/pull/88) |

Gałęzie: skasowane leftover po squash/merge + `cursor/*` po zamkniętych planach Cloud (lista w PR handoffu). **Nie ruszane:** `docs/qui-16-wfp9` (worktree).

## Co live (odczyt po Fali 1)

| Check | Wynik |
| --- | --- |
| `/ops/diag` tick_alive | true |
| GET `/ops/status` (po #60) | engine **PAUSED**, verdict **paused** (duch QUI-87, `pr=None`) |
| today.tokens / cost | `null` → HUD `brak źródła` |
| live.repo | `workflow-lab` |
| public GET `/ops` | HTTP 200 |

## Co zablokowane

- QUI-87 historyczny duch: lock zdjęty, Fala 0 **nie** dopisze `merged` wstecz. `today.merged` urośnie przy następnym prawdziwym squashu.
- Token/koszt Cursor Cloud — brak źródła w kodzie.
- Telefon jako pulpit dziecka: pkt 1–4 DoD na **następnym** Start, nie na duchu QUI-87.
- Merge z telefonu: zabroniony.
- Deploy SPA QuietForge / dsaas runtime: osobny tor.

## Następny krok (jeden TERAZ)

1. Twarde odświeżenie `/ops`.
2. Jeśli VPS akademia ≠ `cb3d74e`: `bash scripts/deploy-akademia-vps.sh` (GO).
3. **Start** na kolejnym Linear. DoD: ≤ 2 ticki po PR jest `pr_number`; po squash pigułka DONE, silnik PAUSED, kolejka czeka na ręczne Start.

## Komendy weryfikacji

```bash
ssh root@185.243.54.115 'cd /opt/workflow-lab && git log -1 --oneline'
curl -fsS http://127.0.0.1:8097/ops/diag
curl -fsS http://127.0.0.1:8097/ops/status
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
```

## Pliki (kod już na main)

- `workflow-lab`: `scripts/hermes_ops/{github,orchestrator,live_enrich}.py`, `phone_loop_github.py`, `test_hermes_ops.py`
- `akademia`: `OPS.html`, `host/progress_vault.py`, `scripts/test_progress_vault.py`
- ten plik: `docs/handoffs/2026-09-23-ops-observe-hud.md`
