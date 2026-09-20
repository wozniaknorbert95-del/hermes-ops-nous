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

Stan w chwili pisania handoffu: **nie zdeployowano** (Zasada 11 — deploy tylko na GO
Dowódcy; zmiana za PR i za CI `academy-gate`). Później Dowódca dał GO: Fala I, wieczór
i fix TERAZ są na produkcji — patrz „Domknięcie" niżej.

---

## Domknięcie tej samej sesji — TERAZ: obietnica bez wykonania

Zgłoszenie Dowódcy (po deployu Fali I, już na telefonie): *na TERAZ nie ma checkboxów
labu ani przycisku „Zalicz rozdział", a tekst każże je klikać*.

**Co było naprawdę:** karta TERAZ pokazywała bieżący krok jako **tekst**. Przy komplecie
odhaczonych kroków pisała „Wszystkie kroki odhaczone — zostaje jedno kliknięcie:
«Zalicz rozdział»", a przycisku na tym ekranie nie było. Bindowanie i re-render już
istniały (`bindDataInputs` / `bindDynamic` / `afterDataChange`) — kod czekał na te
kontrolki, gałąź `currentTab()==='now'` w `renderNowTab()` była martwa. Instrukcja
„Pierwsze 30 sekund" mówi „Odhacz laboratorium → zalicz rozdział" na TERAZ, a TERAZ
odsyłała do WORKFLOW: najczęstsza akcja całej Akademii w dwóch przeskokach zakładek.

**Naprawa:** `renderNowTab()` renderuje checkboxy wszystkich kroków (`data-k`) i przycisk
`data-pass` na miejscu. Przycisk jest `disabled`, dopóki kroki zostały, i sam mówi ile
(„Zalicz rozdział A1 — zostało kroków: 2"); po ostatnim kroku odblokowuje się w miejscu.
Stary przycisk zostaje jako drugorzędny „Cały rozdział: pliki i reguły".

### Lekcja z mutacji — ważniejsza niż sam fix

Mutacja I15 („usuń `data-k` z TERAZ") **przechodziła**, choć kod, który miał zniknąć,
nie zniknął. Anchor `data-k="'+esc(k)+'"` występuje w **dwóch** funkcjach
(`renderChapterCard` i `renderNowTab`) — `replace()` trafiał w pierwszą, więc mutacja
„była łapana" przez guard na kartę rozdziału, a karta TERAZ zostawała nietknięta.
To był błąd **mojego narzędzia**, nie kodu — i dokładnie ten typ błędu, który daje
fałszywe „wszystko zielone".

Zasada na przyszłość: **anchor mutacji musi nieść prefiks swojej funkcji.** Każda
mutacja ma teraz w anchorze fragment specyficzny dla `renderNowTab` (albo dla
`renderChapterCard` — nigdy wspólny). Karta rozdziału w WORKFLOW, jako jedyna inna
droga do odhaczenia kroku, ma własny guard. Przed naprawą: 30/31. Po: 32/32.

### Weryfikacja (Chrome, ten sam origin co vault, realny `localStorage`)

| Krok | Zmierzone |
| --- | --- |
| odhaczenie 3 kroków | `A1l1=true, A1l2=true, A1l3=true` — wszystko na TERAZ, 0 przeskoków |
| przycisk w trakcie | `disabled`, etykieta sama liczy: „zostało kroków: 2" → „: 3" |
| po ostatnim kroku | `disabled` zdjęty **w miejscu**, bez przeładowania |
| klik „Zalicz rozdział A1" | `A1_pass=true`, karta sama przeszła na A2, nagłówek „25 rozdziałów" |
| DOM | 0 duplikatów kluczy `data-k` (brak podwójnego bindowania) |
| konsola | `errors: []`, `warns: []` |

Bramka przed commitem: walidator PASS, vault PASS, mutacje **87/87**
(0: 10/10, D: 19/19, E: 26/26, I: 32/32).

### Produkcja

PR [#23](https://github.com/wozniaknorbert95-del/akademia/pull/23) → CI `academy-gate`
PASS → squash na `main` (`49807cb`) → deploy. Dowód, że na produkcji leży **dokładnie
ten** plik: `sha256(DASHBOARD.html)` lokalnie == na VPS == w tym, co leci **po HTTPS**
(`7a9d9e95…`). Vault: `llm: true, model: deepseek-flash`. Instalacja PWA bez zmian:
`manifest=200 ikona512=200 html_bez_hasła=401`.

### Świadomie zostawione

* Fraza „Wszystkie kroki odhaczone — zalicz rozdział …" żyje dalej w **lepkim karcie**
  (górny pasek, `renderNowCard`). To nie obietnica bez wykonania: jej przycisk to
  „Przejdź do rozdziału A1" i prowadzi do karty w WORKFLOW, gdzie checkboxy i przycisk
  są. Etykieta mówi wprost, że to nawigacja.
* Sieć na telefonie: potwierdzenie „na oko" Dowódcy, nie pomiar.

### Dług narzędziowy (zostaje otwarty)

`gh pr create` z **cudzysłowem w tytule** wywala się w PowerShell 5.1 (argumenty do
natywnego exe gubią wewnętrzne `"`) — pierwszy PR „nie powstał", a `gh` wypisał pomoc
zamiast błędu. Obejście: tytuł bez `"` albo `--body-file`. To samo dotyczy `ssh`
z zagnieżdżonymi cudzysłowami — działa dopiero skrypt przez `base64 -d | tr -d '\r' | sh`
(pamiętaj o `\r`, inaczej `set -e` czyta się jako `set -e\r`).
