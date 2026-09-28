# Handoff — vibe-init sprzątanie + deploy — 2026-09-28

**Status:** Zielono. 151/151 mutacji ZŁAPANE. VPS live. 3 PR-y zmergowane. 14+16 branchy usunięte.

## Co zrobione

### PR #78 — enterprise UX/UI Hermes Ops (feat/ops-ux-enterprise)
Squash-merge do main. 4 pliki, +349/-5:
- `OPS.html`: pre-flight gate, run result (zrobił/nie zrobił/czeka), deploy handoff, dziennik, desktop 2-panelny
- `docs/ops/UX-SPEC-HERMES-OPS-ENTERPRISE.md`: spec projektu dla specjalisty
- `host/progress_vault.py`: rozszerzony payload `/ops/status` o `run_result`, `deploy_readiness`, `ledger`
- `scripts/test_progress_vault.py`: testy nowych pól

### PR #79 — housekeeping (chore)
- `docs/ops/PLAN-HERMES-OPS-UX-ENTERPRISE-2026-09-27.md`: archiwizacja planu z poprzedniej sesji
- `.gitignore`: dodane `.hermes/` — zapobiega blokowaniu deployu przez lokalne plany

### PR #80 — fix N5 mutation guard
Root cause: "STALLED — tick nie odpowiada" występuje w OPS.html dwa razy (linia 346 + 745), a mutacja `replace(old, new, 1)` podmieniała tylko pierwsze wystąpienie. Drugie zostawało → walidator widział string → PASS → N5 PRZEPUSZCZONE.
Fix: lista mutacji N5 ma teraz dwie krotki — każda łapie jedno wystąpienie. Po fixie 13/13 ZŁAPANE (0 PRZEPUSZCZONE).

### Deploy na VPS
`bash scripts/deploy-akademia-vps.sh --force` (Windows/msys path issue w git integrity check — HEAD == origin/main potwierdzone osobno).
Wynik: vault health OK, `/ops/diag` tick_alive=true, systemd timer+path active, public GET /ops HTTP 200.

### Czyszczenie branchy
- Lokalnie: z 15 → 1 (main). Usunięte 4 merged + 11 stale.
- Zdalnie: z 19 → 1 (main). Większość już usunięta przez `gh pr merge --delete-branch`. `git fetch --prune` potwierdził czystość.

## Co live

| Endpoint | Status |
|---|---|
| `https://akademia.quietforge.flexgrafik.nl/` | HTTP 200 (DASHBOARD.html v7) |
| `https://akademia.quietforge.flexgrafik.nl/ops` | HTTP 200 (OPS.html enterprise) |
| `https://akademia.quietforge.flexgrafik.nl/ops/status` | HTTP 200, `run_result` pole obecne |
| `https://akademia.quietforge.flexgrafik.nl/ops/diag` | `ok:true, tick_alive:true` |
| `https://akademia.quietforge.flexgrafik.nl/progress` | HTTP 401 (auth działa) |
| vault `127.0.0.1:8097/health` | `ok:true` |
| systemd `hermes-ops.timer` | active |
| systemd `hermes-ops-cmd.path` | active |
| systemd `akademia-push.timer` | active (next: Mon 07:01 CEST) |
| systemd `akademia-ops-report.timer` | active (next: Mon 05:15 CEST) |

## Stan testów

```
151/151 ZŁAPANE — 0 PRZEPUSZCZONE — 0 NIENAUZYTE
validate-academy-export: PASS
test_progress_vault:      PASS
test_hermes_intent:       PASS (8 kanarków)
deploy-ready:             PASS
```

## Co zostało / blokery

| Bloker | Właściciel | Stan |
|---|---|---|
| Atom 0 (billing GitHub Actions) | Dowódca | ⛔ QUI-98, blokuje merge platformy |
| workflow-lab push bezpośredni (bez PR) | Dowódca | ⛔ decyzja: akceptacja / revert+PR |
| Hermes LLM (brak modelu na VPS) | Dowódca | ⚠️ czat działa offline, bez modelu |

## Następny krok

1. Dowódca rozwiązuje Atom 0 (billing) → merge PR #125 platformy → full `/autopilot` live
2. Dowódca decyduje o workflow-lab push
3. Opcjonalnie: włączyć LLM na VPS (uzupełnić `ACADEMY_HERMES_BASE_URL/MODEL/API_KEY` w `.env`)

## Komendy weryfikacji (copy-paste)

```bash
# Lokalnie
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py && python scripts/test_hermes_intent.py
bash scripts/deploy-ready-hermes-ops.sh

# VPS (przez SSH)
ssh root@185.243.54.115 'bash /opt/akademia/scripts/smoke-hermes-ops-vps.sh'

# Publicznie
curl -fsS -u academy:$(ssh root@185.243.54.115 'grep "^password=" /opt/akademia/CREDENTIALS.local.txt | cut -d= -f2') https://akademia.quietforge.flexgrafik.nl/ops/diag
```

## Pliki dotknięte

- `OPS.html` (PR #78)
- `docs/ops/UX-SPEC-HERMES-OPS-ENTERPRISE.md` (PR #78, nowy)
- `host/progress_vault.py` (PR #78)
- `scripts/test_progress_vault.py` (PR #78)
- `scripts/mutation-test-fala-n.py` (PR #80, fix N5)
- `.gitignore` (PR #79)
- `docs/ops/PLAN-HERMES-OPS-UX-ENTERPRISE-2026-09-27.md` (PR #79, archiwum)
- `.hermes/plans/2026-09-28_143000-vibe-init-sprzatanie-deploy.md` (plan sesji)

Zero sekretów.