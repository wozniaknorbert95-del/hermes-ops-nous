# SPEC — Hermes Ops UX/UI enterprise (implementacja + kontrakt dla specjalisty)

**Status:** ZAPROJEKTOWANE I WDROŻONE (backend + UI). Ten dokument = SoT pikseli już wdrożonych. **P0 live**; **P1–P3** (IA / hierarchia / dispatch / confirm / fold / skróty) w [`PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md`](PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md).
**Data:** 2026-09-27 · **Repo UI:** `akademia/OPS.html` · **Payload:** `GET /ops/status` (`host/progress_vault.py` → `ops_status_view`).

---

## 1. Model domeny (specjalista musi to rozumieć, zanim ruszy piksele)

Hermes Ops to **control plane autonomicznej pętli inżynieryjnej**, nie dashboard analityczny:
`Linear (issue + etykieta agent)` → Hermes Engineer (Nous, Cloud Agents API) → Cursor otwiera `PR` → CI + AC/DoD → `auto-merge` (squash) → **deploy = Dowódca, lokalnie, Zasada 11 (NIE w orchestratorze)**. Komentarz `@cursor` nie jest S2.

- Maszyna stanów **S0–S6** (deploy = brak, to granica Dowódcy).
- Werdykt: **PASS | FAIL | UNKNOWN**. UNKNOWN **nigdy** nie jest zielone.
- HITL = etykieta w Linear **zanim** ruszy agent, nie przycisk merge. **Telefon nie merguje.**

## 2. Kontrakt payloadu (`/ops/status`) — co UI ma do dyspozycji

| Pole | Znaczenie |
|---|---|
| `engine` / `status` | PAUSED · QUEUED · RUNNING · STOPPED · UNKNOWN |
| `mode` | zawsze `AUTOPILOT` (vault normalizuje) |
| `lanes` | `{autopilot[], local[]}` |
| `live` | `{issue, step, action, steps[], progress, checks, tests[{cmd,excerpt,verdict}], conductor{ac,dod,local_remaining,report_pl,mode,followups_used}, pr_number, pr_url, ci_url, agent{run_url}, recent[], duration_sec, github_issue_url, cursor_comment_url (legacy)}` |
| `run` | `{verdict, reason, passed, proof{pr_url,ci_url,agent_run_url,pr_number,github_issue_url,cursor_comment_url,wake_state}, agent, dispatch{state}}` |
| `today` | `{runs, merged, failed, waiting, cap}` |
| `dor` | `{ok, code, missing, lane, id, todo_match, todo_active}` |
| `report` | `{line, runs, merged, failed, ...}` (synteza jednolinijkowa) |
| **`run_result`** (NOWE) | `{verdict, done[{label,ok,url}], not_done[{label}], waiting[{label}]}` |
| **`deploy_readiness`** (NOWE) | `{ready, label, pr_number, pr_url, owner:"dowódca", s6}` |
| **`recommended_issue`** | `{id, title, url?, reason, reason_code, selected}` — głowa kolejki Autopilot + *dlaczego*; `Użyj tego` = `select_next` (ustawia `next`, nie startuje) |

## 3. Architektura informacji — STERUJE / KONTEKST / DZIENNIK

- **STERUJE** (primary, góra/lewa): pre-flight gate, Run/Pause/Stop/Retry/Take over, fail triage, deploy handoff.
- **KONTEKST** (secondary): live S0–S6, kolejka, dziś.
- **DZIENNIK** (tertiary, dół/pełna szerokość): historia + aktywność.

## 4. Struktura ekranu

**Desktop (≥960px):** 2 kolumny — lewa = wynik + deploy (STERUJE), prawa = live + kolejka + dziś + approval; DZIENNIK pełna szerokość na dole. HUD (pre-flight + sterowanie) sticky u góry.

**Mobile (<960px):** jedna kolumna, kolejność = STERUJE → KONTEKST → DZIENNIK.

## 5. Komponenty (wdrożone)

1. **Pre-flight gate** (`#preflight`): 6 checks ✓ / ✗ / `?` — DoR, tor, tick żywy, CI, slot, limit dnia. UNKNOWN **nigdy** zielone (CI bez dowodu = `?`, nie ✓). Tick bez cache / UNKNOWN = ✗. ✗ blokuje Start; `?` nie udaje OK. `#btn-run:disabled` nie wygląda jak tappable cyan. Chip `todo zgodny` tylko gdy `todo_match===true` **i** jest `todo_active`.
2. **Run result** (`#panel-result`): 3 buckety — ✅ Zrobił / ❌ Nie zrobił (granica) / ⏳ Czeka — z proof-linkami (tylko realne https URL, fail-closed).
3. **Deploy handoff** (`#panel-deploy`): pojawia się tylko gdy `deploy_readiness.ready` — „deploy Zasada 11, lokalnie, nie z telefonu", z linkiem PR.
4. **DZIENNIK** (`#panel-dziennik`): dziś (runs/merged/failed/cap) + `live.recent` (ostatnia aktywność).

## 6. Zasady twarde (nie łamać — to są guardy CI)

- UNKNOWN startuje jako `pill unk`, nie zieleń.
- QUEUED ≠ RUNNING (opt. `lastStatus.status='QUEUED'`; nigdy RUNNING bez ack+`live.issue`+https `run_url`).
- Zero `JSON.stringify(live)` w UI; Live pokazuje krok S n + `tryb buduj|testuj|ulepszaj`.
- Zero `$0.00` hardcode; Tokens/Cost HUD martwy (`#t-tokens`/`#t-cost` zakazane).
- Cel dotykowy `min-height:44px;min-width:44px`; safe-area-inset; manifest-ops.webmanifest.
- `data-ops="take_over" id="btn-take"` stały; copy STALLED/QUEUED/NO-ACK/REFUSED/cursor_wake.
- Tylko `AUTOPILOT` (zero MANUAL/SUPERVISED/lane-manual/n-manual).
- Linia prawdy: `Cloud: /autopilot · sesja|brak sesji Cloud API · CI · AC` (paleta EV-454). Chip testów **nie** maluje S-kroków; zieleń tylko ze strumienia + https sesji.
- Proof Live: https `run_url` albo „Sesja: brak sesji Cloud API”. `comment sent` / `Wake:` nie są sesją.

## 7. DoD

Enterprise gotowe gdy: pre-flight renderuje 6 checks z blokadą; run result = 3 buckety z linkami; S0–S6 czytelne; deploy handoff jawny; desktop 2-panel + mobile 1 kolumna; DZIENNIK dostępny; UNKNOWN nigdy zielone; całość vanilla JS bez sekretów. Wszystko wprost z payloadu (żadnego wyliczania werdyktu po stronie klienta).