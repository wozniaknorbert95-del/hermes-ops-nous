# Plan aktualizacji Akademii — Linear OS Wave 2 (2026-09-13)

**Repo:** `akademia`  
**Autor planu:** sztab R1 (Cursor)  
**Status:** PLAN — bez edycji runtime / platformy  
**Kontekst platformy:** EV-335 · PR `feat/linear-os-wave2` (pending merge) · QUI-18 open

---

## 1. Cel

Dopasować `DASHBOARD.html` i dokumentację Akademii do stanu **Linear OS Wave 2 (partial)** na `dsaas-platform-main`, tak aby poranny start dnia w Akademii wskazywał właściwy tor **WF-P\***, aktualne widoki Linear i uczciwy scoreboard platformy — bez fałszywego sygnału „ENT-12 TERAZ” ani przestarzałego „Linear SETUP”.

**Zakres tego planu:** tylko repo `akademia`.  
**Poza zakresem:** merge PR platformy, Settings Linear (QUI-18 HITL), deploy VPS, kod runtime.

---

## 2. Stan wyjściowy (audyt 2026-09-13)

### 2.1 Platforma (SoT — read-only)

| Fakt | Źródło |
|------|--------|
| Projekt Linear `dsaas-platform-main` istnieje; WF-P2 = **PASS** | `dsaas-platform-main/docs/ops/PLATFORM-WORKFLOW-GATE.md` |
| 8 widoków zapisanych (CEO/Today, Execution, HITL, …) | `dsaas-platform-main/docs/ops/LINEAR-PLATFORM.md` §6 |
| Workflow 12 statusów MCP | `D-WF-LINEAR-OS-WAVE2` · QUI-18 |
| QUI-14 WF-P6 rytuały: **day 2/7**, due 2026-09-20 | `LINEAR-PLATFORM.md` §5 · QUI-14 |
| QUI-16 WF-P9 akademia: **Done** (PR #4 `a229ddc`) | `PLATFORM-DECISIONS.md` D-WF-P9 |
| QUI-18 Wave 2 HITL: **In Progress** (filtry, powiadomienia, GitHub scope) | `HANDOFF-LINEAR-OS-WAVE2-2026-09-13.md` |
| Rytuały platformy: pliki gotowe, tydzień użycia = PARTIAL | `MORNING-RITUAL-PLATFORM.md` · `EVENING-RITUAL-PLATFORM.md` |

### 2.2 Akademia — co jest dziś w `DASHBOARD.html`

| Obszar | Stan | Problem |
|--------|------|---------|
| **TERAZ** | Kurs (`firstOpen()` → rozdział A1…) | OK dla nauki; **nie** odzwierciedla toru WF-P6/QUI-18 — to zamierzone (UX spec: TERAZ = lekcja). Tor operacyjny = zakładka **DZIEŃ**. |
| **DZIEŃ → tor WF-P** | `torDefault = WF-P9 — sync vault` | **STALE** — QUI-16 Done; aktywny tor to **WF-P6** (QUI-14, 2/7) + równolegle QUI-18 (Dowódca HITL). |
| **DZIEŃ → rano 10 min** | Checklist labu (digest 7:30, runy agentów) | **Niespójne** z `MORNING-RITUAL-PLATFORM.md` (5 kroków: TERAZ → Linear → issue → git status → Today first). |
| **DZIEŃ → wieczór 5 min** | MR / Linear / 1 zdanie | Częściowo OK; brak linku do `EVENING-RITUAL-PLATFORM.md` i reguły WIP ≤ 3. |
| **NARZĘDZIA → `plat_linear`** | `SETUP` / „Brak projektu/URL” | **Fałszywe** — projekt i 8 widoków istnieją (Wave 2 partial). |
| **NARZĘDZIA → `plat_cloud`** | `R7 STOP` | **Niespójne** z WF-P5 PASS (smoke Cloud Agent PR #28); status powinien być uczciwy (np. PASS smoke / STOP produkcja). |
| **DSAAS → dział F** | F1–F3 tylko | Brak **F4 „Bramka workflow (WF-P\*)”** opisanego w `D-WF-P9` (PR #4 na remote — lokalny `main` @ `728f34a` **nie ma** tego merge). |
| **Linear links** | Brak | Brak szybkich linków do widoków §6 (CEO/Today, HITL, …). |

### 2.3 Dokumentacja Akademii

| Plik | Stan |
|------|------|
| `docs/OPERATING-MODEL.md` | v1.0 · 2026-09-12 — brak Linear platform PASS, brak odniesienia Wave 2 |
| `docs/ACADEMY-UX-SPEC.md` | v3.1 — DZIEŃ/WF-P* OK; brak specyfikacji linków Linear i rytuału platformy |
| `scripts/validate-academy-export.py` | Gate `"WF-P9 tor platformy"` — wymaga aktualizacji po zmianie domyślnego toru |

### 2.4 WIP — **NIE DOTYKAĆ** w tej sesji aktualizacji treści Linear

Gałąź `main` ma **niecommitowany** diff (handoff VPS sync):

```
M  DASHBOARD.html, AGENTS.md, docs/ACADEMY-UX-SPEC.md, …
?? host/, docs/handoffs/, docs/runbooks/, manifest.webmanifest, …
```

**Decyzja:** praca Linear OS Wave 2 w Akademii idzie na **osobną gałąź** (`docs/linear-os-wave2-akademia` lub kontynuacja `docs/qui-16-wfp9`), **po** zamknięciu lub commitnięciu WIP vault osobnym PR. Mieszanie obu torów = ryzyko regresji sync/PWA.

Źródło WIP: `docs/handoffs/2026-09-13-akademia-vps-sync-deploy.md`

---

## 3. Co zmienić — szczegółowy backlog

### 3.1 `DASHBOARD.html` — zakładka **DZIEŃ**

#### A. Tor platformy (`renderDay` → `torDefault` + placeholder)

| Było | Ma być (2026-09-13) |
|------|---------------------|
| `WF-P9 — Akademia sync vault + VPS (TERAZ)` | `WF-P6 — Rytuały platformy (QUI-14, dzień 2/7)` |

Dodać pod polem toru (read-only mini):

- Link: [QUI-14](https://linear.app/quietforge/issue/QUI-14)
- Równoległy tor HITL: [QUI-18](https://linear.app/quietforge/issue/QUI-18) (filtry/powiadomienia — Dowódca)
- `ENT-12` = **WAIT** (bez zmian tekstu bramki)

#### B. Rytuał poranny — align z platformą

Zastąpić / uzupełnić checkboxy w „Mój dzień — rano 10 minut” mapowaniem z `MORNING-RITUAL-PLATFORM.md`:

| Min | Checkbox (propozycja PL) | `data-k` (propozycja) |
|-----|--------------------------|------------------------|
| 0–2 | Otworzyłem DASHBOARD → **TERAZ** (jeden krok widoczny) | `day_teraz` |
| 2–4 | Otworzyłem Linear **dsaas-platform-main** — sprawdziłem In Review / blocked | `day_linear_proj` |
| 4–6 | Otworzyłem **jedno** issue priorytetowe (6 pól kompletne) | `day_one_issue` |
| 6–8 | `git status` w platform-main — czysty main lub feature branch | `day_git_clean` |
| 8–10 | Zapisałem linię **Today first:** (Linear comment lub PLATFORM-DECISIONS) | `day_today_first` |

**Migracja stanu:** stare klucze `day_digest`, `day_board`, `day_runs` — zachować w `_scratch` (nie kasować historii) lub mapować w `load()` jednorazowo; nowe klucze od dnia cutover.

Opcjonalnie: zostawić digest labu jako **collapsed** `<details>` „Lab (workflow-lab)” — nie mieszać z tor platformy.

#### C. Rytuał wieczorny — align z platformą

Uzupełnić checkboxy wg `EVENING-RITUAL-PLATFORM.md`:

| Checkbox | Treść |
|----------|-------|
| `day_wip` | WIP Linear ≤ 3 — zdjąłem skończone z In Progress |
| `day_mr` | (zachować) MR: approve / komentarz / zamknięty |
| `day_evidence` | PR merged → URL + check w issue Linear |
| `day_blockers` | Blockery oznaczone (`blocked` / `blocked:external`) |
| `day_next` | (zachować) 1 zdanie: co pierwsze jutro |

Link w stopce sekcji: `dsaas-platform-main/docs/ops/EVENING-RITUAL-PLATFORM.md` (ścieżka względna lub URL GitHub raw — **bez sekretów**).

#### D. Szybkie linki Linear (nowy `<details>` w DZIEŃ)

Tytuł: **„Linear — widoki platformy (Wave 2)”**. Tabela 8 linków z `LINEAR-PLATFORM.md` §6:

| Widok | URL |
|-------|-----|
| CEO/Today | https://linear.app/quietforge/team/QUI/view/ceotoday-1ef420fc07c0 |
| Execution | https://linear.app/quietforge/team/QUI/view/execution-7b7b81ee3be1 |
| HITL approvals | https://linear.app/quietforge/team/QUI/view/hitl-approvals-e0732a590998 |
| Security gate | https://linear.app/quietforge/team/QUI/view/security-gate-51544a7a21ff |
| Release board | https://linear.app/quietforge/team/QUI/view/release-board-bf9a81e03e09 |
| Agent queue | https://linear.app/quietforge/team/QUI/view/agent-queue-404a1ff192a4 |
| Technical debt | https://linear.app/quietforge/team/QUI/view/technical-debt-59fe0ebd6a72 |
| Client value | https://linear.app/quietforge/team/QUI/view/client-value-8191c191c6ea |

Projekt: https://linear.app/quietforge/project/dsaas-platform-main-d40484fe9522

---

### 3.2 `DASHBOARD.html` — scoreboard platformy (`PLATFORM_SCOREBOARD`)

#### `plat_linear`

```javascript
// BYŁO
{ id:'plat_linear', name:'Linear projekt platformy', status:'SETUP', tone:'warn',
  detail:'Brak osobnego projektu/URL w repo.' }

// MA BYĆ (Faza A — po merge PR platformy Wave 2 docs na main)
{ id:'plat_linear', name:'Linear OS platformy', status:'PARTIAL', tone:'warn',
  detail:'Projekt + 8 widoków ✅ (EV-335). Filtry/powiadomienia/GitHub = QUI-18 HITL.' }

// MA BYĆ (Faza B — QUI-18 Done)
{ id:'plat_linear', name:'Linear OS platformy', status:'PASS', tone:'ok',
  detail:'Wave 2 zamknięte: workflow 12 + widoki + filtry + powiadomienia (QUI-18 Done).' }
```

Dodać `proofHref` jako link do GitHub `LINEAR-PLATFORM.md` (jeśli scoreboard rozszerzymy o href — opcjonalnie w Fazie B).

#### `plat_cloud` (korekta uczciwości)

```javascript
// BYŁO: R7 STOP (myli z WF-P5 PASS)
// MA BYĆ:
{ id:'plat_cloud', name:'Cloud Agents na dsaas', status:'PASS SMOKE', tone:'ok',
  detail:'WF-P5: 1 MR smoke (PR #28). Produkcja / sekrety = nadal human-stop R7.' }
```

#### Pozostałe pozycje (bez zmiany w Fazie A)

| ID | Status | Uwaga |
|----|--------|-------|
| `plat_github`, `plat_ci`, `plat_gitleaks` | DONE | OK |
| `plat_bugbot` | SPRAWDZIC | Bez zmiany do osobnego issue |
| `plat_automations` | BRAK | OK — automations platformy poza falą |
| `plat_prod` | WAIT | OK — ENT-12 blocked |

---

### 3.3 `DASHBOARD.html` — dział **F** (moduł F / WF-P9)

**Luka:** lokalny `main` nie zawiera rozdziału **F4** z PR #4 (`a229ddc`).

Dodać (lub zsynchronizować z remote po pull PR #4):

```text
F4 — Bramka workflow platformy (WF-P*)
  pliki:
    - dsaas-platform-main/docs/ops/PLATFORM-WORKFLOW-GATE.md
    - dsaas-platform-main/docs/ops/LINEAR-PLATFORM.md
    - dsaas-platform-main/docs/ops/MORNING-RITUAL-PLATFORM.md
  lab:
    - W DZIEŃ: aktywny tor ≠ ENT-12
    - Otwórz CEO/Today — wskaż 1 issue P0/P1
    - Powiedz: co blokuje ENT-12 (M0 / QUI-14 / QUI-18 / GO)
  dod: Tor WF-P* w DZIEŃ. ENT-12 WAIT z uzasadnieniem. 1 issue z CEO/Today wskazany.
```

Diagram/link w dziale F: `PLATFORM-WORKFLOW-GATE.md` scoreboard WF-P1..P10 (read-only opis, nie API).

---

### 3.4 `DASHBOARD.html` — zakładka **TERAZ**

**Decyzja R1:** TERAZ **pozostaje** kursem (`firstOpen()`). Nie przełączać TERAZ na issue Linear — łamie to `ACADEMY-UX-SPEC.md` §2 i ADHD „jeden fokus = lekcja”.

**Opcjonalne (Faza B):** w `#nowcard` na zakładkach ≠ TERAZ dodać jednolinijkowy **kontekst platformy** tylko gdy `state.plat_tor` ustawione (np. „Tor platformy dziś: WF-P6 QUI-14 2/7”) — bez przełączania głównej akcji.

---

### 3.5 `scripts/validate-academy-export.py`

| Gate | Akcja |
|------|-------|
| `"WF-P9 tor platformy"` | Zmienić na `"WF-P tor platformy (nie ENT-12)"`: wymaga `WF-P6` **lub** `WF-P` + `ENT-12` + `WAIT` w HTML |
| Nowy gate (Faza A) | `"Linear widoki Wave 2"`: `ceotoday-1ef420fc07c0` lub tekst `CEO/Today` w DZIEŃ |
| Nowy gate (Faza A) | `"MORNING-RITUAL platform align"`: `day_today_first` lub `Today first` w DZIEŃ |

---

### 3.6 `docs/OPERATING-MODEL.md`

Sekcja **§4 Stan stacku** — dodać wiersz:

| Element | Stan | Znaczenie |
|---------|------|-----------|
| Linear platform (`dsaas-platform-main`) | **PARTIAL → PASS** | Projekt QUI + 8 widoków (EV-335); QUI-18 = filtry HITL |

Sekcja **§2 Przepływy** — doprecyzować:

> Poranek: `DASHBOARD.html` DZIEŃ + widok [CEO/Today](https://linear.app/quietforge/team/QUI/view/ceotoday-1ef420fc07c0) → issue platformy → **nie** ENT-12 przed M0 PASS.

Data wersji: **v1.1 · 2026-09-13**.

---

### 3.7 `docs/ACADEMY-UX-SPEC.md`

Dopisać w §2 (DZIEŃ):

- Rytuał poranny/wieczorny platformy = mirror `MORNING/EVENING-RITUAL-PLATFORM.md` (checkboxy, nie API).
- `<details>` z 8 linkami Linear (Wave 2).
- Tor WF-P w polu `plat_tor` — SSoT operacyjny; TERAZ = kurs.

Wersja: **v3.2** (planowana).

---

## 4. Fazy wdrożenia

### Faza A — minimalna ( **po human merge** PR `feat/linear-os-wave2` na `dsaas-platform-main` )

**Trigger:** `LINEAR-PLATFORM.md` §6 na `main` platformy + EV-335 na main.

**Zakres Akademii (1 PR, gałąź czysta — nie `main` WIP vault):**

1. `plat_linear` → **PARTIAL** + opis QUI-18
2. `plat_cloud` → **PASS SMOKE** (WF-P5)
3. DZIEŃ: `torDefault` → **WF-P6 / QUI-14 2/7**
4. DZIEŃ: checkboxy poranne/wieczorne aligned z ritual platformy
5. DZIEŃ: `<details>` 8 widoków Linear + link projektu
6. Pull/rebase **F4** z PR #4 jeśli brak lokalnie
7. `validate-academy-export.py` — zaktualizowane gate’y
8. `OPERATING-MODEL.md` v1.1 (tylko §4 + §2 akapit)

**Nie w Fazie A:** pełny PASS `plat_linear`, zmiany QUI-18 Settings, WF-P10 tor.

**Szacunek:** 1 sesja Cursor · ~150–250 LOC `DASHBOARD.html` + docs.

---

### Faza B — pełne zamknięcie Wave 2

**Trigger:** QUI-18 **Done** + QUI-14 **Done** (7/7, ≥2026-09-20) + opcjonalnie QUI-17/WF-P10 start.

**Zakres Akademii (2. PR lub amend Fazy A):**

1. `plat_linear` → **PASS**
2. DZIEŃ: `torDefault` → **WF-P10 / ENT-OPS** (gdy PLATFORM-DECISIONS + GO) lub **QUI-17** checklist
3. F4 lab: rozszerzyć o filtry HITL i GitHub scope verify
4. `ACADEMY-UX-SPEC.md` v3.2 final
5. Opcjonalnie `#nowcard` kontekst `plat_tor`
6. Handoff: `docs/handoffs/YYYY-MM-DD-akademia-linear-wave2.md`

**Nie w Fazie B:** deploy Kokpitu widget, ENT-12 deploy, edycja platformy z poziomu Akademii.

---

## 5. Kryteria akceptacji

### Faza A — DONE gdy

- [ ] `python scripts/validate-academy-export.py` → **PASS**
- [ ] `python scripts/test_progress_vault.py` → **PASS** (jeśli gałąź zawiera vault — inaczej skip na gałęzi docs-only)
- [ ] Ręczny walkthrough 360px: DZIEŃ → link CEO/Today otwiera Linear · tor ≠ ENT-12 · `plat_linear` = PARTIAL
- [ ] `OPERATING-MODEL.md` v1.1 w tym samym PR
- [ ] Zero sekretów / tokenów w diff
- [ ] PR akademii zlinkowany w komentarzu QUI-14 (day N/7) lub QUI-18 — opcjonalnie Dowódca
- [ ] **Nie** zmieszano z WIP vault na `main` bez osobnej decyzji

### Faza B — DONE gdy

- [ ] Wszystko z Fazy A +
- [ ] `plat_linear` = PASS zgodnie z QUI-18 Done
- [ ] F4 zaliczalny (lab + DoD) z 8 widokami i blokadą ENT-12
- [ ] Handoff w `docs/handoffs/` z EV platformy (numer po merge)
- [ ] Dowód: screenshot DZIEŃ + Linear HITL view (lokalny plik poza repo lub Linear comment)

---

## 6. Linki SoT (checklist implementera)

### Platforma (read-only)

| Dokument | Ścieżka |
|----------|---------|
| Linear OS + issues M0 | `dsaas-platform-main/docs/ops/LINEAR-PLATFORM.md` |
| 8 widoków §6 | j.w. |
| Bramka WF-P* | `dsaas-platform-main/docs/ops/PLATFORM-WORKFLOW-GATE.md` |
| Rytuał poranny | `dsaas-platform-main/docs/ops/MORNING-RITUAL-PLATFORM.md` |
| Rytuał wieczorny | `dsaas-platform-main/docs/ops/EVENING-RITUAL-PLATFORM.md` |
| Decyzje | `dsaas-platform-main/docs/ops/PLATFORM-DECISIONS.md` |
| Handoff Wave 2 | `dsaas-platform-main/docs/handoffs/HANDOFF-LINEAR-OS-WAVE2-2026-09-13.md` |
| EV | `dsaas-platform-main/kanon/EVIDENCE_LEDGER.md` → EV-335 |

### Linear (live)

| Issue / widok | URL |
|---------------|-----|
| QUI-14 WF-P6 | https://linear.app/quietforge/issue/QUI-14 |
| QUI-16 WF-P9 | https://linear.app/quietforge/issue/QUI-16 |
| QUI-17 WF-P10 | https://linear.app/quietforge/issue/QUI-17 |
| QUI-18 Wave 2 HITL | https://linear.app/quietforge/issue/QUI-18 |
| Projekt platformy | https://linear.app/quietforge/project/dsaas-platform-main-d40484fe9522 |
| CEO/Today | https://linear.app/quietforge/team/QUI/view/ceotoday-1ef420fc07c0 |
| HITL approvals | https://linear.app/quietforge/team/QUI/view/hitl-approvals-e0732a590998 |

### Akademia

| Dokument | Ścieżka |
|----------|---------|
| Dashboard | `akademia/DASHBOARD.html` |
| UX spec | `akademia/docs/ACADEMY-UX-SPEC.md` |
| Operating model | `akademia/docs/OPERATING-MODEL.md` |
| WIP vault handoff | `akademia/docs/handoffs/2026-09-13-akademia-vps-sync-deploy.md` |
| Walidator | `akademia/scripts/validate-academy-export.py` |

---

## 7. Kolejność pracy (rekomendacja R1)

```
1. [Dowódca] Merge PR feat/linear-os-wave2 (platforma) — human-stop
2. [Dowódca] Commit/PR osobno: WIP vault (akademia main) — NIE mieszać
3. [Cursor] Gałąź docs/linear-os-wave2-akademia od czystego main (po kroku 2 lub od origin/main)
4. [Cursor] Implementacja Fazy A (ten plan §4)
5. [Dowódca] Review PR akademii + merge
6. [Dowódca] QUI-18 Settings HITL (filtry, powiadomienia) — poza repo
7. [Cursor] Faza B po QUI-18 Done + QUI-14 7/7
```

---

## 8. Ryzyka

| Ryzyko | Mitigacja |
|--------|-----------|
| Mieszanie WIP vault z Linear update | Osobne gałęzie/PR; ten plan explicite STOP na dirty main |
| Fałszywy PASS Linear przed QUI-18 | Faza A = PARTIAL; PASS dopiero Faza B |
| Regresja checkboxów DZIEŃ (utrata historii) | Migracja `_scratch`; nie kasować starych kluczy w Fazie A |
| PR #4 (F4) nie na lokalnym main | `git fetch` + cherry-pick F4 lub rebase przed Fazą A |
| DNS akademia (VPS) | Osobny tor — handoff VPS; nie blokuje Fazy A treści |

---

## 9. NASTĘPNY KROK (po tym planie)

**Wykonaj Fazę A** na gałęzi `docs/linear-os-wave2-akademia` **po** merge PR platformy Wave 2 — pierwszy commit: `plat_linear` PARTIAL + DZIEŃ tor WF-P6 + linki CEO/Today.

**WŁAŚCICIEL:** R1 (implementacja) · Dowódca (merge platformy + QUI-18 HITL)  
**ŹRÓDŁO:** EV-335 · `dsaas-platform-main/docs/ops/LINEAR-PLATFORM.md:79-92` · `akademia/docs/handoffs/2026-09-13-akademia-vps-sync-deploy.md:46`
