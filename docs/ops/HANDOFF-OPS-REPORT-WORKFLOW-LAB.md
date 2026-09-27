# Handoff → workflow-lab: kontrakt danych, żeby raporty Ops ożyły

**Od:** akademia (to repo) · **Do:** `workflow-lab` (orchestrator / hermes-ops-tick)
**Data:** 2026-09-27 · **Status:** wymóg danych, nie zmiana kodu w tym repo

## co już zrobiliśmy po stronie Akademii (nie musisz tego dotykać)

Akademia ma teraz **cały tor raportowania Ops** — brakuje tylko danych z ticka:

- Karta **„Raport”** na `/ops` (`#report-line`, `OPS.html`) — renderuje syntezę z `ops-status.json`.
- `scripts/ops-report.py` + timer `akademia-ops-report.timer` (co 15 min) — **automatycznie**
  wyprowadza raport z `ops-status.json` (werdykt `done`/`failed`/`running` → Web Push do Dowódcy),
  idempotentnie (tylko delta). Reużywa VAPID + subskrypcji Akademii.
- `scripts/push-send.py --ops` — dostarcza `data/ops-push-pending.json` (już istniał).

**Konkluzja:** tick **nie musi** pisać `ops-push-pending.json` do raportu dziennego/zdarzeń —
akademia sama to wyprowadza. Tick pisze tylko **bogaty `ops-status.json`**, a reszta dzieje się sama.

## czego brakuje w ticku (to blokuje raporty = „0 runów, pusto”)

Wg [`CONTRACT-OPS-STATUS.md`](CONTRACT-OPS-STATUS.md) tick **musi** pisać po każdym runie:

| Pole | § | Po co |
| --- | --- | --- |
| `updated_at` (heartbeat co ≤15 min) | §2 | `tick_alive`, dispatch |
| `today.runs / merged / failed / waiting` | §2 | karta Raport + push „Dziś N runów…” |
| `live.issue / step / steps[]` (PASS/FAIL/RED per krok) | §4 | `derive_run` → werdykt `done`/`failed`/`running` |
| `live.pr_number` + ewent. `pr_url` | §4 | `done` wymaga PR + 6/6 PASS |
| `live.wake_state`, `live.cursor_comment_url` | §4 | dowód wake-up |
| `live.recent[]` (opcjonalne) | §4 | historia/karta Raport |

**Reguła fail-closed:** `derive_run` zwraca `done` **tylko** gdy `pr_number` + 6/6 `PASS`. Brak tych
pól = `paused`/`idle` (uczciwie, nie „DONE” na kłamstwo).

## zdarzenia „specjalne” (opcjonalne, masz już kanał)

Dla alertów, których **nie** da się wyprowadzić z liczników (np. „gates czerwony — nie merguj”,
„HITL czeka na Dowódcę”), tick może pisać `data/ops-push-pending.json`:

```json
{ "title": "Hermes Ops — HITL czeka", "body": "QUI-100 czeka na Twoją decyzję.",
  "url": "./OPS.html", "tag": "hermes-ops-hitl" }
```

`push-send.py --ops` (timer co 15 min) ją dostarczy i sprzątnie. Raport dzienny/zdarzeniowy i tak
idzie osobno przez `ops-report.py` — nie kolidują.

## benchmark (co dostaje Dowódca po wdrożeniu u Ciebie)

- Run skończony + zmergowany → push „Ostatni run DONE — merge OK (PR #…)”.
- Run padł → push „Ostatni run FAILED (step N)”.
- Brak ruchu → **cisza** (koniec spamu „nic się nie dzieje”).

Zero zmian po stronie Akademii wymaganych — to tylko wzbogacenie pól, które kontrakt już definiuje.