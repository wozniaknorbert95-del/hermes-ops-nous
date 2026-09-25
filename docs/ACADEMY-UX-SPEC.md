# Academy Command Dashboard — UX spec (local-first, v5)

**Cel:** w 30 sekund wiesz co robisz teraz w **kursie**, jak używać **narzędzi**, gdzie jest **workflow** laptop/telefon i że **praca agentowa = `/ops`**. Jeden fokus naraz (ADHD-first), **quiet landing** (U1–U5).

## 1. Użytkownik i kontekst

- Właściciel (ADHD-friendly): laptop + telefon; nauka na `/`, pętla inżynierska na `/ops` (osobna PWA).
- Urządzenia: mobile-first (360px), desktop max 1180px. Offline/file:// musi działać; HTTPS + vault = ten sam stan telefon/laptop.
- Ograniczenia (`AGENTS.md` akademii): jedno TERAZ; eksport v0.1.0; brak iframe Kokpitu; brak 7. działu; zero sekretów.

## 2. Sześć zakładek Akademii (IA v4.2 + kolory v5)

| Zakładka | Pytanie | Główna akcja |
|---|---|---|
| `TERAZ` | Co robię w tej minucie w kursie? | Jeden rozdział: kroki lab + zaliczenie + CTA **Hermes Ops** |
| `WORKFLOW` | Jak wygląda pętla pracy (laptop + telefon)? | Jeden banner skrótu + playbooki |
| `NARZĘDZIA` | Co działa naprawdę i jak tego nie zepsuć? | Karty `TOOL_DATA`; scoreboard w `<details>` |
| `DSAAS` (`id: dsaas`) | Gdzie jest platforma, mermaidy i mapa ról? | Produkt, mermaid, scoreboard, mastery, accordion **B–H** (H = monetyzacja), INSTRUKCJA (max 1 `<details open>`). Dział A = WORKFLOW. |
| `NOTATKI` | Co zapisałem dla siebie? | `_scratch.notes` + opcjonalny **Calm mode** (`_scratch.ui_calm`) |
| `DZIEŃ` | Jaki rytuał dnia kursu? | Poranek/wieczór + sync; **nie** zleca PR (to `/ops`) |

**Hermes Ops (osobny produkt):** `/ops` — Control Plane; nie jest siódmą zakładką Akademii.

**Nawigacja (v5):** nieaktywne taby neutralne; aktywna = `--nav-active`. Kolory działów tylko w `.dzial-acc` / kartach KURS. Legenda semantyki pod tabami (jedna linia).

**Legacy nawigacja:** `guide`, `hermes` → zakładka DSAAS + scroll. `dsaas` / `#dsaas` → blok produktu (nie INSTRUKCJA). `data-go-tab="workflow"` / `"tools"` otwierają właściwe zakładki.

**Reguła TERAZ:** Na zakładce TERAZ widoczny tylko panel (bez duplikatu `#nowcard`). Na innych zakładkach — kompaktowa karta TERAZ u góry (bez `filepath` na wąskim ekranie).

**Status:** `#sync-bar` = sync + nazwa aktywnej zakładki (bez osobnego `#zone-strip`).

## 3. Stany

- Pierwszy start: welcome ≤3 kroki; PWA w `<details>`; primary → **TERAZ**; pusty postęp → **H1**.
- Pasek postępu: **zwinięty** przy 0 zaliczonych rozdziałów.
- Sync vault, PWA, export — schema 0.1.0 bez zmian.
- Kotwice `#roz-*` otwierają zakładkę z `TAB_BY_DZIAL` (H→DSAAS `id: dsaas`, A→WORKFLOW).

## 4. Motion

- Migający cursor w `.nowcard .tag`: tylko gdy `prefers-reduced-motion: no-preference` i **brak** Calm mode.
- Calm mode: wyłącza animację tagu i redukuje cienie kart.

## 5. Odbiór (DoD v5)

- `python scripts/validate-academy-export.py` → PASS (guards `academy-ux-v5`)
- Pełna linia `testy:` z `AGENTS.md`
- Walkthrough 360px: TERAZ, WORKFLOW, NARZĘDZIA, DSAAS (H1 open), NOTATKI (calm), DZIEŃ
- Deploy: [`docs/DEPLOY-PLAN-AKADEMIA-2026-09-24.md`](DEPLOY-PLAN-AKADEMIA-2026-09-24.md) — **GO Dowódcy (Zasada 11)**

**Powiązane:** [`PLAN-UX-UI-AKADEMIA-2026-09-24.md`](PLAN-UX-UI-AKADEMIA-2026-09-24.md) · [`docs/ops/README.md`](ops/README.md)
