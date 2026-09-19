# Audyt UX/UI + plan napraw — Akademia Command Dashboard v3.1 (2026-09-19)

**Zakres:** `DASHBOARD.html` + `manifest.webmanifest` + `icons/` (repo `akademia`).
**Metoda:** live walkthrough (Chrome DevTools MCP) — pomiary DOM/layoutu, axe-core 4.10.2,
console + network,klawiatura, viewporty 375 / 390 / 768 / 1024 / 1280 / 1440 / 1920,
offline (`file://` + brak CDN), throttling Slow 4G + CPU 4×, real-flavour input battery.
**Zasada:** `max efekt / min złożoność` — żadna zmiana nie łamie kontraktu walidatora
(`proofHref:` = 14, klucze `DIAGRAMS`, jedno `#nowcard`, brak `alert(`).

## 0. Persona (zablokowana)

**Dowódca (R1).** ADHD-first. Laptop + telefon. Sesje 30–45 min. Na telefonie w przerwie
między zadaniami. Pyta jedno: *„co robię w tej minucie?”*. Nie czyta docsów, nie debuguje.
Ufa kolorom i pozycji. Jeśli coś wygląda na zepsute — ucieka z ekranu i nie wraca tego dnia.

## 1. Verdict

**Stan PRZED (wyjściowy) — FAIL:**

```
Console: 1 error (favicon 404), 1 warning (deprecated meta), 1 verbose (password bez <form>)
Network: 1× 404 (favicon.ico)
axe:     0 Critical, 1 Serious (color-contrast #welcome-dismiss)
Layout:  0 collapse (375–1920)   Perf: LCP 144 ms / CLS 0 / INP 0 ms → GREEN
```

**Stan PO (zweryfikowany ponownie — PASS):**

```
Console: 0 errors / 0 warnings / 0 verbose
Network: 0× 4xx/5xx     axe: 0 Critical / 0 Serious (40 passes)
Mobile 375: --scroll-offset 128 px vs sticky 114 px → 14 px zapasu (było -26 px)
Klawiatura: roving tabindex 0,-1,-1,-1,-1 · Home/End OK · fokus zostaje na zakładce
Round-trip: Zalicz A1 → A2 odblokowany → Cofnij A1 → A2 zablokowany
Offline (file://, brak CDN): diagramy jako tekst + komunikat
Walidatory: validate-academy-export PASS · test_progress_vault PASS
```

## 2. Findings

| ID | Sev | Warstwa | Co | Dowód |
|---|---|---|---|---|
| F-01 | **Critical** | Feedback | `/favicon.ico` → 404 + console error. Brak `<link rel="icon">`. | `list_network_requests` reqid=4 [404]; console msgid=3 |
| F-02 | **High** | Feedback | Console warning: `apple-mobile-web-app-capable` deprecated. | console msgid=2 |
| F-03 | **High** | Visual | `axe color-contrast` Serious: `.btn` `#08111f` na `--now #8b5cf6` = **4.47:1** (< 4.5). | `axe.run()` → `#welcome-dismiss`; pomiar: now=4.47, workflow=10.47, tools=8.81, dsaas=6.95, day=7.38 |
| F-04 | **High** | Interaction | `--scroll-offset: 88px` na sztywno, a sticky `.tabs` na 375 px ma **114 px** → cel kotwicy ląduje **26 px pod** paskiem zakładek. Telefon = persona główna. | pomiar: `tablistH=114`, `offsetVar=88`, `overlapPx=26` |
| F-05 | Medium | Interaction | Aktywacja zakładki (klik/Enter) gubi fokus → `activeElement === BODY`. `renderTabs()` przebudowuje DOM. | `focusAfterClick: "BODY (lost)"` |
| F-06 | Medium | Interaction | Brak roving tabindex — wszystkie 5 zakładek w tab-order (`tabIndex 0`). | `tabIndexes: [0,0,0,0,0]` |
| F-07 | Medium | Interaction | `role="tabpanel"` bez `aria-labelledby`; `#main-panel` ma `aria-live="polite"` → cały panel czytany przy każdej zmianie zakładki; cel skip-linku niefokusowalny. | `tabpanelLabelledby: null`, `mainPanelAriaLive: "polite"`, `mainPanelTabIndex: -1` |
| F-08 | Medium | Delight | Manifest ma tylko SVG (`sizes:"any"`). Chrome do instalacji wymaga PNG 192/512; iOS ignoruje SVG `apple-touch-icon` (potrzebne 180×180 PNG). Welcome każe „Dodaj do ekranu głównego” → ikona pusta/generyczna. | `manifest.webmanifest`; brak PNG w `icons/` |
| F-09 | Medium | Feedback | „Zalicz rozdział” jest **nieodwracalne** — brak undo/resetu w całym UI. | `unpassControls: 0`, `resetButtons: []` |
| F-10 | Medium | Feedback | Offline (brak CDN) diagramy cicho degradują się do surowego tekstu mermaid — `msg()` tylko w gałęzi `catch`, nie w gałęzi `!window.mermaid`. | `mermaidGlobal: "undefined"`, `fallbackCount: 2`, `statusMsg: ""` |
| F-11 | Low | Architecture | Statyczny HTML ma zaszyte `0% (0 z 24 rozdziałów)` — po dodaniu A7 prawda to 26; liczba rozjeżdża się z `DZIAL_DATA`, a przy padniętym JS użytkownik widzi kłamstwo. | `DASHBOARD.html` L29 vs `ALL_ROZ.length = 26` |
| F-12 | Low | Interaction | Pole hasła poza `<form>` (Chrome: *Password field is not contained in a form*) → menedżery haseł/autofill nie działają; telefon wpisuje hasło ręcznie co sesję. | console msgid=1 `[verbose]` |
| F-13 | Low | Visual | `.dzial-acc > summary` ukrywa natywny znacznik `<details>` bez zamiennika → 6 działów DSAAS wygląda jak zwykły tekst, brak afordancji „rozwijalne”. | `list-style:none` + `::-webkit-details-marker{display:none}`; 6/34 summary bez markera |
| F-14 | Low | Visual | `.mini` = 12.8 px, `.badge` = 11.52 px — za mało na telefon dla persony ADHD. | `getComputedStyle` pomiar |
| F-15 | Low | Visual | Brak `viewport-fit=cover` + `env(safe-area-inset-*)` → w PWA standalone treść może wchodzić pod notch. | brak w `<meta viewport>` / CSS |
| F-16 | Low | Architecture | Mermaid z CDN bez przypiętej wersji (`mermaid@latest`) → zachowanie i supply-chain zmieniają się bez commita. | `script src="…/npm/mermaid/dist/mermaid.min.js"` |

## 3. Plan napraw (quick wins — wszystkie tanie, additywne)

| ID | Naprawa | Plik |
|---|---|---|
| F-01 | `<link rel="icon">` (SVG + PNG 192) → przeglądarka nie pyta o `/favicon.ico` | `DASHBOARD.html` |
| F-02 | `+ <meta name="mobile-web-app-capable">` (apple zostaje dla starszego iOS) | `DASHBOARD.html` |
| F-03 | token `--ink:#04070d` dla `.btn` / `.tab[aria-selected]` → najgorszy akcent (`--now`) **4.76:1** | `DASHBOARD.html` CSS |
| F-04 | `--scroll-offset` liczone w JS z realnej wysokości `#tablist` (+ zapas), przeliczane na `resize` | `DASHBOARD.html` JS |
| F-05 | fokus wraca na aktywną zakładkę po re-renderze (`focus({preventScroll:true})`) | `DASHBOARD.html` JS |
| F-06 | roving tabindex (`0` dla aktywnej, `-1` dla reszty) + `Home`/`End` | `DASHBOARD.html` JS |
| F-07 | `aria-labelledby` na `tabpanel`, `tabindex="-1"` na `#main-panel`, usunięcie `aria-live` z panelu (zostaje na małych statusach) | `DASHBOARD.html` |
| F-08 | PNG 192/512 + apple-touch 180 (Pillow) → manifest + `apple-touch-icon` | `icons/*`, `manifest.webmanifest`, `scripts/make-icons.py` |
| F-09 | „Cofnij zaliczenie” na zaliczonym rozdziale (`data-unpass`) | `DASHBOARD.html` JS |
| F-10 | komunikat także gdy `!window.mermaid`; guard na `mermaid.init` | `DASHBOARD.html` JS |
| F-11 | statyczny licznik → neutralne `—`; `aria-valuetext` z JS | `DASHBOARD.html` |
| F-12 | poświadczenia vault w prawdziwym `<form>` (`autocomplete`, submit) | `DASHBOARD.html` |
| F-13 | chevron `summary::after` (`▸`/`▾`) dla działów | `DASHBOARD.html` CSS |
| F-14 | `.mini` → `.84rem`, badge/park-tag → `.74rem` | `DASHBOARD.html` CSS |
| F-15 | `viewport-fit=cover` + `env(safe-area-inset-*)` | `DASHBOARD.html` |
| F-16 | Mermaid przypięty do konkretnej wersji | `DASHBOARD.html` |

## 4. Świadomie POZA zakresem (i dlaczego)

- **Service worker / offline cache.** Deploy Akademii to `rsync/tar` bez hashowanych nazw plików.
  SW bez wersjonowania = realne ryzyko, że po deployu użytkownik dostanie **stary** DASHBOARD.
  Efekt (ikona + skrót na ekranie głównym) osiągamy samymi PNG w manifeście. SW = osobna decyzja.
- **Redesign IA / nowe zakładki.** Sprzeczne z `AGENTS.md` §4 („nie dodawać 7. działu”, jedno TERAZ).
- **`prefers-reduced-motion`** — już obsłużone, bez zmian.
- **Branding / zmiana palety** — nie; naprawiamy wyłącznie kontrast tam, gdzie łamie AA.

## 5. Ryzyka

| Ryzyko | Mitigacja |
|---|---|
| JS liczący `--scroll-offset` psuje `scroll-margin-top` (walidator tego pilnuje) | zostaje literał `--scroll-offset` + `scroll-margin-top` w CSS; JS tylko nadpisuje wartość |
| Dodanie przycisku „Cofnij” zmienia stan (`_pass=false`) | tylko istniejące klucze `*_pass`; zero migracji, zero nowych kluczy `_scratch` |
| Ikony PNG → zmiana kontraktu PWA | manifest dostaje **dodatkowe** wpisy; wpis SVG zostaje |
| Regresja walidatora | `python scripts/validate-academy-export.py` + `test_progress_vault.py` po każdej zmianie |

## 6. Weryfikacja (ponowny walkthrough na zmienionej wersji)

- [x] `python scripts/validate-academy-export.py` → PASS
- [x] `python scripts/test_progress_vault.py` → PASS
- [x] axe-core po zmianach → **0 Critical / 0 Serious** (40 rules pass; `color-contrast` w `incomplete` tylko dla tekstu na gradiencie `body` — ręcznie policzone 7.4–15.6:1)
- [x] console po zmianach → **0 errors / 0 warnings / 0 verbose**
- [x] network → 0× 4xx/5xx (żądanie `/favicon.ico` już nie powstaje)
- [x] 375 px: kotwica `#roz-A1` ląduje 14 px **pod** paskiem zakładek (`--scroll-offset` 88 → 128)
- [x] klawiatura: Enter na zakładce → fokus zostaje (`document.activeElement.id === "tab-dsaas"`); `←/→`, `Home`, `End` OK; roving tabindex `0,-1,-1,-1,-1`
- [x] „Cofnij zaliczenie A1” → `A1_pass` znika, A2 **ponownie zablokowany**
- [x] offline (`file://`, brak CDN) → diagramy jako tekst **z komunikatem**
- [x] resize 375 → 1440 → `--scroll-offset` przelicza się (128 → 76)
- [x] `#main-panel` `tabindex="-1"` → skip-link realnie przenosi fokus
- [x] brak poziomego przewijania na 375 / 1440

### Świadomie odłożone (backlog, nie „przy okazji”)

| Co | Dlaczego nie teraz |
|---|---|
| Service worker / offline cache | deploy = tar bez hashowanych nazw → ryzyko serwowania starego `DASHBOARD.html` |
| Vault: pierwszy realny PUT | `/opt/akademia/data` **nie ma `progress.json`** — sync telefon↔laptop nigdy nie zapisał danych; sprawdzić na HTTPS z telefonu |
| Playwright killer-flows | repo nie ma CI; wymaga decyzji o runnerze |

## 7. Follow-up (2026-09-19, po wdrożeniu): warstwa Jupyter widoczna

Powód: pierwsza aktualizacja (auto-merge + notebooki) opisała warstwę, ale **nie nazwała jej wprost** i nie było jej w loopach ani jako kafla — kontrakt walidatora blokował 15. kartę (`proofHref:14`).

| Element | Zmiana |
|---|---|
| Kontrakt | `proofHref` 14 → **15** + nowe twarde checki: `Jupyter`, `D-W7-JUPYTER`, `execute`, `notebook execute`, `DIAGRAMS.layers` |
| `NARZĘDZIA` | nowy kafel `Jupyter Notebook (lab)`; kafel `CI` przestaje twierdzić „dsaas 4 workflows”, mówi `validate + execute` |
| Loopy | `CI green` → `CI green: validate + execute` + **kropkowana** krawędź `notebook execute (opt-in)` w loopie telefonu i laptopa |
| NOWY diagram | `DIAGRAMS.layers` — Node core (validate→auto-merge) vs warstwa analizy (execute, opt-in) |
| `A7` | pełny: 7 → **14 plików** (`DECISIONS.md`, `.cursor/Dockerfile`, `review-bezpieczenstwa`, `.gitlab-ci.yml`, `AGENTS.md`, `ARCHITECTURE.md`, `TESTING.md`), +1 krok labu (Cloud Agents z telefonu) |
| Deep-link | `#roz-A7` otwiera zwinięte `<details>` i przełącza zakładkę na WORKFLOW (`openHashTarget`) |
| Źródła | `docs.jupyter.org`, `nbstripout` |
| Docs | `OPERATING-MODEL.md` v1.3, `README.md`, `cursor-kurs/szablony/README.md`, `ACADEMY-UX-SPEC.md` (§4 diagramy 8 szt., §5 kontrakty) |
