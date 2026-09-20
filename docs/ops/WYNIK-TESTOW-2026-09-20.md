# WYNIK TESTÓW — Akademia OS oczami użytkownika (fokus: Hermes)

Data: 2026-09-20 · Plan: `docs/ops/PLAN-TESTOW-2026-09-20.md`
Metoda: prawdziwa przeglądarka (Chrome), prawdziwa klawiatura, prawdziwe klikanie.
Nie czytałem kodu, żeby ocenić narzędzie — czytałem kod tylko wtedy, gdy coś było zepsute
i trzeba było znaleźć przyczynę.

**Zakres:** 5 scenariuszy, 6 zakładek, 33 pytania do Hermesa, desktop + telefon (390×844,
`pointer:coarse`), 1 marszruta pełnego dnia (LOCK → odblokowanie), przejście rozdziału A1 → A2.

---

## 1. Werdykt: czy to ma sens dla użytkownika?

**Ma — pod jednym warunkiem, który dziś dopiero został spełniony: narzędzie musi przestać
przeczyć samemu sobie.**

Przed tym testem Akademia była **merytorycznie poprawna i użytkowo niewiarygodna**:

- Karta „TERAZ ROBISZ TYLKO TO" kazała robić **krok 1**, gdy krok 1 był już odhaczony —
  a Hermes obok poprawnie podawał **krok 2**. Dwa sprzeczne komunikaty na jednym ekranie.
- Kliknięcie zakładki **wyrzucało na górę strony**, a treść zostawała ~900–1200 px niżej.
  Efekt: „kliknąłem HERMES i nic się nie stało".
- Wszystkie potwierdzenia i **wszystkie błędy** lądowały w stopce, ~4461 px pod treścią.
  Kliknięcie „Zalicz rozdział" bez odhaczonego labu: brak komunikatu **i** przewinięcie
  do innego, zablokowanego rozdziału. Narzędzie wyglądało na zepsute, choć działało.

To jest najgorszy możliwy typ defektu w narzędziu, które ma być kontrolerem: użytkownik
przestaje wierzyć, że cokolwiek działa, i przestaje z niego korzystać.

**Po naprawach (zmierzone, nie obiecane):**

- 6/6 zakładek ląduje równo pod paskiem nawigacji (panel 126–148 px, nav kończy się na 114 px).
- Karta TERAZ i Hermes **mówią to samo**: po odhaczeniu kroku 1 oba pokazują „Krok 2 z 3".
- Błąd i potwierdzenie są **widoczne na ekranie**: toast na 731 px, klasa `toast err`/`toast ok`.
- Po zaliczeniu rozdziału użytkownik **idzie do następnego rozdziału** (`roz-A2`), nie na górę.
- 0 błędów i 0 ostrzeżeń konsoli przez całą sesję.

### Hermes — co realnie robi

| Funkcja | Ocena | Dowód z testu |
|---|---|---|
| Kontroler („co dalej") | **Działa i jest precyzyjny** | Po zaliczeniu A1: „Jeden kawał: W ci.yml wskaż linię uruchamiającą npm test, lint i build · Krok 1 z 3 w laboratorium rozdziału A2 · Plik: workflow-lab/package.json" |
| Kontroler („gdzie jestem") | **Działa** | „Postęp: 4% — 1 z 26 rozdziałów, zostało 25 · Otwartych kroków lab: 77" |
| Kontroler („dlaczego zablokowane") | **Działa, z lista braków** | Stale dzień → nazwana blokada + 5 konkretnych braków + „To nie kara, tylko bezpiecznik" |
| Nauczyciel (10 pojęć) | **Działa** | ODCS, HITL, ledger, R7, Cedar+RLS, objective, MCP, budżet złożoności — każde: co to + po co + plik źródłowy |
| Uczciwość | **Działa — i to jest mocna strona** | „asdfghjkl", „jaka jutro pogoda w Gdańsku", „kubernetes operator w moim repo" → „Nie mam tego w źródłach — i nie będę zgadywać" z listą tego, o co wolno pytać |
| Odporność na literówki | **Naprawione dziś** | Przed: „wytlumacz odc" i „co to ledzer" → odmowa. Po: ODCS i ledger, poprawnie |
| Pytanie o sekret | **Naprawione dziś** | Przed: prośba o klucz API dostawała odpowiedź o eksporcie (nie wyciekało, ale nie było odmowy). Po: jednoznaczna odmowa + wyjaśnienie, gdzie klucze faktycznie żyją |
| Koszt i limity | **Dobre** | 22 pytania = 22 żądania `/hermes/chat` (1:1, zero marnotrawstwa), limit dzienny widoczny w UI („dziś 2 / 200") |
| Fallback offline | **Działa i jest uczciwy** | Bez dostawcy modelu: „Uczciwie: odpowiedział silnik lokalny (brak łączności z dostawcą (URLError)). Postęp i tak liczy się z Twojego stanu, nie z modelu" |
| Puste Enter / Shift+Enter / ściana 5000 znaków | **Działa** | Puste i Shift+Enter nie wysyłają; 5000 znaków obsłużone bez przełamania layoutu |

**Ograniczenie, które trzeba powiedzieć wprost:** dzisiejsze odpowiedzi pochodziły
z **lokalnego silnika** (intencje + słownik pojęć), bo lokalny vault nie ma podłączonego
modelu. Szlak z prawdziwym modelem (system prompt, przycinanie kontekstu, użycie tokenu)
był sprawdzony wcześniej na atrapie dostawcy. Lokalny silnik odpowiada dobrze na pytania
o kurs i stan, a na pytania spoza tego zakresu **odmawia** — to jest zgodne z projektem,
ale nie zastąpi modelu, gdy chcesz pytać o cokolwiek.

---

## 2. Co DZIAŁA (z dowodem)

1. **Pętla dnia domyka się end-to-end.** Zaległy dzień → LOCK z dokładną listą braków →
   uzupełnienie rytuału → dzień zamknięty na zielono → następny rozdział odblokowany.
   Sprawdzone realnym klikanciem, nie założeniem.
2. **Przejście rozdziału A1 → A2.** Odhaczenie 3 kroków labu → „Wszystkie kroki odhaczone —
   zalicz rozdział A1" → zaliczenie → toast + lądowanie na A2.
3. **Read-only jest prawdziwe.** Czat nie zmienił postępu; rozmowa żyje w `sessionStorage`
   i nie wchodzi do eksportu.
4. **Eksport trzyma kontrakt.** `schema_version=0.1.0`, `source=academy-os`,
   `academy_url` bez tokena, zero treści rozmowy w pliku. Toast „Eksport gotowy —
   skopiowano do schowka."
5. **PWA.** Przeglądarka zgłasza gotowość („promocja instalacji: gotowa — przycisk wyżej działa"),
   manifest i ikony są publiczne, więc WebAPK ma z czego powstać.
6. **Telefon.** 390×844: 0 px przelewania w poziomie, **0 celów dotykowych poniżej 44 px**
   (na 24 zbadanych), `pointer:coarse` aktywne.
7. **Dostępność.** Zakładki na strzałkach/Home/End, `role=tab`/`aria-selected`, pasek postępu
   z `aria-valuenow`/`aria-valuetext`, focus-visible, skip-link.
8. **Zero błędów konsoli** i zero ostrzeżeń w całej sesji (desktop i telefon).

---

## 3. LISTA DO DZIAŁA

### Zrobione w tej sesji (blokery — bo psuły zaufanie)

| # | Defekt | Status |
|---|---|---|
| 1 | Klik zakładki wyrzucał na górę strony, treść zostawała pod ekranem | **naprawione** — `alignPanelToNav` |
| 2 | Karta TERAZ pokazywała na sztywno krok 1, sprzecznie z Hermesem | **naprawione** — `nextLabIdx` |
| 3 | Odhaczenie kroku nie odświeżało karty TERAZ | **naprawione** — `afterDataChange` |
| 4 | Potwierdzenia i błędy niewidoczne (stopka, ~4461 px) | **naprawione** — toast nad paskiem dolnym |
| 5 | Błąd „odhacz laboratorium" przewijał do złego (zablokowanego) rozdziału | **naprawione** — prowadzi do właściwego |
| 6 | Po zaliczeniu rozdziału — na górę strony zamiast do następnego rozdziału | **naprawione** |
| 7 | Prośba o klucz API → odpowiedź o eksporcie zamiast odmowy | **naprawione** — jawna odmowa |
| 8 | Literówki („odc", „ledzer") → „nie mam tego w źródłach" | **naprawione** — tolerancja ±1 znak |
| 9 | „Co potrafisz?" dawało identyczną odpowiedź jak „Jak używać?" | **naprawione** — osobna gałąź |
| 10 | „Rytuał DZIEŃ jest **zgrane** na zielono" | **naprawione** |
| 11 | Karta LOCK ucinała listę braków do 3 bez słowa o reszcie | **naprawione** — 4 + „…i jeszcze N" |
| 12 | `❯❯ Zapytaj Hermesa` (podwójny szewron z CSS) | **naprawione** |

### Do zrobienia — w kolejności ważności

**P2 — pierwsze wejście (dotyczy telefonu)**
Pasek zakładek na pierwszym wejściu jest poza ekranem: telefon ~1080 px, desktop 1199 px
(okno 844 px). Karta powitalna zajmuje 543 px na telefonie. Złagodzone dziś przyciskiem
„❯ Przejdź do TERAZ — jeden krok" w karcie powitalnej, ale to nadal kompromis.
Propozycja: po pierwszym zamknięciu karty powitalnej pokazywać ją zwiniętą do jednej linii,
a sekcję „JAK TO ZROBIĆ NA TWOIM SYSTEMIE" schować w rozwijane `<details>`.

**P2 — Hermes bez modelu nie odpowie na pytanie spoza kursu**
Teraz uczciwie odmawia. Jeśli chcesz pytać o cokolwiek, trzeba podłączyć model:
`ACADEMY_HERMES_BASE_URL`, `ACADEMY_HERMES_MODEL`, `ACADEMY_HERMES_API_KEY` **na VPS**
(zmienne środowiskowe vaulta, nie w repo). Kod nie wymaga wtedy żadnej zmiany.
Warto podnieść limit dzienny i sprawdzić koszt — dziś 200 pytań/dzień.

**P3 — powrót po przerwie ląduje na ostatniej zakładce**
Wracasz po dniu przerwy, a aplikacja otwiera np. DSAAS. Skoro sytuacja się zmieniła
(zaległy dzień → LOCK), sensowniej wylądować na DZIEŃ albo TERAZ.

**P3 — rytuał dnia jest ciężki**
13 checkboxów + 2 linie tekstowe do zamknięcia dnia. Panel DZIEŃ mówi prawdę o brakach,
ale nie ma jednego „domknij rytuał". Warto rozważyć tryb skrócony (rano: 3 pozycje).

**P3 — checkboxy zablokowanych rozdziałów są klikalne**
Rozdział pokazuje LOCK, ale jego kroki labu można odhaczać. Nie psuje danych,
ale uczy złego nawyku. Propozycja: `disabled` + komunikat, dlaczego.

**P3 — frustracja nie jest obsłużona**
„to gówno nic nie działa" → sucha odmowa. Kontroler mógłby odpowiedzieć: rozumiem +
„powiedz, co dokładnie nie działa, albo zapytaj »co dalej«".

**P3 — biblioteka jest gęsta**
NARZĘDZIA ~19,9 tys. znaków, DSAAS ~45,8 tys. znaków na jednej zakładce. To zamierzone
(biblioteka, nie lektura), ale warto liczyć się z tym, że z telefonu nikt tego nie przeczyta
liniowo — i tak było projektowane.

---

## 4. Jak tego używać (krótko, dla mnie samego za tydzień)

1. **TERAZ** — jedno zadanie. Nic więcej. Karta „TERAZ ROBISZ TYLKO TO" u góry pokazuje
   ten sam kawał, więc nie musisz szukać.
2. **HERMES** — pytaj, gdy stoisz: „co dalej", „gdzie jestem", „dlaczego zablokowane",
   „wytłumacz ODCS". Nie zapisuje niczego.
3. **DZIEŃ** — rano i wieczorem. Bez zielonego rytuału następny rozdział jest LOCK.
   Jeśli lista braków jest długa, panel DZIEŃ pokazuje je wszystkie z regułą.
4. **WORKFLOW / NARZĘDZIA / DSAAS** — biblioteka. Wchodzisz po konkret, nie „poczytać".
5. Zainstaluj na telefonie z **menu → Zainstaluj aplikację**, nie „Utwórz skrót" —
   skrót nie dostaje powiadomień przy zamkniętej aplikacji.

---

## 5. Dowód, że te defekty nie wrócą

Nie wystarczy naprawić — trzeba zapewnić, że nikt tego nie cofnie „przy okazji".

- `scripts/validate-academy-export.py` ma 12 nowych guardów (D1–D11) i celują w **konstrukcje
  kodu**, nie w napisy: wywołanie `alignPanelToNav` w `activateTab`, kolejność gałęzi
  (odmowa sekretu przed eksportem, „co potrafisz" przed „jak używać"), użycie `hermesFuzzyHit`
  w dopasowaniu słownika.
- `scripts/mutation-test-fala-d.py` **cofa każdą naprawę pojedynczo** i sprawdza, czy walidator
  to złapie. Wynik: **19/19 mutacji złapanych, 0 przepuszczonych, plik zawsze przywrócony**.

Dwie z tych mutacji wykryły w trakcie pracy, że **moje własne guardy były dekoracją**
(sprawdzały obecność napisu zamiast konstrukcji). Dopiero po wzmocnieniu złapały defekt.
To jest właśnie powód, dla którego mutation test istnieje.

Uruchomienie: `python scripts/mutation-test-fala-d.py`

---

## 6. Czym ten test NIE jest
- Nie testowałem z prawdziwym modelem językowym (tylko lokalny silnik + wcześniejsza atrapa dostawcy).
- Nie testowałem na prawdziwym telefonie — emulacja 390×844 z `pointer:coarse`. Instalacja
  WebAPK zależy od przeglądarki i musi być potwierdzona na Twoim urządzeniu.
- Nie testowałem eksportu do Kokpitu ani wysyłki push (wymaga HTTPS i zgody).
- Oceny „ładne/brzydkie" są subiektywne — mierzone były tylko liczby podane wyżej.
