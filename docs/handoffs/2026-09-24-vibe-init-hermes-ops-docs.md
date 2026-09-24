# Handoff — dopięcie Akademia + Hermes Ops docs/UI (2026-09-24)

## Co zrobione

- Dokumentacja Fale 0–4 (README, OPERATING-MODEL v1.4, runbook, kurs, L3) + guardy CI
- **UI dopięte:** INSTRUKCJA + Hermes + karta Engineer w zakładce **KURS**; `goAcademyTab` mapuje legacy `guide/hermes/workflow/tools` → KURS + kotwica
- INSTRUKCJA w UI zsynchronizowana z `/ops` (Autopilot, brak merge z telefonu)
- `docs/ACADEMY-UX-SPEC.md` → **v4.0** (4 zakładki + `/ops` osobno)
- **Plany audytu (propozycja, nie wykonane):**
  - `docs/AUDYT-PLAN-AKADEMIA-2026-09-24.md`
  - `docs/ops/AUDYT-PLAN-HERMES-OPS-2026-09-24.md`
- Mutacje Fala 0/D zaktualizowane pod `bindGoTabButtons` i nowy `load()`

## Co live

Bez deploy VPS — merge + ewentualny deploy Dowódcy (Zasada 11).

## Co zablokowane (świadomie)

- **Audyty A1–A7 i O1–O8** — czekają na checkbox GO w planach audytu (R1)

## Następny krok (po GO Dowódcy)

1. Zatwierdź plan(y) audytu (jeden lub oba).
2. Sesja audytu → raporty `AUDYT-WYNIK-*`.
3. P0 z audytu w osobnych PR.

## Komendy weryfikacji

```bash
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
# pełna bramka: linia testy: w AGENTS.md
python -m http.server 8765
# KURS → #guide, #hermes; TERAZ → sekcja /ops
```

## Pliki dotknięte (ostatnia iteracja)

- `DASHBOARD.html`, `docs/ACADEMY-UX-SPEC.md`
- `docs/AUDYT-PLAN-AKADEMIA-2026-09-24.md`, `docs/ops/AUDYT-PLAN-HERMES-OPS-2026-09-24.md`
- `scripts/validate-academy-export.py`, `scripts/mutation-test-fala-0.py`, `scripts/mutation-test-fala-d.py`
