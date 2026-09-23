# HERMES-ROLE-CONTRACT — Linear-first, auto-merge, deploy lokalny

**Status:** obowiązuje od split Academy / Ops (2026-09-21).  
**UI nauki:** `/` = `DASHBOARD.html` (4 zakładki).  
**UI pracy:** `/ops` = `OPS.html` (Control Plane).  
**Jak używać (30 s):** [`HERMES-OPS-HOWTO.md`](HERMES-OPS-HOWTO.md).  
**SoT kolejki:** Linear (etykiety), nie GitHub issues.

## Zdania kanoniczne (guard CI)

- **Cursor Cloud Agent jest jedynym executorem kodu w Telefon loopie.**
- **POST /hermes/chat nie ma narzędzi MCP.**
- **Decyzja jest w Linear, nie na GitHubie.**
- **Hermes Engineer + Cursor + CI dowożą aż do merge.**
- **Wgranie na serwer = lokalnie, ręcznie (Zasada 11).**

HITL = wybór i etykieta issue **zanim** ruszy agent. Nie przycisk Merge na GitHubie.

## Role

| Rola | R | A | C | I (nie robi) |
| --- | --- | --- | --- | --- |
| Dowódca | Linear (wybór + etykieta), deploy lokalny | decyzja toru | R7 / blocked | review diffu, merge z telefonu |
| Cursor Cloud Agent | kod, branch, PR | wykonanie w loopie | — | deploy, sekrety tenanta |
| Hermes Engineer (VPS / `/ops`) | kolejka Linear → `@cursor` → CI → auto-merge **obu** repo | pętla aż do merge | Pause/Stop | deploy, SSH prod, `workflow_dispatch` release |
| Hermes Akademii | nauka A–G, notatki, rytuał DZIEŃ | PWA kursu | — | DeepSeek, git, Linear write, MCP, PR |
| CI labu (`validate`/`execute`) | jakość kodu przed auto-merge labu | required checks | — | — |
| CI platformy (required z AGENTS.md) | jakość kodu przed auto-merge `dsaas-platform-main` | required checks | — | deploy |
| academy-gate | kontrakt UI + vault + mutacje | — | — | — |

## Routing Linear (SoT)

- **Hermes Autopilot (jedyny tryb `/ops`):** label `agent`, status kolejki Ready/unstarted, **brak** `hitl:approval-required`, **brak** `blocked` / `blocked:external`. Szablon 6 pól / §0.1 AC — inaczej 400. Dowódca: **Start / Run next / Pause / Stop**.
- **Take over:** Pause + issue → lokalnie. Zero `@cursor`.
- **Lokalnie:** brak `agent` **albo** `hitl:approval-required` **albo** Human review / Security gate. `/ops` pokazuje „zrób na laptopie”. Zero `@cursor`, zero merge.
- **Run all:** tylko gdy `OPS_RUN_ALL=1` (default OFF).
- Worker v1 = **Cursor** tylko. Codex/Claude = późniejszy adapter.

R7 / `hitl:approval-required` = **nie wchodzi do kolejki**. Nie blokuje merge PR, które już jest w torze `agent` i ma zielone CI.

**Telefon nie merguje.** Approval na `/ops` = Pause / Stop / laptop / link CI — nie przycisk Merge.

## Maszyna stanów (S0–S6, brak S-deploy)

| Krok | Co | Werdykt |
| --- | --- | --- |
| S0 | Issue Linear + etykieta | PASS / FAIL / UNKNOWN |
| S1 | 6 pól + `agent` | jak S0 |
| S2 | `@cursor` na GitHub twin | PASS / FAIL / UNKNOWN |
| S3 | PR `cursor/*` | PASS / FAIL / UNKNOWN |
| S4 | required checks zielone | UNKNOWN nigdy nie jest zielone |
| S5 | (historyczny review mobile) — nie jest bramką merge | — |
| S6 | squash/merge labu **i** platformy | orchestrator |
| — | deploy / ENT-12 / restart | **nie istnieje w orchestratorze** |

Werdykt: `PASS` | `FAIL` | `UNKNOWN`. **UNKNOWN nigdy nie jest zielone.**

## Flaga e2e

`engineer_loop_e2e`: **true** — dowód: `docs/ops/engineer-loop-e2e.json`.

## LLM

Akademia = **0** tokenów modelu. Brief Ops = szablon, nie DeepSeek. DeepSeek-flash może zostać na VPS dla Engineera, ale nie jest mózgiem kursu.
