# Hermes Ops — jak używać (`/ops`)

**UI pracy:** `https://akademia…/ops` (PWA Hermes Ops).  
**UI nauki:** `/` = Akademia (kurs A–G).  
**Kontrakt ról:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md).

## 30 sekund

1. Decyzja i kolejka = **Linear** (etykieta `agent` + 6 pól).
2. Otwórz **`/ops`** na telefonie.
3. Wybierz tryb → **Start / Run next** (gdy chcesz ruszyć).
4. **Nie merguj z telefonu.** Merge robi pętla po zielonym CI.
5. **Deploy = lokalnie, ręcznie** (Zasada 11).

## Trzy tryby

| Tryb | Kto rusza następne issue | Kiedy |
| --- | --- | --- |
| **Manual** | Ty tapasz **Run next** | Pełna kontrola — nic samo nie startuje |
| **Autopilot** | Pętla bierze z toru `agent` | Hermes pracuje; Ty: Pause / Stop |
| **Supervised** | Jak Autopilot + **Web Push** przy HITL / ryzyku | Auto, ale budzi Cię na telefonie |

Push Supervised działa tylko gdy: PWA zainstalowana, zgoda na powiadomienia, tryb = SUPERVISED (cooldown ~1 h).

## Sekcje na `/ops`

- **Teraz / Next** — bieżące lub następne issue + pasek S1–S6.
- **Sterowanie** — Pause, Stop, Retry, **Take over** (Pause + praca lokalnie, zero `@cursor`).
- **Kolejka** — Autopilot / Manual / Lokalnie·HITL (routing z etykiet Linear).
- **Live** — aktualny run (wymaga prawdziwego issue).
- **Approval** — **nie Merge**. To: „zrób na laptopie” (HITL) albo „CI green · czeka na pętlę”.

## Czego nie robić z telefonu

- Merge na GitHubie.
- Deploy / `workflow_dispatch` produkcji.
- Start Autopilot / Run next „w ciemno” przy pillu **UNKNOWN**.

## Etykiety Linear (skrót)

- Tor agenta: `agent` + Ready, **bez** `hitl:approval-required` / `blocked`.
- HITL / laptop: `hitl:approval-required` albo brak `agent` → tor **Lokalnie**.
