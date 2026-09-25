# Plan sztabu — czysta Akademia (Cloud SoT)

**Status:** Fala 0 (dokument) na `main`. Live UI nadal 6 tabów (`4632afb`) aż Cloud zmerguje PR-y 1–6.  
**Spec:** [`docs/ACADEMY-UX-SPEC.md`](../ACADEMY-UX-SPEC.md) **v6**.  
**Nie deployuj** tego dokumentu na VPS jako „gotowy produkt”. Deploy UI = osobne **GO Dowódcy** (Zasada 11).

Cloud: czytaj ten plik od góry do „Kolejność PR-ów”. Nie zgaduj IA. Nie usuwaj zakładki bez GO.

---

## Werdykt

Dwa lata budujesz platformę i nie zarabiasz, bo Akademia **kradnie uwagę** (chrome + 7 mermaidów naraz + homework H) zamiast dawać **jedną lekcję** i **jedną ścieżkę pieniądza**.

Prompt założyciela (kim jestem / platforma / działy / monetyzacja, [quietforge.flexgrafik.nl](https://quietforge.flexgrafik.nl/)) zostaje **celem produktu**, nie ścianą copy w hero.

Sztab: UX narzędzia + lis sprzedaży MKB. Szum chowamy; zostaje tylko to, co prowadzi do lekcji albo do klienta.

---

## Kontrakt 8 zakładek (twardo)

Nic z obecnego nav nie znika. Dokładasz dwa. **Bez zgody Dowódcy nie dodajesz i nie usuwasz tabów.** Kokpit nadal 6 działów. `/ops` nie jest tabem Akademii. Osobnego przycisku **KURS** nie ma.

| # | `id` | Title | Pytanie |
|---|---|---|---|
| 1 | `now` | TERAZ | Co robię w tej minucie? Jeden rozdział w panelu. Zero duplikatu `#nowcard`. |
| 2 | `workflow` | WORKFLOW | Jedna pętla (chip Telefon / Laptop) + bieżący A. |
| 3 | `tools` | NARZĘDZIA | Karty narzędzi. |
| 4 | `dsaas` | DSAAS | Biblia `dsaas-platform-main`: plik → obowiązek → co psuje tenant. 3 strefy. |
| 5 | `money` | MONETYZACJA | Szkoła lisa H1–H4. Zero mermaid. |
| 6 | `sources` | ŹRÓDŁA | 3 karty briefingu, nie bibliografia. |
| 7 | `notes` | NOTATKI | `_scratch.notes`. |
| 8 | `day` | DZIEŃ | Rytuał. Nie zleca PR. |

`TAB_BY_DZIAL`: A→`workflow`, B–G→`dsaas`, **H→`money`**.  
`load()`: legacy `kurs` / `guide` / `hermes` → `dsaas`. Hash `#money` / `#sources` = ID zakładki (jak `#day`).  
`firstOpen()`: bez zmian — `KURS_DZIAL_ORDER` H-first, **nie** `ALL_ROZ`.

Nav 360px: 2 rzędy × 4, każdy tab `min-height: 44px`.

---

## Chrome — zabić szum

Dziś first viewport w [`DASHBOARD.html`](../../DASHBOARD.html) ~248–260 zjada uwagę:

- `.hero .sub` — „Jeden rozdział naraz. Kurs A–H…”
- `#sync-bar` — „Online — zapisano · WORKFLOW”
- `#barwrap` + `#pct` + `#remain` — „3% (1 z 29) / Do końca kursu: 28… Dziś wystarczy jeden.”
- `#nowcard` poza TERAZ
- `.nav-legend` — 🟢🟡🔴
- `#tty-left` / `#tty-right` (klawisze)

**Zostaje na foldzie:** `h1` skrócone do **Akademia** + link `Hermes Ops →` + **mapa A–H** + taby + panel.

**Usuń / ukryj CSS+DOM:**

- `.hero .sub` (nie `display:none` na chips — chips już ukryte; **usuń** ten `<p class="sub">`)
- `#sync-bar` — sync tylko kropka w `#tty-sync` (`Online` / `Offline`)
- `#pct`, `#remain`, morał, pojedynczy `#bar` / `#barwrap` (zastępuje `#course-map`)
- `#nav-legend`
- `#nowcard` — zawsze `is-hidden` (TERAZ = panel). `renderNowCard()` może zostać martwy albo no-op; nie maluj karty
- `#tty-left`, `#tty-right`
- `phone-first-banner` na WORKFLOW i `renderKursMap()`
- `.panel-head` desc + badge `local-first` — skróć do tytułu albo wytnij

**„Dwie warstwy workflow-lab: Node core vs analiza”** (`DIAGRAMS.layers` w `renderWorkflow`): **zakaz first-card.** `<details>` summary: `Node core vs notebooki (A7)`.

---

## Widget: mapa A–H

Zastępuje `#barwrap`. `nav#course-map` (nie `role="progressbar"`):

- 8 przycisków A–H
- fill = zaliczone/total **tego** działu (nie globalne 1/29)
- `is-current` = dział `firstOpen()` (pusty start = **H**)
- Click: `activateTab` + otwórz `#dzial-X` / `#roz-*` + `gentleScroll`
  - H → tab `money`
  - A → `workflow`
  - B–G → `dsaas`

ARIA: nawigacja. Label: `A Workflow Lab, 2 z 7 zaliczone`. Globalne „1 z 29” tylko `aria-live` (toast) po zaliczeniu, **nie** na foldzie.

---

## DSAAS — 3 strefy, nie burdel

Dziś `renderDsaas()` + `renderKurs()`: cytat + **7 mermaidów** w `#dsaas-flows.grid.two` + scoreboard + mastery + accordion **B–H** + `renderKursMap` + INSTRUKCJA + Hermes.

**Above-fold (dokładnie 3 bloki):**

1. **Werdykt** ≤4 linie: TENANT-READY CORE (POC) + „model nie decyduje — polityka + człowiek”. `PRODUCT_MISSION` w `<details>`.
2. **Jeden** mermaid + 7 chipów (Platforma · Łańcuch · HITL · Agenty · Izolacja · Kokpit · Budżet). `#dsaas-flows` może zostać jako **scena jednego** diagramu. Zakaz grida 7 kart. Brak duplikatów tego samego mermaida w accordionie B/E/F.
3. **Jeden** otwarty accordion działu B–G (`firstOpen` jeśli B–G; jeśli TERAZ=H, otwórz B albo nic — H jest na MONETYZACJA). Reszta B–G zamknięta.

**Below-fold `<details>` (0 open):** misja pełna, scoreboard, mastery, INSTRUKCJA, Hermes, `PLATFORM_BIBLE`.

`PLATFORM_BIBLE`: tabela wierszy **plik → obowiązek → co psuje wynik tenanta**. Źródło: istniejący `PLATFORM_SCOREBOARD` / `DZIAL_DATA` B–G. **Nie zgaduj EUR.** To jest „pojąć platformę w pełni”.

H **wychodzi** z `renderDsaas` / `KURS_DZIAL_ORDER` pętli DSAAS (`if(oid==='A'||oid==='H')return`).

---

## WORKFLOW

Widoczne: jedna pętla (chip Telefon | Laptop, default Laptop na szerokim / Telefon ≤480px) + playbook + bieżący rozdział A.  
`<details>`: druga pętla, layers mermaid, pozostałe A, onboarding 10 kroków.  
`renderSources('WORKFLOW')` **wycinamy** z działów — lista żyje w ŹRÓDŁA.

---

## MONETYZACJA — lis, nie lejek

Cel promptu: skończyć platformę **i** zacząć zarabiać. Ty = produkt. H uczy sprzedaży, nie odhacza AI-slop.

**Zakaz DoD lab:** wpisz EUR, 20 firm, 10 maili.  
Pliki `docs/akademia/SKU-SKAN-DECYZJI-MKB.md`, `OUTREACH-SKRYPT-MKB.md`, `PILOT-RETAINER-CHECKLIST.md` zostają **papierem po lekcji** (link), nie checkboxem zaliczenia.

Sylabus (LEARN, potem 1–2 ROBISZ). Dodaj **H4** do `DZIAL_DATA` (dziś są H1–H3).

| id | LEARN | ROBISZ |
|---|---|---|
| **H1** Kim jesteś + jedno SKU | Winda, tak/nie, ICP = właściciel w procesie (nie „firmy AI”) | Głos 30 s **albo** 4 zdania windy. **Nie** pole ceny. |
| **H2** Ciepłe wejście | Intro / stary klient FlexGrafik / księgowy; 4 pytania discovery | **Jedna** wiadomość. Nie spray, nie 10 zimnych. |
| **H3** Pieniądz przed budową | Skan = produkt; 50/50 lub z góry; obiekcje (za drogo / za darmo / pokaż Kokpit / cały OS) | Demo human-stop, nie wykład. |
| **H4** Dowód → retainer | Mail zamknięcia + termin; retainer = utrzymanie działającego; skan może powiedzieć „nie automatyzuj” | Jedna wiadomość zamknięcia. |

UI: ścieżka 4 stopni, jeden otwarty, **zero mermaid**. TERAZ pokazuje tylko ROBISZ z bieżącego H.

`function renderMoney()` — analog `renderNowTab` ale dział H. Gałąź `tab==='money'` w `renderMainPanel`.

**Zakaz treści:** LinkedIn drip, sekwencje GPT, ads, darmowy POC, „jeszcze jeden moduł zamiast rozmowy”, BANT.

---

## ŹRÓDŁA — briefing

Nie dump 30 URL. Above-fold **3 karty:**

1. Źródło **dzisiejszego** rozdziału (`firstOpen()`)
2. Docs **pętli** (handbook / HOWTO)
3. Jedna **bramka/spec** (kontrakt / LOCAL-GATE / schema)

Szablon karty: typ · tytuł · jedno zdanie `why` · jeden przycisk Otwórz.

Below: archiwum A–H w zagnieżdżonych `<details>`, max 1 grupa open. „Blog ≠ dowód” = jedna linia w archiwum.

`function renderSourcesTab()`. Usuń wywołania `renderSources(key)` ze ścian działów (zostaw funkcję jako helper kart, jeśli używasz `SOURCES_DATA`).

---

## Guardy, które explodują, jeśli zmienisz HTML bez walidatora

Dziś `scripts/validate-academy-export.py` i Fala 0 **wymagają** starego świata. Każdy PR UI **w tym samym commicie** aktualizuje guardy. Inaczej `deploy-ready` FAIL.

| Dziś (live `4632afb`) | Po PR (v6) |
|---|---|
| `ACADEMY_TAB_COUNT=6` + `tab_count != 6` | `=8` + krotka 8 id w kolejności wyżej |
| `TAB_BY_DZIAL.H` musi być `dsaas` | musi być `money` |
| Fala 0 A3: „zamiast 6”; A8: `H:'dsaas'` | A3: zamiast **8**; A8: mutacja `H:'money'` → `H:'dsaas'` **albo** `H:'kurs'` musi FAIL |
| `academy-ux-v5: brak legendy` | **zakaz** `#nav-legend`; nowy prefiks `academy-ux-v6` |
| `id="dsaas-flows"` + 7 `renderDiagram` | scena 1 mermaid; guard: brak `.grid.two` z 7 diagram-card above-fold |
| H1 H2 H3 w `DZIAL_DATA` | + **H4** |
| brak `{id:'money'` / `sources` | wymagane; mutacja „zabrano MONETYZACJA albo ŹRÓDŁA” FAIL |
| `#course-map` nie istnieje | wymagane 8 `[data-course-dzial]` A–H |

Fala J: nowy `scripts/mutation-test-*.py` = ten sam PR dopina [`.github/workflows/academy-gate.yml`](../../.github/workflows/academy-gate.yml) **i** linię `testy:` w [`AGENTS.md`](../../AGENTS.md).

Schema eksportu **0.1.0** bez zmian. `source` academy-os.

---

## Poza scope

- Wymyślanie EUR / wysyłka 10 maili jako zaliczenie.
- 7. dział Kokpitu.
- Deploy VPS bez GO.
- Płatny GitHub Actions (`academy-gate.yml` zostaje `workflow_dispatch`).
- Zmiana architektury vault / `/ops`.
- Osobny przycisk KURS.

---

## Kolejność PR-ów Cloud (jeden PR = jedna myśl)

Nie łącz 8 tabów + rewrite H + 3 strefy w jednym diffie >400 linii bez podziału.

1. **Lock 8 tabów** — `ACADEMY_TABS` + `renderMainPanel` gałęzie `money`/`sources` (placeholdery OK) + `TAB_BY_DZIAL.H='money'` + walidator + mutacje A3/A8. DSAAS może chwilowo bez H w accordionie.
2. **Chrome kill + `#course-map`** — hero/sync/bar/legend/nowcard/tty. Guardy ux-v6 (legenda zakazana).
3. **DSAAS 3 strefy** + layers mermaid w WORKFLOW `<details>` + `PLATFORM_BIBLE`.
4. **`renderMoney()`** + rewrite lab H1–H4 (LEARN+DO). Placeholdery z PR1 znikają.
5. **`renderSourcesTab()`** 3 karty + wycinanie `renderSources` z działów.
6. **Testy + smoke 360px** (8 tabów, mapa klika, DSAAS 1 mermaid, H1 na money, ŹRÓDŁA 3 karty). Handoff. **Stop.** Czekaj GO na deploy.

Lokalna bramka: `bash scripts/deploy-ready-hermes-ops.sh` (Git Bash). Nie trzymaj `python -m http.server` na `DASHBOARD.html` na Windows (OSError 22 / lock pliku).

---

## Prompt dla agenta Cloud (wklej)

```
Repo akademia. SoT: docs/ops/PLAN-AKADEMIA-SZTAB-2026-09-25.md + docs/ACADEMY-UX-SPEC.md v6.
Nie ruszaj /ops poza linkiem. Nie deployuj. Nie usuwaj tabów. Kokpit = 6 działów.
Zrób TYLKO kolejny otwarty PR z listy 1–6 w planie. W tym samym PR zaktualizuj
validate-academy-export.py i mutacje, które ten PR psuje.
Pełna linia testy: z AGENTS.md przed zgłoszeniem.
```
