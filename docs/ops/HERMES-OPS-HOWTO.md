# Hermes Ops — jak używać (`/ops`)

**UI pracy:** `https://akademia…/ops` (PWA Hermes Ops).  
**UI nauki:** `/` = Akademia (7 tabów, TERAZ wchłania DZIEŃ). Lekcja 30 s tego pliku = karta **Hermes Engineer** w [`TOOL-MASTERY.md`](TOOL-MASTERY.md), nie zakładka TERAZ.  
**Kontrakt ról:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md).  
**Maszyna:** [`PLAN-HERMES-CONDUCTOR-2026-10-01.md`](PLAN-HERMES-CONDUCTOR-2026-10-01.md).

**Prawda:** lab e2e (QUI-113) dał https `run_url` i follow-up na tym samym `agentId` — [`conductor-slice-e2e.json`](conductor-slice-e2e.json). Unit `hermes-conductor` woła Cloud API. Bez `CURSOR_API_KEY` na hoście Start kończy się `missing_CURSOR_API_KEY`, nie zielonym running. `/ops` pokazuje pola fail-closed. Deploy HTML Akademii = **WAITING-GO** (Zasada 11). To **nie** jest komentarz `@cursor`. HOWTO nie twierdzi, że sesja już działa.

## 30 sekund

1. Decyzja i kolejka = **Linear** (etykieta `agent` + 6 pól).
2. Otwórz **`/ops`** na telefonie.
3. Chip **buduj / testuj / ulepszaj**, potem **Start / Run next** (silnik = Autopilot).
4. **Nie merguj z telefonu.** Merge robi pętla po warstwie D + zielonym CI.
5. **Deploy = lokalnie, ręcznie** (Zasada 11).

## Pętla operatora (5 kroków) — SoT produktu

To jest kanoniczna ścieżka użytkownika `/ops` (nie dashboard analityczny):

1. **Linear** — wybierasz pracę: etykieta `agent`, 6 pól, tryb.
2. **`/ops`** — ustawiasz buduj / testuj / ulepszaj i dajesz **Start / Run next**.
3. **System** (vault → tick → Nous na VPS) odpala sesję Cursor Cloud; HUD pokazuje https `run_url`, postęp, testy, AC.
4. **Ty** możesz Pause / Stop / przejąć na laptop — **nie** mergujesz i **nie** deployujesz z telefonu.
5. Gdy coś nie gra — dostajesz **jasną odmowę** (DoR, HITL, blocked, mismatch todo platformy, brak klucza…), nie fałszywą zieleń.

Linia **Teraz:** w HUD (`#hud-truth`) skraca „co robić teraz”. SoT zadań inżynieryjnych tego repo = [`../../todo.json`](../../todo.json) (tor `NOUS-PRODUCT-LOOP`) — nie bramka Start.

**Lag URL vs KPI create:** po Start journal conductor (`created` / `unchanged`) jest KPI create. HUD / `/ops/status` bierze https `run_url` z ticka + path `hermes-ops-conductor.path` (+ vault overlay z `hermes-conductor-live.json`). Cel: URL ≤30s. Gdy status żyje bez URL: **Teraz: Czekaj** — nie spamuj Retry/Start. Fałszywa zieleń ≠ dowód sesji; dowód = https `run_url` albo jasny refuse.

**Zapytaj (stan):** fold na `/ops` → `POST /ops/chat` — krótkie pytania o status/URL/DoR z faktów vaulta (0 tokenów). To **nie** jest czat Akademii (`/hermes/chat` = 410) ani Agents Window. Deploy / merge / MCP = odmowa.

**Użyj tego / select_next:** ustawia `next` (nie startuje). Bez `issue_id` vault bierze głowę Autopilot (albo bieżący `next` jeśli nadal w kolejce).

## Tryb silnika: Autopilot (jedyny)

Pętla bierze issue z toru Linear (`agent`). Ty: **Pause**, **Stop**, **Zatrzymaj i przejmij** (laptop, zero follow-up do Cursora). **Run next** / **Start** kolejkują komendę — Nous (gdy GO) albo tick-adapter ją zjada. Gdy Start zablokowany — link **Otwórz Linear** na foldzie. **Pause nie ożywia ticka**. Brak `ops-cmd.json` po ACK = **idle**, nie awaria. QUI-88: Pause / stale lock **nie** startuje następnego issue samo.

`work_mode`: **buduj** (wdroż) · **testuj** (dowód, bez merge) · **ulepszaj** (jedna propozycja, bez kodu).

## Sekcje na `/ops`

Fold (telefon, 360px): **krótki HUD** (pille + raport) → karta Next + Run (pre-flight = „Wymagania przed startem”) → **Kolejka** od razu pod spodem. Kontekst / Wynik / Dziennik niżej. Dispatch nie klonuje przycisków. Zatrzymaj i przejmij pyta confirm. Enter=Start, Escape=Pause, R=Retry.

- **Dashboard · pulse** — 3 issue `dsaas-platform-main` + chip gdy kolejka ≠ todo **platformy** (`ops-status.todo_active`). SoT zadań Control Plane = `hermes-ops-nous/todo.json` (nie bramka Start).
- **Kolejka** — Autopilot + Lokalnie·HITL. **Kolejka nie udaje Run** (otwiera Linear).
- **Live** — sesja `run_url`, `live.tests[]` (w trakcie), AC/DoD, raport. Puste testy przy RUNNING = UNKNOWN, nie zieleń. Czerwony `gates` (billing) ≠ Ready-for-automerge — chip CI / QUI-98.
- **Approval** — **nie Merge**. To: „zrób na laptopie” (HITL) albo „CI green · czeka na pętlę”.
- **Sterowanie** — na foldzie (Pause, Stop, Retry, Zatrzymaj i przejmij).

Start 400 gdy: DoR dziurawe, HITL, LOCAL (prawdziwy VPS/SSH), mismatch todo platformy (`qui_todo_mismatch`), dirty PR. Brak tokenu Linear = fail-closed.

Po starcie fold pokazuje: `Cloud: /autopilot · sesja|brak sesji Cloud API · CI · AC n/m` oraz chip testów ze strumienia. Chip **buduj / testuj / ulepszaj** zostaje po tapnięciu (localStorage) aż do Run. **Pause** = PAUSED, **Stop** = STOPPED — nigdy FAIL.

## Czego nie robić z telefonu

- Merge na GitHubie.
- Deploy / `workflow_dispatch` produkcji.
- Start Autopilot / Run next „w ciemno” przy pillu **UNKNOWN**.
- Nie oczekuj, że ticket `dsaas-platform-main` „przeskoczy” na `workflow-lab` przy 403 — to jest `target_repo_create_forbidden`.

## Ticket platformy vs lab

Cloud klonuje **repo GitHub issue**, nie pole Linear `repo`. Dlatego:

- Issue Linear na `dsaas-platform-main` → Cloud API na **tym repo** + bootstrap `.cursor/README.md` + `python scripts/session-preflight.py <id>` + procedura `/autopilot` w briefie (anty-lista: nigdy `/deploy` `/publish` `/skip-gate` `/force-merge`). `LANE=UNKNOWN` ≠ PASS. Zero deploy/SSH.
- Issue Linear na `workflow-lab` → gym (npm bramki). Slice P0 = to repo.
- 403 na create platformy = REFUSE na telefonie, nie fałszywy RUNNING w labie.

## Etykiety Linear (skrót)

- Tor agenta: `agent` + Ready, **bez** `hitl:approval-required` / `blocked`.
- HITL / laptop: `hitl:approval-required` albo brak `agent` → tor **Lokalnie**.
