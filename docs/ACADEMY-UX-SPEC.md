# Academy Command Dashboard — UX spec (local-first, v7)

**Cel:** w 10 sekund wiesz **jaki jeden ruch** i **który DoD platformy**. Chrome nie uczy. Kurs = zakładka DSAAS.  
**Plan wdrożenia (reguły):** [`docs/ops/PLAN-AKADEMIA-START-2026-09-26.md`](ops/PLAN-AKADEMIA-START-2026-09-26.md).  
**Live HTML:** 7 tabów (v7). Deploy = WAITING-GO.  
**Narzędzia:** [`docs/ops/TOOL-MASTERY.md`](ops/TOOL-MASTERY.md).

## 1. Użytkownik i kontekst

- Właściciel (ADHD-friendly): laptop + telefon; nauka na `/`, pętla inżynierska na `/ops` (osobna PWA).
- Urządzenia: mobile-first (360px), desktop max 1180px. Offline/file:// musi działać; HTTPS + vault = ten sam stan telefon/laptop.
- Ograniczenia (`AGENTS.md`): jedno TERAZ; eksport v0.1.0; brak iframe Kokpitu; brak 7. działu Kokpitu; zero sekretów.
- Taby kontraktu: **7**. `/ops` nie jest ósmym tabem. Live = 7.

## 2. Siedem zakładek

| Zakładka | `id` | Pytanie | Główna akcja |
|---|---|---|---|
| `TERAZ` | `now` | Co dziś? | Poranek Hermesa + jeden ruch B–G + pasek 18 DoD + mix czasu + 1 linia `/ops` |
| `WORKFLOW` | `workflow` | Jakie zasady? | Chip Telefon/Laptop, 1 mermaid, zasady pod węzłami. A1–A7 w details |
| `NARZĘDZIA` | `tools` | Jak opanować narzędzie? | Karty `TOOL-MASTERY`. Lekcja `/ops` tylko tu |
| `DSAAS` | `dsaas` | Kim jestem i czego się uczę? | Tożsamość + 18 DoD B→G + 1 mermaid. Wave 2 Linear tutaj |
| `MONETYZACJA` | `money` | Jak wziąć pieniądze? | H1–H4 LEARN+DO. Nie `firstOpen`. Zero mermaid, zero EUR |
| `ŹRÓDŁA` | `sources` | Co czytam dziś? | 3 karty (dziś = rozdział B–G) + archiwum |
| `NOTATKI` | `notes` | Egzamin? | Notatka przy id rozdziału; wolny tekst na dole |

**Hermes Ops:** `/ops` — Control Plane. Link w hero + jedna linia na TERAZ. Nie tab. Nie karta „jak używać” na TERAZ.

**Nawigacja:** nieaktywne taby neutralne; aktywna = `--nav-active`. **Zakaz** `.nav-legend`. 360px: wrap, `min-height: 44px`.

**Legacy:** `guide`, `hermes`, `kurs` → DSAAS. `#day` → TERAZ. `#money` / `#sources` = ID tabów.

**Reguła TERAZ:** panel = jedyne TERAZ. `#nowcard` zawsze ukryty. Rytuał dnia + wieczór w jednym `<details>` „Ręcznie / wieczór”, nie druga karta. Polerka gęstości: [`ops/PLAN-UX-POLISH-2026-10-03.md`](ops/PLAN-UX-POLISH-2026-10-03.md).

**Sync:** kropka `#tty-sync`. Vault/eksport tylko w kole zębatym. **Zakaz** stopki zapisu na foldzie.

## 3. Chrome (fold)

**Widoczne:** `h1` = **Akademia** · `Hermes Ops →` · koło zębate · `nav#course-map` · `nav#tablist` · `#main-panel`.

**Zakaz na foldzie (usuń z DOM, nie chowaj CSS-em):**

- `.hero .sub`
- `#sync-bar`
- `#barwrap` / `#pct` / `#remain` / morał „Dziś wystarczy jeden”
- `#nav-legend`
- `#tty-left` / `#tty-right`
- `phone-first-banner`
- `renderOpsCta()` / karta „Praca — Hermes Ops”
- stopka vault/eksport/import/biblioteka
- globalne „1 z N rozdziałów” jako karta

**Mapa A–H:** 8 przycisków; fill per-dział; `is-current` = dział `firstOpen()` **wśród B–G** (pusty = **B**). Klik = tab + scroll. To nawigacja, nie jeden `progressbar`. H i A nie ustawiają `firstOpen` nauki.

**Koło zębate:** eksport, JSON, import, vault, schema 0.1.0, PWA.

## 4. TERAZ — brief, nie dwie strony

Kolejność above-fold: poranek → jeden ruch → pytanie z pamięci → pasek 18 DoD (+ kreski A/H) → mix `local|ops|phone` → linia kolejki.  
Wieczór: ten sam wzór, **pod** porankiem, po południu.  
LOCK zostaje kije. Odpoczynek ≠ LOCK.

Paski: nauka = DoD; godziny = diagnostyka (`_scratch.work_log`). Zero estymacji.

## 5. DSAAS — roadmapa tożsamości

Above-fold: (1) kim jesteś ≤6 linii, (2) ścieżka B→C→D→E→F→G, jeden dział otwarty, (3) jeden mermaid + 7 chipów.  
Biblioteka „Jak zaliczam” na górze (5 reguł).  
Linear Wave 2 pod F / details.  
Below-fold: biblia, scoreboard, mastery, misja.  
Zakaz: H w accordionie DSAAS; 7 mermaidów naraz; first-card warstw labu.

`firstOpen` nauki: B–G. Nie `KURS_DZIAL_ORDER` H-first.

## 6. WORKFLOW

Jeden mermaid trybu. Zasady pod diagramem. Węzeł → kotwica zasady. Pliki = dowód pod zasadą. Siłownia A + layers w details.

## 7. NARZĘDZIA

Pola karty: po co · kiedy tak/nie · max 3 linki producenta · 1–2 praktyków (nazwane; blog ≠ dowód) · jedna gotcha · jeden dowód „umiem” · status.  
Pełne: Linear, Cursor local, Cursor Cloud, Hermes Engineer (PARTIAL + WAITING-GO aż `conductor-slice-e2e.json`), GitHub, CI, Gitleaks.  
PARKED: skrót „nie startuj / warunek”.

## 8. MONETYZACJA

H1–H4, jeden stopień otwarty. LEARN + 1–2 ROBISZ. Papier po lekcji.  
Zakaz: mermaid, input ceny, 10 maili, LinkedIn, ads, darmowy POC.  
H nie kradnie TERAZ. H nie jest zablokowane do 18 DoD.

## 9. ŹRÓDŁA

3 karty: źródło bieżącego B–G (albo H na money) · docs pętli · bramka. Archiwum A–H w details.  
Zakaz: dump URL; `renderSources()` na ścianach działów.

## 10. NOTATKI

Notatka przy id rozdziału. Archiwum. Wolne pole na dole. `_scratch.notes`. Calm mode.

## 11. Stany

- Pusty postęp → **B1** (orkiestracja), nie H1.
- Welcome ≤3 kroki; PWA w kole zębatym / details.
- Mapa A–H zawsze widoczna.
- Schema 0.1.0 bez zmian.
- Kotwice `#roz-*` otwierają tab z `TAB_BY_DZIAL`.

## 12. Motion

Calm mode tłumi cienie. `prefers-reduced-motion: reduce` — zero animacji fill.

## 13. Odbiór

**Dokument + HTML:** `ACADEMY_TAB_COUNT=7`; kill `renderOpsCta` na TERAZ; `firstOpen` B–G. Pełna linia `testy:` (w tym Fala P). Smoke 360px: TERAZ (poranek, bez karty /ops), mapa A→H, WORKFLOW (zasady pod mermaid), NARZĘDZIA (karta Engineer), DSAAS (B otwarte, 1 mermaid), MONETYZACJA, ŹRÓDŁA (karta B), NOTATKI. Brak zakładki DZIEŃ. `#day` → TERAZ.

Deploy: **WAITING-GO**.

**Powiązane:** [`PLAN-AKADEMIA-START-2026-09-26.md`](ops/PLAN-AKADEMIA-START-2026-09-26.md) · [`HERMES-ROLE-CONTRACT.md`](ops/HERMES-ROLE-CONTRACT.md) · [`TOOL-MASTERY.md`](ops/TOOL-MASTERY.md)
