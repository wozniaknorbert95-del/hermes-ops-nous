# Plan audytu — produkt **Akademia** (`/`)

**Status:** **W TRAKCIE / GO 2026-09-24** (Dowódca)  
**Zakres:** warstwa nauki — `DASHBOARD.html`, postęp, rytuał DZIEŃ, PWA kursu, vault `/progress`, intent Hermes Akademii. **Bez** orchestratora tick (`/ops` = osobny audyt).

---

## 1. Cel audytu

Potwierdzić, że Akademia spełnia kontrakt UX **v4.1** i `schema/academy-progress.v0.json`: jedno TERAZ, **WORKFLOW + NARZĘDZIA** jako pierwsza klasa IA (nie martwy kod), uczciwy LOCK DZIEŃ, sync vault, brak obietnic wykonawczych (merge/deploy/PR).

**Deliverable:** raport [`docs/AUDYT-WYNIK-AKADEMIA-2026-09-24.md`](AUDYT-WYNIK-AKADEMIA-2026-09-24.md) (P0–P2 + repro + plik).

---

## 2. Wejścia (przed startem)

- [x] Merge dokumentacji / dopięcie UI (branch docs + KURS/guide + przywrócenie 6 zakładek).
- [x] `python scripts/validate-academy-export.py` + pełna linia `testy:` z `AGENTS.md` → zielone (lokalnie).
- [ ] Lokalnie: `python -m http.server 8765` → smoke WORKFLOW/NARZĘDZIA (manual).

---

## 3. Fazy audytu

| Faza | Obszar | Metoda | Kryterium PASS |
| --- | --- | --- | --- |
| **A1** | IA **6 zakładek** | Manual 360px + 768px + walidator A3 | TERAZ/WORKFLOW/NARZĘDZIA/KURS/NOTATKI/DZIEŃ; brak martwych CTA; #guide/#hermes w KURS |
| **A2** | TERAZ | Script + manual | Jeden krok lab odhaczalny; jedna karta TERAZ; CTA /ops obecne |
| **A3** | DZIEŃ / morning | `test_progress_vault` + manual | LOCK/F8; `/hermes/morning`; brak fałszywego LOCK po rest day |
| **A4** | Sync / eksport | Round-trip import/export | `schema_version` 0.1.0; brak tokenów w `academy_url` |
| **A5** | Intent Hermes | `test_hermes_intent.py` + manual chips | Nie obiecuje MCP/merge; wskazuje /ops dla pracy |
| **A6** | Docs vs UI | Diff checklist | `ACADEMY-UX-SPEC.md` v4.1, `AKADEMIA-INSTRUKCJA.md` zgodne z ekranem |
| **A7** | Regresja CI | Pełna bramka + mutacje | 0 PRZEPUSZCZONE w Fala 0/D/I/K |
| **A8** | **NARZĘDZIA / WORKFLOW** | Code + manual | `renderMainPanel` wywołuje `renderWorkflow`/`renderTools`; TOOL_DATA z instrukcjami; mapa ról linkuje tabs |

---

## 4. Poza zakresem (Hermes Ops)

Linear routing, `/ops/diag`, tick timer, auto-merge — patrz [`docs/ops/AUDYT-PLAN-HERMES-OPS-2026-09-24.md`](ops/AUDYT-PLAN-HERMES-OPS-2026-09-24.md).

---

## 5. Po audycie

- P0 naprawa w osobnych PR (max jeden temat na PR).
- Aktualizacja `docs/handoffs/` po zamknięciu sesji audytu.
- Deploy VPS tylko na GO (Zasada 11) — smoke `/` i `/progress`, nie tick.

---

## 6. Decyzja Dowódcy

- [x] **GO** — start audytu Akademia (data: **2026-09-24**)
- [ ] **STOP / zmiana zakresu** — komentarz: _____
