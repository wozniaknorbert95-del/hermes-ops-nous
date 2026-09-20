# HERMES-ROLE-CONTRACT — dwa byty, jeden loop

**Status:** obowiązuje od Fali A (Dual-Control Plane).  
**SoT playbooku telefonu:** `PLAYBOOK_PHONE` w `DASHBOARD.html` (6 kroków).  
**UI dla Dowódcy:** zakładka **INSTRUKCJA** w `DASHBOARD.html` + mirror [`AKADEMIA-INSTRUKCJA.md`](AKADEMIA-INSTRUKCJA.md).

## Zdania kanoniczne (guard CI)

- **Cursor Cloud Agent jest jedynym executorem kodu w Telefon loopie.**
- **POST /hermes/chat nie ma narzędzi MCP.**

## Macierz RACI (skrót)

| Rola | R | A | C | I (nie robi) |
| --- | --- | --- | --- | --- |
| Dowódca | GO platformy, review mobile, sekrety | merge/deploy `dsaas-platform-main` | decyzje R7 | — |
| Cursor Cloud Agent | kod, branch, PR | wykonanie w Telefon loopie | — | merge platformy bez GO |
| Hermes Engineer (VPS) | obserwacja S1–S6 | alarm ciszy supervisora | „krok N: zrób X” | push, merge poza polityką labu, deploy |
| Hermes Akademii (czat) | nauka, rytuał, kierunek kursu | odpowiedź read-only | — | git, Linear write, MCP, PR |
| CI labu (`validate`/`execute`) | — | jakość kodu przed auto-merge labu | — | — |
| academy-gate | — | kontrakt UI + vault + mutacje | — | — |

## Maszyna stanów Telefon loop (S1–S6)

| Krok | Co | Dowód (evidence) | Plik SoT |
| --- | --- | --- | --- |
| S1 | Issue w Linear (6 pól, etykieta `agent`) | issue id + pola | `workflow-lab/docs/LINEAR.md` |
| S2 | `@cursor` trigger | komentarz / run Cloud | `workflow-lab/docs/W2-CLOUD-AGENTS.md` |
| S3 | Cloud Agent buduje PR | PR URL `cursor/*` | `workflow-lab/.cursor/environment.json` |
| S4 | CI zielone | `validate` + `execute` success, job wykonał kroki | `workflow-lab/.github/workflows/ci.yml` |
| S5 | GitHub mobile review | polityka W6 | `workflow-lab/docs/W6-PHONE-LOOP.md` |
| S6 | Auto-merge labu | squash na `main` labu | `workflow-lab/DECISIONS.md` |

Werdykt kroku: `PASS` | `FAIL` | `UNKNOWN`. **UNKNOWN nigdy nie jest zielone.** Cisza supervisora = alarm (`SUPERVISOR_SILENCE`).

## Flaga e2e (karta NARZĘDZIA)

`engineer_loop_e2e`: **true** — dowód: `docs/ops/engineer-loop-e2e.json` + replay W-06 PR #34 (`phone-loop-status --pr 34` → step 6 PASS). Karta NARZĘDZIA: `ENGINEER_LOOP_E2E=true`.

## Most do platformy (Fala D)

Auto-merge **labu** ≠ auto-merge / deploy **`dsaas-platform-main`**. Cloud Agents na dsaas = STOP (karta NARZĘDZIA). Draft issue/PR pod platformę tylko po zielonym loopie labu + HITL Dowódcy. Runbook: `workflow-lab/docs/ops/PLATFORM-HITL-BRIDGE.md`.

## Implementacja labu (Fala C)

- Status: `workflow-lab/scripts/phone-loop-status.py`
- Głos operatora: `workflow-lab/scripts/hermes-operator-brief.py`
- Sekrety: `workflow-lab/docs/ops/HERMES-ENGINEER-SECRETS.md`
- Watchdog: `workflow-lab/docs/ops/phone-loop-watchdog.md`

## LLM

DeepSeek-flash (Hermes Akademii / Engineer) = **głos i streszczenie** werdyktu deterministycznego. Nie zmienia enuma PASS/FAIL/UNKNOWN ani nie zastępuje Cursora.
