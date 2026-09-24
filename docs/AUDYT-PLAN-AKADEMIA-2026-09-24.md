# Plan audytu — produkt **Akademia** (`/`)

**Status:** **PROPOZYCJA — czeka na GO Dowódcy (R1)**  
**Nie uruchamiać** przed zatwierdzeniem. Ten plik to tylko harmonogram i kryteria.

**Zakres:** wyłącznie warstwa nauki — `DASHBOARD.html`, postęp, rytuał DZIEŃ, PWA kursu, vault `/progress`, intent Hermes Akademii. **Bez** orchestratora tick (`/ops` = osobny audyt).

---

## 1. Cel audytu

Potwierdzić, że Akademia spełnia kontrakt UX v4 i `schema/academy-progress.v0.json`: jedno TERAZ, uczciwy LOCK DZIEŃ, sync vault, brak obietnic wykonawczych (merge/deploy/PR).

**Deliverable:** raport `docs/AUDYT-WYNIK-AKADEMIA-YYYY-MM-DD.md` z listą findingów P0–P2 + repro + plik.

---

## 2. Wejścia (przed startem)

- Merge dokumentacji / dopięcia UI (branch docs + KURS/guide).
- `python scripts/validate-academy-export.py` + pełna linia `testy:` z `AGENTS.md` → zielone.
- Lokalnie: `python -m http.server 8765` → `DASHBOARD.html`.

---

## 3. Fazy audytu (szacunek effort techniczny)

| Faza | Obszar | Metoda | Kryterium PASS |
| --- | --- | --- | --- |
| **A1** | IA 4 zakładek | Manual 360px + 768px | Brak martwych CTA; #guide/#hermes działają w KURS |
| **A2** | TERAZ | Script + manual | Jeden krok lab odhaczalny; jedna karta TERAZ; CTA /ops obecne |
| **A3** | DZIEŃ / morning | `test_progress_vault` + manual | LOCK/F8; `/hermes/morning`; brak fałszywego LOCK po rest day |
| **A4** | Sync / eksport | Round-trip import/export | `schema_version` 0.1.0; brak tokenów w `academy_url` |
| **A5** | Intent Hermes | `test_hermes_intent.py` + manual chips | Nie obiecuje MCP/merge; wskazuje /ops dla pracy |
| **A6** | Docs vs UI | Diff checklist | `ACADEMY-UX-SPEC.md`, `AKADEMIA-INSTRUKCJA.md` zgodne z ekranem |
| **A7** | Regresja CI | Pełna bramka + mutacje | 0 PRZEPUSZCZONE w Fala D/I/K |

---

## 4. Poza zakresem (Hermes Ops)

Linear routing, `/ops/diag`, tick timer, auto-merge — patrz [`docs/ops/AUDYT-PLAN-HERMES-OPS-2026-09-24.md`](ops/AUDYT-PLAN-HERMES-OPS-2026-09-24.md).

---

## 5. Po audycie

- P0 naprawa w osobnych PR (max jeden temat na PR).
- Aktualizacja `docs/handoffs/` po zamknięciu sesji audytu.
- Deploy VPS tylko na GO (Zasada 11) — smoke `/` i `/progress`, nie tick.

---

## 6. Decyzja Dowódcy (do wypełnienia)

- [ ] **GO** — start audytu Akademia (data: _____)
- [ ] **STOP / zmiana zakresu** — komentarz: _____
