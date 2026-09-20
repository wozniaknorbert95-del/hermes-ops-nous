# AUDYT UX/UI — Akademia OS

Data: 2026-09-20 · Audytor: agent (Cursor) na zlecenie Dowódcy
Zakres: cała Akademia (6 zakładek), instalacja na telefon, czat z Hermesem, backend vaulta
Wejście: zgłoszenia Dowódcy — „nie da się pobrać, tylko skrót", „gdzie czat?", „czy to wgl ma sens?"

---

## 0. Werdykt w trzech zdaniach

**Ma sens — ale nie dla „użytkownika w ogóle", tylko dla jednego konkretnego człowieka:
Dowódcy z ADHD, któremu trzeba pokazać JEDEN następny kawał.** Cała reszta (WORKFLOW, NARZĘDZIA,
DSAAS) jest biblioteką, do której wchodzi się świadomie po konkret, i tak właśnie działa — nie
jest to wada, jest to decyzja projektowa, która się broni.

Przed tym audytem Akademia miała **trzy realne defekty blokujące** (nie dało się jej zainstalować
z telefonu, nie było czatu z Hermesem, czat nie był wykrywalny z ekranu startowego) plus **dwa
defekty ciche** (10× 404 w konsoli i 30 zamiast 2 żądań do GitHub API przy każdym starcie) oraz
**306 elementów klikalnych mniejszych niż 44 px** — czyli na telefonie, w który Dowódca celuje,
nie dało się wygodnie trafić palcem.

Po naprawach: **wszystkie bramki zielone i zmierzone** (tabela w §2), a nie obiecane.

---

## 1. Co było zepsute → co jest teraz (z dowodami)

| # | Defekt | Dowód „przed" | Dowód „po" |
|---|--------|----------------|-------------|
| 1 | **Instalacja PWA dawała tylko skrót** | `sw.js` bez handlera `fetch` (Chrome przestaje promować instalację → menu proponuje „Utwórz skrót"), a `manifest.webmanifest` i `/icons/` były za Basic Auth (WebAPK nie pobierze ich bez poświadczeń) | nginx: manifest **200**, ikona-512 **200**, `DASHBOARD.html` bez hasła **401**; na emulowanym Androidzie strzela `beforeinstallprompt` i pojawia się przycisk „Zainstaluj Akademię" |
| 2 | **Czat z Hermesem nie istniał** | Hermes był panelem read-only; brak endpointu, brak UI rozmowy | `POST /hermes/chat` + `GET /hermes/status` w vaulcie; UI czatu w HERMES; pytanie z **prawdziwej klawiatury** zwraca: `Postęp: 0% — 0 z 26 rozdziałów, zostało 26 · 80 kroków lab · DZIEŃ bez blokady` |
| 3 | **Czatu nie dało się znaleźć** | zakładka TERAZ nie miała żadnego odnośnika do rozmowy — dokładnie to zgłosił Dowódca („gdzie czat?") | sekcja **„❯ Zapytaj Hermesa"** na TERAZ z 4 pytaniami; kliknięcie przełącza na HERMES i **od razu zadaje pytanie** (zmierzone: `tabPo: HERMES`, odpowiedź przyszła) |
| 4 | **10× 404 w konsoli** | przy każdym starcie ~10 równoległych zapytań do GitHub API o `dsaas-platform-main`, o którym **wiemy**, że jest prywatne | **30 → 2 żądania** (1× repo + 1× issues), **404 → 0**, `console errors → 0` |
| 5 | **306 elementów klikalnych < 44 px** | pomiar przy 390×844, `pointer:coarse` — przyciski słownika 34 px, szybkie akcje 34 px, `<summary>` 21 px, etykiety 19–21 px | **0 poniżej 44 px** na wszystkich 6 zakładkach; layout nie pęka (overflow 0 px) |
| 6 | **Czat mógł wisieć bez końca** | brak zegara po stronie klienta — vault czekał na dostawcę do 45 s, użytkownik patrzył w zamrożone „pisze…", przycisk wyłączony, Enter milczy | watchdog **20 s**: czat sam wraca, odpowiada silnik lokalny i mówi wprost: `dostawca milczał ponad 20 s`; przycisk znów aktywny |
| 7 | **5 kliknięć „Wyślij" = 5 pytań do modelu** | brak guardu na czas odpowiedzi | zmierzone: **5 kliknięć → 1 wysłana wiadomość** (limit dzienny i koszt chronione) |

---

## 2. Bramki — zmierzone, nie obiecane

| Bramka | Próg | Wynik |
|---|---|---|
| axe-core 4.10.2 (6 zakładek) | 0 critical / 0 serious | **0 naruszeń w ogóle** (critical 0 · serious 0 · moderate 0 · minor 0) |
| Błędy w konsoli | 0 | **0** |
| Sieć 4xx/5xx | 0 | **0** |
| Layout collapse przy 390 px | 0 | **0** na wszystkich zakładkach |
| Cele dotykowe < 44 px | 0 | **0** |
| `validate-academy-export.py` | PASS | **PASS** |
| `test_progress_vault.py` | PASS | **PASS** (m.in. auth czatu, odrzucenie wstrzyknięcia roli `system`, zejście na silnik lokalny, dzienny sufit, „czat nie dotyka postępu", brak wycieku klucza) |
| Mutacje guardów walidatora | wszystkie złapane | **11/11** |
| Mutacje testów vaulta | wszystkie złapane | **6/6** |

> Dlaczego mutacje: guard, który **nie potrafi paść**, jest dekoracją. Pierwsza wersja moich
> guardów sprawdzała obecność słowa w całym pliku — mutacja samego komentarza przechodziła
> niezauważona. Dlatego guardy przepisałem na **konstrukcje kodu**, a każdy z nich udowodniłem
> mutacją. To samo zrobiłem z testami vaulta.

---

## 3. Co zostaje nieidealne (uczciwie)

1. **axe skanuje tylko widoczną treść.** Treść w zwiniętych `<details>` (instrukcje narzędzi,
   onboarding) nie została przeskanowana — przy rozwijaniu warto powtórzyć.
2. **Linki inline w zdaniu mają cel < 44 px — świadomie.** WCAG 2.5.8 wyłącza je z wymogu
   (wyjątek „inline"), a rozdmuchanie ich do 44 px rozsypałoby akapity. Kontrolki samodzielne
   (przycisk, `summary`, etykieta, wiersz listy) są naprawione.
3. **`/hermes/status` odpowiada anonimowo**, ale tylko na loopbacku i za Basic Auth nginx.
   To świadoma decyzja (jak `/push/public-key`): sonda nie zawiera sekretu i nie wydaje pieniędzy.
   Test pilnuje mocniejszej własności — **zero wycieków** w treści odpowiedzi.
4. **Pomiar był na emulacji Chrome (Pixel 7), nie na fizycznym telefonie.** Ten sam silnik, ale
   realne urządzenie może się różnić — pierwsza instalacja na telefonie to nadal najlepszy test.
5. **Hermes na darmowym modelu będzie wolniejszy** niż silnik lokalny (2 s). Sufit 200 pytań/dobę.
6. **Bateria scenariuszy** objęła: świeży start, zaległy rytuał (LOCK), kurs zamknięty (26/26),
   dostawca nieosiągalny, dostawca wiszący, długi tekst (5000 znaków), 5× szybkie kliknięcia,
   Enter/Shift+Enter, praca z klawiatury. Nie objęła: dwóch osób na tym samym koncie, bardzo
   wolną sieć (3G), trybu offline od pierwszego wejścia.

---

## 4. JAK TEGO UŻYWAĆ (instrukcja)

### 4.1 Instalacja na telefonie (to była Twoja pierwsza skarga)

**Android (Chrome):**
1. Wejdź na Akademię i **odczekaj kilka sekund** — Chrome sprawdza, czy witryna nadaje się do instalacji.
2. W zakładce **HERMES** zobaczysz panel **APLIKACJA** z przyciskiem **„Zainstaluj Akademię"**. Kliknij go.
3. Jeśli przycisku nie ma: menu **⋮** → **„Dodaj do ekranu głównego"** → wybierz **„Zainstaluj aplikację"**.
4. **Nie wybieraj „Utwórz skrót"** — to zwykły skrót: bez powiadomień przy zamkniętej aplikacji i bez pełnego ekranu.

**iPhone (Safari):** Udostępnij (kwadrat ze strzałką) → **„Dodaj do ekranu początkowego"**. iOS
nie ma przycisku „Zainstaluj" — to normalne, ikona zachowa się jak aplikacja.

**Dlaczego to ważne:** powiadomienia przy zamkniętej aplikacji działają **wyłącznie** z zainstalowanej
PWA. Skrót ich nie dostanie.

### 4.2 Rozmowa z Hermesem — dwie drogi

- **Szybka:** zakładka **TERAZ**, sekcja **„❯ Zapytaj Hermesa"** → klikasz pytanie, Akademia
  przełącza się na HERMES i **sama je zadaje**.
- **Pełna:** zakładka **HERMES** → pole „Twoje pytanie do Hermesa" → **Enter** wysyła
  (Shift+Enter = nowa linia).

**O co warto pytać:** `Co dalej?` · `Gdzie jestem?` · `Dlaczego zablokowane?` · `Jak używać?` ·
`Co potrafisz?` · `Instalacja na telefonie` · i wprost o pojęcia: `ODCS`, `HITL`, `ledger`, `R7`,
`Cedar`, `RLS`, `objective`, `MCP`, `budżet złożoności`.

**Jak czytać odpowiedź:** pod odpowiedzią jest zdanie prawdy —
`lokalny silnik` = odpowiadałem z faktów o kursie, bez modelu LLM (brak klucza / brak łączności /
dostawca milczał). Hermes **nigdy** nie udaje, że coś zrobił: jest read-only, nie zapisuje postępu,
nie merguje, nie deployuje. Rozmowa żyje w tej sesji przeglądarki i **nie wchodzi do eksportu**.

### 4.3 Codzienny rytuał (tak to ma działać)

1. **TERAZ** — robisz **jeden** kawał. Nic więcej. Odhaczasz laboratorium, zaliczasz rozdział.
2. **DZIEŃ** — rytuał rano/wieczorem. Bez zielonego rytuału następny rozdział jest **LOCK**.
   To nie kara, to bezpiecznik: rozdział bez domkniętego dnia wraca jako dług.
3. **WORKFLOW / NARZĘDZIA / DSAAS** — biblioteka. Wchodzisz świadomie, po konkret.
4. **HERMES** — kontroler: mówi, co dalej, tłumaczy pojęcia, pokazuje stan.

### 4.4 Jak włączyć prawdziwy model (np. DeepSeek) — bez dotykania kodu

Na VPS, w `/etc/akademia/hermes.env` (chmod 600 — **klucz nigdy nie trafia do repo ani do przeglądarki**):

```
ACADEMY_HERMES_BASE_URL=https://api.deepseek.com/v1
ACADEMY_HERMES_MODEL=deepseek-chat
ACADEMY_HERMES_API_KEY=...twoj-klucz...
ACADEMY_HERMES_DAILY_CAP=200
```

Przełączenie darmowy ↔ DeepSeek to zmiana tych zmiennych i restart vaulta — **zero zmian w kodzie**.
Bez klucza czat nadal działa (silnik lokalny), więc nie da się go „zepsuć brakiem konfiguracji".

---

## 5. Co bym WYCIĄŁ, a czego NIE dodawać

- **Nie dodawać siódmego działu** — sześć jest domknięte i policzalne.
- **Nie dodawać drugiego „▶ TERAZ"** — jeden „teraz" albo człowiek z ADHD zaczyna negocjować z listą.
- **Nie iframe'ować Akademii w Kokpicie** — to ma być osobne, ciche miejsce.
- **Nie dawać Hermesowi prawa zapisu** — read-only jest jego największą zaletą, nie ograniczeniem.

---

## 6. Plan wykonania (dla porządku — zrealizowany)

| Fala | Zakres | Stan |
|---|---|---|
| A | Instalacja PWA: przyczyna (handler `fetch` + publiczny manifest i ikony), fix, deploy, dowód 200/200/401 | ✅ |
| B1 | Backend czatu: `POST /hermes/chat`, `GET /hermes/status`, dostawca za konfiguracją, klucz tylko na VPS, dzienny sufit | ✅ |
| B2 | Silnik lokalny Hermesa: odpowiedzi z faktów (stan, DZIEŃ, reguły, pliki) + fallback offline | ✅ |
| B3 | UI czatu w HERMES: transkrypt, input, szybkie akcje, status mózgu, stany błędu + **wejście z TERAZ** | ✅ |
| B4 | Guardy walidatora (11/11 mutacji) + testy vaulta dla czatu (6/6 mutacji) | ✅ |
| C1 | Ten audyt: axe, konsola, sieć, mobile, bateria scenariuszy, werdykt, instrukcja | ✅ |
| C2 | Naprawy z audytu: 404 → 0, 30 → 2 żądania, 306 → 0 celów dotykowych, watchdog czatu | ✅ |
| D | Deploy na VPS + smoke public | ✅ |

**Nie testowałem na fizycznym telefonie** — pierwsza próba instalacji na Twoim urządzeniu jest
ostatnim brakującym dowodem. Jeśli w menu nadal zobaczysz tylko „Utwórz skrót", zgłoś to: to błąd
Akademii, nie Twój.
