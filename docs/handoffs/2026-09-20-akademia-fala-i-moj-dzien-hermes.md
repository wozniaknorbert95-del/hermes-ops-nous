# Fala I — „Mój dzień" robi Hermes (deterministyczny rdzeń)

Data: 2026-09-20 · repo: `akademia` · gałąź: `feat/fala1-moj-dzien-hermes`
Zakres: Fala 1 z `docs/ops/PLAN-HERMES-NADZORCA-NAUCZYCIEL-2026-09-20.md`

Cel z planu: **2 tapnięcia, 0 wpisywania.** Hermes przygotowuje, Dowódca zatwierdza.
Rdzeń ma działać **bez LLM i bez internetu** — dlatego werdykt o rytuale jest policzalny,
a model służy tylko do sformułowań.

## Co powstało

| Element | Plik | Rola |
| --- | --- | --- |
| `morning_brief(progress, today_hint)` | `host/progress_vault.py` | JEDNO źródło prawdy o rytuale (czysta funkcja, zero sieci) |
| `GET /hermes/morning?today=YYYY-MM-DD` | `host/progress_vault.py` | Za `authorized()`, read-only |
| `morning_brief_of` → import | `scripts/push-send.py` | Push 07:00 przestał mieć własną kopię reguły |
| `morningBriefLocal()` / `fetchMorningBrief()` / `renderDayBrief()` / `approveDay()` / `dayUntouched()` / `autoStaleResolve()` | `DASHBOARD.html` | Mirror offline + render + JEDEN zapis |
| `<details class="manual-ritual">` | `DASHBOARD.html` | 13 checkboxów schowanych — rytuał przestał być formularzem |

## Trzy defekty znalezione przez czytanie, nie przez guardy

To najważniejsza część tego handoffu. Walidator był **zielony** przez cały czas —
te trzy rzeczy znalazłem, czytając odpowiedź vaulta i odpowiedź przeglądarki jak człowiek.

### 1. Jeden dzień, trzy zegary (fałszywy LOCK o północy)

Ten sam `morning_brief` woła **kontener** i **host**:

* kontener: `python:3.12-alpine`, **bez tzdata** → `TZ=Europe/Amsterdam` cicho nic nie robi,
  `time.gmtime()` daje UTC;
* host: timer systemd `OnCalendar=*-*-* 07:00:00` → czas lokalny;
* telefon: `todayISO()` → czas lokalny.

W oknie 00:00–02:00 lokalnie UTC i czas lokalny wskazują **różne daty**. Werdykt
„zaległy dzień" zależałby od tego, gdzie akurat trafił import — u kogoś, kto pracuje
po północy, pojawiałby się LOCK na dzień, który dla niego jest bieżący.

Naprawa: dzień **nie jest czytany z zegara**. Telefon Dowódcy jest autorytetem
(`?today=`), zegar zostaje jako świadomy fallback, a brief **mówi wprost**, którego użył
(`today_source: client|clock`). Niezmiennik pilnowany guardem: **dokładnie jedno miejsce
w vaulcie czyta dzień z zegara** — fallback w `human_today()`. Budżet tokenów
(`hermes_usage_*`) też przeszedł na tę definicję, żeby „dzień" miał jedno znaczenie.

### 2. Przycisk obiecywał wieczór, którego nie podpisywał

`counts` i `approved_by_human` liczyły **wszystkie 10 kroków** (rano + wieczór), a
`proposal` — tylko 5 rano. Skutki widoczne dla użytkownika:

* karta mówiła „Twoje do potwierdzenia: **10**", a przycisk podpisywał 5;
* toast po tapnięciu mówił „**10** potwierdzone przez Ciebie";
* ta sama liczba szła do śladu audytu w `_scratch` — czyli **zapis przypisywał Dowódcy
  zatwierdzenie wieczoru, którego nie złożył**.

Naprawa: `counts` (rano), `counts_evening`, `approved_by_human` (tylko rano),
`evening_to_confirm` (wieczór ma własne zatwierdzenie — inna pora, inne tapnięcie).
Mirror offline liczy identycznie, inaczej offline i online pokazywałyby różne liczby.

### 3. Trzy guardy mierzyły słowo, nie kod

Mutation testing wykrył, że guardy przepuszczały własne mutacje:

* `counts_evening` — słowo występowało też w ciele funkcji, więc usunięcie **pola
  ze zwracanego dyktu** przechodziło;
* `counts_evening` w dashboardzie — słowo zostawało w `renderDayBrief`, więc
  usunięcie pola z mirrora przechodziło;
* „13 checkboxów schowanych" — liczone w całym pliku, a brief Fali 1 sam dodaje
  `<details class="manual-ritual">`, więc próg `>= 2` był spełniony mimo odsłonięcia formularza.

Naprawa: asercje na **kształcie zwracanym** (`"counts_evening": counts_evening`,
`counts_evening:countsEvening`) i pomiar w `renderDay()` przez `fn_body()`, nie w całym pliku.
To ten sam antywzorzec, który złapałem już przy G3 — **trzeci raz**. Guard na słowie
to guard, który za tydzień zostanie wyłączony.

## Dowód (nie „zielone testy")

Gate: `validate-academy-export.py` ✅ · `test_progress_vault.py` ✅ · **22/22 mutacji złapanych**.

Przeglądarka (Chrome, vault na `127.0.0.1:8098`, treść serwowana przez sam vault —
jedno origin, więc to prawdziwy styk, nie makieta):

```
stan przed tapnięciem:  karta „DZIEŃ GOTOWY DO ZATWIERDZENIA — 2026-09-20"
                       „Policzone przeze mnie: 1 · Twoje do potwierdzenia: 4"
                       „Przycisk podpisuje tylko kroki rano (4)."
                       15 elementów ukrytych przez „Ręcznie" (checkVisibility)
po JEDNYM tapnięciu:   rano_zapisane:    [day_teraz, day_linear_proj, day_one_issue,
                                          day_git_clean, day_today_first]
                       wieczor_zapisane: []            ← nietknięty
                       linia_today:      „Today first: Workflow Lab / A1 … — krok 1 z TERAZ"
                       ślad audytu:      verified:[day_teraz] approved:[4 kroki RANO]
                       toast:            „1 policzone przeze mnie, 4 potwierdzone przez Ciebie."
                       karta wraca do:   „Workflow Lab / A1 — Fundament repozytorium"
```

F8 (dzień odpoczynku) — obie gałęzie, zmierzone w przeglądarce:

| Scenariusz | Wynik |
| --- | --- |
| zaległy, **zero śladu pracy** | `day_skipped=2026-09-15`, `lock=false`, karta czysta — **bez kary za przerwę** |
| zaległy, **jest praca** | `lock=true`, „DOKOŃCZ DZIEŃ — 2026-09-15", lista braków — reguła żyje |

Sieć: 0 odpowiedzi 4xx/5xx, 2 żądania na czystym starcie.
P0 z Fali H nadal trzyma: świeże urządzenie stempluje `day_stamp`, ale **nie**
`_local_updated_at` (`stan_poczatkowy: [_scratch, active_tab, day_stamp]`).

## Pułapka pomiarowa — zapisz to

`getBoundingClientRect()` **zwraca pudełko** treści zwiniętego `<details>`, mimo że Chrome
jej nie maluje. Mój pierwszy pomiar ogłosił „formularz nie jest schowany" — fałszywy alarm.
Rozstrzyga dopiero `element.checkVisibility({checkVisibilityCSS:true})` albo
`document.elementFromPoint()`. Nie mierz widoczności bounding boxem.

## Czego jeszcze nie ma (świadomie)

* Fala 2 — nadzorca workflow (deterministyczny rdzeń, GitHub-first, bez Linear).
* Fala 3 — nauczyciel (router-first + pinned fact, NIE pełny RAG).
* Wieczór ma pole `evening_to_confirm` i własne kroki, ale **nie ma jeszcze przycisku**
  zatwierdzenia wieczoru — dziś wieczór zostaje w „Ręcznie".
* `docs/runbooks/AKADEMIA-VPS.md`: warto dopisać sprawdzenie strefy czasowej VPS,
  bo timer 07:00 działa w czasie systemowym hosta.

## Deploy

**Nie zdeployowano.** Zasada 11 — deploy tylko na GO Dowódcy. Zmiana jest na gałęzi,
za PR i za CI (`academy-gate`).
