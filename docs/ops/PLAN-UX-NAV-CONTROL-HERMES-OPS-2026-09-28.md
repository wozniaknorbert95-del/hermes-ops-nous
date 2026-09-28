# PLAN — nawigacja i kontrola Hermes Ops (`/ops`)

**Status:** SPECYFIKACJA + **P0–P3 WYKONANE lokalnie** (P0 live `01afcfe`; P1–P3 na gałęzi, deploy po GO).  
**Data:** 2026-09-28  
**UI:** `akademia/OPS.html` (`/ops`)  
**Payload:** `GET /ops/status` · komendy: `POST /ops/run` (`host/progress_vault.py`)  
**Źródła:** ten inwentarz z live HTML; luki z [`docs/handoffs/2026-09-28-preflight-fix-ux-roadmap.md`](../handoffs/2026-09-28-preflight-fix-ux-roadmap.md) §4; piksele już wdrożone = [`UX-SPEC-HERMES-OPS-ENTERPRISE.md`](UX-SPEC-HERMES-OPS-ENTERPRISE.md).

**Nie jest to:** kurs Akademii (`DASHBOARD.html`), paleta 38 komend platformy, deploy z telefonu.

---

## 1. Cel + persona + job (2 minuty)

**Persona:** Dowódca na telefonie (360px) i laptopie (≥960px). ADHD-first: jeden gest, zero zgadywania.

**Job w 2 minuty:**

1. Czy mogę ruszyć? (pre-flight 6× ✓/✗ + pill silnika)
2. Co ruszy? (Next-card: id + DoR/lane)
3. Jeden gest Start / Run next
4. Gdzie jest dowód / granica / deploy? (Wynik + Live proof + panel Deploy gdy `ready`)

To **control plane**, nie dashboard analityczny. HITL = etykieta w Linear *zanim* agent ruszy, nie przycisk Merge.

---

## 2. Zasady twarde (nie łamać w implementacji)

1. **Zasada 11** — deploy tylko laptop, ręcznie, GO Dowódcy. Zero `deploy` / `workflow_dispatch` w `POST /ops/run`.
2. **Telefon nie merguje** — zero akcji `merge` / `request_changes`.
3. **UNKNOWN nigdy zielone.** QUEUED ≠ RUNNING (HUD optymistycznie tylko QUEUED).
4. **Tylko AUTOPILOT** — nie przywracać MANUAL / SUPERVISED / `.mode` toggle.
5. **`#btn-take`** + `data-ops="take_over"` zostają (guard CI). Copy STALLED / QUEUED / NO-ACK / REFUSED / `cursor_wake` / `Cloud: /autopilot` — zmiana stringu = ten sam PR co `scripts/validate-academy-export.py`.
6. Paleta `/autopilot` = repo **platformy**. Akademia nie dostaje 5. rytuału slash.
7. Zero sekretów, zero tokenów w URL. Proof-linki tylko `https?`.
8. `/ops` nie jest 8. tabem Akademii.

Allowed `action` w vault: `run_next` · `pause` · `stop` · `retry` · `start` · `take_over` · `run_all` · `set_mode` · `autopilot`.

---

## 3. Katalog sterowania (as-is)

Kolumny: **Pokazuje** / **Robi** / **Nie robi** / **Stan**.

### 3.A Gesty komend — `POST /ops/run`

| Id / `data-ops` | Pokazuje | Robi | Nie robi | Stan as-is |
|---|---|---|---|---|
| `#btn-run` `run_next` \| `start` | `▶ Run next` albo `▶ Start pętli` (gdy PAUSED) | Kolejkuje tick na `next.id` / `issue_id`. HUD → QUEUED. `title` = lista ✗ pre-flight gdy disabled. | RUNNING bez ack. Merge. Deploy. | **Primary.** `disabled` gdy UNKNOWN albo dowolny pre-flight ✗ (wyjątek: `slot` gdy `live.issue`). |
| `#btn-pause` `pause` | `⏸ Pause` | `engine`/`status` PAUSED. **Nie** bumpuje `updated_at` (Pause ≠ żywy tick). | Resume. Start agenta. | Secondary, `.ghost`, zawsze widoczny. |
| `#btn-stop` `stop` | `⏹ Stop` | STOPPED. Halt kolejki. | Resume (to jest Start). Deploy. | Secondary, `.ghost`. |
| `#btn-retry` `retry` | `↻ Retry` | Jak run na **tym samym** `live.issue` (inaczej next). | Nowy issue z kolejki. Retry loop przy cap / REFUSED token. | Secondary, `.ghost`. `hidden` gdy DONE. Duplikat w dispatch. |
| `#btn-take` `take_over` | `👤 Take over` | PAUSED, „laptop, zero @cursor”. Tick nie budzi Cloud. | Merge. Potwierdzenie (brak confirm). | Tertiary, `.danger` full width. Copy pod spodem; brak `title`/dialog. **Id stały.** |
| `#btn-run-all` `run_all` | `Run all` | Burst kolejki (cap dnia). | Domyślny fold. | `hidden` dopóki `run_all_enabled`. **Nie eksponować** bez jawnej polityki cap. |

Dispatch (`#dispatch-banner`) **klonuuje** Retry i/lub Take over przy NO-ACK, STALLED, FAIL, części REFUSED. To ten sam `send()`, nie osobna semantyka.

### 3.B Duplikaty i martwy DOM

| Element | Pokazuje | Robi | Nie robi | Stan |
|---|---|---|---|---|
| `#panel-steer` | nic | nic | Sterowanie (jest na foldzie) | `hidden`, pusty. **Usunąć z DOM** w implementacji. |
| CSS `.modes` / `.mode` | (brak HTML) | — | Przełącznik 3 trybów | Martwy CSS. **Nie przywracać** MANUAL. |
| `ensureTickAutopilot()` | — | raz `set_mode` AUTOPILOT | Wybór trybu przez usera | Zostaje, nie UI. |

### 3.C Nawigacja (nie steruje pętlą)

| Element | Pokazuje | Robi | Nie robi | Stan |
|---|---|---|---|---|
| `.issue[data-issue]` | id + tytuł + repo + hint „Kolejka nie udaje Run” | `window.open(found.url)` gdy jest `it.url` | Run / Start. `data-run` zawsze `"0"`. | **Affordance zła:** wygląda jak akcja pętli; brak ↗; bez URL = martwy tap. |
| `.more[data-expand]` | `Pokaż jeszcze N` / `Zwiń listę` | Toggle `laneExpanded` (preview 4) | POST | OK jako expand. |
| Pulse (`#pulse-list`) | 3 issue platformy + chip DoR | nic | Link Linear | Display-only. **P0:** dodać URL jak Approval. |
| Active agents | id, worker, S, bar | nic | Sterowanie agentem | Display-only (max 1). |
| Approval `Otwórz ↗` | kind + id + message | `href` `pr_url` lub `url` | Merge | Link **jest**. Fallback HITL: id jako `<a href=it.url>`. |
| Stopka `← Akademia (kurs)` | link | `href="/"` | 8. tab | Zostaje. |

### 3.D Proof-linki (navigate-out, fail-closed `https?`)

| Etykieta | Źródło | Robi | Nie robi |
|---|---|---|---|
| `issue #n ↗` | `proof.github_issue_url` / `live.github_issue_url` | GitHub twin | Wake bez URL (wtedy span, nie link) |
| `comment sent ↗` | `cursor_comment_url` | Komentarz `@cursor` | |
| `PR ↗` | `proof.pr_url` | PR | Sam `pr_number` bez URL = span |
| `CI ↗` | `proof.ci_url` | Checks | |
| `Agent run ↗` | `proof.agent_run_url` | Cursor Cloud run | |
| Wynik `↗` | `run_result.done[].url` | Ten sam kontrakt https | Werdykt po stronie klienta |
| Deploy `PR #n ↗` | `deploy_readiness.pr_url` | PR do ręcznego deploy | Deploy z UI. Panel `hidden` gdy `!ready` |

### 3.E Display-only (nie tap)

| Id | Pokazuje | Semantyka |
|---|---|---|
| `#engine-pill` | UNKNOWN / QUEUED / RUNNING / PAUSED / STOPPED / STALLED / NO-ACK / REFUSED / DONE / FAIL | UNKNOWN = `pill unk`. Dispatch state ma pierwszeństwo przed kłamliwym RUNNING. |
| `#mode-pill` | `AUTOPILOT` | Zawsze. |
| `#report-line` | jednolinijkowa synteza `report.line` | Odczyt. |
| `#next-title` + chipy | issue + DoR / lane / testy / CI / todo | „Co ruszy”, bez *dlaczego*. |
| `#run-truth` | `Cloud: /autopilot — …` | Guard walidatora. |
| `#preflight-checks` | 6× ✓/✗: DoR, tor, tick, CI, slot, cap | Blokuje `#btn-run`. Nie są przyciskami. |
| Pasek S0–S6 | `aria-valuenow` 0–6 | Postęp, nie tap. |
| `#health-banner` | UNKNOWN / no_cache / LINEAR / cache >12 min | Ostrzeżenie; nie gest. |
| Dashboard stats | Runs / Merged / Failed / Waiting | Dziś. |
| Dziennik | te same 4 liczby + cap + `live.recent` (max 8) | Historia. |

---

## 4. Docelowa IA

Warstwy bez zmiany produktu:

1. **STERUJE** (fold, sticky HUD): raport → Next → pre-flight → **primary Start** → secondary Pause/Stop → tertiary Retry + Take over (Take over węższy/ghost-danger, nie full-bleed obok Start) → dispatch (tekst, bez klonów przycisków albo z jednym „użyj Retry u góry”) → **Wynik** → **Deploy** gdy `deploy_readiness.ready` (natychmiast pod HUD, nie na końcu `main`).
2. **KONTEKST:** Live (S + proof) → Kolejka (linki Linear) → Dashboard/pulse (linki) → Approval (nie Merge).
3. **DZIENNIK:** pełna szerokość, pod spodem; collapse OK (P2).

**Fold 360px:** jedna kolumna, kolejność jak wyżej. 2-col grid tylko `min-width: 960px` (dziś `body` `max-width: 720` do media 960 — desktop 2-panel działa od 960 przy `max-width: 1200`).

**Desktop ≥960:** lewa = wynik + deploy; prawa = live + queue + dash + approval; dziennik `grid-column: 1 / -1`. HUD nadal sticky nad gridem.

Usunąć `#panel-steer`. Nie dodawać tabów w Akademii.

---

## 5. Hierarchia wizualna i ról

| Rola | Elementy | Wygląd docelowy |
|---|---|---|
| **Primary** | `#btn-run` | Jeden, full width, `--accent`. Jedyny gest „rusz pętlę”. |
| **Secondary** | Pause, Stop | `.ghost`, równe, **mniejsze** niż Start (nie 33% w jednym rzędzie ze Start). |
| **Tertiary** | Retry, Take over | Retry ghost; Take over danger **nie** `width:100%` na równi ze Start. Confirm (P2). |
| **Navigate-out** | kolejka, pulse, approval, proof, deploy PR, stopka | Wyglądają jak **linki** (`<a class="proof-btn">` / ↗), nie jak `.btn` pętli. |
| **Display-only** | pille, chipy, pre-flight, stats, dziennik | Zero `cursor:pointer` poza prawdziwym href. |
| **Ukryte** | `#btn-run-all` | Tylko flaga `run_all_enabled`. |

Copy: **gest EN** (kontrakt `data-ops`: Run next, Pause, Stop, Retry, Take over) + **`aria-label` i jedna linia PL** pod grupą (już jest przy Take over; dodać analogicznie przy Start: „Kolejkuje tick. To nie jest merge.”).

---

## 6. Luki vs kokpit (zamknięte P0–P3)

1. Affordance kolejki / Pulse bez ↗. **P0**
2. Brak *dlaczego ten issue* + przycisk „Użyj tego”. **P0**
3. Deploy schowany na dole `main` gdy `ready`. **P1**
4. Pause/Stop/Retry ten sam `.ghost`; Take over krzyczy full danger. **P1**
5. Mix EN/PL bez `aria-label`. **P1** (linia PL + `aria-label` przy Start)
6. Take over bez confirm. **P2**
7. Brak sticky H2 poza HUD; skip-link do `#panel-live`. **P2**

---

## 7. Backlog implementacji (po GO)

| # | Atom | Priorytet | Pliki |
|---|---|---|---|
| 1 | Kolejka + Pulse: widoczny Linear `href` (nie goły `button` udający Run). Hint zostaje. | **P0 WYKONANE** | `OPS.html` `renderLane` / `renderPulse` |
| 2 | `recommended_issue` w vault + UI „dlaczego” + „Użyj tego” (ustawia next, **nie** startuje sam) | **P0 WYKONANE** | `host/progress_vault.py` + `OPS.html` + `test_progress_vault.py` |
| 3 | IA: Deploy pod HUD gdy `ready`; wynik tuż pod sterowaniem; usunąć `#panel-steer` | **P1 WYKONANE** | `OPS.html` HTML/CSS grid |
| 4 | CSS hierarchia Primary/Secondary/Tertiary | **P1 WYKONANE** | `OPS.html` CSS |
| 5 | Dispatch: zero klonów przycisków albo jeden CTA „Retry u góry” | **P1 WYKONANE** | `OPS.html` `renderDispatch` |
| 6 | Confirm + `title` na Take over | **P2 WYKONANE** | `OPS.html` JS (`#btn-take` zostaje) |
| 7 | Collapse sekcji KONTEKST/DZIENNIK + `localStorage` | **P2 WYKONANE** | `OPS.html` |
| 8 | Sticky `h2` desktop; opcjonalnie skip-link | **P2 WYKONANE** | `OPS.html` CSS |
| 9 | Skróty: Enter = Start (gdy enabled), Escape = Pause, R = Retry — tylko gdy focus nie w polu | **P3 WYKONANE** | `OPS.html` JS |

Jeden atom = jeden PR. Zmiana copy HUD / STALLED = walidator w tym samym PR. Nowe pole status = test vault.

---

## 8. DoD tego dokumentu (spełnione, gdy spec jest w repo)

- [x] Katalog A–E: każde sterowanie ma Pokazuje / Robi / Nie robi / Stan
- [x] IA fold + desktop, hierarchia ról
- [x] Backlog P0–P3 spisany; implementacja P0–P3 w OPS.html
- [x] Zero sekretów, zero 8. tabu Akademii, zero palety 38

## 9. DoD implementacji P0 (spełnione + live 2026-09-28)

- [x] validate-academy-export + test_progress_vault + test_hermes_intent PASS
- [x] Mutacje Fala Q: 13/13 (P0 href + P1–P3 IA); pozostałe fale bez zmian kontraktu
- [x] `#btn-take` / `take_over` / `Cloud: /autopilot` / UNKNOWN nie-zielone
- [x] Zero `JSON.stringify(live)`, zero `$0.00`, zero MANUAL
- [x] Smoke `/ops` po deploy (Zasada 11, GO Dowódcy) — `SMOKE PASS`, `/ops/diag` ok+tick_alive, `recommended_issue` QUI-104 `dor_ok` selected=true HTTPS

## 9b. DoD implementacji P1–P3 (lokalnie 2026-09-28, deploy po GO)

- [x] `#panel-steer` usunięty; Wynik + Deploy w DOM przed Dashboard
- [x] Hierarchia: Start full; Pause/Stop `steer-sec`; Take over nie `width:100%`
- [x] Dispatch bez klonów `<button>`; hint „Użyj Retry u góry”
- [x] Take over: `title` + `confirm`; `#btn-take` zostaje
- [x] KONTEKST / DZIENNIK: `<details>` + `localStorage`
- [x] Sticky h2 desktop ≥960; skip-link `#panel-live`
- [x] Enter=Start (gdy enabled), Escape=Pause, R=Retry; nie w INPUT
- [x] Mutacje Fala Q Q7–Q13 łapią regresje IA

---

## 10. Świadomy non-scope

- `DASHBOARD.html` / 7 tabów Akademii
- Tick w `workflow-lab` (producent `live.recent` / proof)
- Hook deny-deploy, skills Cursor
- Deploy VPS z tej specyfikacji (P0 live 2026-09-28; P1–P3 po merge + GO deploy)
