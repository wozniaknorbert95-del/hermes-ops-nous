# PLAN — Hermes Ops UX/UI enterprise (przepisanie Control Plane)

**Status:** PROJEKT — research dla specjalistów UX/UI + spec do implementacji. Do GO Dowódcy.
**Data:** 2026-09-27 · **Repo UI:** `akademia/OPS.html` (= `/ops`). **Kontrakt nav:** bez zmian w akademia (to inny produkt niż `/`).
**Cel:** przeprojektować `/ops` z „biednego/amatorskiego" zlepku paneli na **enterprise control plane** dla Dowódcy operującego autonomiczną pętlą inżynieryjną (Linear → Cursor → CI → auto-merge → lokalny deploy).

---

## 1. Kontekst domenowy (research dla specjalisty UX/UI)

Specjalista dostaje tu ŚCISŁY model domeny — bez tego UI będzie dekoracją, nie narzędziem.

### 1.1 Co robi system
Hermes Ops to **autonomiczna pętla inżynieryjna**, nie „asystent czatu":
1. Dowódca wybiera issue w **Linear** i daje etykietę `agent`.
2. Hermes Engineer (VPS `/ops`) kolejki Linear → komentarz `@cursor` (wake) → **Cursor Cloud Agent** otwiera `PR` → CI → **auto-merge** (squash).
3. Deploy = **NIE w orchestratorze**. Robi Dowódca, lokalnie (Zasada 11).

### 1.2 Role (z `HERMES-ROLE-CONTRACT.md`)
| Rola | Robi | NIE robi |
|---|---|---|
| **Dowódca** | Linear (wybór + etykieta), Start/Run/Pause/Stop, deploy lokalny | merge z telefonu, review diffu |
| Hermes Engineer (`/ops`) | kolejka → `@cursor` → CI → auto-merge | deploy, SSH prod |
| Cursor Cloud | kod, branch, PR | deploy, sekrety |

**Kluczowy fakt UX:** HITL (human-in-the-loop) = **etykieta w Linear ZANIM ruszy agent**, nie przycisk Merge. „Telefon nie merguje."

### 1.3 Maszyna stanów S0–S6 (bez S-deploy)
| Krok | Co | Werdykt |
|---|---|---|
| S0 | issue Linear + etykieta | PASS/FAIL/UNKNOWN |
| S1 | 6 pól DoR + `agent` | jak wyżej |
| S2 | `@cursor` na GitHub twin (to samo repo) | — |
| S3 | PR `cursor/*` | — |
| S4 | required checks zielone | — |
| S5 | (historyczny review mobile — nie jest bramką) | — |
| S6 | squash/merge | orchestrator |
| — | deploy / ENT-12 / restart | **nie istnieje w orchestratorze** |

**Werdykty: PASS | FAIL | UNKNOWN. UNKNOWN NIGDY nie jest zielone.**

### 1.4 Co dziś dostarcza backend (payload `/ops/status`)
`mode` (AUTOPILOT/MANUAL/SUPERVISED) · `engine` (PAUSED/RUNNING/STOPPED/UNKNOWN) · `lanes` (autopilot/manual/local) · `live` (issue + steps S0–S6 + links) · `approval` · `today` (runs/merged/failed/waiting) · `run_all_enabled` · `active_agents`.
**Brakuje dziś w payload:** `run_result` (podsumowanie „co zrobił/czego nie"), `deploy_readiness`, `ledger` (historia runów), `next_action` (rekomendacja), `duration/cost`.

---

## 2. Audyt obecnego UX (`OPS.html`, 759 linii vanilla JS)

### 2.1 Mocne strony (zachować)
- **Uczciwe stany** — QUEUED ≠ RUNNING, „nie udaje running" (fix QUI-70). To jest enterprise-grade.
- **Realne proof-linki** — issue # / comment / PR / CI / agent-run URL (zero „🤖 Cursor" bez URL).
- **Bogaty refuse-copy** — konkretne powody REFUSED (DoR, HITL, blocked, dirty PR, limit runów) z akcją naprawczą.
- **UNKNOWN nigdy zielone**, fail-closed.
- **Take over / Pause / Stop** jako świadome granice (phone ≠ merge).

### 2.2 Luki (dlaczego „amatorskie")
1. **Brak ścieżki Dowódcy** — panele (Steer/Dashboard/Kolejka/Live/Approval) są płaskie; nie ma prowadzonego przepływu „co teraz".
2. **Brak pre-flight** — Dowódca nie widzi w jednym miejscu „co muszę sprawdzić zanim tapnę Start".
3. **Brak podsumowania runu** — S0–S6 jako kropki, ale zero narracji „zrobiłem X · nie zrobiłem Y · czekam na Z".
4. **Mobile-only (720px)** — brak layoutu desktop (command center); enterprise = też biurko.
5. **Brak DZIENNIKA (audit)** — jest `today` (4 liczby), nie ma niezmiennej historii runów.
6. **Brak granicy deploy** — Commander nie widzi „wszystko zmerge'owane → teraz Twój lokalny deploy" jako jawnego kroku (chociaż to Zasada 11).
7. **Komunikacja asymetryczna** — system raportuje stany maszynowe, nie „co jest gotowe na TWOJĄ decyzję".
8. **Triage FAIL to tylko Retry/Take over** — brak hintu root-cause + linku do runbooka.

---

## 3. Persona + ścieżka Dowódcy (end-to-end, do zaprojektowania wprost)

**Persona:** właściciel-mała-firma, 2 minuty rano na telefonie + sesje przy biurku. Chce: (a) wiedzieć co stoi, (b) podjąć minimalną liczbę decyzji, (c) mieć pewność że autopilot nie kłamie.

### Ścieżka (to jest SZKIELET IA nowego UI)
1. **PORANEK (10 s):** jeden ekran stanu — „pętla zdrowa / co czeka na Ciebie / co zmerge'owane nocą".
2. **PRE-FLIGHT (przed Start):** co MUSZĘ widzieć zanim tapnę Start (sekcja §5).
3. **START:** jeden przycisk. Od tego momentu autopilot robi S0–S6.
4. **WATCH:** progres S0–S6 jako pipeline, uczciwe stany, proof-linki per krok.
5. **TRIAGE (gdy FAIL):** co padło → dlaczego (hint) → co robię (Retry raz / Take over / runbook).
6. **DONE + DEPLOY HANDOFF:** „S6 merge zrobiony. Deploy = Ty, lokalnie (Zasada 11)." — jawne zamknięcie pętli, NIE w UI jako przycisk.
7. **HITL / Local:** osobna, jasno oznaczona strefa „zrób na laptopie".

---

## 4. Architektura informacji — STERUJE / KONTEKST / DZIENNIK

(bezpośrednio ze skilla `autonomous-operations-planning` — to jest kręgosłup)

| Warstwa | Co | Przykład w Hermes Ops |
|---|---|---|
| **STERUJE** (primary) | decyzje Dowódcy + stan sterowania | pre-flight, Start/Pause/Stop, triage FAIL, deploy handoff |
| **KONTEKST** (secondary) | stan operacyjny wspierający decyzję | kolejka lane, live S0–S6, dziś (runs/merged) |
| **DZIENNIK** (tertiary) | niezmienna historia | run ledger, telemetria, evidence ledger |

**Zasada:** STERUJE na górze i zawsze widoczne; KONTEKST jeden poziom niżej; DZIENNIK pod fałdą/oddzielną kartą — nigdy nie zagraca widoku decyzyjnego.

---

## 5. Pre-flight — co Dowódca MUSI widzieć przed Startem

Jedna sekcja „Zanim ruszysz" (odpowiednik checklisty HITL), binarnie zielona/czerwona:
1. **Kolejka gotowa?** (issue z `agent`, DoR 6 pól komplet, nie `blocked`).
2. **Lane poprawny?** (autopilot vs local — brak HITL w złym torze).
3. **Lane zgodny z Linear SoT?** (todo mismatch?).
4. **CI baseline zielony?** (gates — teraz self-hosted; brak billing-red).
5. **Nie ma dirty PR / locka innego runu?** (mergeable_state, active agent = max 1).
6. **Limit dzienny runów?** (cap OPS_MAX_RUNS_PER_DAY).

Każdy punkt = `✓ / ✗` + link/kontekst (nie surowy kod). Jeżeli któryś czerwony → blokada akcji i powód (bez Startu „w ciemno").

---

## 6. Model komunikacji runu — „co zrobił / czego NIE zrobił"

Po każdym runie / na koniec runu, narracja w ludzkim języku, 3 kolumny:

**✅ ZROBIŁ** (z proof-linkami): issue # + @cursor comment → PR # → CI green → squash merge #.
**❌ NIE ZROBIŁ** (jawna granica): deploy (Zasada 11 — Twoje), HITL/local (laptop), restart usług, ENT-12.
**⏳ CZEKA / WYMAGA CIEBIE**: HITL na QUI-X, blocked Y, kolejny issue w torze, deploy ready.

Dodatkowo per-krok werdykt S0–S6 jako **pipeline z drill-down** (klik w krok → co, werdykt, URL dowodu), a nie 6 anonimowych kropek.

---

## 7. Wzorce enterprise — referencje dla specjalisty

| Wzorzec | Źródło inspiracji | Co wziąć |
|---|---|---|
| **Control plane ≠ dashboard** | AWS/GCP console, K8s (Lens) | STERUJE pierwsze; sterowanie z konkretną decyzją + ryzykiem |
| **Pipeline/DAG stepów** | Temporal UI, Airflow, GitHub Actions (lista job/step) | S0–S6 jako pipeline z per-step drill-down + retry-from-step |
| **HUD / cockpit density** | kokpity NOC/SIEM (Datadog, PagerDuty, Grafana OnCall) | jeden kolor stanu na górze, „wszystko zielone" w 1 rzut oka |
| **Fail triage first-class** | PagerDuty (acknowledge → runbook → escalate) | FAIL = hint root-cause + akcja + link runbooka, nie surowy traceback |
| **Receipts / audit trail** | LangSmith/LangFuse (trace agenta per run) | każdy claim ma URL dowodu; DZIENNIK niezmienny |
| **Queue SoT = link, nie duplikat** | Linear-first (ten projekt) | kolejka otwiera Linear, nie kopiuje stanu w HTML |
| **Deploy boundary** | GitOps (ArgoCD — widok „ready to sync") | deploy jako JAWNY krok Dowódcy poza orchestratorem, sygnał „ready" |

---

## 8. Kluczowe funkcje operacyjne (top N, do dopracowania najpierw)

W kolejności ważności (maks efekt / min złożoności):
1. **Pre-flight gate** (§5) — jedna zielona/czerwona lista + blokada Startu przy czerwonym.
2. **Run result summary** (§6) — „zrobił/nie zrobił/czeka" z proof-linkami. To najbardziej brakujący element.
3. **S0–S6 pipeline z drill-down** — zamiast kropek, klikalne kroki z URL.
4. **Deploy handoff** — po S6: „merge gotowy · deploy = Ty (Zasada 11)" + link.
5. **Desktop layout** — dwa panele (LEWA: kolejka + sterowanie; PRAWA: live + detail), obok mobile.
6. **DZIENNIK / run history** — niezmienna lista dzisiejszych + historycznych runów.
7. **Fail triage** — hint root-cause + akcja (Retry raz / Take over / runbook) zamiast gołych przycisków.

(Niższy priorytet: cost/duration per run, multi-worker wizualizacja — worker v1 to wciąż tylko Cursor.)

---

## 9. Propozycja struktury ekranu

**MOBILE (telefon, 2 min rano):**
```
[ HUD: stan pętli (1 kolor) + tryb AUTOPILOT ]
[ PRE-FLIGHT: 6 ✓/✗ → jeden CTA "Start" (disabled gdy czerwony) ]
[ LIVE: S0–S6 pipeline + "zrobił/nie zrobił/czeka" (collapse) ]
[ TRIAGE: tylko gdy FAIL — hint + akcje ]
[ Kolejka (link Linear) · Deploy handoff · DZIENNIK (fałda) ]
```

**DESKTOP (biurko):**
```
┌───────────────────────────┬──────────────────────────┐
│ STERUJE (lewa)            │ KONTEKST (prawa)          │
│  Pre-flight gate          │  Live S0–S6 pipeline      │
│  Start/Pause/Stop/Retry   │  run result summary       │
│  Fail triage              │  active agent             │
│  Deploy handoff           │  dziś (stats)             │
│  Kolejka (lane'y)         │  approval                 │
├───────────────────────────┴──────────────────────────┤
│ DZIENNIK (run history, evidence) — pełna szerokość     │
└──────────────────────────────────────────────────────┘
```

**Zasoby maintainerskie:** vanilla JS (parity z AGENTS.md — zero npm), IBM Plex Sans (już w użyciu), dark theme (już jest). Bez frameworka — chyba że specjalista dostarczy solidny argument za svelte/alpine, ale to koszt złożoności.

---

## 10. DoD (co znaczy „UX/UI enterprise gotowe")

1. Pre-flight gate renderuje 6 binarnych warunków z blokadą Startu przy czerwonym; każdy czerwony ma powód + link.
2. Po S6 run wyświetla narrację „zrobił / nie zrobił / czeka" z proof-linkami (nie same kropki).
3. S0–S6 = klikalny pipeline z drill-down (werdykt + URL per krok).
4. Deploy handoff po merge jest widoczny i JAWNIE oznaczony jako Dowódca (bez przycisku deploy w UI).
5. Desktop 2-panel + mobile 1-kolumna (oba czytelne, STERUJE na górze).
6. DZIENNIK (historia runów) dostępny, niezagracający widoku decyzyjnego.
7. UNKNOWN nadal nigdy nie zielone; QUEUED nadal ≠ RUNNING (nie łamać QUI-70).
8. Zero regresji kontraktu nav akademia (to inny produkt `/ops`, nie dotykamy `/`).
9. Wszystko vanilla JS + bez sekretów w HTML (proof-linki = URL, nie tokeny).

---

## 11. Co potrzebuję od Ciebie (Dowódca) / następny krok

Nie ruszam kodu (plan-mode). Do wyboru:
- **A)** GO na pełny rewrite `/ops` wg §9 (desktop + mobile + pre-flight + run result + DZIENNIK).
- **B)** GO inkrementalny — tylko top-3 funkcje najpierw: pre-flight gate + run result summary + S0–S6 drill-down.
- **C)** Najpierw podaję spec jako **oddzielny plik designerski** (`docs/ops/UX-SPEC-HERMES-OPS.md`) dla specjalisty, a implementację robi on — ja dostarczam payload-y backendu (do rozszerzenia: `run_result`, `deploy_readiness`, `ledger`).

Rekomendacja: **C → B** (najpierw spec + rozszerzenie payloadu, potem inkrementalny rewrite),
bo enterprise UX wymaga najpierw danych (`run_result`/`deploy_readiness`), których payload dziś nie ma (§1.4).