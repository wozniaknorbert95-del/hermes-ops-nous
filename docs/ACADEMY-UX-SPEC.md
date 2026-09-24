# Academy Command Dashboard — UX spec (local-first, v4.1)

**Cel:** w 30 sekund wiesz co robisz teraz w **kursie**, jak używać **narzędzi**, gdzie jest **workflow** laptop/telefon i że **praca agentowa = `/ops`**. Jeden fokus naraz (ADHD-first).

## 1. Użytkownik i kontekst

- Właściciel (ADHD-friendly): laptop + telefon; nauka na `/`, pętla inżynierska na `/ops` (osobna PWA).
- Urządzenia: mobile-first (360px), desktop max 1180px. Offline/file:// musi działać; HTTPS + vault = ten sam stan telefon/laptop.
- Ograniczenia (`AGENTS.md` akademii): jedno TERAZ; eksport v0.1.0; brak iframe Kokpitu; brak 7. działu; zero sekretów.

## 2. Sześć zakładek Akademii (IA v4.1, split Ops)

| Zakładka | Pytanie | Główna akcja |
|---|---|---|
| `TERAZ` | Co robię w tej minucie w kursie? | Jeden rozdział: kroki lab + zaliczenie + CTA **Hermes Ops** |
| `WORKFLOW` | Jak wygląda pętla pracy (laptop + telefon)? | Playbooki, mapa ról → INSTRUKCJA (KURS) i NARZĘDZIA |
| `NARZĘDZIA` | Co działa naprawdę i jak tego nie zepsuć? | Karty `TOOL_DATA`: instrukcje, statusy, złote zasady, gotcha; karta Hermes Engineer |
| `KURS` | Gdzie jest materiał i mapa ról? | INSTRUKCJA (#guide), Hermes (intent), accordion A–G |
| `NOTATKI` | Co zapisałem dla siebie? | `_scratch.notes` (sync vault) |
| `DZIEŃ` | Jaki rytuał dnia kursu? | Poranek/wieczór + sync; **nie** zleca PR (to `/ops`) |

**Hermes Ops (osobny produkt):** `/ops` — Control Plane; nie jest siódmą zakładką Akademii.

**Reguła TERAZ:** Na zakładce TERAZ widoczny tylko panel (bez duplikatu `#nowcard`). Na innych zakładkach — kompaktowa karta TERAZ u góry.

**Legacy nawigacja:** `guide`, `hermes`, `dsaas` w starym `active_tab` → **KURS**. Kotwice `#guide`, `#hermes` → KURS + scroll. `data-go-tab="workflow"` / `"tools"` otwierają właściwe zakładki.

## 3. Stany

- Pierwszy start: banner powitalny + link **Praca — Hermes Ops** + TERAZ → A1.
- Sync vault, PWA, export — bez zmian względem v3.1 (schema 0.1.0).
- Kotwice `#roz-*` otwierają zakładkę **KURS**.

## 4. Komponenty

- `renderWorkflow()` — pełne pętle pracy, linki do rozdziałów i `/ops`.
- `renderTools()` — `TOOL_DATA` + rozwijane instrukcje per narzędzie; `#tool-hermes-engineer` dla karty Engineera.
- `NowCard`, playbook, diagramy — w accordionie KURS (działy B–F zachowują diagramy).
- `ops-howto` na TERAZ — skrót HOWTO + link `/ops`.
- INSTRUKCJA — `renderGuide()` w KURS, id `guide`.

## 5. Odbiór (DoD v4.1)

- `python scripts/validate-academy-export.py` → PASS (6 zakładek, split /ops, kontrakt eksportu)
- `python scripts/test_progress_vault.py` → PASS
- Walkthrough 360px: TERAZ + WORKFLOW + NARZĘDZIA + KURS (guide, hermes) + NOTATKI + DZIEŃ; `/ops` ładuje OPS.html
- Runbook: `docs/runbooks/AKADEMIA-VPS.md`

**Powiązane:** [`docs/ops/README.md`](ops/README.md) · [`OPERATING-MODEL.md`](OPERATING-MODEL.md) §1.1
