# Plan poprawek UX/UI Hermes Ops (2026-10-04)

**Repo:** `hermes-ops-nous`  
**UI:** `OPS.html`  
**Cel:** czytelny styl terminala, białe tło, zero gradientów, wszystko klikalne

## Audyt UX/UI — wyniki

### Co działa:
- Fail-closed: "Run next" zablokowany bez DoR — bezpieczne
- Czytelny layout: białe tło, monospace, kolory semantyczne
- Zero gradientów: czysty, terminalowy styl
- Wszystko klikalne: przyciski, chipy, statystyki

### Problemy UX:

| # | Problem | Rekomendacja |
|---|---|---|
| 1 | Brak wskazówki po odblokowanie | Dodaj link "Otwórz Linear" przy zablokowanym "Run next" |
| 2 | "Run next" nie działa | Dodaj tooltip "Uzupełnij DoR w Linear" przy zablokowanym przycisku |
| 3 | Brak feedbacku | Dodaj wizualny stan pętli (uruchomiona/zatrzymana) |
| 4 | "Take over" mylący | Zmień na "Zatrzymaj i przejmij" |
| 5 | "ZANIM RUSZYSZ" zbyt techniczne | Zmień na "Wymagania przed startem" |
| 6 | Brak linku do Linear | Dodaj link w nagłówku kolejki |
| 7 | Brak instrukcji | Dodaj "Jak zacząć" — 1. Uzupełnij DoR w Linear, 2. Kliknij Run next |

## Plan wdrożenia

### Faza 1: Szybkie poprawki (P0)
1. Dodaj link "Otwórz Linear" przy zablokowanym "Run next"
2. Dodaj tooltip "Uzupełnij DoR w Linear" przy zablokowanym przycisku
3. Zmień "ZANIM RUSZYSZ" na "Wymagania przed startem"
4. Zmień "Take over" na "Zatrzymaj i przejmij"
5. Dodaj link do Linear w nagłówku kolejki

### Faza 2: Lepszy feedback (P1)
1. Dodaj wizualny stan pętli (uruchomiona/zatrzymana)
2. Dodaj animację ładowania przy kliknięciu "Run next"
3. Dodaj potwierdzenie po kliknięciu "Take over"

### Faza 3: Instrukcja (P1)
1. Dodaj "Jak zacząć" — 1. Uzupełnij DoR w Linear, 2. Kliknij Run next
2. Dodaj link do dokumentacji

## Kryteria akceptacji
- [ ] Wszystkie linki działają
- [ ] Tooltips są czytelne
- [ ] Stan pętli jest widoczny
- [ ] Instrukcja jest zrozumiała dla nowego użytkownika
