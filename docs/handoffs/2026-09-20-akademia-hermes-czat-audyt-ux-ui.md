# Handoff — Akademia: czat z Hermesem + audyt UX/UI

**Data:** 2026-09-20
**Repo:** `akademia`
**Sesja:** instalacja PWA (domknięcie) + czat z Hermesem (backend, UI, wykrywalność) + audyt UX/UI z werdyktem
**Poprzedni handoff:** [`2026-09-20-akademia-terminal-ux-fala-3-4.md`](2026-09-20-akademia-terminal-ux-fala-3-4.md)
**Plan:** [`docs/ops/AUDYT-UX-UI-2026-09-20.md`](../ops/AUDYT-UX-UI-2026-09-20.md)
**Branch / PR:** `feat/hermes-chat-ux-audit` → [PR #17](https://github.com/wozniaknorbert95-del/akademia/pull/17)
**Status:** czat działa, audyt domknięty z werdyktem, **deploy wykonany na GO Dowódcy** i zweryfikowany na produkcji.

---

## Wejście (trzy zgłoszenia Dowódcy)

1. „odpaliłem akademie w przeglądarce telefonu w celu pobrania, ale nie da się pobrać, można jedynie utworzyć skrót"
2. „w jaki sposób mam się komunikować z Hermesem? gdzie czat? przecież to ma być mój kontroler i nauczyciel"
3. „audyt UX/UI na ile spełnia swoje zadania i jak tego używać, czy to wgl ma sens dla użytkownika"

---

## Co zrobione

| Fala | Zakres | Stan |
|---|---|---|
| A | PWA: handler `fetch` w `sw.js` + publiczny manifest i ikony w nginx | ✅ |
| B1 | Backend czatu w vaulcie: `POST /hermes/chat`, `GET /hermes/status`, dostawca za konfiguracją, klucz tylko na VPS, dzienny sufit | ✅ |
| B2 | Silnik lokalny Hermesa (fakty o kursie + stan) i fallback offline | ✅ |
| B3 | UI czatu w HERMES + **wejście „Zapytaj Hermesa" na TERAZ** | ✅ |
| B4 | Guardy walidatora i testy vaulta, oba udowodnione mutacjami | ✅ |
| C1 | Audyt UX/UI: axe, konsola, sieć, mobile, bateria scenariuszy, werdykt, instrukcja | ✅ |
| C2 | Naprawy z audytu (szczegóły niżej) | ✅ |
| D | Deploy na VPS + smoke public | ✅ |

## Defekty znalezione i naprawione (z dowodami)

| Defekt | Przed | Po |
|---|---|---|
| 404 w konsoli — pytaliśmy GitHub API o repo, o którym **wiemy**, że jest prywatne | 10× 404 | **0** |
| Duplikaty żądań — flaga `GH_LOADING` stała **po** `fetch`, nie przed | 30 żądań | **2** |
| Cele dotykowe na telefonie (390×844, `pointer:coarse`) | **306** < 44 px | **0** |
| Czat przy wiszącym dostawcy | zamrożone „pisze…" bez końca | watchdog **20 s** → silnik lokalny, uczciwy komunikat |
| Czatu nie dało się znaleźć z ekranu startowego | brak wejścia na TERAZ | sekcja z 4 pytaniami → przełącza i **sama pyta** |

> Dwie pułapki po drodze, obie złapane pomiarem, nie „na oko":
> **(1)** pierwsza poprawka duplikatów nie działała, bo flaga stała po odpaleniu żądań — wykryło to dopiero liczenie żądań w przeglądarce;
> **(2)** pierwsza wersja guardów walidatora sprawdzała **podłańcuch w całym pliku**, więc mutacja komentarza przechodziła niezauważona — dopiero test mutacyjny pokazał, że **5 z 8 guardów było dekoracją**. Przepisane na konstrukcje kodu, potem 11/11.

## Bramki (zmierzone)

- axe-core 4.10.2, **6 zakładek**: 0 naruszeń (critical 0 · serious 0 · moderate 0 · minor 0)
- console errors **0** · sieć 4xx/5xx **0** · layout collapse przy 390 px **0**
- cele dotykowe < 44 px **0**
- `validate-academy-export.py` **PASS** · `test_progress_vault.py` **PASS**
- mutacje guardów walidatora **11/11** · mutacje testów vaulta **6/6**
- bateria: świeży start · zaległy rytuał (LOCK) · kurs 26/26 · dostawca nieosiągalny · dostawca **wiszący** · tekst 5000 znaków · 5× szybkie klikanie (1 wysyłka) · Enter/Shift+Enter · prawdziwa klawiatura

## Smoke produkcyjny (po deployu, na wdrożonej wersji)

```
manifest.webmanifest        200
icons/icon-512.png          200
DASHBOARD.html (bez hasła)  401
/hermes/status              {"ok": true, "llm": false, "model": "", "used_today": 0, "daily_cap": 200}
POST /hermes/chat (Basic)   {"source": "local", "reason": "not_configured", "reply": ""}
POST /hermes/chat (anonim)  401
GET  /progress   (anonim)   401
klucz LLM na VPS            brak — czat odpowiada silnikiem lokalnym
```

## Czego świadomie **nie** zrobiłem

- **Nie wrzuciłem klucza LLM na VPS.** Czat działa na silniku lokalnym; podłączenie DeepSeeka to dwie zmienne w `/etc/akademia/hermes.env` (klucz nigdy nie trafia do repo ani do przeglądarki).
- Nie dodałem siódmego działu, drugiego „TERAZ", nie iframe'owałem Akademii w Kokpicie.
- Nie ruszałem `workflow-lab` ani `dsaas-platform-main`, nie zmieniałem schematu eksportu.
- Nie commitowałem wprost do `main` — praca siedzi na `feat/hermes-chat-ux-audit` (PR #17), **mergowanie zostawiam Dowódcy**.

## Co zostaje nieidealne (uczciwie, z raportu)

1. **Fizyczny telefon nietknięty** — pomiary były na emulacji Chrome (Pixel 7). Pierwsza instalacja na prawdziwym urządzeniu jest ostatnim brakującym dowodem.
2. axe skanuje tylko widoczną treść — rzeczy w zwiniętych `<details>` nie były sprawdzane.
3. Linki inline w zdaniu zostają < 44 px **celowo** (wyjątek WCAG 2.5.8); naprawione są kontrolki samodzielne.
4. `/hermes/status` odpowiada anonimowo na loopbacku za Basic Auth nginx — świadoma decyzja (jak `/push/public-key`); test pilnuje **zera wycieków** w treści.
5. Nie objęte: dwie osoby na jednym koncie, sieć 3G, tryb offline od pierwszego wejścia.
6. **Repo nie ma CI** (`.github/workflows` nie istnieje) — bramki działają tylko lokalnie. Największa luka systemowa, nie ta sesja.

## Następny krok (jeden TERAZ)

**Dowódca na fizycznym telefonie: Chrome → menu ⋮ → „Zainstaluj aplikację".** Jeśli nadal widać
tylko „Utwórz skrót" — zgłosić, to błąd Akademii, nie użytkownika (raport §4.1 ma ścieżkę diagnozy).

Dopiero potem (osobną decyzją): merge PR #17 i ewentualne podłączenie klucza DeepSeek.

## Pliki tej sesji

- `DASHBOARD.html` — czat, wejście z TERAZ, watchdog, poprawki mobilne, cache GitHub API
- `host/progress_vault.py` — `/hermes/chat`, `/hermes/status`, silnik promptu, dzienny sufit
- `scripts/validate-academy-export.py` — guardy czatu, PWA, celów dotykowych, klucza API
- `scripts/test_progress_vault.py` — testy czatu + kanarek na wyciek klucza
- `docs/ops/AUDYT-UX-UI-2026-09-20.md` — raport z audytu (werdykt, dowody, instrukcja)
- ten handoff
