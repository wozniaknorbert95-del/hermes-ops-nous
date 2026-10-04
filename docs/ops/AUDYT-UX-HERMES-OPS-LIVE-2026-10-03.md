# AUDYT UX — Hermes Ops LIVE — 2026-10-03

═══════════════════════════════════════════════════════════
VERDICT: Fail

Persona: dowodca-ops — Dowódca, ADHD, 30 s na Start pętli / Retry
Source: argument użytkownika (autopilot + kod; Akademia schodzi z drogi)
Locked at: 2026-10-03 08:57 CEST
Surfaces audited: 2 / 2 (`/` 401 gate, `/ops` vault UI)
Interaction Manifest: complete enough for Fail (no text input exists on /ops)

Hard Gates: console errors n/m (Chrome MCP down; Cursor browser), warnings n/m, network 5xx 0, 403/404 auth 2 public 401 (expected Basic), layout-collapse 0, axe Critical 0, axe Serious 1 (4 nodes, GENERIC — dropped)  
Performance (tunnel `/ops`): FCP 0.56s / CLS n/m / INP n/m — under 4.0s

Findings:
  Critical: 3    High: 8    Medium: 1    Low: 0

Self-critique pass ([Prune Ops audit findings](a974fd34-45e0-4950-bbb5-6c639459207e)): Drafted: 16  Kept: 12  Generic: 3  Duplicate: 1

Time per phase: Phase 3 ~12m / Total ~20m
Manifest plausibility: 9 entries, median gap > 2s, 5 screenshots, 2 routes

TOP 5 (impact × ease):
  1. C2 Start martwy + Retry ukryty po FAIL — control plane nie steruje
  2. H1 Jedna karta = trzy prawdy (leftover / Next / DoR)
  3. H2 Raport „Padło: nic” przy S3 FAIL
  4. C1 Publiczny URL wygląda jak martwa Akademia
  5. C3 Auto `set_mode` przy każdym wejściu
═══════════════════════════════════════════════════════════

**Persona Lock**: Dowódca — Hermes Ops = autopilot kodowania  
**Source**: ten chat (nie plik persony)  
**Device**: laptop + telefon; publiczny URL za Basic Auth

## Scope

Tylko Hermes Ops. `/` (Akademia) sprawdzony wyłącznie jako first-contact: ten sam 401. „Dokończ dzień” **nie** był re-walkowany w tej rundzie.

Chrome MCP (`:9222`) nie wstał. Live UI = tunel `127.0.0.1:18097` → VPS `:8097` (ten sam vault co produkcja). Publiczny HTTPS = first-contact 401.

## INTERACTION MANIFEST — /ops (vault)

  Persona: Dowódca, 30 s na Start
  [✓] 08:58:00 Otwarto publiczny `/ops` — 401 „Akademia OS — logowanie”, 0 kontrolek
  [✓] 08:58:20 Tunel `/ops` — cold „Ładowanie…”, UNKNOWN
  [✓] 08:58:25 paint: PAUSED + leftover QUI-113 + Start disabled + Retry hidden
  [✓] 08:58:40 Klik Testuj — hint „wejdzie w następnym Start”; Start nadal disabled
  [✓] 08:59:10 Klik Pause (już PAUSED) — steer „…”, potem „OK pause”
  [✓] 09:00:00 Viewport 375 — preflight otwarty, Start pod foldem
  [✓] axe.run: link-in-text-block serious×4, region moderate×14
  [✓] FCP 560 ms; 0 zasobów 5xx
  [✗] Brak pola tekstowego — nie da się wpisać zadania (H3)

## Sitemap

| Route | Cel |
|---|---|
| `https://akademia.quietforge.flexgrafik.nl/` | Akademia (kurs) — 401 gate |
| `https://akademia.quietforge.flexgrafik.nl/ops` | Hermes Ops — 401 gate, potem control plane |
| `http://127.0.0.1:8097/ops` | ten sam HTML + `/ops/status` bez nginx |

## Threads

1. Wejść i odpalić / wznowić autopilot — **FAIL** (C2, H1, H7)
2. Zrozumieć, co padło na QUI-113 — **FAIL** (H2, Retry hidden)
3. Wybrać QUI-33 z kolejki i wystartować — **FAIL** (H3, DoR gate)

---

## Findings (KEEP)

### C1 — Publiczny `/ops` to martwa Akademia
- **Layer:** Architecture · **Severity:** Critical · **Surface:** `/` i `/ops` @ public HTTPS
- **Persona:** Dowódca otwiera bookmark, nie kod
- **Reproduce:** 1) Incognito / embedded browser. 2) Otwórz `https://akademia.quietforge.flexgrafik.nl/ops`. 3) Jeśli dialog Basic Auth nie wyskoczy — zostaje kremowa karta.
- **Observed:** H1 „Akademia OS”, jeden akapit, zero przycisków. `WWW-Authenticate: Basic realm="Akademia OS"` jest. Cursor browser nie pokazał dialogu.
- **Expected:** Marka Hermes Ops na `/ops`. Widoczna akcja „Pokaż okno logowania” gdy dialog nie wstanie.
- **Evidence:** snapshot view `6dc0b2`; `curl -sI` 401 + WWW-Authenticate; `host/auth-gate.html`
- **Suspected:** `host/auth-gate.html` + `host/nginx-akademia.conf:70-78`
- **Patch:** Osobny copy na `/ops` (nginx `error_page` / jeden HTML z dwoma nagłówkami). Przycisk `location.reload()` — nie formularz hasła (guard zabrania).

### C2 — Start martwy, Retry zniknął po FAIL
- **Layer:** Interaction · **Severity:** Critical · **Surface:** `/ops` HUD 1440+1920
- **Reproduce:** 1) Otwórz live `/ops`. 2) Zobacz leftover QUI-113 S3 FAIL. 3) Szukaj Retry. 4) Tapnij Start pętli.
- **Observed:** `#btn-retry` hidden. `#btn-run` disabled, hint „Zablokowane: DoR komplet (6 pól). To nie jest merge.” `canRetry` wymaga `run.verdict==='failed'` — w DOM retry i tak `hidden`. Preflight ✗ DoR + ✗ tor Autopilot gasi Start.
- **Expected:** Po FAIL: Retry widoczny. Start mówi *który* issue blokuje i *co* dodać w Linear. Nie mieszać leftover z Next.
- **Evidence:** CDP `retryHidden:true`, `runDisabled:true`; JSON `run.verdict=failed`, `live.steps[S3]=FAIL`
- **Suspected:** `OPS.html` `paint()` ~732–735, `canAct` ~901–916
- **Patch:** `canRetry` od `run.verdict` / S-FAIL niezależnie od PAUSED. Start title = pełna lista `blockedBy`. Hero nie jest leftover, gdy Next ≠ live.

### C3 — Wejście na stronę samo woła `set_mode`
- **Layer:** Interaction · **Severity:** Critical · **Surface:** `/ops` load
- **Reproduce:** 1) Otwórz `/ops`. 2) Nie klikaj. 3) Steer: „Tryb: Autopilot · OK”. Ledger: seria `kind:mode`.
- **Observed:** `loadStatus` → `ensureTickAutopilot()` → `send('set_mode')` raz na sesję.
- **Expected:** POST tylko gdy tick nie jest już AUTOPILOT, albo nigdy z cold GET.
- **Evidence:** `OPS.html:544-547`, `1083`; `/ops/status` ledger
- **Suspected:** `ensureTickAutopilot`
- **Patch:** `if (s.mode==='AUTOPILOT') return;` zanim `send`.

### H1 — Jedna karta, trzy prawdy
- **Layer:** Architecture · **Severity:** High
- **Observed:** Eyebrow „Ostatni run” QUI-113; chip DoR `qui_dor_not_ready`; rekomendacja QUI-33 STOP; pigułki PAUSED+AUTOPILOT.
- **Expected:** Blok A leftover (FAIL/Retry). Blok B Next + dlaczego Start nie idzie.
- **Suspected:** `paint()` 720–780
- **Patch:** Rozdziel `leftoverIdle` od `next` w DOM (dwa eyebrow albo jedna linia prawdy).

### H2 — Raport kłamie „Padło: nic”
- **Layer:** Feedback · **Severity:** High
- **Observed:** `report.line` = „Zrobione: follow-up. Do laptopa: deploy. Padło: nic.” przy S3 FAIL i `verdict=failed`.
- **Expected:** Linia zaczyna się od FAIL / S3.
- **Suspected:** conductor `report_pl` + `paint()` `report-line`; `CONTRACT-OPS-STATUS.md` przykład
- **Patch:** UI override: jeśli `run.verdict==='failed'`, prefix „FAIL S3 — ” zanim `report.line`.

### H3 — Kolejka nie uruchamia issue
- **Layer:** Interaction · **Severity:** High
- **Observed:** Klik w QUI-33 = Linear. Copy to przyznaje. „Użyj tego” hidden (`selected===true`).
- **Expected:** „Ustaw Next” / „Odblokuj DoR” na karcie kolejki, nie tylko ↗ Linear.
- **Suspected:** `renderLane`, `btn-use-rec` 786–799
- **Patch:** Przycisk select_next na pierwszym Autopilot nawet gdy already Next — albo CTA „otwórz DoR w Linear” z powodem `blockedBy`.

### H4 — Pause na PAUSED = „OK pause”
- **Layer:** Feedback · **Severity:** High
- **Reproduce:** Status PAUSED → klik Pause → „OK pause”.
- **Expected:** „Już wstrzymane” bez POST, albo disable Pause.
- **Suspected:** `send('pause')` 1108–1111; click handler 1168
- **Patch:** Guard w click: jeśli `stU==='PAUSED'` nie wołaj `send`.

### H6 — Telefon: Start pod preflightem
- **Layer:** Interaction · **Severity:** High · **Surface:** 375
- **Observed:** `#preflight` otwarte, 6 wierszy, Start pod spodem. Kontekst (Live/Wynik) domyślnie zamknięty ≤959px.
- **Expected:** Start + Retry w pierwszym ekranie. Preflight zwinięty, badge „2 ✗”.
- **Suspected:** `OPS.html` kolejność DOM 264–275; default `open` na details
- **Patch:** Przenieś bar Start nad `<details id="preflight">`. `preflight.open=false` default.

### H7 — Testuj to teatr
- **Layer:** Interaction · **Severity:** High
- **Observed:** Klik Testuj → „wejdzie w następnym Start”. Start disabled. Nic nie wejdzie.
- **Expected:** Albo Start odblokowany w trybie testuj, albo chip disabled z powodem DoR.
- **Suspected:** `paintWorkMode` 628–647
- **Patch:** Gdy `!canAct`, hint: „Tryb zapisany. Start zablokowany: {blockedBy[0]}.”

### H8 — WAITING-GO vs żywa sesja Cloud
- **Layer:** Feedback · **Severity:** High
- **Observed:** Baner „Prowadzenie = WAITING-GO (lab+Nous). To nie jest @cursor.” ukrywany tylko gdy jest `run_url`; cold/partial nadal myli.
- **Expected:** Gdy `worker=cursor` i jest sesja: „Cloud API · cursor”. WAITING-GO tylko przy braku mózgu.
- **Suspected:** `conductor-banner` 257, 895–899

### M3 — Dziennik pusty przy żywym ledgerze
- **Layer:** Feedback · **Severity:** Medium
- **Observed:** `live.recent=null` → „tick nie dał live.recent”. Ledger w JSON ma eventy.
- **Patch:** Render `ledger` gdy `recent` puste.

### M4 — Approval: `hitl:approval-required`
- **Layer:** Visual · **Severity:** Medium
- **Patch:** Zamiana raw kind na zdanie PL.

Dropped (self-critique): H5, M1, M5 = GENERIC. M2 = DUPLICATE H3.

## Hard-gate scorecard

| Gate | Result |
|---|---|
| Console | Incomplete (no Chrome MCP stream) |
| 5xx | 0 |
| Layout collapse | 0 at 1920/375 (emulation) |
| axe Critical | 0 |
| axe Serious | 4 nodes GENERIC |
| LCP/FCP | 0.56s |

## Perfection roadmap

- **Quick Wins:** C2 Retry, H2 prefix FAIL, H4 Pause guard, H6 Start above preflight, C3 skip set_mode, H7 hint
- **Structural:** H1 split leftover/next, C1 /ops gate copy, H3 select-from-queue
- **Later:** M3 ledger, M4 copy, Nous LLM (parked)

## Scenarios (skrót)

1. First Contact — FAIL (C1)
2. Interrupted — N/A (brak formularza)
3. Wrong turn — queue → Linear, wraca; Start nadal martwy
4. Returning — leftover QUI-113 wieczny; Retry brak
5. Keyboard — Enter=Start ale Start disabled; Escape=Pause (H4)
6. Heavy data — 12 HITL + 5 auto, bez wirtualizacji (OK przy N)
7. Destructive — Take over ma confirm (nie klikane)
8. Second user — jeden Basic Auth, brak ról
9. Lifecycle — leftover FAIL dominuje Day-N
10. Round-trip — Testuj nie wraca do zdolności Start
11. Seasoning — ledger mode-spam zamiast run history

## Hold this in your hands

Gdyby to był pulpit maszyny, dostałbyś trzy zegary, każdy inny czas, duży czerwony przycisk zalepiony taśmą „DoR”, i karteczkę „nic nie padło” na silniku, który właśnie zgasł na biegu S3. Mózgi (tick, Cloud, Linear) są. Uchwyty kłamią. Nie chcesz tego trzymać w ręku w biegu — chcesz jeden włącznik i jedno zdanie, co się stało.

## Fix-and-verify

Kod na `feat/ops-hud-truth` (jeszcze nie na VPS): Retry po FAIL+PAUSED, linia leftover vs Next, prefix FAIL na raporcie, Pause → „Już wstrzymane”, `set_mode` skip gdy już AUTOPILOT, Start nad preflightem (bez auto-open), 401 mówi o `/ops` + przycisk odśwież. Guardy: validate, vault, Fala S 18/18. Re-walk i deploy = po GO.
