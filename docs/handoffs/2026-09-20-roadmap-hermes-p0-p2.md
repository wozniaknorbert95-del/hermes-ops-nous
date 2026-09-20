# Handoff — roadmap Hermes P0–P2 (2026-09-20)

## Co zrobiono (agent)

| Priorytet | Akcja | Stan | Dowód |
|-----------|--------|------|--------|
| **P0** | PAT read-only → `/etc/workflow-lab/hermes-engineer.env` (600) + `verify-engineer-pat.sh` → merge **403** | **BLOCKER (Dowódca)** | Fine-grained PAT nie da się wygenerować przez API; pełny `gh auth token` na VPS daje merge **200** — env **wyczyszczony**. Runbook: `workflow-lab/scripts/verify-engineer-pat.sh` + `HERMES-ENGINEER-SECRETS.md`. |
| **P0** | Clone lab `/opt/workflow-lab` + timer | **DONE** | `hermes-phone-loop.timer` **active**, `phone-loop-status.py --pr 34` → krok **6 PASS** (≠ UNKNOWN). |
| **P1** | Jeden loop W-06 z telefonu (log S1→S6 = GitHub) | **CZĘŚCIOWO** | Replay API + `engineer-loop-e2e.json` (lab + akademia). **Fizyczny telefon** — nie wykonany przez agenta. |
| **P1** | PR akademia `ENGINEER_LOOP_E2E=true` | **DONE** | [#31](https://github.com/wozniaknorbert95-del/akademia/pull/31) → merge `e75431b`, deploy VPS OK. |
| **P2** | Draft issue platformy R7 | **DONE** | [dsaas-platform-main#81](https://github.com/wozniaknorbert95-del/dsaas-platform-main/issues/81) — **zero merge bez GO**. |

## Deploy

- **Akademia VPS:** `main` @ `e75431b`, health OK, Hermes LLM OK, HTTPS smoke OK.
- **Lab VPS:** timer co ~5 min, status script bez tokena dla publicznego PR #34.

## Testy (lokalnie + CI)

- `validate-academy-export.py` PASS (nowy guard: `true` wymaga `docs/ops/engineer-loop-e2e.json`).
- Mutacje Fala L **6/6** (L3 usuwa JSON na czas testu).
- CI **academy-gate** na #31: PASS.
- Live: `hermes-eval --digest-only` PASS na VPS.

## Chrome / UX (surowo)

**Działa**

- Skok **Hermes Engineer → NARZĘDZIA** (`#tool-hermes-engineer`) — scroll + zakładka OK.
- Badge **AKTYWNY W LABIE** przy `ENGINEER_LOOP_E2E=true` (DOM: `tool-hermes-engineer`).
- 6 zakładek, statusbar, brak błędów konsoli w szybkim przejściu TERAZ/NARZĘDZIA/HERMES (localhost).

**Nie / słabo**

- **Audyt produkcyjny z Basic Auth** — nie pełny walkthrough w tej sesji (hasło tylko na VPS; bez wklejania do chata).
- **P0 PAT** — bez read-only tokena timer na VPS nie ma sensownego `verify-engineer-pat` PASS; status PR nadal działa publicznym API dla #34.
- **Telefon loop fizyczny** — jedyna brakująca linia P1; JSON ≠ dowód UX na urządzeniu.
- Instrukcja Engineer w manualu nadal wspomina „Po Fali C4 e2e” — treść historyczna; status UI już AKTYWNY W LABIE (kosmetyka copy, opcjonalny follow-up).

## Następny krok (Dowódca, ~5 min)

1. GitHub → **Fine-grained PAT** (repo workflow-lab + akademia): Contents/PR/Checks/Actions **Read**, 90 dni.
2. Na VPS: `nano /etc/workflow-lab/hermes-engineer.env` → `GITHUB_ENGINEER_TOKEN=…`, `chmod 600`.
3. `bash /opt/workflow-lab/scripts/verify-engineer-pat.sh` — oczekiwane: merge **403**, reszta PASS.
4. Opcjonalnie: jeden W-06 z telefonu → dopisać timestamp do `engineer-loop-e2e.json`.

## Git

- `main` zsynchronowany z origin po #31.
- Zremote'owane gałęzie zmergowane — `git fetch --prune` wykonany; lokalne `feat/hermes-*` można skasować ręcznie jeśli już niepotrzebne.
