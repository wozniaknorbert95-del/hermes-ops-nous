# Plan — profesjonalny deploy + UX/UI Hermes Ops (kontrola · podgląd · raport)

**Status:** **WYKONANE (Tier 1+2)** — deploy czeka na GO Dowódcy (Zasada 11)
**Data:** 2026-09-27
**Zlecenie:** „profesjonalnie deploy” + „profesjonalnie zoptymalizuj UX/UI Hermes Ops — nie czuję
kontroli, nie mam podglądu co zrobił, nie wysyła raportów, a Akademia ma push”. Zasada: **maks. efektu,
min. złożoności**. Granica: **Zasada 11** (deploy = lokalnie, ręcznie, Dowódca) + **agenda = to repo,
nie workflow-lab**.

---

## CZĘŚĆ A — ANALIZA (co jest, co nie działa)

### A1. Kontrola — JEST, ale słabo wygląda w oczach Dowódcy

`/ops` już ma: Run next · Pause · Stop · Retry · Take over (fold 360px) + Autopilot-only + dispatch
banner (QUEUED/PICKED-UP/RUNNING/REFUSED/STALLED) + pasek S0–S6. **Brakuje pętli zwrotnej:** po
wciśnięciu „Run next” nie widać *wyniku* w jednym miejscu — trzeba sklejać chipsy + Live + dispatch.

### A2. Podgląd „co zrobił” — JEST w kontrakcie, NIE MA w danych

`CONTRACT-OPS-STATUS.md` §4 (`live`) definiuje komplet dowodów: `pr_number`, `pr_url`,
`cursor_comment_url`, `github_issue_url`, `wake_state`, `live.recent`, `steps[]`. `OPS.html` już to
renderuje (`renderProof`, `renderLane`, `paintChips`). **Problem:** tick (`workflow-lab`) jako
„budzik + sekretarz” **nie pisze** tych pól do `ops-status.json` na koniec runu → HUD zostaje pusty.
To nie jest błąd tego repo — to luka producenta danych.

### A3. Raporty push — INFRASTRUKTURA JEST, OKABLOWANIA BRAK

- `scripts/push-send.py --ops` **już istnieje**: czyta `data/ops-push-pending.json` i wysyła alert
  Ops przez Web Push (te same subskrypcje co Akademia: `data/push-subscriptions.json`).
- `sw.js` obsługuje push + klik (focus/otwórz OPS.html) — wspólny dla Akademii i Ops.
- **Luka 1:** w `setup-akademia-vps.sh` jest timer tylko `akademia-push.timer → push-send.py --once`
  (poranek), **brak timera `--ops`**.
- **Luka 2:** producent `ops-push-pending.json` to `hermes-ops-tick` (**workflow-lab**) — nie pisze.

### A4. Deploy — stan i granica

- PR **#74** (fix P2 `_NEG_ENV`) jest **otwarty**, branch `fix/dor-neg-env-p2`, **niezmergowany**.
- `deploy-akademia-vps.sh` wymaga `HEAD==origin/main` + czysty tree + gate `deploy-ready` (fail-closed,
  `--force` tylko świadomie). SSH → `root@185.243.54.115:/opt/akademia`.
- Deploy = **Zasada 11** (Dowódca, lokalnie, ręcznie). Merge = **LOCAL-GATE** (`deploy-ready-hermes-ops.sh`
  na `main`). Żadnego nie robię sam.

---

## CZĘŚĆ B — PLAN: DEPLOY (profesjonalnie, bez naruszania Zasady 11)

**Rekomendacja: jeden merge + jeden deploy** (fix P2 + Tier 1 UX razem — min. złożoności).

| Krok | Kto | Co |
| --- | --- | --- |
| 1 | **ja (przygotowanie)** | scalać pracę do jednego brancha; `bash scripts/deploy-ready-hermes-ops.sh` musi PASS |
| 2 | **Dowódca** | review diffu → merge do `main` (LOCAL-GATE zielone) |
| 3 | **Dowódca** | `bash scripts/deploy-akademia-vps.sh` (Zasada 11) |
| 4 | **Dowódca — ja asystuję** | `bash scripts/smoke-hermes-ops-vps.sh` + `curl -u academy:HASLO /ops/diag` |

Mój obowiązek = doprowadzić branch do stanu „deploy-ready na zielono” + zweryfikować smoke po Twoim
deploy. Samego `deploy-akademia-vps.sh` nie uruchamiam (SSH prod = Twoja Zasada 11).

---

## CZĘŚĆ C — PLAN: UX/UI Hermes Ops (max efektu, min złożoności)

Cel: Dowódca **na jednym rzucie oka** widzi (1) co agent robi, (2) co zrobił, (3) co wynikło —
i dostaje to **proaktywnie**, nie tylko po otwarciu `/ops`.

### Tier 1 — „Raport” na `/ops` (czysty UI + vault, zero nowego backendu) — **robię to**

1. **Karta „Raport dnia”** (`panel-report`): agregat z danych, które vault **już wylicza** z
   `ops-status.json` — `today` (runs/merged/failed/waiting), `run.verdict`, `lanes` (długość kolejek),
   `dispatch`, `live` (gdy run trwa). Jedno zdanie-synteza: „Dziś N runów · M mergów · K fail ·
   kolejka N · status PAUSED”.
2. **Sekcja „Ostatnie runy”** — renderuje `live.recent`/`today` gdy tick je napisze; **fail-graceful**
   („brak danych = tick nie zapisał dowodu, nie kasujmy”). Bez dokańczania za tick.
3. **Pętla zwrotna** po komendzie: po `Run next` → jednolity blok wyniku (nie rozsypane chipsy).

Koszt: OPS.html + `ops_status_view` (vault) + test. **Zero nowych serwisów.**

### Tier 2 — proaktywny raport push (okablowanie istniejącej infrastruktury) — **robię to**

1. Nowy `scripts/ops-report.py` (stdlib + import `push-send.build_ops_payload`): czyta
   `ops-status.json`, buduje digest dnia, pisze `data/ops-push-pending.json` (tytuł/ciało/url→OPS.html).
2. `setup-akademia-vps.sh`: dodaj timer `akademia-ops-push.timer → push-send.py --ops` (albo rozszerz
   istniejący). Zasypuje **lukę 1**.
3. Dry-run lokalnie (`--dry-run`) — zero kluczy, zero sieci w teście.

Koszt: 1 skrypt + 1 wpis timer. **Reużywa** subskrypcji i VAPID, które już działają dla Akademii.

### Tier 3 — producent danych (workflow-lab) — **HANDOFF, nie kodzisz tu**

Tick musi **pisać** `ops-status.json.live.*` (pr_number/urls/steps/recent) po każdym runie oraz pisać
`ops-push-pending.json` na zdarzenia (run skończony, HITL czeka, fail). To jest repo `workflow-lab` →
produkuję notkę handoff z dokładnym kontraktem pól (już opisanym w `CONTRACT-OPS-STATUS.md`), nie
edytuję tam niczego.

---

## CZĘŚĆ D — Zakres/luka (szczerze)

Bez Tier 3 nawet idealny UI/push pokaże „0 runów, pusto”, bo `workflow-lab` nie daje danych.
Dlatego Tier 1+2 robimy teraz (make-ready), a Tier 3 to osobne repo/GO. Wartość Tier 1+2: (a) naprawa
okablowania push (zapowiedź raportów natychmiast po wzbogaceniu ticka), (b) UI czeka gotowy, (c) fail-graceful bez kłamstw.

---

## CZĘŚĆ E — Decyzje Dowódcy (do wypełnienia)

- [ ] **GO Tier 1** — karta Raport + pętla zwrotna (UI/vault, bez nowego backendu)
- [ ] **GO Tier 1+2** — + raport push (skrypt + timer)
- [ ] **STOP / zmiana zakresu**
- [ ] Deploy fixu P2 — teraz osobno, czy **razem z Tier 1+2** (rekomendacja: razem)?

**Granice, których nie przekraczam bez Twojego jawnego GO:** merge do `main`, `deploy-akademia-vps.sh`
(Zasada 11), edycja `workflow-lab`.