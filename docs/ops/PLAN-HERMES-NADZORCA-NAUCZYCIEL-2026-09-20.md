# PLAN — Hermes: nauczyciel · nadzorca workflow · „Mój dzień"

**Data:** 2026-09-20 · **Autor:** sztab 4 inżynierów (research) + synteza · **Status:** do decyzji Dowódcy
**Zakres:** `akademia` (narzędzie) + nadzór nad `dsaas-platform-main` (produkt) · **Branch:** `feat/hermes-chat-ux-audit`

---

## 0. Werdykt w jednym akapicie

Dowódca zlecił trzy role dla Hermesa: **nauczyciel**, **główny nadzorca workflow** i **wykonawca „Mojego dnia"**.
Sztab zbadał wszystkie trzy i doszedł do wniosku, który zmienia kolejność prac: **żadna z tych trzech ról nie jest
dziś blokowana przez brak modelu AI — wszystkie trzy są blokowane przez brak danych i brak wyzwalacza.**
Hermes ma mózg (deepseek-flash działa, zmierzone 1,8–8,8 s), ale:
(1) **nie zna treści kursu** — więc na pytanie o materiał odpowiada „nie mam tego w źródłach", mimo że silnik lokalny
zna odpowiedź; (2) **nie ma czego nadzorować** — repo `akademia` ma **0 workflow GitHub Actions** i **main bez
ochrony**, a jej jedyny otwarty PR (#17) już żyje na produkcji, bo deploy pakuje *working copy* bez sprawdzenia SHA;
(3) **nie ma kiedy pomóc w rytuale** — powiadomienie o 07:00 istnieje i jest poprawnie zaplanowane, ale tapnięcie
w nie **gubi zakładki** (`client.focus()` bez nawigacji), więc poranek „od jednego tapnięcia" jest dziś nieosiągalny.
Do tego jedno realne ryzyko: `dayLock()` **karze za dzień odpoczynku**, co zgodnie z handbookiem i praktyką
oznacza, że funkcja zostałaby wyłączona w dwa tygodnie.

**Dlatego pierwsze ~3 godziny idą nie na AI, tylko na zamknięcie żywych dziur w integralności.** Dopiero potem
budujemy deterministyczny rdzeń rytuału i nadzorcy — i **LLM wchodzi dopiero na końcu**, na jedno zadanie:
zamienić gotowy werdykt na jedno zdanie po polsku.

---

## 1. Skład sztabu i co każdy ustalił

| # | Rola | Główne ustalenie | Rekomendacja |
|---|---|---|---|
| 1 | **Architekt AI / retrieval** | `cursor-kurs/*.md` **nie zawiera ani jednego** pojęcia, o które Dowódca pyta (grep `ODCS\|HITL\|ledger\|R7` → 0 trafień). Definicje żyją **tylko** inline w `DASHBOARD.html` (4 245 znaków). Model odpowiada „nie mam tego w źródłach" **poprawnie** — naprawdę ich nie ma | **Router-first + przypięty fakt** (G0+G1), **nie** pełny RAG. Full-context ~31k tok. jest *tańszy niż wygląda* (€0,02–3/mies.), ale odpada nie za cenę — za **darmowy tier (Groq TPM 8000), latencję i rozmycie uwagi** |
| 2 | **Integracje (Linear/GitHub)** | `akademia` **nie istnieje w Linear** (tylko 2 projekty: `dsaas-platform-main`, `workflow-lab`). Repo ma **0 Actions** i **main bez ochrony**. Token `gh` w keyringu ma zakres `repo`+`workflow` = **ZAPIS** → nie wolno go skopiować na VPS | **GitHub-first**, Linear **dopiero po osobnej zgodzie** (klucz osobisty Linear = zakres całego workspace, brak read-only). Ostrzeżenie: `QUI-39` zawiera **realne dane biznesowe** (oferta €690, marża 96%) → **do LLM idą wyłącznie liczby**, nigdy treści |
| 3 | **Nadzorca workflow** | Mapa **47 reguł** w 4 klasach sprawdzalności, **18 luk** z dowodami. Reguły są mocne (guardy + mutacje), ale **nie mają wyzwalacza** — odpalają się tylko wtedy, gdy Dowódca pamięta. Żywy skutek: **PR #17 otwarty, jego 6 commitów na produkcji, `main` 6 commitów za produkcją** | Supervisor **poza** nadzorowanym artefaktem (timer na VPS), werdykt **zawsze deterministyczny**, LLM tylko formułuje zdanie. Status trójwartościowy `PASS/FAIL/UNKNOWN` — **„nie wiem" nigdy nie jest zielone, a cisza supervisora to osobny alarm** |
| 4 | **UX / produkt („Mój dzień")** | Rytuał to dziś **13 checkboxów + 2 linie** ≈ **8–11 interakcji rano**, z czego 4–5 to potwierdzanie pracy wykonanej poza aplikacją, a linia `Today first:` jest **przepisywana dwa razy**. Do tego **P0**: `sw.js:92` `client.focus()` **bez nawigacji** → push 07:00 prowadzi donikąd | **Hermes przygotowuje, Dowódca zatwierdza: 2 tapnięcia, 0 wpisywania.** Zero nowych zakładek, zero drugiej karty — reuse `#nowcard` + `hermesKawal()` |

---

## 2. Fakty zweryfikowane (twarde, nie opinie)

| # | Fakt | Dowód |
|---|---|---|
| F1 | Push 07:00 istnieje i dogania po śnie VPS, ale **tapnięcie gubi zakładkę** | `scripts/setup-akademia-vps.sh:215-226` (`Persistent=true`) + `sw.js:88-96` (**`client.focus()` bez `navigate`**) |
| F2 | Deploy pakuje **working copy**, zero weryfikacji `origin/main` | `scripts/deploy-akademia-vps.sh:11-20` (`tar -cf ... -C "${SRC}" .`) |
| F3 | `akademia` ma **0 workflow** i **main bez ochrony** | `actions/workflows` → `total_count:0`; `branches/main/protection` → **404 "Branch not protected"** |
| F4 | PR #17 **otwarty**, branch **6 commitów przed `main`**, te commity **są na VPS** | `compare main...feat/hermes-chat-ux-audit` → `ahead_by=6`; deploy F2 |
| F5 | Linear: **dokładnie 2 projekty**, brak projektu dla `akademia`; 41 issue w `dsaas-platform-main` | `list_projects` → 2 wyniki; `list_issues` project=`dsaas-platform-main` → 41 |
| F6 | Linear↔GitHub **integracja działa** (QUI-39 → PR #71) | `get_issue QUI-39` → `attachments[0].url = .../dsaas-platform-main/pull/71` |
| F7 | `QUI-39` zawiera **dane biznesowe tenanta** (ICP, oferta €690, marża 96%, budżet mediowy) | treść `QUI-39` przez MCP |
| F8 | `dayLock()` blokuje **3 miejsca** i jest **stale-only**; niekompletny dzień bieżący nie blokuje niczego | `DASHBOARD.html:936` + `:1246`, `:992`, `:1251` |
| F9 | `Today first:` walidowane **wyłącznie formatem** (`trim`→`toLowerCase`→`indexOf(prefix)===0`), zero treści | `DASHBOARD.html:931` |
| F10 | W repo są **6 zakładek**, nie 5 — guard „5 zakładek IA" to test **obecności napisów**, nie licznik. Twardy jest tylko `id="nowcard" == 1` | `DASHBOARD.html:453` (`ACADEMY_TABS`) vs `validate-academy-export.py:72` vs `:69` |
| F11 | Model dostaje **tylko `state`** (limit 300 znaków/pole, `note` 600), nigdy treść kursu | `progress_vault.py:237-266`, `HERMES_SYSTEM` `:75-101` |
| F12 | `ACADEMY_PROGRESS_TOKEN` jest na produkcji **pusty** → `authorized()` zwraca `True`; realną bramką jest **wyłącznie nginx Basic Auth** | `setup-akademia-vps.sh:37` + `progress_vault.py:190-191` |
| F13 | Mózg LLM **działa** (potwierdzone na produkcji): `deepseek-flash`, `max_tokens` 2500, vault timeout 20 s < watchdog 25 s | deploy 2026-09-21 + guardy E1–E3 |

### 2.1 Otwarta pozycja bezpieczeństwa (do zamknięcia ręcznie, ~5 min)

**Klucz DeepSeek był wklejony w czacie → zgodnie z własnym handoffem należy traktować go jako spalony**
(`docs/handoffs/2026-09-21-akademia-hermes-model-deploy.md` §7). Nie ma sposobu zweryfikować rotacji z repo.
**Rekomendacja: rotuj klucz przed dalszą pracą.** Sekundarna obserwacja: `ACADEMY_PROGRESS_TOKEN` jest pusty,
więc nowy endpoint nadzorcy będzie stał na **jednym haśle współdzielonym** z `CREDENTIALS.local.txt` (F12).

---

## 3. Trzy role Hermesa — rozdzielone (to jest sedno planu)

Dziś te trzy role są pomieszane w jednym promptcie, w którym model nie ma danych do żadnej z nich.
Plan rozdziela je **architektonicznie**, bo każda ma inny nośnik prawdy:

| Rola | Nośnik prawdy | Werdykt wydaje | LLM robi | Koszt |
|---|---|---|---|---|
| **Nauczyciel** — „wytłumacz ODCS" | słownik pojęć w repo (`docs/SLOWNIK-HERMESA.md` — do napisania) | **silnik lokalny** (deterministyczny, zna definicję) | tłumaczy **głębiej** na jawne żądanie (przycisk) | 0 tok. domyślnie |
| **Nadzorca workflow** — „czy workflow jest zgodny" | `workflow/rules.json` + GitHub API (+ Linear po zgodzie) | **skrypt deterministyczny** (`workflow-checks.py`) | zamienia gotowy werdykt na **jedno zdanie po polsku** | ~0 (1 wywołanie/dzień) |
| **„Mój dzień"** — „zrób za mnie poranek" | `progress_vault.morning_brief()` + `hermesKawal()` | **deterministyczny rdzeń** | dopisuje **1–3 zdania** „co to dziś znaczy dla nauki" | ~0,2% dziennego capa |

**Twarda zasada architektoniczna (guard G-04):** LLM **nigdy** nie ustawia pola `status` ani nie zapisuje `day_*`.
Halucynacja może dać fałszywą **czerwień** (koszt: 5 sekund), ale **nie może** dać fałszywej **zieleni** (koszt: cały system).

---

## 4. Decyzje, których nie podejmujemy za Dowódcę

To są **bramki**, nie detale. Każda wymaga Twojego „tak". Bez nich fale poniżej idą w wariancie minimalnym (bez nowych sekretów).

| # | Decyzja | Domyślnie (bez zgody) | Z zgodą | Ryzyko |
|---|---|---|---|---|
| **A1** | **Rotacja klucza DeepSeek** | — | rotuj teraz | Klucz z czatu = spalony |
| **A2** | **PAT GitHub na VPS** (odczyt Actions/PR z prywatnych repo) | czyta tylko `akademia` i `workflow-lab` (publiczne, bez tokena) | + `dsaas-platform-main` | Nowy sekret na VPS (nie w repo, chmod 600, fine-grained, `Actions:Read`+`Checks:Read`+`Contents:Read`+`Pull requests:Read`, expiry 90 dni). **NIE kopiować tokena z keyringu** (ma zapis) |
| **A3** | **Klucz Linear API na VPS** | Linear → `unknown` (uczciwie „nie wiem") | prawdziwe „In Review/blocked" | ⚠️ Klucz osobisty Linear = **zakres całego workspace, brak read-only**. Wymaga OAuth na `read` albo świadomej akceptacji |
| **A4** | **Egress treści Linear do LLM** | do modelu idą **wyłącznie liczby** (`blocked:2, hitl:12`) | treści issue (F7!) | **Dane biznesowe tenanta → third-party LLM.** Rekomendacja: **nie** |
| **A5** | **Branch protection na `akademia/main`** | zostaje jak jest | włącz, required check `academy-gate` | Zmienia sposób pracy (deploy idzie tar-em, więc ryzyko niskie) |
| **A6** | **Pierwszy workflow Actions w `akademia`** | 0 workflow (jak dziś) | włącz `academy-gate.yml` | Nowa powierzchnia CI i nowy tryb awarii — ale bez tego „nadzorca" nie ma czego pilnować |

---

## 5. Plan wykonania — falami (1-1-1, kolejność po ryzyku na godzinę)

### FALA 0 — Integralność: zamknij żywe dziury (≈3 h) · **bez AI, bez nowych sekretów**

Kryterium: po tej fali **prawda w repo == prawda na produkcji**, a kanał poranny działa.

| # | Zadanie | h | Dlaczego pierwsze |
|---|---|---|---|
| 0.1 | **`sw.js`: `notificationclick` → `client.navigate(target)`** (F1) | 0,5 | ⭐ Bez tego cały push 07:00 prowadzi donikąd. Największa dźwignia w repo |
| 0.2 | **Zmerguj PR #17** (F4) | 0,25 | `main` jest 6 commitów za produkcją — „prawda" nie odpowiada rzeczywistości |
| 0.3 | **`deploy-akademia-vps.sh` odmawia deployu, gdy drzewo ≠ `origin/main`** (chyba że `--force`) (F2) | 0,75 | Zamyka lukę, która może **cicho** wprowadzić na produkcję kod, którego nikt nie zrecenzował |
| 0.4 | **`.github/workflows/academy-gate.yml`** uruchamiający dokładnie `AGENTS.md:19` (walidator + vault tests) | 1,0 | Zamienia „gate z pamięci" w gate z CI — to jest **wyzwalacz**, którego brakuje wszystkim regułom |
| 0.5 | **Branch protection `akademia/main`**: required `academy-gate`, `strict:true` (A5/A6) | 0,5 | Domyka lukę F3 |

**Guard po fali:** `G8` — `sw.js` musi mieć nawigację w `notificationclick`; `G-deploy` — deploy odmawia przy rozjeździe SHA.

---

### FALA 1 — „Mój dzień" robi Hermes (≈7,5 h) · **deterministyczny, działa bez LLM i bez internetu**

Cel: **2 tapnięcia, 0 wpisywania.** Rytuał przestaje być formularzem, staje się zatwierdzeniem.

| # | Zadanie | h | Uwaga |
|---|---|---|---|
| 1.1 | `morning_brief(progress)` w `progress_vault.py` + `GET /hermes/morning` (za `authorized()`, **nie** publiczny) | 2,5 | **Jedna prawda**: `push-send.py:build_payload()` **importuje** ją zamiast duplikować (dziś jest kopia) |
| 1.2 | `fetchMorningBrief()` + `morningBriefLocal()` (mirror offline) + `renderDayBrief()` w istniejącym `#day-status` | 2,0 | Zero nowych kontenerów — slot już istnieje (`DASHBOARD.html:1238`) |
| 1.3 | `approveDay()` — **jedyny** zapis rytuału, jedno `save()` | 1,0 | Wypełnia `day_*` i `Today first:` z `brief.proposal` (format i tak wymuszony) |
| 1.4 | `autoStaleResolve()` — **dzień odpoczynku nie generuje LOCK-a** (F8) | 1,0 | ⭐ Bez tego funkcja zostanie wyłączona w ~2 tygodnie |
| 1.5 | Nowa pierwsza gałąź `renderNowCard()`: „dzień gotowy do zatwierdzenia" + `hermesKawal(opts)` z gałęzią rest-day **przed** `lk.locked` | 1,0 | Reuse `#nowcard` — **jedna karta, bez zmian** |

**Kontrakt:** `checks[].status ∈ {auto, confirmed, unknown}` — **„nie wiem" musi być wolno powiedzieć**
(ten sam idiom co `hermesLocalAnswer` „Nie mam tego w źródłach"). 13 checkboxów **zostaje** pod `<details>` „Ręcznie".
Eksport `schema_version 0.1.0` **bez zmian** (nowe pola tylko w `_scratch`).

**Liczby przed → po:** rano 8–11 interakcji → **2 tapnięcia**; wpisywanie linii ~20–40 znaków ×2 → **0**.

---

### FALA 2 — Nadzorca workflow (≈6 h) · **deterministyczny rdzeń, GitHub-first, bez Linear**

| # | Zadanie | h | Uwaga |
|---|---|---|---|
| 2.1 | `workflow/rules.json` — rejestr reguł (**≤12**, nie 47) + `scripts/workflow-checks.py --local-only` | 2,5 | Zaczynamy od reguł A1–A16 + S1–S6 (sprawdzalne z wnętrza repo) |
| 2.2 | `GET/PUT /workflow/checks` w vaulcie + `EMPTY_CHECKS_AT` + **monotoniczny `run_seq`** + `ttl_seconds` | 1,5 | Replay starego zielonego → **409** |
| 2.3 | Reguły GitHub (G1, G3, G6-proxy, G7, G8, G12) | 1,5 | Wymaga **A2**; bez niej tylko `akademia` |
| 2.4 | `checkLock()` wpięty jako **rodzeństwo** `dayLock()` w istniejącym `hermesKawal()` + precedencja w `build_payload()` | 0,5 | ⭐ **Zero nowych powierzchni UI** (zakaz drugiej karty, `AGENTS.md:5`) |

**Inwarianty wymuszone testami, nie dobrą wolą:**
- `status` domyślnie **`UNKNOWN`**, nigdy `PASS` — żeby pokazać zielone, trzeba **wpisać** `PASS` i mieć niepusty `evidence`;
- `coverage` musi się zgadzać z `rules.json` — wyłączenie reguły to **FAIL**, nie PASS;
- **brak raportu = FAIL**, a **cisza supervisora to osobny push** (supervisor, który milczy, bo padł, jest gorszy niż jego brak);
- pushuje **tylko `blocking`** (sufit: **3 reguły blokujące**), `advisory` nigdy nie dzwoni.

**Liczby, które realnie potrzebuje telefon (6, nie 41):** status `gates` + czas · ile PR czeka · ile `blocked` · ile `hitl`
(**to jest dosłownie „Mój dzień"**) · ile w kolejce agenta · **jeden** kawał.

---

### FALA 3 — Nauczyciel (≈2 h) · **router-first + przypięty fakt, NIE pełny RAG**

| # | Zadanie | h | Uwaga |
|---|---|---|---|
| 3.1 | `docs/SLOWNIK-HERMESA.md` — 11 pojęć z `HERMES_GLOSSARY` rozbudowane do ~600–900 znaków (to jest **blokada**, nie ozdoba) | 1,0 | Bez tego retrieval nie naprawia **niczego** (F: kurs nie ma tych pojęć) |
| 3.2 | `hermesIntent(q)` → `'state'` \| `'fact'` \| `'open'`; pytania o postęp **nigdy** nie idą do modelu | 0,5 | ⭐ Model w pytaniach o postęp jest **gorszy** niż lokalny (widzi digest, nie stan). −40% zapytań płatnych |
| 3.3 | Przycisk **„Wytłumacz głębiej (model)"** w istniejącym bąbelku odpowiedzi | 0,5 | To jest **HITL dla tokenów** — Dowódca sam decyduje, kiedy płacić |

**Czego świadomie NIE robimy:** pełnego kontekstu (31k tok.). Odrzucony **nie za cenę** (€0,02–3/mies. — tanio),
ale za: **darmowy tier (Groq TPM 8000 nie weźmie 31k)**, latencję (sufit 20 s) i rozmycie uwagi modelu rozumującego.

---

### FALA 4 — Dowód, że to działa (≈4 h) · **guardy + mutacje + testy behawioralne**

Bez tej fali wszystko powyżej to dekoracja — i to jest w tym repo zmierzone, nie teoretyczne.

| # | Zakres | h |
|---|---|---|
| 4.1 | Guardy w `validate-academy-export.py` (idiom: asercje na **konstrukcjach**, numerowane) | 1,5 |
| 4.2 | `mutation-test-fala-g.py` — **bajt-w-bajt + weryfikacja SHA** (10 mutacji) | 1,5 |
| 4.3 | Rozszerzenie `test_progress_vault.py` — testy behawioralne na realnym vaulcie + **kanarek** na wyciek sekretu | 1,0 |

**Mutacje obowiązkowe (bez nich fala nie ma zębów):**
`M4` domyślny `status:"PASS"` w `CheckResult` (fałszywa zieleń w zarodku) · `M8` `notificationclick` bez nawigacji ·
`M9` usunięcie gałęzi rest-day · `M2` druga karta `nowcard` · `M10` `/hermes/morning` bez `authorized()`.

---

## 6. Czego NIE budować (explicite)

| ❌ Nie | Dlaczego |
|---|---|
| Druga karta „teraz" / 7. zakładka „COMPLIANCE" | Łamie `AGENTS.md:5`. Wymusiłoby **edycję guardu**, żeby coś przeszło — dokładnie ten antywzorzec, który ten plan ma zwalczać |
| Pełny kontekst kursu (31k tok.) | Nie wejdzie na darmowy tier, ryzyko dobicia 20 s, rozmywa uwagę modelu. Tanio ≠ dobrze |
| Vector DB / RAG z embeddingami | 190 chunków, 1 użytkownik, 20 pytań/dzień → BM25-lite z pełnym skanem to <5 ms. Embeddingi to koszt bez zysku |
| Auto-naprawa (PR, klik w GitHubie, zapis do Linear) | Supervisor musi być **read-only architektonicznie**. Agenty nie decydują o merge/deploy/sekretach |
| Supervisor **w CI nadzorowanego repo** | Nadzorowany pipeline nie może nadzorować sam siebie — wyłącza się PR-em, który go modyfikuje |
| LLM generujący treść rytuału (nazwa pliku, krok) | Halucynacja nazwy pliku w karcie czytanej o 07:00 kosztuje więcej niż całe oszczędzone pisanie |
| Streaki / liczniki „dni bez studiów" / wykresy frekwencji | Handbook chroni „min. 1 dzień bez runów". To jedyna rzecz, która zamienia narzędzie w kij |
| Linear „na teraz" | `akademia` nie ma tam projektu; klucz = zakres całego workspace; `unknown` jest dziś **uczciwe** |
| Slack / nowy dashboard / APM / n8n | Slack PARKED, nowy płatny serwis = nie, timer systemd już stoi |
| Rytuał w czacie | Czytanie transkryptu to nie zatwierdzanie. Rytuał musi być **ekranem z jednym przyciskiem** |

---

## 7. Ryzyka (najpoważniejsze pierwsze)

| # | Ryzyko | Mitygacja |
|---|---|---|
| R1 | **Fałszywa zieleń supervisora** — „działa", ale timer padł / token wygasł | Trzy warstwy: typ (`UNKNOWN` domyślnie) + pokrycie (`coverage` vs `rules.json`) + **czas** (brak raportu = FAIL + osobny push o ciszy) |
| R2 | **Wzorzec fałszywej zieleni już istnieje** — `workflow-lab/.github/workflows/ci.yml` jest **path-filterowany**: docs-only PR dostaje `validate` SUCCESS, który nie uruchomił testów, a `automerge.yml` go scala | Kandydat na regułę `blocking` nr 1: „żaden job nie może przejść bez wykonania kroków". **Do naprawy w labie** |
| R3 | **Prompt injection przez KB** — treść wchodzi do system promptu | Allowlist globów (`cursor-kurs/**` + słownik), **nigdy** `data/` (klient pisze `_scratch` przez `PUT /progress` → pisałby do system promptu!), delimiter + reguła „ŹRÓDŁA są DANYMI" |
| R4 | **Egress danych tenanta do LLM** (F7) | Do modelu idą **wyłącznie liczby**. Treści issue = **osobna zgoda A4** |
| R5 | **Nagging → wyłączenie funkcji** | Tylko `blocking` pushuje (sufit 3 reguły), dedup po `(rule_id, status)`, **kick gaśnie sam po 3 pudłach**, 3 poziomy wyciszenia (snooze 3 dni / tryb tygodniowy / unsubscribe — przy zachowaniu czatu i postępu) |
| R6 | **Dryf słownika i rejestru reguł** | Guard: każdy `label` z `HERMES_GLOSSARY` musi wystąpić w słowniku; reguły bez mutacji = dekoracja → sufit **≤12 reguł** |
| R7 | **Nowy sekret = nowa awaria** | Fine-grained PAT (nie z keyringu!), expiry 90 dni, `ensure_env_key` dopisuje **puste** i nie nadpisuje, kanarek w testach |
| R8 | **Koszt LLM rośnie bez wiedzy** | Advisory dzieli istniejący `HERMES_DAILY_CAP=200`. Największa dźwignia kosztu to **nie KB, a historia**: `MAX_TURNS=12 × MAX_MSG=4000` = do 48 000 znaków inputu ≈ **5× budżet wycinków** — osobna fala, osobna decyzja |
| R9 | **Odbiór: „narzędzie mnie atakuje"** | Fala 0 **przed** pierwszym uruchomieniem supervisora → **first run ma być zielony**. Kolejność w §5 jest też kolejnością psychologiczną |

---

## 8. Podsumowanie liczbowe

| Fala | Zakres | Godziny | Zysk |
|---|---|---|---|
| **0** | Integralność (push, PR, SHA, CI, ochrona main) | **3,0** | Prawda repo == prawda produkcji; kanał poranny działa |
| **1** | „Mój dzień" deterministyczny | **7,5** | 8–11 interakcji → **2 tapnięcia**; koniec kija za odpoczynek |
| **2** | Nadzorca workflow (GitHub-first) | **6,0** | Realny sygnał „czy `gates` na main jest zielone" na telefonie |
| **3** | Nauczyciel (router + fakt) | **2,0** | Koniec „nie mam tego w źródłach" na pytania o materiał |
| **4** | Guardy + mutacje + testy | **4,0** | Regresja zamknięta; fałszywa zieleń niemożliwa |
| | **RAZEM** | **≈22,5 h ≈ 3–4 sesje** | |
| | *Wariant minimalny (bez A2–A4)* | **≈14 h** | Wszystko powyżej **bez nowych sekretów** |

**Kamień milowy: Fala 0 + 1 = 10,5 h.** Po nich Dowódca ma poranek, który **działa**, i repo, które mówi prawdę.
Dopiero potem nadzorca i nauczyciel — bo bez danych do nadzoru i bez słownika do nauki byłyby teatrem.

---

## 9. Następny krok (do zatwierdzenia)

1. **A1 — rotacja klucza DeepSeek** (5 min, ręcznie, przed czymkolwiek).
2. **Fala 0** — start bez czekania na decyzje A2–A4 (żadnych nowych sekretów).
3. Równolegle: decyzje **A2–A6** — od nich zależy zakres Fali 2.

*Dokument nie nadpisuje `docs/OPERATING-MODEL.md` ani `AGENTS.md`. Zmiana ról/SoT/zakazów — decyzja R1 + wpis z datą.*
