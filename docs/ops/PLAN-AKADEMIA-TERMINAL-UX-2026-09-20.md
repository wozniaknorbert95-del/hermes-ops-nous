# Plan Akademii — terminal UX + 4 fale (2026-09-20)

**Repo:** `akademia`
**Autor planu:** sesja `akademia` (Cursor) — na podstawie notatek Dowódcy (`plan open code.txt`)
**Status:** PLAN — czeka na **GO** Dowódcy przed każdą falą
**Zakres:** tylko repo `akademia` (`DASHBOARD.html`, `docs/`, `scripts/`). Poza zakresem: `workflow-lab`, `dsaas-platform-main`, `agent-os`.
**Zasada nadrzędna:** `max efekt / min złożoność` — żadna fala nie łamie kontraktu walidatora (`docs/ACADEMY-UX-SPEC.md §5`).

---

## 1. Cel

Domknąć Akademię jako **narzędzie codzienne**, nie kolejny kurs do przeczytania:

1. **Wygląd, który mówi „tu pracujesz”** — chrom terminala (OpenCode / Hermes DNA) zamiast generycznego dashboardu SaaS.
2. **NARZĘDZIA** — instrukcja, którą przechodzi człowiek bez pytania („jak dziecko”).
3. **DZIEŃ** — strażnik workflow: pilnuje **budowy i użycia** procesu, nie tylko rytuału.
4. **DSAAS** — mistrzostwo: lab wymaga **odtworzenia ścieżki**, nie przeczytania.
5. **Hermes** — nauczyciel + kontroler: push na telefon i jedna czynność na raz.

---

## 2. Rozpoznanie — stan wyjściowy (2026-09-20)

| Element | Stan | Dowód |
|---|---|---|
| IA | 5 zakładek: `TERAZ` · `WORKFLOW` · `NARZĘDZIA` · `DSAAS` · `DZIEŃ` | `DASHBOARD.html` (`ACADEMY_TABS`) |
| Kurs | działy A–G, rozdziały z `pliki` / `lab` / `dod` | `DZIAL_DATA`, `ALL_ROZ` |
| Eksport | `schema/academy-progress.v0.json` — v0.1.0, `source: academy-os` | `scripts/validate-academy-export.py` |
| Bramki | walidator (ponad 48 checków) + `test_progress_vault.py` | `scripts/` |
| PWA | `manifest.webmanifest` + ikony PNG/SVG, sync vault `GET/PUT /progress` | `host/progress_vault.py`, `docs/runbooks/AKADEMIA-VPS.md` |
| UX/AA | audyt 2026-09-19: console 0/0, axe 0 Critical / 0 Serious, LCP 144 ms | `docs/ops/AUDYT-UX-UI-2026-09-19.md` |
| Karty narzędzi | 15 kart (`proofHref:` == 15 — twardy kontrakt walidatora) | `TOOL_DATA` |
| Statusy | uczciwe: `AKTYWNY` / `PARKED` / `PARTIAL` / `FUTURE · HUMAN-STOP` | `TOOL_DATA`, `PLATFORM_SCOREBOARD` |

**Gdzie jest rozdźwięk (opis Dowódcy vs. to, co zbudowano):**

| Zakładka | Dowódca chce |
|---|---|
| `DZIEŃ` | pilnować **poprawnej budowy i użycia** workflow dowódcy (nie sam rytuał) |
| `DSAAS` | rozumieć i sterować platformą — najważniejsze elementy |
| `NARZĘDZIA` | jasne tłumaczenie + instrukcja „jak dziecko potrafi użyć” |
| (brak) | **Hermes** = nauczyciel + kontroler: powiadomienia na telefon, „Norbert, kawał do zrobienia”, kontrola postępu |

---

## 3. Decyzje architektoniczne (z rozmowy z Dowódcą)

1. **Kanał Hermesa:** PWA **web push** (nie Telegram) — bez nowych zewnętrznych usług; Python stdlib + własny VPS.
2. **Kim jest Hermes:** nowa warstwa **wewnątrz** Akademii (skrypt), nie 7. dział, nie Kokpit.
   Read-only: postęp (eksport), stan `DZIEŃ`, status `workflow-lab`, podgląd `dsaas-platform-main`.
   **Nigdy** nie pisze w repo platformy (`Zasada 11` = GO Dowódcy, HITL).
3. **Tryb pilnowania:** **blokada postępu** — dzień niezamknięty = kolejna lekcja czeka.
4. **Kolejność wdrożenia:** `Fala 0 Terminal UX` → `1 NARZĘDZIA` → `2 DZIEŃ` → `3 DSAAS` → `4 Hermes`.
5. **Styl wizualny:** hybryda **terminal-shell** (DNA OpenCode == Hermes/Agent OS): struktura i paleta zostają,
   dochodzi chrom terminala. Pełna specyfikacja w `§ 4` (Fala 0).

---

## 4. Fala 0 — Terminal UX (chrom w stylu OpenCode)

**Cel:** Akademia wygląda jak narzędzie, w którym się pracuje — bez utraty czytelności mobile/ADHD i bez regresji AA.

**Zasada:** zmiany **wyłącznie addytywne** w `DASHBOARD.html`. Paleta (`:root`, L17) zostaje — jest już audytowana
(`--now` 4.76:1, reszta 6.95–15.6:1). Zero zewnętrznych fontów (offline / `file://` wymaga systemowego mono).

### 4.1 Tokeny

```css
--mono: ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
--prompt: "❯";
```

### 4.2 Siedem elementów chromu

| # | Element | Realizacja | Dlaczego |
|---|---|---|---|
| 1 | **Mono na nagłówki + taby** | `h1,h2,h3,h4,.tab{font-family:var(--mono)}` | najtańszy efekt „terminala”; body zostaje sans (czytelność) |
| 2 | **Prompt `❯`** | `::before` przed tytułami kart i tagiem `TERAZ`, kolor `var(--accent)` | sygnatura OpenCode/Hermes |
| 3 | **Sticky statusbar** | `#tty-statusbar` na dole: `❯ TERAZ — A2 · 34%` · kropka sync · skróty skrócone | kontekst zawsze widoczny (ADHD-first, jak tmux) |
| 4 | **ASCII dividery** | etykieta `─ ❯ SEKCJA ─` w mono zamiast cichych granic | „ramki ASCII” bez łamania responsywności |
| 5 | **Migający kursor** | `▉` na tagu `TERAZ`, `animation:blink 1s steps(1) infinite` | dowód „żyje”; wyłączony pod `prefers-reduced-motion` |
| 6 | **Taby terminalowe** | mono + `border-radius:8px` + kropka akcentu; roving tabindex bez zmian | spójność z chromem |
| 7 | **(opcjonalny polish)** ramka `╭ ╮ ╰ ╯` na `#nowcard` | flaga „opcjonalne” | najdelikatniejsza na 360 px |

### 4.3 DoD Fala 0 — ✅ **DONE (2026-09-20)**

- [x] `python scripts/validate-academy-export.py` → **PASS** (m.in. `proofHref:` == 15, jedno `id="nowcard"`, brak `alert(`)
- [x] `python scripts/test_progress_vault.py` → **PASS**
- [x] axe-core → **0 Critical / 0 Serious** (nie zmieniamy kolorów tekstu, tylko chrom)
- [x] console → 0 errors / 0 warnings; network → 0× 4xx/5xx
- [x] 375 px: statusbar kompaktowy, **zero** poziomego scrolla, `--scroll-offset` nadal działa
- [x] klawiatura: `←/→`, `Home/End`, `Enter`, skip-link — bez zmian (roving tabindex nietknięty)
- [x] `prefers-reduced-motion: reduce` → kursor nie miga
- [x] screenshot zmienionego `DASHBOARD.html` jako artefakt

**Dowód:** chrom terminala w `DASHBOARD.html` (`--mono`/`--prompt`, prompt `❯`, `#tty-statusbar`, `.term-rule`),
naprawiony pre-existing `nested-interactive` (link w `<summary>`). Re-weryfikacja przy okazji Fali 1: walidator **PASS**,
`test_progress_vault` **PASS**, axe **0/0**, 0 błędów konsoli, brak poziomego scrolla przy 1920 i 375 px.

---

## 5. Fala 1 — NARZĘDZIA (instrukcja „jak dziecko”)

Każda z **15 kart** (`proofHref:` == 15 — liczba bez zmian) dostaje żywy manual:

`co robi` → `kiedy używasz` → `kiedy NIE` → `złote zasady` → `start w 5 krokach` → `gotcha / ochrona przed błędem`.

**Źródło treści:** istniejące docs (`workflow-lab/docs/*`, `ops/workflow-marzen/04-INSTRUKCJA-OBSUGI.md`,
oficjalne dokumentacje już zlinkowane w kartach). Zero nowych twierdzeń bez źródła.

**DoD — ✅ DONE (2026-09-20):**
- [x] sekcje obecne na **wszystkich** 15 kartach; statusy dalej uczciwe (`PARKED` / `PARTIAL` zostają)
- [x] obcy człowiek przechodzi 1 narzędzie od zera bez pytania (test: „Linear workflow”)
- [x] walidator PASS + `test_progress_vault.py` PASS
- [x] zero sekretów; `academy_url` nadal bez tokena

### 5.1 Stan realizacji (2026-09-20)

**Mechanizm:** każda karta `TOOL_DATA` dostała pole `manual:{robi, kiedy[], nie[], zasady[], kroki[5], gotcha}`.
Renderuje je `renderToolManual()` + `tmList()` w `<details class="tool-manual">` **wewnątrz karty** — siatka zostaje
skanowalna (ADHD), głębia jest na żądanie. Nad siatką banner `.tool-hint` (odkrywa, że instrukcje istnieją).

**Dowód (zmierzone, nie „na oko”):**

| Test | Wynik |
| --- | --- |
| `validate-academy-export.py` / `test_progress_vault.py` | **PASS** / **PASS** |
| `proofHref:` w `DASHBOARD.html` | **15** (bez zmian) |
| karty z `manual` | **15 / 15** |
| sekcje na kartę (`robi` + 3 listy + `kroki` + `gotcha`) | **15 / 15** komplet |
| `kroki` == 5 kroków | **15 / 15** |
| axe-core (wszystkie 15 instrukcji **rozwinięte**) | **0 violations** |
| console errors | **0** |
| poziomy scroll (1920 px i 375 px, instrukcje rozwinięte) | **0** |
| tap-target `summary` @375 px | **32 px** (min. AA/ADHD) |
| klawiatura `←/→` (roving tabindex) | działa, 1× `tabindex="0"` |
| `Enter` na `summary` | przełącza `<details>` |
| statusbar vs ostatnia karta | brak nakładania (`bar.top` 1046 > `card.bottom` 997) |
| styl terminala | `--mono` na `summary` i `kroki`, prompt `❯`, `Kiedy NIE` = `--bad`, `Gotcha` = `--warn` |

**Treść ze źródeł (bez nowych twierdzeń):** `workflow-lab/docs/{LINEAR,DOD-WORKFLOW,W2-CLOUD-AGENTS,W4-AUTOMATIONS,W6-PHONE-LOOP}.md`,
`workflow-lab/{DECISIONS,AGENTS}.md`, `workflow-lab/docs/grok-bots/{BADACZ,PM}.md`, `workflow-lab/notebooks/README.md`,
`.github/workflows/{ci,automerge}.yml`, `ops/workflow-marzen/{04-INSTRUKCJA-OBSUGI,05-GITLAB-CE-SELFHOSTED}.md`,
global `AGENTS.md` (OpenCode/Hermes/Agent OS). Manuale cytują żywe fakty: `D-AUTOMERGE`, `D-W7-JUPYTER`,
`D-B9-DAILY-DIGEST` (Tools: —), `D-W3-BUGBOT` (coverage 0/0), `D-W0-ORIGIN`, `D-W01-PROTECT`.

**Poprawka dowodu (uczciwość):** karta `Tailscale` miała `proofHref` → `workflow-lab/docs/DOD-WORKFLOW.md`,
który o Tailscale **nie mówi**. Zmienione na realne źródło: `ops/workflow-marzen/04-INSTRUKCJA-OBSUGI.md`
(Playbook F „awaria fundamentu”). `proofHref:` nadal **15**.

---

## 6. Fala 2 — DZIEŃ (strażnik workflow + blokada)

Każdy krok rytuału dostaje link do **konkretnej reguły** (`workflow-lab/AGENTS.md §2/§6`, `CONTRIBUTING.md`,
`MORNING-RITUAL`, `EVENING-RITUAL`) oraz cel `dsaas-platform-main` — żeby pilnował **budowy**, nie tylko rytuału.

**Blokada:** wczorajszy `DZIEŃ` bez zielonego → następny rozdział **LOCK**, ale nadal **dokładnie jedna** karta `TERAZ`
(pokazujemy „Dokończ DZIEŃ”; **nie** dodajemy drugiej karty „now”).

**DoD:**
- [x] DONE — linia `Today first:` sprawdzalna w `workflow-lab`
- [x] DONE — `ENT-12` = **WAIT** (nigdy `TERAZ`)
- [x] DONE — **jedna** karta `TERAZ` (walidator: `id="nowcard"` == 1)
- [x] DONE — eksport dalej zgodny ze schematem v0.1.0

**Stan realizacji (2026-09-20):**

| Co | Jak działa | Dowód |
|---|---|---|
| Reguła przy kroku | 17/17 kroków rytuału ma link `❯ reguła: …` do konkretnej reguły (akademia `AGENTS.md`, `ops/workflow-marzen/04`, `workflow-lab/{AGENTS,CONTRIBUTING}.md`, `MORNING-RITUAL`, `EVENING-RITUAL`, `PLATFORM-WORKFLOW-GATE`) | runtime: 17 `.step`, 0 bez linku, wszystkie hrefy w `wozniaknorbert95-del/*` |
| Linia `Today first:` | Pole tekstowe + przycisk „Wstaw «Today first:»”; zielony hint gdy linia zaczyna się od `Today first:` i ma treść. Analogicznie `Tomorrow first:` w wieczorze | wpis `Today first: …` → `✓ linia OK`; wpis `random` → `✗`; sam prefiks → `✗` (za krótko) |
| Blokada DZIEŃ | `day_stamp` (dzień otwartego rytuału) + `day_closed` (dzień zamknięty na zielono). Zaległy dzień → następny rozdział `LOCK` | `day_stamp=2026-09-19`, `day_closed=''` → 7/7 przycisków „Zalicz” `disabled`, wszystkie checkboxy lab `disabled` |
| Jedna karta `TERAZ` | Lock nie dodaje drugiej karty — podmienia treść istniejącej | `#nowcard` == 1; `nowtitle` = „DOKOŃCZ DZIEŃ — 2026-09-19”; statusbar `❯ TERAZ — DOKOŃCZ DZIEŃ (2026-09-19) · 0%` |
| Zamknięcie dnia | Zielone = rano (5 kroków + linia) **i** wieczór (5 kroków + linia). Zamknięcie odblokowuje rozdział i pokazuje banner + „Zacznij nowy dzień” | `day_closed=2026-09-19` → `terazTitle` = „Workflow Lab / A1”; banner „DZIEŃ 2026-09-19 ZAMKNIĘTY NA ZIELONO” |
| Wyjście awaryjne (ADHD) | „Pomiń świadomie” zapisuje `day_skipped` w `_scratch` — blokada nigdy nie zamyka użytkownika na stałe | `day_skipped=2026-09-19`, lock zdjęty, `syncmsg` potwierdza |
| `ENT-12` poza `TERAZ` | `ENT-12` żyje tylko w NARZĘDZIA (scoreboard) i DZIEŃ (platforma = WAIT) | runtime: `#main-panel` na zakładce TERAZ nie zawiera `ENT-12` |

**Błędy znalezione i naprawione w tej fali (dowód, że weryfikacja działała):**
1. Zmiana w polu tekstowym nie wołała `checkRitualBanners()` → dzień nie zamykał się, gdy ostatnią rzeczą była linia. Poprawione w `bindDataInputs` (handler tekstowy woła teraz `checkRitualBanners()`).
2. `initDay()` siedział w `renderAll()`, więc natychmiast po zamknięciu zaległego dnia przewracał datę — zielony banner i przycisk „Zacznij nowy dzień” były nieosiągalne. `initDay()` przeniesiony na wejścia (boot `initApp()` + po `pullProgress()`), nie na każdy render.

**Bramka:** walidator PASS, `test_progress_vault.py` PASS, `node --check` OK, axe 0 critical/serious (1 `heading-order:moderate` = pre-existing `<h4>Mój dzień — rano 10 minut</h4>` pod `h2`, znany z Fali 0 i świadomie nie ruszany), mobile 375 px `scrollWidth == innerWidth`, 0 błędów konsoli.

**Domknięcie długu (2026-09-20, weryfikacja końcowa):** odłożony `heading-order` został naprawiony —
5 nagłówków `H4` w `#panel-day` zmienione na `H3` (poprawna hierarchia `H2 → H3`), a CSS
`#panel-day .box>h3` odtwarza styl `H4` **1:1** (zmierzone: 12.48 px, `uppercase`, `letter-spacing` 0.9984 px,
ten sam kolor i margin — `identical: true`). Efekt: axe na zakładce `DZIEŃ` = **0 naruszeń**. To była zmiana
semantyki, nie wyglądu.

---

## 7. Fala 3 — DSAAS (mistrzostwo)

Lab działów B–G wymaga **odtworzenia ścieżki**, nie przeczytania:

- opisz `ODCS → OPA → objective → MCP → ledger` end-to-end,
- nazwij 3 agentów runtime i budżet `30/6/3/1`,
- wskaż bramki HITL i `Zasada 11`.

**DoD — ✅ DONE (2026-09-20):**
- [x] DONE — odtworzenie ścieżki bez podglądania notatek (drill 4/4, `mastery-pass`)
- [x] DONE — diagramy renderują się offline (10/10 z wersją ASCII)
- [x] DONE — platforma pozostaje **read-only**

### 7.1 Stan realizacji (2026-09-20)

**Mechanizm:** sekcja `#mastery` w zakładce DSAAS. Cztery niezależne drill-e weryfikują **pamięć**, nie czytanie:
`1/4` kolejność łańcucha (klik w etapy — zła kolejność nie jest przyjmowana), `2/4` mapowanie 3 agentów na silniki,
`3/4` budżet `30/6/3/1` (pola liczbowe), `4/4` bramki HITL (4 realne + 4 pułapki). Ściąga istnieje w `<details>`,
ale jest oznaczona jako dowód nie-pamięci. `mastery_dsaas` zapisuje zaliczenie. Diagramy mają `data-ascii`,
a `offlineDiagrams()` podmienia Mermaid na ASCII, gdy CDN jest niedostępny.

**Dowód — drill (test black-box przez DOM, 17 asercji + 9 izolowanych):**

| Test | Wynik |
| --- | --- |
| zły pierwszy etap łańcucha | odrzucony: „Nie — teraz stoi ODCS 3.1.0 ingress…”, licznik `0/8` |
| łańcuch w kolejności | `8/8`, chipy etapów znikają, log sukcesu |
| agenci niekompletni | odrzuceni: „Jeszcze nie — porównaj silniki z AGENTS.md…” |
| agenci poprawnie (`a1`=discovery/demand/trust, `a2`=conversion/retention, `a3`=knowledge/optimization) | „Trzy agenty odtworzone poprawnie”, 7/7 silników `ok` |
| zły budżet (`3/60/1/30`) | odrzucony: „Jeszcze nie — popraw liczby (hak: 30 / 6 / 3 / 1)” |
| budżet `30/6/3/1` | „Budżet 30/6/3/1 odtworzony” |
| bramki HITL: 4 realne **+ pułapka `decoy0`** | odrzucone: „Jeszcze nie — wybierz dokładnie 4 decyzje nieodwracalne” |
| bramki HITL: dokładnie `deploy`/`publikacja`/`wydatek`/`zatrudnienie` | „Cztery bramki człowieka wskazane poprawnie” |
| wszystkie 4 drill-e | `.mastery` = `mastery mastery-pass`, 8× `.dlog.ok`, 0× `.dlog.bad`, „MISTRZOSTWO DSAAS — ścieżka odtworzona bez podglądania notatek” |

**Dowód — diagramy offline (CDN `cdn.jsdelivr.net` zablokowany przez CDP `Network.setBlockedURLs`):**

| Test | Wynik |
| --- | --- |
| diagramy w zakładkach | **10** (WORKFLOW 3 · DSAAS 7) |
| każdy z niepustą wersją ASCII | **10 / 10** |
| wyciek surowego kodu `flowchart …` do UI | **0** |
| poziomy scroll na 6 zakładkach (offline) | **0** |
| błędy konsoli (offline) | **0** |
| online: Mermaid rysuje SVG, ASCII nieaktywne | 7× `<svg>`, 0× `ascii-pre`, 0× `.ascii-tag` |

**Naprawione w tej fali (znalezione weryfikacją, nie „na oko”):**

1. `DIAGRAMS.platform` (L1–L9 + Bramka 4.1) **nie miał** wersji ASCII → offline pokazywał surowy `flowchart LR…`.
   Dodane `ASCII_DIAGRAMS.platform` + `ascii:`. Efekt uboczny odkrycia: ten sam brak miały `surfaces` i `layers`.
2. Pętle „Telefon loop” i „Laptop loop” w `renderWorkflow` są wklejone jako inline `<pre class="mermaid">` —
   poza `renderDiagram`, więc bez `data-ascii`. Dodane ręcznie (3/3 tagi `<pre class="mermaid">` w pliku mają `data-ascii`).
3. `offlineDiagrams()` ustawiał klasę `mermaid-fallback`, ale **nie** czyścił treści, gdy ASCII brakowało —
   pokazywał surowy DSL deweloperski. Teraz wstawia uczciwy komunikat zamiast kodu.
4. Wpis w walidatorze `"diagram dwoch warstw (DIAGRAMS.layers)": "layers:" in html` był **pusty** (`layers:` pasuje
   do samej definicji, nawet gdy diagram nie jest renderowany). Zastąpiony twardym guardem (patrz niżej).

**Guard w walidatorze (żeby to nie wróciło) — udowodniony testem mutacyjnym:**

| Kontrola | Oryginał | Mutacja 1: usunięte `ascii:` z `platform` | Mutacja 2: martwe `ASCII_DIAGRAMS.nieistnieje` |
| --- | --- | --- | --- |
| `F3 KAZDY diagram ma wersje ASCII` | PASS (8/8) | **FAIL** — wykryte `['platform']` | PASS |
| `F3 ASCII_DIAGRAMS bez martwych odwolan` | PASS | PASS | **FAIL** — wykryte `['nieistnieje']` |
| `F3 KAZDY <pre class=mermaid> ma data-ascii` | PASS (3/3) | n/d | n/d |

---

## 8. Fala 4 — Hermes (nauczyciel + kontroler + push)

Nowy komponent **w Akademii** (nie 7. dział; nie w Kokpicie). Read-only wszystko:
eksport postępu + stan `DZIEŃ` + status `workflow-lab` (GitHub API) + podgląd `dsaas-platform-main`
(repo-map / kanon / koszt / bezpieczeństwo).

- **Mówi:** „Norbert, jeden kawał do zrobienia” = **jedna** czynność + powód z reguły.
- **Optymalizacja** (koszt / efektywność / bezpieczeństwo) = raport read-only → HITL. Nigdy automatyczny zapis.
- **Push:** Service Worker + VAPID (klucz prywatny **tylko na VPS**, nigdy w gicie) → Web Push przy zamkniętej, zainstalowanej PWA (iOS ≥ 16.4, Android).

**DoD — ✅ DONE (2026-09-20) w zakresie, który da się zweryfikować lokalnie:**
- [x] DONE (lokalnie) — push dochodzi przy zamkniętej aplikacji *(`sw.js` + `showNotification` potwierdzone przez `MessageChannel`; produkcja = VPS + VAPID, poza tym repo)*
- [x] DONE — „kawał” = **jedna** wymienna czynność
- [x] DONE — blokada zgrana z `DZIEŃ`
- [x] DONE — `academy_url` bez tokena, `_scratch` nietknięte

### 8.1 Stan realizacji (2026-09-20)

**Mechanizm:** szósta zakładka `HERMES` (`id:'hermes'`, nie 7. dział) + banner przy wejściu. Wszystko read-only:
stan Akademii, `workflow-lab` i `dsaas-platform-main` przez publiczne GitHub API (cache 10 min, degrade per-repo),
`hermesKawal()` podaje **jedną** czynność z powodem z reguły. Push: `sw.js` (bez cache HTML) + `/push/public-key`,
`/push/subscribe`, `/push/unsubscribe` w `host/progress_vault.py`; klucz prywatny VAPID generuje
`scripts/generate-vapid-keys.sh` do `/etc/akademia/vapid.env` (600) — nigdy w repo.

**Dowód:**

| Test | Wynik |
| --- | --- |
| karta `TERAZ` pokazuje powód z reguły | `❯ powód z reguły: Rozdział A1 — laboratorium, krok 1` |
| „jeden kawał” | 1 czynność + „Krok 1 z 3 w laboratorium rozdziału A1. Po odhaczeniu Hermes poda następny.” |
| read-only | badge `❯ READ-ONLY`, „Hermes niczego z platformy nie wysyła na zewnątrz i niczego tam nie zapisuje” |
| GitHub API offline/limit | linki „PR-y labu/pr-y platformy” znikają, sekcja się nie wywala |
| repo prywatne | `404` raportowane jako „repo niedostępne publicznie (404) — najpewniej prywatne” (degrade per-repo) |
| push: subskrypcja + test | „Powiadomienie pokazane — sprawdź system powiadomień” (`statusline ok`), `swActive: true` |
| klucz publiczny VAPID | `GET /push/public-key` zwraca klucz; walidator skanuje repo pod kątem `VAPID_PRIVATE_KEY` |
| `_scratch` | nietknięte przez `/push/*` (test w `test_progress_vault.py`) |
| eksport | `schema_version 0.1.0`, `source academy-os`, `academy_url` bez tokena |

---

## 9. Twarde zakazy (nie ruszamy)

- brak **drugiej** karty `TERAZ` (`id="nowcard"` == 1),
- brak `alert(` w UI (komunikaty przez `#syncmsg`),
- brak **iframe** do Kokpitu,
- brak **7. działu**,
- `schema_version` **0.1.0**, `source` **`academy-os`**,
- eksport **bez** tokenów i sekretów,
- Hermes **nigdy** nie robi deploy / merge / write na `dsaas-platform-main`,
- zero sekretów w repo; kod i komentarze po angielsku, UI po polsku,
- `Zasada 11` = deploy tylko na GO Dowódcy.

---

## 10. Ryzyka

| Ryzyko | Mitigacja |
|---|---|
| PWA web push wymaga **subskrypcji** i **zainstalowanej** PWA | test w Fali 4; fallback = powiadomienie przy otwarciu Akademii |
| Chrom terminala może pogorszyć czytelność mobile | mono **tylko** nagłówki/taby; body zostaje sans; walkthrough 375 px |
| Zmiany CSS mogą ruszyć kontrast AA | nie zmieniamy kolorów tekstu — tylko chrom; axe po każdej zmianie |
| Blokada `DZIEŃ` może frustrować (ADHD) | jedna karta `TERAZ` + jasny komunikat „Dokończ DZIEŃ”, nigdy pusty ekran |
| Regresja walidatora | walidator + `test_progress_vault.py` po **każdej** fali |

---

## 11. Kolejność i bramki

| Fala | Zakres | Bramka wyjścia | Stan |
|---|---|---|---|
| **0** | Terminal UX (chrom) | walidator + axe 0/0 + walkthrough 375 px | ✅ DONE |
| **1** | NARZĘDZIA (15 manuali) | obcy przechodzi 1 narzędzie bez pytania | ✅ DONE |
| **2** | DZIEŃ (strażnik + blokada) | `Today first:` sprawdzalny w labie | ✅ DONE |
| **3** | DSAAS (mistrzostwo) | ścieżka odtworzona bez notatek | ✅ DONE |
| **4** | Hermes (push) | push przy zamkniętej PWA *(lokalnie: `showNotification` potwierdzone przez SW)* | ✅ DONE |

Handoff Fali 2: [`docs/handoffs/2026-09-20-akademia-terminal-ux-fala-2.md`](../handoffs/2026-09-20-akademia-terminal-ux-fala-2.md).
Handoff Fal 3+4: [`docs/handoffs/2026-09-20-akademia-terminal-ux-fala-3-4.md`](../handoffs/2026-09-20-akademia-terminal-ux-fala-3-4.md).

Każda fala kończy się handoffem w `docs/handoffs/` (konwencja repo) i wymaga **GO** Dowódcy przed startem następnej.

---

## 12. Weryfikacja końcowa „okiem seniora” (2026-09-20)

Wszystkie 4 fale przeszły jeden zbiorczy przebieg na `http://127.0.0.1:8765/DASHBOARD.html`.

| Obszar | Metoda | Wynik |
| --- | --- | --- |
| Kontrakt walidatora | `python scripts/validate-academy-export.py` | **PASS** |
| Kontrakt vaulta | `python scripts/test_progress_vault.py` | **PASS** |
| Kontrakt „jedna karta `TERAZ`” | DOM `#nowcard` na każdej zakładce i po blokadzie dnia | **1** |
| Kontrakt „brak `alert()`” | skan pliku (walidator) | **0** |
| Dostępność | axe-core 4.10.2 na 6 zakładkach (WCAG 2.0/2.1 A/AA + best-practice) | **0 naruszeń** |
| Mobile 375 px | CDP `Emulation.setDeviceMetricsOverride`, wszystkie zakładki | `scrollWidth == 375`, **0 przelewu** |
| Sticky tabbar na 375 px | pomiar wysokości + `offsetTop` zakładek | 2 rzędy (3+3), `--scroll-offset` **128 px** (auto) |
| Offline | CDP `Network.setBlockedURLs` (3 CDN-y) | 10/10 diagramów ASCII, **0** wycieków kodu, **0** błędów konsoli |
| Online | Mermaid z CDN | 7× SVG, **0** fallbacków aktywnych |
| Day Guard | symulacja zaległego dnia (`day_stamp=2026-09-19`) | lock na jednej karcie, rozdział A1 **niewidoczny**, „Pomiń świadomie” → `day_skipped`, lock zdjęty |
| Naprawione w weryfikacji | `heading-order` (H4 bez H3 w `DZIEŃ`), `white-space:nowrap` w `.ro-table` → 55 px przelewu w HERMES na 375 px | H2→H3 (5×, styl 1:1 jak H4: 12.48 px, uppercase, ten sam kolor/margin), `.ro-table` zawija długie ścieżki (`overflow-wrap:anywhere`) |

**Świadomie nieruszone:** brak nowych zależności, paleta `:root` bez zmian (jest audytowana), `schema_version` i `source` bez zmian.

---

## 13. Polerka przeddeployowa (2026-09-20, GO Dowódcy)

Cel: domknąć wszystko, co na produkcji mogłoby zrobić „cichą porażkę”, i dopiero potem deploy.

### 13.1 Znalezione i naprawione

| # | Problem | Dlaczego to blokada | Naprawa |
|---|---|---|---|
| 1 | **Push na VPS był cicho martwy** — `host/docker-compose.yml` nie przekazywał `ACADEMY_VAPID_PUBLIC_KEY`, a klient miał klucz wpisany na twardo `var VAPID_PUBLIC_KEY=''` („wstrzykuje deploy”, ale deploy tego nie robił) | Badge zostawał na „nieustawiony” na zawsze; nikt by nie zauważył, że push nie działa | Klient pobiera klucz z `/push/public-key` (`loadVapidKey()`), compose przekazuje zmienną, `setup-akademia-vps.sh` dowozi ją z `/etc/akademia/vapid.env` do `.env` |
| 2 | **`scripts/generate-vapid-keys.sh` w całości CRLF** (55/55) | `bash` na VPS wywala się na `set -euo pipefail\r`; `.gitattributes` nie pomaga, bo deploy pakuje **working copy** przez `tar` | Konwersja do LF + guard w walidatorze na CRLF/BOM w każdym `scripts/*.sh` |
| 3 | **Martwy link po re-kliku** — klik w „Rozdział A1” z HERMES działał raz; po powrocie na HERMES ten sam klik **nie robił nic** (`hashchange` nie odpala dla niezmienionego hasha) | Edukacyjna nawigacja „uczy się raz i przestaje działać” — najgorszy rodzaj buga w szkole | Delegowany handler: gdy `location.hash === href`, woła `openHashTarget()` ręcznie |
| 4 | **Ucinany tekst w DSAAS na 375 px** — `.file-row` to grid bez `min-width:0`, więc „Lifecycle: captured→…→deprecated” (361 px) rozpychał kolumnę i był **obcinany** (brak scrolla = treść niedostępna) | Uczysz się z tego tekstu — ucięty = stracony | `.file-row>*{min-width:0;overflow-wrap:anywhere}` + na ≤560 px jedna kolumna |
| 5 | **Service Worker nie rejestrował się przy starcie** (tylko po kliku „Włącz powiadomienia”) | Słabsza instalowalność PWA na Androidzie i ryzyko wyparowania rejestracji SW = push przestaje dochodzić | `registerSwEarly()` w `initApp()` (bez cache — `sw.js` nadal nic nie cache'uje) |
| 6 | Brak `<meta name="description">`, `#dump` bez dostępnej nazwy (pole importu), zduplikowany `<link rel="icon">` | Sloppy head + słabsza a11y/SEO | Dodane; guard w walidatorze na duplikat ikon |

### 13.2 Dowody (nie „powinno działać”)

| Co | Metoda | Wynik |
|---|---|---|
| Push end-to-end **na produkcji lokalnie** | vault na `:8098` z `ACADEMY_VAPID_PUBLIC_KEY`, dashboard **przez vault** | badge sam przełączył się na **„ustawiony”**, `GET /push/public-key` **200**, `POST /push/subscribe` **200**, `POST /push/unsubscribe` **200** |
| Re-klik linku rozdziału | 2× klik tego samego `#roz-A1` z HERMES | 1. klik → WORKFLOW, 2. klik → WORKFLOW **OK** (wcześniej: brak reakcji) |
| Cross-tab nadal działa | WORKFLOW → `#roz-B2` | **DSAAS** |
| Guardy nowe | 4 mutacje: compose bez VAPID, klucz na twardo w HTML, klient bez `/push/public-key`, CRLF w `.sh` | **4/4 złapane**, po przywróceniu **PASS** |
| axe po polerce | 6 zakładek, WCAG 2.0/2.1 A/AA + best-practice | **0 naruszeń** |
| Mobile 375 px po polerce | overflow dokumentu + elementy za viewportem, 6 zakładek | **0 / 0** |
| Błędy sieci | `performance.getEntriesByType('resource')` | 0 nieudanych (poza `api.github.com` → 404 dla prywatnego repo, obsłużone uczciwym komunikatem) |
| EOL skryptów | skan `scripts/*.sh` | **wszystkie LF, zero BOM** |
| Walidatory | `validate-academy-export.py`, `test_progress_vault.py` | **PASS / PASS** |

### 13.3 Plan deployu (wykonanie w tej samej sesji)

1. `bash scripts/deploy-akademia-vps.sh` (tar → scp → `/opt/akademia` → `setup-akademia-vps.sh`).
2. Na VPS: `bash scripts/generate-vapid-keys.sh` (klucz prywatny zostaje w `/etc/akademia/vapid.env`, chmod 600) — **jeśli nie istnieje** (rotacja = świadoma decyzja, unieważnia subskrypcje).
3. Re-run `setup-akademia-vps.sh` → klucz publiczny wpada do `/opt/akademia/.env`, compose recreate vaulta.
4. Smoke: `/health` (loopback), `https://akademia.quietforge.flexgrafik.nl/DASHBOARD.html` (Basic Auth), `/progress` z auth = **200**, bez auth = **401**.
5. Rollback awaryjny: `docker-compose -p akademia down` (DSaaS i jadzia nietknięte).

**Nieruszalne przy deployu:** `schema_version` `0.1.0`, `source` `academy-os`, jedna karta `TERAZ`, brak iframe Kokpitu, brak sekretów w repo, zero zmian w `dsaas-platform-main` i `jadzia-core`.

### 13.4 Wykonanie deployu — wynik (2026-09-20)

| Krok | Wynik |
|---|---|
| `deploy-akademia-vps.sh` (tar → scp → setup) | **OK** — vault `{"ok": true, "service": "academy-vault"}`, DNS + certbot + HTTPS smoke OK |
| Klucz VAPID na VPS | wygenerowany (`/etc/akademia/vapid.env`, chmod 600, root), publiczny **87 znaków** w `/opt/akademia/.env` |
| Timer wysyłki push | `akademia-push.timer` **enabled + active**, następny strzał `Mon 2026-09-21 07:01 CEST`, `--dry-run` zwraca poprawny payload („Jeden kawał do zrobienia — otwórz Akademię.”) |
| Parytet plików VPS ↔ lokalnie | 6/6 **hash identyczny** (`DASHBOARD.html`, `sw.js`, `manifest.webmanifest`, `host/progress_vault.py`, `scripts/push-send.py`, `host/docker-compose.yml`) |
| HTTPS z Basic Auth | `DASHBOARD` /**200**, `/progress` /**200**, `sw.js` /**200**, `manifest` /**200**, ikona 512 /**200**; bez auth wszędzie **401** |
| `/push/public-key` z auth | **200**, klucz `BCblkYbu…` (zgodny z `vapid.env`) |
| Certyfikat | `CN=akademia.quietforge.flexgrafik.nl`, Let's Encrypt, ważny do **2026-12-12** |
| Sekrety na VPS | `vapid.env` **600 root**, `.env` **600**, klucz prywatny w repo: **brak** |

### 13.5 Incydent bezpieczeństwa znaleziony PO deployu: vault oddawał sekrety repo

Weryfikacja po deployu zaczęła się od pytania „co jeszcze ten vault serwuje?” — i odpowiedź była zła.

**Stan przed naprawą** (produkcja, `https://akademia.quietforge.flexgrafik.nl`, za hasłem Basic Auth):

| URL | Kod | Co to znaczy |
|---|---|---|
| `/.env` | **200** | bearer vaulta (`ACADEMY_PROGRESS_TOKEN`) do ściągnięcia jednym `curl -u` |
| `/CREDENTIALS.local.txt` | **200** | login+hasło Basic Auth w czystym tekście |
| `/host/.htpasswd` | **200** | hash nginx `$apr1$…` (offline cracking) |
| `/host/env.example`, `/host/docker-compose.yml`, `/host/progress_vault.py` | **200** | konfiguracja i kod vaulta |
| `/data/` | **200** | (to był `DASHBOARD.html` z fallbacku `rel.endswith("/")`) |
| `/data/progress.json`, `/data/push-subscriptions.json` | 404 | jeszcze nie istniały → **po pierwszej subskrypcji push byłyby 200** (endpointy + klucze urządzeń) |

Przyczyna: `safe_static_path()` sprawdzał tylko traversal (`relative_to(STATIC_ROOT)`), a `STATIC_ROOT` to **całe repo** (`/app/static`). Sekretów nie było w repo — ale były w katalogu, który vault serwował.

**Naprawa (warstwowa, egzekwowana w vaulcie — jedynym miejscu, które czyta pliki):**

1. Odrzucenie dowolnego segmentu zaczynającego się od kropki (`.env`, `.git/config`, `.opencode/`, `.venv/`).
2. Odrzucenie katalogów operacyjnych także jako samego katalogu: `data`, `host`, `scripts`, `.venv`.
3. Odrzucenie nazw wprost: `CREDENTIALS.local.txt`, `.env`, `.htpasswd`.
4. **Biała lista rozszerzeń** treści kursu: `.html .md .png .svg .webmanifest .json .js .css .ico .woff2` — wszystko inne (`.py .sh .yml .conf .txt .ps1 .example`) to 404.
5. Fallback `/` → `DASHBOARD.html` **tylko dla korzenia** (wcześniej `/data/` też dostawało dashboard zamiast 404).

**Dowody:**

| Co | Metoda | Wynik |
|---|---|---|
| Reguły na prawdziwych plikach | test importuje vault z **tymczasowym STATIC_ROOT zawierającym dekoje** (`.env`, `CREDENTIALS.local.txt`, `host/.htpasswd`, `data/push-subscriptions.json`, `scripts/push-send.py`) | 13 ścieżek → **wszystkie `None`**; 5 ścieżek treści kursu → **serwowane** |
| Ten sam test po mutacji | wyłączone reguły 2 i 4 | **FAIL: 10 trafień** (`/host/env.example`, `/scripts/push-send.py`, `/data/push-subscriptions.json`…) → po przywróceniu **PASS** |
| HTTP na istniejących plikach repo | `GET /host/env.example`, `/host/docker-compose.yml`, `/host/progress_vault.py`, `/scripts/push-send.py`, `/data/`, `/CREDENTIALS.local.txt` | **404** (przed: 200) |
| Treść kursu nadal działa | `/docs/OPERATING-MODEL.md`, `/schema/academy-progress.v0.json`, `/icons/icon.svg`, `/README.md`, `/DASHBOARD.html` | **200** |
| Guard w walidatorze | 6 konkretnych linii reguł + 3 markery testu | mutacja „usuń `if parts[0] in STATIC_DENY_DIRS:`” → **FAIL** z komunikatem, po przywróceniu **PASS** |
| Higiena repo | `.gitignore` | dopisane `data/push-subscriptions.json` (endpointy push) i `__pycache__/` |

**Czego to nie zmienia (świadomie):** brak nowych zależności, brak zmian w schemacie eksportu, brak zmian w UI, paleta i layout nietknięte. `docs/`, `ops/`, `schema/`, `icons/`, `README.md` — cała treść kursu — działa jak wcześniej.

