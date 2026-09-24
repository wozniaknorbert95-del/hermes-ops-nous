# AKADEMIA-INSTRUKCJA — kto robi co

**UI kursu:** `DASHBOARD.html` (6 zakładek: TERAZ / WORKFLOW / NARZĘDZIA / **DSAAS** / NOTATKI / DZIEŃ). Zakładka DSAAS (`id: kurs`): mermaidy, produkt, mastery, działy **A–H** (H = monetyzacja). To ≠ 8. dział Kokpitu. Mapa ról: **INSTRUKCJA** (`#guide`). Narzędzia → **NARZĘDZIA**.
**UI pracy:** [`/ops`](../../OPS.html) — Hermes Ops Control Plane.  
**Kontrakt ról:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md) · **30 s:** [`HERMES-OPS-HOWTO.md`](HERMES-OPS-HOWTO.md).

## Winda (QuietForge)

Nie sprzedajesz aplikacji — sprzedajesz **skalowalność i odzyskany czas** z rygorem inżyniera. Pierwszy SKU w kursie: [`docs/akademia/SKU-SKAN-DECYZJI-MKB.md`](../akademia/SKU-SKAN-DECYZJI-MKB.md) · strona [quietforge.flexgrafik.nl](https://quietforge.flexgrafik.nl/).

## Dwa poranki

| Gdzie | Co |
| --- | --- |
| **Akademia → DZIEŃ** | Rytuał **kursu** (checkboxy, Today first, vault, `GET /hermes/morning`). Nie zleca PR. |
| **workflow-lab → MORNING-RITUAL** | Rytuał **pracy**: [daily digest issue #44](https://github.com/wozniaknorbert95-del/workflow-lab/issues/44), board Linear, 1–3 priorytety. |

## Trzy role (Hermes ≠ jeden pilot)

| Rola | Gdzie | Robi | Nie robi |
| --- | --- | --- | --- |
| **Hermes Akademii** | TERAZ / intent w UI | Kurs, pojęcia, „co dalej" read-only | git, Linear write, MCP, PR, `POST /hermes/chat` (410) |
| **Hermes Engineer** | `/ops` + tick VPS | S0–S6, kolejka Linear → CI → auto-merge | Deploy, merge z telefonu, czat kursu |
| **Cursor Cloud Agent** | GitHub `@cursor` | Kod, branch, PR | deploy produkcji |

Zdanie kanoniczne: **Cursor Cloud Agent jest jedynym executorem kodu w Telefon loopie.**

## Zlecenie kodu (telefon, 2026-09-21+)

1. **Linear** — issue w repo docelowym, label `agent`, 6 pól, bez `blocked` / `hitl:approval-required` (inaczej tor lokalny).  
2. **`/ops`** — **Start** lub **Run next** (Autopilot). Pill **UNKNOWN** → nie startuj „w ciemno”.  
3. **Nie merguj z telefonu** — merge robi pętla po zielonym CI. Deploy = laptop (Zasada 11).

Playbook historyczny (manual @cursor): [`workflow-lab/docs/W6-PHONE-LOOP.md`](https://github.com/wozniaknorbert95-del/workflow-lab/blob/main/docs/W6-PHONE-LOOP.md) — uzupełniony przez `/ops`.

## Czego nie robić

- Nie oczekiwać czatu LLM w Akademii — **`POST /hermes/chat` = 410**.  
- Nie mylić Approval na `/ops` z Merge na GitHubie.  
- Auto-merge **labu/platformy przez orchestrator** ≠ deploy / SSH prod (R7, Zasada 11).
