# AKADEMIA-INSTRUKCJA — kto robi co

**UI:** zakładka **INSTRUKCJA** w `DASHBOARD.html` (id `guide`, 2. na pasku po TERAZ).  
**Kontrakt ról:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md).

## Dwa poranki

| Gdzie | Co |
| --- | --- |
| **Akademia → DZIEŃ** | Rytuał **kursu** (checkboxy, Today first, vault). Nie zleca PR. |
| **workflow-lab → MORNING-RITUAL** | Rytuał **pracy**: [daily digest issue #44](https://github.com/wozniaknorbert95-del/workflow-lab/issues/44), board Linear, 1–3 priorytety. |

## Trzy role (Hermes ≠ jeden pilot)

| Rola | Gdzie | Robi | Nie robi |
| --- | --- | --- | --- |
| **Hermes Akademii** | Zakładka HERMES (czat) | Kurs, pojęcia, „co dalej" read-only | git, Linear write, MCP, PR |
| **Hermes Engineer** | VPS + karta NARZĘDZIA | S1–S6, brief operatora (read-only API) | Czat, start Cursora, merge |
| **Cursor Cloud Agent** | GitHub `@cursor` | Kod, branch, PR | — |

Zdanie kanoniczne: **Cursor Cloud Agent jest jedynym executorem kodu w Telefon loopie.**

## Zlecenie kodu (telefon)

1. **Linear** — issue `workflow-lab`, label `agent`, 6 pól.  
2. **GitHub** — komentarz `@cursor` (krótki scope).  
3. **GitHub mobile** — review + merge gdy CI zielone.

Playbook: [`workflow-lab/docs/W6-PHONE-LOOP.md`](https://github.com/wozniaknorbert95-del/workflow-lab/blob/main/docs/W6-PHONE-LOOP.md).

## Czego nie robić

- Nie pisać „zrób PR" do czatu HERMES (brak MCP w `/hermes/chat`).  
- Nie oczekiwać startu agenta z karty Engineer — to mapa + VPS, nie pilot.  
- Auto-merge **labu** ≠ deploy / merge **dsaas-platform-main** (R7).
