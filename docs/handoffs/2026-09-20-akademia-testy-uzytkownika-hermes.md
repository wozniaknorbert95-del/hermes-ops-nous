# Handoff — Akademia: testy oczami użytkownika + naprawa 12 defektów (2026-09-20)

**Zakres:** test narzędzia w roli użytkownika (Chrome, realne klikanie, desktop + telefon),
fokus na Hermesie. Znalezione defekty naprawione, guardy postawione.

**Gałąź:** `feat/hermes-chat-ux-audit` · **PR:** [#17](https://github.com/wozniaknorbert95-del/akademia/pull/17)

---

## 1. Dokumenty

- Plan testów: `docs/ops/PLAN-TESTOW-2026-09-20.md`
- **Wynik testów z werdyktem i listą DO DZIAŁA: `docs/ops/WYNIK-TESTOW-2026-09-20.md`** ← czytaj to pierwsze
- Audyt UX/UI z poprzedniej sesji: `docs/ops/AUDYT-UX-UI-2026-09-20.md`

## 2. Co zostało zrobione

Test 5 scenariuszy / 6 zakładek / 33 pytań do Hermesa / pełna pętla dnia. Znalezione i naprawione:

| Obszar | Defekt | Naprawa |
|---|---|---|
| Nawigacja | Klik zakładki robił `scrollTo(0)`; treść zostawała 900–1200 px pod ekranem | `alignPanelToNav()` — prowadzi do treści pod paskiem zakładek |
| Spójność | Karta „TERAZ" pokazywała na sztywno krok 1, Hermes poprawnie krok 2 | `nextLabIdx()` — jedno źródło prawdy dla karty i Hermesa |
| Odświeżanie | Odhaczenie kroku nie odświeżało karty TERAZ | `afterDataChange()` |
| Informacja zwrotna | `msg()` pisał do stopki (~4461 px) — potwierdzenia i **błędy** niewidoczne | toast nad paskiem dolnym (6 s ok / 11 s błąd) |
| Błąd | „odhacz laboratorium" przewijał do innego, zablokowanego rozdziału | prowadzi do właściwego rozdziału |
| Płynność | Po zaliczeniu rozdziału — skok na górę strony | przejście do następnego rozdziału |
| Bezpieczeństwo | Prośba o klucz API → odpowiedź o eksporcie zamiast odmowy | jawna odmowa + gdzie klucze faktycznie żyją |
| Hermes | „wytlumacz odc", „co to ledzer" → odmowa, choć pojęcia są w słowniku | tolerancja literówek ±1 znak (`hermesDist`/`hermesFuzzyHit`) |
| Hermes | „Co potrafisz?" = identyczna odpowiedź jak „Jak używać?" | osobna gałąź |
| Hermes | „Rytuał DZIEŃ jest **zgrane** na zielono" | poprawiona polszczyzna |
| Karta LOCK | Lista braków ucięta do 3 bez słowa o reszcie (rytuał ma 13 pozycji) | 4 + „…i jeszcze N pozycji" |
| Karta powitalna | Podwójny szewron `❯❯` (CSS dokleja `❯` do `<h3>`) | usunięty literał |

Dodatkowo: przycisk **„❯ Przejdź do TERAZ — jeden krok"** w karcie powitalnej (pasek zakładek
na pierwszym wejściu jest poza ekranem).

## 3. Weryfikacja (zmierzona, nie obiecana)

```
python scripts/validate-academy-export.py    → PASS (12 nowych guardów D1–D11)
python scripts/test_progress_vault.py        → PASS
python scripts/mutation-test-fala-d.py       → 19/19 mutacji złapanych, 0 przepuszczonych
```

W przeglądarce (desktop 1230×844 i telefon 390×844, `pointer:coarse`):

- 6/6 zakładek ląduje na treści (panel 126–148 px, pasek kończy się na 114 px)
- karta TERAZ i Hermes mówią to samo: „Krok 2 z 3" po odhaczeniu kroku 1
- toast błędu widoczny na 731 px; toast potwierdzenia po zaliczeniu i po eksporcie
- po zaliczeniu A1 użytkownik ląduje na `roz-A2`
- 0 błędów i 0 ostrzeżeń konsoli; 0 px przelewania; 0 celów dotykowych < 44 px na telefonie
- eksport: `schema_version=0.1.0`, `source=academy-os`, `academy_url` bez tokena, rozmowa nie wycieka

## 4. Czego NIE zrobiono (świadomie)

- **Nie deployowano.** Zgodnie z Zasadą 11 (deploy tylko ręcznie na GO Dowódcy).
- Nie testowano z prawdziwym modelem — lokalny vault nie ma podłączonego dostawcy, więc
  odpowiedzi szły z lokalnego silnika. Ścieżka z modelem była sprawdzona wcześniej na atrapie.
- Nie testowano na fizycznym telefonie (tylko emulacja) i nie testowano wysyłki push.

## 5. Następne kroki (propozycja, w kolejności)

1. **GO/NO-GO na deploy** — zmiany są zweryfikowane i czekają na Twoją decyzję.
2. Podłączyć model (DeepSeek) przez zmienne środowiskowe vaulta na VPS, jeśli Hermes ma
   odpowiadać także na pytania spoza kursu. Kod nie wymaga zmian.
3. P2: pierwsze wejście na telefonie — schować instrukcję instalacji w `<details>`.
4. P3: powrót po przerwie powinien lądować na DZIEŃ/TERAZ, nie na ostatniej zakładce.
5. P3: rozważyć skrócony rytuał dnia (13 checkboxów + 2 linie to dużo).
6. P3: zablokować (`disabled`) kroki labu w rozdziałach z LOCK.
