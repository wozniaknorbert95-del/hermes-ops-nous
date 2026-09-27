# Raport audytu — Hermes Ops (`/ops`) — round 3

**Data:** 2026-09-27
**Plan:** [`AUDYT-PLAN-HERMES-OPS-2026-09-27.md`](AUDYT-PLAN-HERMES-OPS-2026-09-27.md) (GO Dowódcy: „GO — start audytu round 3, bez e2e”)
**Repo SHA:** `fa7922f` (`main`, HEAD == origin/main)
**Kontrakt:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md) · [`CONTRACT-OPS-STATUS.md`](CONTRACT-OPS-STATUS.md)
**Deploy:** **nie** (Zasada 11 — brak GO; O6 e2e **SKIP** zgodnie z decyzją Dowódcy)
**Metoda:** read-only + testy + sondy logiczne. Zero zmian kodu, zero zmian na VPS.

---

## Executive summary

**GATE DOР i RUN-TRUTH HUD trzymają się kontraktu.** Gate DoR (`scripts/ops_linear_dor.py`)
jest fail-closed: brak `LINEAR_OPS_READ` → `missing_LINEAR_OPS_READ` + `lane=UNKNOWN` → 400;
`qui_hitl` / `qui_lane_local` / `qui_todo_mismatch` / `qui_dirty_pr` → 400 przed `@cursor`;
deploy/merge z telefonu → 403. Run-truth HUD (`derive_dispatch`/`derive_run` w vault) nie kłamie:
UNKNOWN ≠ zielone, RUNNING tylko po ack + `live.issue`, `stalled` tylko przy martwym ticku.
Mutacje Fala 0–R: **0 PRZEPUSZCZONE**. Sekrety: token Linear nie wychodzi do diag/cache/logów.

**Jeden finding P2** — negacja `_NEG_ENV` jest za wąska: frazy typu „nie wymaga SSH” /
„nie dotyczy VPS” / „bez dostępu do VPS” **fałszywie spychają na LOCAL**. Fail-safe (nigdy nie
auto-akceptuje zadania lokalnego), ale psuje routing — ta sama klasa co fix `fa7922f`, który
pokrył tylko „zero VPS” sąsiadujące bezpośrednio.

---

## Metody

| Faza | Wynik | Dowód |
| --- | --- | --- |
| **G** regresja + mutacje | **PASS** | `test_progress_vault` / `test_hermes_intent` / `validate-academy-export` PASS; 16× `mutation-test-fala-*` **0 PRZEPUSZCZONE** |
| **B** gate DoR | **PASS + P2** | `dor_gate_unit` + integracja (todo/hitl/local/dirty/deploy=403) + sondy `_NEG_ENV` |
| **C** run-truth HUD | **PASS** | `test_progress_vault` (UNKNOWN≠green, merge 403, take_over 200, set_mode AUTOPILOT-only, brak github.com w cache) |
| **D** invarianty I1–I7 | **PASS** | `test_progress_vault` (ensure_ops_cmd_file, ops_cmd_state, dispatch idle/stalled, patch_ops_status) |
| **A** kontrakt/SSoT | **PASS** | kody refuse 1:1 (ROLE §routing ↔ CONTRACT §3b ↔ `ops_linear_dor`); academy-gate.yml wymienia 14 plików mutation = linia `testy:` |
| **F** deploy-ready | **PASS*** | wszystkie `step` green; `HEAD==origin/main`; **jedyny** FAIL = working copy nieczyste (2 nietrackowane pliki **audytu**) |
| **E** e2e O6 | **SKIP** | decyzja Dowódcy (bez e2e) |

\* „working copy nie jest czysty” to artefakt audytu: `docs/handoffs/2026-09-26-koniec-dnia.md`
(zastany) + `docs/ops/AUDYT-PLAN-HERMES-OPS-2026-09-27.md` (ten plan). Żaden plik kodu nie jest
zmodyfikowany; wszystkie bramki testowe PASS.

`engineer_loop_e2e`: bez zmian (nie odtwarzano S0–S6).

---

## Findingi

### P2 — `_NEG_ENV` za wąski: „nie wymaga SSH” fałszywie = LOCAL — **OPEN (rekomendacja)**

| | |
| --- | --- |
| **Objaw** | `_requires_local()` zwraca `True` (→ `qui_lane_local`, 400, tor Lokalnie) dla zadań, które **wprost wykluczają** VPS/SSH. |
| **Przyczyna** | `_NEG_ENV = \b(zero\|bez\|nie\|no)\s+(vps\|ssh\|deploy)\b` kasuje negację tylko gdy czasownik-zaprzeczenie styka się **bezpośrednio** z rzeczownikiem. `fa7922f` naprawił TYLKO „zero VPS”. „nie **wymaga** SSH”, „nie **dotyczy** VPS”, „bez **dostępu** do VPS” mają czasownik pośrodku — negacja nie łapie, a „ ssh”/„vps ” z `REQUIRE_LOCAL` wciąż trafia. |
| **Zmierzono** | `requires_local=1` dla: `"nie wymaga SSH"`, `"nie dotyczy VPS"`, `"bez dostępu do VPS"`. `requires_local=0` (OK) dla: `"zero VPS"`, `"bez SSH"`, `"nie deploy"`, `"no vps"`. „bezpośrednio na VPS” = 1 to zachowanie **poprawne** (de facto lokalne). |
| **Kierunek** | Fail-safe. Fałszywy LOCAL **blokuje** autopilota (za dużo ostrożności), nigdy nie auto-aprobuje zadania naprawdę lokalnego. Nie jest to luka bezpieczeństwa. |
| **Rekomendacja** (plan-only, bez edycji) | 1) Rozszerzyć `_NEG_ENV` o wzorce czasownik-pośredni: `nie (wymaga\|dotyczy\|używa\|potrzebuje\|zawiera)\s+(vps\|ssh\|deploy)` oraz `bez\s+(dostępu\|wymogu\|potrzeby)\s+do\s+(vps\|ssh\|deploy)`. 2) Dodać mutację **Fala S** (negacja pośrednia → NIE lokalne) i wpiąć do linii `testy:` + `academy-gate.yml` **w tym samym PR** (guard Fala J). |

### Świadomie poza zakresem

- Orchestrator tick + worker Cursor (`workflow-lab`) — read-only.
- Markery preflight platformy / session-entry `/gate`+`/verify` (P0#3 z 26.09) — inne repo.
- Deploy VPS / redeploy Akademii — Zasada 11.
- O6 e2e — decyzja Dowódcy.

### Zweryfikowane jako NIE-findingi (hipotezy §4 planu)

| Hipoteza | Werdykt |
| --- | --- |
| Stale cache pulse (60s, klucz = id) | **OK** — `read_cache` wymaga `id == next_id`; zmiana issue to miss (re-fetch). 60s na tym samym issue nie kłamie HUD. |
| Cache zapisuje opis/labels issue | **OK** — `evaluate_issue` zwraca tylko `title/url/project` (+`missing/lane/code`), **nie** opis ani labels. `write_cache` nie niesie wrażliwych pól. |
| `load_todo_active` czyta dysk bez tokenu | **OK** — `status_overlay`/`gate_start` robią early-return `missing_LINEAR_OPS_READ` zanim dotrą do `load_todo_active`. |
| `_NEG_ENV` bypass | **P2** (jedyny realny finding — patrz wyżej). |
| Academy-gate wpięcie 14 plików mutation | **OK** — academy-gate.yml (workflow_dispatch) wymienia 0,d,e,i,j,k,l,m,n,o,p,q,r = linia `testy:` AGENTS.md. |

---

## Checklist kontraktu

| Reguła | Status |
| --- | --- |
| Telefon nie merguje | OK (merge → 400/403) |
| Brak S-deploy w orchestratorze | OK (deploy flag → 403) |
| RUNNING tylko po ack + live.issue | OK (dispatch) |
| UNKNOWN nigdy nie zielone | OK (test + Fala) |
| Autopilot-only | OK (set_mode SUPERVISED/MANUAL → 400) |
| 410 `/hermes/chat` | OK (od audytu 1; bez regresji) |
| Zero sekretów w diag/cache | OK (diag bez tokenu; `_URL_DENY`; `today.tokens/cost=None`) |
| Gate DoR fail-closed (brak LINEAR_OPS_READ → 400) | OK |

---

## Następne kroki

1. **P2** — decyzja Dowódcy: wdrożyć rekomendację + mutację Fala S (osobny PR, nie tu).
2. **O6 e2e** — gdy Dowódca dostarczy issue testowy lab.
3. **Deploy** — czeka na GO Zasada 11; `deploy-ready-hermes-ops.sh` da zielone po wciągnięciu 2 nietrackowanych plików audytu do repo albo ich usunięciu.

Zero sekretów w tym raporcie.

**Podpis:** Hermes Ops audit round 3 (lokalny agent, 2026-09-27).