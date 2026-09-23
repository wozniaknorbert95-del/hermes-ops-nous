# Hermes Ops — jak używać (`/ops`)

**UI pracy:** `https://akademia…/ops` (PWA Hermes Ops).  
**UI nauki:** `/` = Akademia (kurs A–G).  
**Kontrakt ról:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md).

## 30 sekund

1. Decyzja i kolejka = **Linear** (etykieta `agent` + 6 pól).
2. Otwórz **`/ops`** na telefonie.
3. **Start / Run next** (gdy chcesz ruszyć) — tryb zawsze **Autopilot**.
4. **Nie merguj z telefonu.** Merge robi pętla po zielonym CI.
5. **Deploy = lokalnie, ręcznie** (Zasada 11).

## Tryb: Autopilot (jedyny)

Pętla bierze issue z toru Linear (`agent`). Ty: **Pause**, **Stop**, **Take over** (laptop). **Run next** / **Start** kolejkują komendę — tick wykonuje.

## Sekcje na `/ops`

- **Teraz / Next** — bieżące lub następne issue + pasek S1–S6.
- **Sterowanie** — Pause, Stop, Retry, **Take over** (Pause + praca lokalnie, zero `@cursor`).
- **Kolejka** — Autopilot + Lokalnie·HITL (routing z etykiet Linear).
- **Live** — aktualny run (wymaga prawdziwego issue).
- **Approval** — **nie Merge**. To: „zrób na laptopie” (HITL) albo „CI green · czeka na pętlę”.

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
