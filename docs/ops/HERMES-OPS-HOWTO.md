# Hermes Ops — jak używać (`/ops`)

**UI pracy:** `https://akademia…/ops` (PWA Hermes Ops).  
**UI nauki:** `/` = Akademia (7 tabów, TERAZ wchłania DZIEŃ). Lekcja 30 s tego pliku = karta **Hermes Engineer** w [`TOOL-MASTERY.md`](TOOL-MASTERY.md), nie zakładka TERAZ.  
**Kontrakt ról:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md).  
**Maszyna:** [`PLAN-HERMES-CONDUCTOR-2026-10-01.md`](PLAN-HERMES-CONDUCTOR-2026-10-01.md).

**Prawda:** prowadzenie sesji (Nous + Cloud API) = **WAITING-GO** (lab + Nous na VPS). `/ops` pokazuje pola fail-closed. To **nie** jest komentarz `@cursor`. HOWTO nie twierdzi, że sesja już działa.

## 30 sekund

1. Decyzja i kolejka = **Linear** (etykieta `agent` + 6 pól).
2. Otwórz **`/ops`** na telefonie.
3. Chip **buduj / testuj / ulepszaj**, potem **Start / Run next** (silnik = Autopilot).
4. **Nie merguj z telefonu.** Merge robi pętla po warstwie D + zielonym CI.
5. **Deploy = lokalnie, ręcznie** (Zasada 11).

## Tryb silnika: Autopilot (jedyny)

Pętla bierze issue z toru Linear (`agent`). Ty: **Pause**, **Stop**, **Take over** (laptop, zero follow-up do Cursora). **Run next** / **Start** kolejkują komendę — Nous (gdy GO) albo tick-adapter ją zjada. **Pause nie ożywia ticka**. Brak `ops-cmd.json` po ACK = **idle**, nie awaria. QUI-88: Pause / stale lock **nie** startuje następnego issue samo.

`work_mode`: **buduj** (wdroż) · **testuj** (dowód, bez merge) · **ulepszaj** (jedna propozycja, bez kodu).

## Sekcje na `/ops`

Fold (telefon, 360px): **krótki HUD** (pille + raport) → karta Next + Run (pre-flight zwijany) → **Kolejka** od razu pod spodem. Kontekst / Wynik / Dziennik niżej. Dispatch nie klonuje przycisków. Take over pyta confirm. Enter=Start, Escape=Pause, R=Retry.

- **Dashboard · pulse** — 3 issue `dsaas-platform-main` + chip gdy kolejka ≠ `todo.json`.
- **Kolejka** — Autopilot + Lokalnie·HITL. **Kolejka nie udaje Run** (otwiera Linear).
- **Live** — sesja `run_url`, `live.tests[]` (w trakcie), AC/DoD, raport. Puste testy przy RUNNING = UNKNOWN, nie zieleń. Czerwony `gates` (billing) ≠ Ready-for-automerge — chip CI / QUI-98.
- **Approval** — **nie Merge**. To: „zrób na laptopie” (HITL) albo „CI green · czeka na pętlę”.
- **Sterowanie** — na foldzie (Pause, Stop, Retry, Take over).

Start 400 gdy: DoR dziurawe, HITL, LOCAL (prawdziwy VPS/SSH), mismatch `todo.json`, dirty PR. Brak tokenu Linear = fail-closed.

Po starcie fold pokazuje: `Cloud: API · CI … · AC n/m` oraz chip testów ze strumienia.

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
