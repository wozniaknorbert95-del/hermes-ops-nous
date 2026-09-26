# Hermes Ops — jak używać (`/ops`)

**UI pracy:** `https://akademia…/ops` (PWA Hermes Ops).  
**UI nauki:** `/` = Akademia (7 tabów, TERAZ wchłania DZIEŃ). Lekcja 30 s tego pliku = karta **Hermes Engineer** w [`TOOL-MASTERY.md`](TOOL-MASTERY.md), nie zakładka TERAZ.  
**Kontrakt ról:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md).

## 30 sekund

1. Decyzja i kolejka = **Linear** (etykieta `agent` + 6 pól).
2. Otwórz **`/ops`** na telefonie.
3. **Start / Run next** (gdy chcesz ruszyć) — tryb zawsze **Autopilot**.
4. **Nie merguj z telefonu.** Merge robi pętla po zielonym CI.
5. **Deploy = lokalnie, ręcznie** (Zasada 11).

## Tryb: Autopilot (jedyny)

Pętla bierze issue z toru Linear (`agent`). Ty: **Pause**, **Stop**, **Take over** (laptop). **Run next** / **Start** kolejkują komendę — tick wykonuje. **Pause nie ożywia ticka** (`updated_at` zostaje sercem timera). Brak `ops-cmd.json` po ACK = **idle**, nie awaria.

## Sekcje na `/ops`

Fold (telefon, 360px): **jedno QUI** + chipy `DoR` · `lane` · `testy` · `CI` · `todo zgodny?` + Run / Pause / Stop / Take over.

- **Dashboard · pulse** — 3 issue `dsaas-platform-main` + chip gdy kolejka ≠ `todo.json`.
- **Kolejka** — Autopilot + Lokalnie·HITL. **Kolejka nie udaje Run** (otwiera Linear).
- **Live** — aktualny run (wymaga prawdziwego issue). Czerwony `gates` (billing) ≠ Ready-for-automerge — chip CI / QUI-98.
- **Approval** — **nie Merge**. To: „zrób na laptopie” (HITL) albo „CI green · czeka na pętlę”.
- **Sterowanie** — na foldzie (Pause, Stop, Retry, Take over).

Start 400 gdy: DoR dziurawe, HITL, LOCAL (prawdziwy VPS/SSH), mismatch `todo.json`, dirty PR. Brak tokenu Linear = fail-closed.

Po starcie fold pokazuje: `Cloud: /gate · CI … · AC n/m`. Czerwony `gates` (billing) = chip QUI-98, nie Ready-for-automerge.

## Czego nie robić z telefonu

- Merge na GitHubie.
- Deploy / `workflow_dispatch` produkcji.
- Start Autopilot / Run next „w ciemno” przy pillu **UNKNOWN**.
- Nie oczekuj, że ticket `dsaas-platform-main` „przeskoczy” na `workflow-lab` przy 403 — to jest `target_repo_create_forbidden`.

## Ticket platformy vs lab

Cloud klonuje **repo GitHub issue**, nie pole Linear `repo`. Dlatego:

- Issue Linear na `dsaas-platform-main` → GitHub issue **w tym repo** + `@cursor` z bootstrapem `.cursor/README.md` + `python scripts/session-preflight.py <id>`. `LANE=UNKNOWN` ≠ PASS. Zero deploy/SSH.
- Issue Linear na `workflow-lab` → gym (npm bramki). Nie woła preflightu platformy.
- 403 na create/comment platformy = REFUSE na telefonie, nie fałszywy RUNNING w labie.

## Etykiety Linear (skrót)

- Tor agenta: `agent` + Ready, **bez** `hitl:approval-required` / `blocked`.
- HITL / laptop: `hitl:approval-required` albo brak `agent` → tor **Lokalnie**.
