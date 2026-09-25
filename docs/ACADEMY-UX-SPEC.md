# Academy Command Dashboard — UX spec (local-first, v6)

**Cel:** w 10 sekund wiesz **który dział A–H** i **jaki jeden krok**. Chrome nie uczy. Szum schowany.  
**Plan wdrożenia:** [`docs/ops/PLAN-AKADEMIA-SZTAB-2026-09-25.md`](ops/PLAN-AKADEMIA-SZTAB-2026-09-25.md).  
Live do czasu PR Cloud: 6 tabów (v5). Ten dokument opisuje **docelowy** kontrakt v6.

## 1. Użytkownik i kontekst

- Właściciel (ADHD-friendly): laptop + telefon; nauka na `/`, pętla inżynierska na `/ops` (osobna PWA).
- Urządzenia: mobile-first (360px), desktop max 1180px. Offline/file:// musi działać; HTTPS + vault = ten sam stan telefon/laptop.
- Ograniczenia (`AGENTS.md` akademii): jedno TERAZ; eksport v0.1.0; brak iframe Kokpitu; brak 7. działu Kokpitu; zero sekretów.
- Taby Akademii: **8**. `/ops` nie jest dziewiątym tabem.

## 2. Osiem zakładek

| Zakładka | `id` | Pytanie | Główna akcja |
|---|---|---|---|
| `TERAZ` | `now` | Co robię w tej minucie? | Jeden rozdział: kroki lab + zaliczenie + CTA **Hermes Ops** |
| `WORKFLOW` | `workflow` | Jak wygląda **jedna** pętla? | Chip Telefon/Laptop + playbook + bieżący A. Layers mermaid w `<details>` |
| `NARZĘDZIA` | `tools` | Co działa naprawdę? | Karty `TOOL_DATA`; scoreboard w `<details>` |
| `DSAAS` | `dsaas` | Jak skonfigurować platformę, by tenant dawał wynik? | 3 strefy above-fold + biblia plik→obowiązek. B–G. Nie H |
| `MONETYZACJA` | `money` | Jak wziąć pieniądze za skan/pilot? | H1–H4 LEARN+DO. Zero mermaid. Zero pola EUR |
| `ŹRÓDŁA` | `sources` | Co czytam **dziś**? | 3 karty + archiwum w `<details>` |
| `NOTATKI` | `notes` | Co zapisałem? | `_scratch.notes` + Calm mode |
| `DZIEŃ` | `day` | Jaki rytuał? | Poranek/wieczór + sync; **nie** zleca PR |

**Hermes Ops:** `/ops` — Control Plane. Link w hero. Nie tab.

**Nawigacja:** nieaktywne taby neutralne; aktywna = `--nav-active`. Kolory działów tylko w accordionach / mapie A–H. **Zakaz** `.nav-legend`. 360px: 2×4, `min-height: 44px`.

**Legacy:** `guide`, `hermes`, `kurs` → zakładka DSAAS + scroll. `dsaas` / `#dsaas` → werdykt produktu. `#money` / `#sources` = ID tabów. `data-go-tab="workflow"` / `"tools"` / `"money"` / `"sources"` otwierają właściwe zakładki.

**Reguła TERAZ:** panel = jedyne TERAZ. `#nowcard` zawsze ukryty.

**Sync:** tylko `#tty-sync` (kropka Online/Offline). **Zakaz** `#sync-bar` jako drugi pasek z nazwą zakładki.

## 3. Chrome kill-list (fold)

**Widoczne:** `h1` = **Akademia** · `Hermes Ops →` · `nav#course-map` · `nav#tablist` · `#main-panel`.

**Zakaz na foldzie (usuń z DOM, nie chowaj `display:none` jako „rozwiązanie”):**

- `.hero .sub` („Jeden rozdział naraz…”)
- `#sync-bar`
- `#barwrap` / `#pct` / `#remain` / morał „Dziś wystarczy jeden”
- `#nav-legend`
- `#tty-left` / `#tty-right`
- `phone-first-banner` (WORKFLOW i stara mapa KURS)
- globalne „1 z 29 rozdziałów” jako karta

**Mapa A–H** (`#course-map`): 8 przycisków; fill per-dział; `is-current` = dział `firstOpen()` (pusty = H). Klik = tab + scroll do działu. To nawigacja, nie jeden `progressbar`.

## 4. DSAAS — 3 strefy

Above-fold: (1) werdykt ≤4 linie, (2) jeden mermaid + chip-picker 7 przepływów, (3) jeden otwarty dział B–G.  
Below-fold `<details>`: misja, scoreboard, mastery, INSTRUKCJA (0 open), Hermes, `PLATFORM_BIBLE`.  
Zakaz: 7 kart mermaid naraz; H w accordionie DSAAS; first-card „Dwie warstwy workflow-lab…”.

## 5. MONETYZACJA

Ścieżka H1–H4, jeden stopień otwarty. LEARN potem 1–2 ROBISZ. Papier SKU/outreach/checklist = link po lekcji, nie DoD.  
Zakaz: mermaid, input ceny, „wyślij 10 maili”, LinkedIn drip, ads, darmowy POC.

## 6. ŹRÓDŁA

3 karty: źródło bieżącego rozdziału · docs pętli · jedna bramka. Archiwum A–H w `<details>`.  
Zakaz: dump listy URL above-fold; `renderSources()` jako ściana na dole każdego działu.

## 7. Stany

- Pierwszy start: welcome ≤3 kroki; PWA w `<details>`; primary → **TERAZ**; pusty postęp → **H1** (`KURS_DZIAL_ORDER`, nie `ALL_ROZ`).
- Mapa A–H zawsze widoczna (nie zwijaj całego widgetu przy 0% — to nawigacja).
- Sync vault, PWA, export — schema 0.1.0 bez zmian.
- Kotwice `#roz-*` otwierają tab z `TAB_BY_DZIAL` (H→`money`, A→`workflow`, B–G→`dsaas`).

## 8. Motion

- Migający cursor w `.nowcard .tag`: nieistotne po ukryciu karty. Calm mode nadal tłumi cienie w panelu.
- `prefers-reduced-motion: reduce` — zero animacji fill na mapie.

## 9. Odbiór (DoD v6)

- `python scripts/validate-academy-export.py` → PASS (`academy-ux-v6` + `ACADEMY_TAB_COUNT=8`)
- Pełna linia `testy:` z `AGENTS.md`
- Walkthrough 360px: TERAZ, mapa A→H klik, WORKFLOW (layers w details), NARZĘDZIA, DSAAS (1 mermaid + 1 dział), MONETYZACJA (H1 LEARN), ŹRÓDŁA (3 karty), NOTATKI (calm), DZIEŃ
- Zero `#nav-legend`, zero `.hero .sub`, zero 7 mermaid-card above-fold
- Deploy: **GO Dowódcy (Zasada 11)** — nie w tym samym PR co pierwsza fala UI

**Powiązane:** [`PLAN-AKADEMIA-SZTAB-2026-09-25.md`](ops/PLAN-AKADEMIA-SZTAB-2026-09-25.md) · [`docs/ops/README.md`](ops/README.md)
