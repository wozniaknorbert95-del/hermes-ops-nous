# Academy Command Dashboard — UX spec (local-first, v4.0)

**Cel:** w 30 sekund wiesz co robisz teraz w **kursie**, gdzie kliknąć i że **praca agentowa = `/ops`**. Jeden fokus naraz (ADHD-first).

## 1. Użytkownik i kontekst

- Właściciel (ADHD-friendly): laptop + telefon; nauka na `/`, pętla inżynierska na `/ops` (osobna PWA).
- Urządzenia: mobile-first (360px), desktop max 1180px. Offline/file:// musi działać; HTTPS + vault = ten sam stan telefon/laptop.
- Ograniczenia (`AGENTS.md` akademii): jedno TERAZ; eksport v0.1.0; brak iframe Kokpitu; brak 7. działu; zero sekretów.

## 2. Cztery zakładki Akademii (IA v4, split Ops)

| Zakładka | Pytanie | Główna akcja |
|---|---|---|
| `TERAZ` | Co robię w tej minucie w kursie? | Jeden rozdział: kroki lab + zaliczenie + CTA **Hermes Ops** |
| `KURS` | Gdzie jest materiał i mapa ról? | INSTRUKCJA (#guide), Hermes (intent), Engineer card, accordion A–G |
| `NOTATKI` | Co zapisałem dla siebie? | `_scratch.notes` (sync vault) |
| `DZIEŃ` | Jaki rytuał dnia kursu? | Poranek/wieczór + sync; **nie** zleca PR (to `/ops`) |

**Hermes Ops (osobny produkt):** `/ops` — Control Plane; nie jest piątą zakładką Akademii.

**Reguła TERAZ:** Na zakładce TERAZ widoczny tylko panel (bez duplikatu `#nowcard`). Na innych zakładkach — kompaktowa karta TERAZ u góry.

**Legacy nawigacja:** linki `#guide`, `#hermes`, stare nazwy zakładek → przekierowanie na **KURS** + kotwica (nie pusty panel).

## 3. Stany

- Pierwszy start: banner powitalny + link **Praca — Hermes Ops** + TERAZ → A1.
- Sync vault, PWA, export — bez zmian względem v3.1 (schema 0.1.0).
- Kotwice `#roz-*` otwierają zakładkę **KURS** (nie usunięte WORKFLOW/DSAAS).

## 4. Komponenty

- `NowCard`, playbook, diagramy — w accordionie KURS (działy B–F zachowują diagramy).
- `ops-howto` na TERAZ — skrót HOWTO + link `/ops`.
- INSTRUKCJA — `renderGuide()` w KURS, id `guide`.

## 5. Odbiór (DoD v4)

- `python scripts/validate-academy-export.py` → PASS (4 zakładki, split /ops, kontrakt eksportu)
- `python scripts/test_progress_vault.py` → PASS
- Walkthrough 360px: TERAZ + KURS (guide, hermes) + NOTATKI + DZIEŃ; `/ops` ładuje OPS.html
- Runbook: `docs/runbooks/AKADEMIA-VPS.md`

**Powiązane:** [`docs/ops/README.md`](ops/README.md) · [`OPERATING-MODEL.md`](OPERATING-MODEL.md) §1.1
