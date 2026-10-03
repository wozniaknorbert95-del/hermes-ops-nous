# HERMES-ROLE-CONTRACT — Linear-first, auto-merge, deploy lokalny

**Status:** obowiązuje od split Academy / Ops (2026-09-21). Rewizja prowadzącego: 2026-10-01 ([`PLAN-HERMES-CONDUCTOR-2026-10-01.md`](PLAN-HERMES-CONDUCTOR-2026-10-01.md)).  
**UI nauki:** `/` = `DASHBOARD.html`. Kontrakt nav = 7 tabów (TERAZ wchłania DZIEŃ). Live HTML = 7.  
**UI pracy:** `/ops` = `OPS.html` (Control Plane).  
**Jak używać (30 s):** [`HERMES-OPS-HOWTO.md`](HERMES-OPS-HOWTO.md) — lekcja UI w [`TOOL-MASTERY.md`](TOOL-MASTERY.md) (karta Hermes Engineer), nie na TERAZ.  
**SoT kolejki:** Linear (etykiety), nie GitHub issues.

## Zdania kanoniczne (guard CI)

- **Cursor Cloud Agent jest jedynym executorem kodu w Telefon loopie.**
- **POST /hermes/chat nie ma narzędzi MCP.**
- **Decyzja jest w Linear, nie na GitHubie.**
- **Hermes Engineer + Cursor + CI dowożą aż do merge.**
- **Wgranie na serwer = lokalnie, ręcznie (Zasada 11).**
- **Hermes Engineer nie commituje kodu platformy.**
- **S2 = Cursor Cloud Agents API, nie komentarz @cursor.**
- **Tick nie woła POST /v1/agents.**

HITL = wybór i etykieta issue **zanim** ruszy agent. Nie przycisk Merge na GitHubie.

## Dwa Hermesy

| | Hermes Akademii (`/`) | Hermes Engineer (`/ops`) |
| --- | --- | --- |
| Jest | nauczyciel + szablon poranka | prowadzący sesji (Nous); tick tylko heartbeat + HUD |
| Robi | cytuje plik, składa brief z danych kursu | Linear → Cloud API → weryfikacja AC×DoD → CI → auto-merge |
| Tokeny | **0** (brief = szablon, nie model) | Nous na VPS (lab e2e); nie jest mózgiem kursu |
| Na TERAZ | poranek, jeden ruch, pytanie z `lab`, linia stanu kolejki | jedna linia `Kolejka: N · PASS\|FAIL\|UNKNOWN` + link |
| Nie robi | MCP, git, Linear write, PR, zapis postępu za Dowódcę, deploy | kod platformy, deploy, SSH prod, merge z telefonu, nauka na foldzie Akademii |

Mieszanie ich w karcie „Praca — Hermes Ops” na TERAZ jest zakazane. Instrukcja 30 s, 6 pól, Pause/Stop/Take over, Approval ≠ Merge = karta NARZĘDZIA.

## Role

| Rola | R | A | C | I (nie robi) |
| --- | --- | --- | --- | --- |
| Dowódca | Linear (wybór + etykieta + `work_mode`), deploy lokalny | decyzja toru | R7 / blocked | review diffu, merge z telefonu |
| Cursor Cloud Agent | kod, branch, PR | wykonanie w loopie (Cloud API) | — | deploy, sekrety tenanta |
| Hermes Engineer (Nous / `/ops`) | brief + sesja Cloud API + narzędzie D + raport | pętla aż do merge albo HITL | Pause/Stop | commit kodu, deploy, SSH prod, `workflow_dispatch` |
| Tick (`workflow-lab`) | heartbeat + zapis `ops-status.json` z Nousa | adapter statusu | — | `POST /v1/agents` (zakaz drugiego S2) |
| Hermes Akademii | poranek TERAZ, jeden ruch B–G, powtórka z `lab`, notatki | PWA kursu | — | DeepSeek, git, Linear write, MCP, PR, dopisywanie DoD |
| CI labu (`validate`/`execute`) | jakość kodu przed auto-merge labu | required checks | — | — |
| CI platformy (required z AGENTS.md) | jakość kodu przed auto-merge `dsaas-platform-main` | required checks | — | deploy |
| academy-gate | kontrakt UI + vault + mutacje | — | — | — |

## Hermes Akademii — szablon (0 tokenów)

Poranek i „jeden ruch” **nie są generacją**. Składają się z danych: otwarty rozdział B–G, DoD, brakujące kroki lab, LOCK dnia, zaliczone id.

- Nagłówek zostaje: `❯ HERMES PRZYGOTOWAŁ PORANEK` + data. Jedno zdanie: co policzone / czego nie wie.
- **Jeden ruch** na `dsaas-platform-main`: najmniejszy krok, który domyka otwarty DoD albo pierwszy niezaliczony rozdział w kolejności B→C→D→E→F→G. A i H nie zajmują tego miejsca.
- **Jedno pytanie** bierze z tablicy `lab` **już zaliczonego** rozdziału. Brak zaliczeń = puste. Nie wymyśla pytania.
- Gdy brak pliku: **„Nie podam — i nie mam czego podać.”**
- Nie zapisuje postępu, nie odhacza checkboxów, nie merguje, nie deployuje.

## Hermes Ops — 24 h ≠ deploy

**24 h** = brief kolejki gotowy, zanim Dowódca usiądzie. Liczy: N issue w torze `agent`, werdykt PASS|FAIL|UNKNOWN, otwarty DoD z kanonu jeśli jest w danych. Mówi, czego nie wie. Nie pisze eseju.

Nocny merge jest dozwolony **tylko** tam, gdzie ten kontrakt już pozwala: etykieta `agent`, 6 pól, CI zielone, brak R7 / `hitl:approval-required`, warstwa D PASS.  
Deploy, ENT-12, restart usług = **nie istnieje** w orchestratorze. Zostaje u Dowódcy (Zasada 11).

Slice prowadzenia sesji (Nous + Cloud API) = **WYKONANY** w labie ([`conductor-slice-e2e.json`](conductor-slice-e2e.json)). HUD fail-closed: `running` tylko z https `run_url`. Merge labu i deploy HTML = osobne GO.

## Anty-slop (cytuj plik albo odmawiaj)

Każde odrzucenie ma kotwicę. Brak kotwicy = „nie wiem”, nie nowa reguła.

| Slop | Kotwica |
| --- | --- |
| Vibe-coding bez lint/test/build | `AGENTS.md` §2 (lab i platforma) — parity komend z CI |
| Filtr w aplikacji zamiast RLS | `runtime/db.py` + `kanon/KONSTYTUCJA.md` |
| Token z ciała żądania | `runtime/tenant_auth.py` (S-12) |
| Model klika produkcję | `runtime/approval_queue.py` (recorded-not-executed) |
| JSONL w git jako SoT | `kanon/DOD-PLATFORMY.md` (0 jsonl) |
| Growth mimo veta R7 | `polityki/opa/r7_veto.rego` + `runtime/growth_gate.py` |
| Sprzedaż całego OS zamiast skanu | `docs/akademia/SKU-SKAN-DECYZJI-MKB.md` |
| Nowy moduł zamiast rozmowy z właścicielem | dział G / H3 — pieniądz przed budową |
| UNKNOWN jako zielone | ten plik, S4 |
| Merge z telefonu | ten plik, „Telefon nie merguje” |
| Deploy z `/ops` | Zasada 11 + wiersz S-deploy |
| Instrukcja `/deploy` `/publish` `/skip-gate` `/force-merge` w wake | paleta `.cursor/commands/` platformy (EV-454) — anty-lista nie jest uczona |
| Tick woła Cloud API (drugi S2) | ten plik, wiersz Tick |
| LLM maluje FAIL D na PASS | [`hermes-conductor/CONDUCTOR.md`](hermes-conductor/CONDUCTOR.md) krok 5 |

## Routing Linear (SoT)

- **Hermes Autopilot (jedyny tryb silnika `/ops`):** label `agent`, status kolejki Ready/unstarted, **brak** `hitl:approval-required`, **brak** `blocked` / `blocked:external`. Szablon 6 pól / §0.1 AC — inaczej 400. Dowódca: **Start / Run next / Pause / Stop** + chip `work_mode` (`buduj` \| `testuj` \| `ulepszaj`).
- **DoR przed sesją Cloud API:** `POST /ops/run` 400: `qui_dor_not_ready` · `qui_hitl` · `qui_blocked` · `qui_lane_local` · `qui_todo_mismatch` · `qui_dirty_pr`. Brak `LINEAR_OPS_READ` = fail-closed. Słowo `workflow_dispatch` w AC **nie** spycha na LOCAL.
- **Take over:** Pause + cancel/archive sesji Cloud + issue → lokalnie. Zero follow-up do Cursora.
- **Lokalnie:** brak `agent` **albo** `hitl:approval-required` **albo** Human review / Security gate. `/ops` pokazuje „zrób na laptopie”. Zero sesji Cloud, zero merge.
- **Run all:** tylko gdy `OPS_RUN_ALL=1` (default OFF). QUI-88: brak auto-chain po stale lock / PAUSED.
- Builder = **Cursor Cloud API** tylko. Nous nie commituje.

R7 / `hitl:approval-required` = **nie wchodzi do kolejki**. Nie blokuje merge PR, które już jest w torze `agent` i ma zielone CI.

**Telefon nie merguje.** Approval na `/ops` = Pause / Stop / laptop / link CI — nie przycisk Merge.

## Maszyna stanów (S0–S6, brak S-deploy)

| Krok | Co | Werdykt |
| --- | --- | --- |
| S0 | Issue Linear + etykieta | PASS / FAIL / UNKNOWN |
| S1 | 6 pól + `agent` | jak S0 |
| S2 | Nous: create/follow-up Cursor Cloud Agents API + `live.agent.run_url` (nie komentarz `@cursor`); procedura `/autopilot` w briefie | PASS / FAIL / UNKNOWN |
| S3 | PR `cursor/*` | PASS / FAIL / UNKNOWN |
| S4 | required checks + lista AC + DoD ids; puste testy w RUNNING = UNKNOWN | UNKNOWN nigdy nie jest zielone |
| S5 | (historyczny review mobile) — nie jest bramką merge | — |
| S6 | squash/merge labu **i** platformy | orchestrator po D PASS |
| — | deploy / ENT-12 / restart | **nie istnieje w orchestratorze** |

Werdykt: `PASS` | `FAIL` | `UNKNOWN`. **UNKNOWN nigdy nie jest zielone.**

## Flaga e2e

`engineer_loop_e2e`: **true** po [`conductor-slice-e2e.json`](conductor-slice-e2e.json) (`github_pr` + https `run_url`). Stary `engineer-loop-e2e.json` (W-06 / `@cursor`) **nie** zapala AKTYWNY.

## LLM

Akademia = **0** tokenów modelu. Brief Ops = szablon albo Nous conductor — nie DeepSeek jako mózg kursu.
