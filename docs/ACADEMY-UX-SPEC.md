# Academy Command Dashboard — UX spec (local-first, v1.0)

**Cel:** w 30 sekund wiesz co robisz teraz, gdzie kliknąć i czyja jest piłka. Jak dla dziecka: duże litery, jedno zadanie naraz, zero żargonu na wierzchu.

## 1. Użytkownik i kontekst

- Właściciel (ADHD-friendly): pracuje z telefonu i laptopa, potrzebuje spokoju, nie kolejnego chaosu.
- Urządzenia: mobile-first (360px), potem desktop (max 980px). Tryb offline/file:// musi działać.
- Ograniczenia twarde (`AGENTS.md`): jedno `▶ TERAZ`; eksport zgodny ze schematem v0.1.0; brak iframe do Kokpitu; brak 7. działu; brak sekretów/tokenów.

## 2. Pięć stref (każda = 1 pytanie + max 1 główna akcja)

| Strefa | Pytanie | Główna akcja |
|---|---|---|
| `Teraz` | Co robię w tej minucie? | 1 klik do lekcji / zadania (prawdziwy link/przycisk, nie `<span>`) |
| `Dzień` | Jaki jest mój poranek i wieczór? | Rano 10′ checklist; wieczorem 5′ domknięcie; 1 priorytet dnia (ręcznie) |
| `Platforma` | Gdzie jest główna praca? | Ręczny status toru (tekst + link do `todo.json`); granice w 3 linijkach |
| `Akademia` | Czego się uczę? | Tryb dnia: tylko bieżący moduł rozwinięty; reszta zwinięta; lekcje klikalne |
| `Piątek` | Co z kosztami i porządkiem? | Lokalny formularz (koszt/lekcja/porządek) + eksport; bez integracji billingowej |

Kolejność `▶ TERAZ`: (1) ręczny priorytet właściciela (jeśli ustawiony), (2) bieżący moduł nauki, (3) egzamin po 6 modułach. Jedna karta, nigdy dwie.

## 3. Stany (wszystkie zaprojektowane, nie tylko happy path)

- Pierwszy start: powitanie 3 kroki (otwórz → zrób 1 rzecz → zamknij), zero pełnego syllabusa na wierzchu.
- Brak zapisu / uszkodzony `localStorage`: spokojny komunikat + przycisk „Zacznij od nowa" (bez utraty eksportu, jeśli istnieje).
- Moduł w toku: pasek postępu + „zostało N kroków" + przycisk Wstecz/Dalej.
- Zaliczony moduł: zielony znacznik słowny „Zaliczone" (nie sam emoji), kolejny moduł odblokowany.
- Zablokowany moduł: wyszarzony + tekst „Najpierw ukończ poprzedni", pola naprawdę `disabled` (nie tylko CSS).
- Import OK: „Wczytano — jesteś w module X"; import zły: czerwony box z powodem, bez `alert()` i bez przeładowania strony.
- Eksport: widoczne „Skopiowano / Pobrano plik JSON" + data; błąd kopiowania z instrukcją ręczną.
- Telefon: jedna kolumna, przyciski min. 44px, brak poziomego scrolla.

## 4. Komponenty i zasady interakcji

- `NowCard`: nagłówek „TERAZ ROBISZ TYLKO TO", 1 zdanie czynności + 1 przycisk. Mapa na Kokpit (Tor F) wyłącznie w zwiniętym detalu.
- `DayChecklist`: checkboxy rano/wieczór z zapisem lokalnym; pole „Mój 1 priorytet" (tekst, max 140 znaków).
- `ModuleAccordion`: `<details>` z prawdziwym gatingiem; bieżący auto-rozwinięty; checkpointy jako `<fieldset>` + `<legend>`.
- `LibraryLinks`: każda pozycja biblioteki to `<a href="cursor-kurs/...">`, nie sam tekst ścieżki. Na `file://` dopuszczalny komunikat „uruchom przez `python -m http.server`".
- `ProgressBar`: `role="progressbar"` + `aria-valuenow` + tekst „X% (N z 6 modułów)".
- `ExportBox`: przyciski „Kopiuj" i „Pobierz JSON" + `<textarea>` schowane pod „Więcej"; Kokpit ignoruje `_scratch`.
- Feedback: nigdy sam kolor/emoji; zawsze słowo („Zaliczone", „Zablokowane", „Błąd importu").

## 5. Tokeny i język

- Tło ciemne jak dziś; tekst główny min. 16px; nagłówki hierarchiczne bez skoków.
- Kolory znaczeń: fiolet = teraz, zielony = zaliczone, szary = zablokowane, bursztyn = odzysk/NIE. Kontrast docelowo AA.
- Mikrocopy po polsku, krótkie zdania. Technika (localStorage, JSON, Tor W/F) wyłącznie w sekcji „Więcej / Jak to działa".
- Ruch: `prefers-reduced-motion` wyłącza smooth scroll i animacje paska.
- Fokus klawiatury zawsze widoczny (`:focus-visible`); całość obsługiwalna Tab + Enter.

## 6. Handoff wdrożeniowy

- Cel implementacji: statyczny `DASHBOARD.html` (bez frameworka), `python -m http.server` do klikalnych lekcji.
- Zakaz: backend, API GitHub/Linear, tokeny, iframe, drugi `TERAZ`, kopiowanie kanonu DSaaS.
- Odbiór: (a) kontrakt eksportu/importu przechodzi walidator, (b) podstawowe sprawdzenie a11y (landmarki, fokus, progressbar, fieldsety), (c) test ręczny na telefonie 360px, (d) tryb `file://` nie wywala błędów.
