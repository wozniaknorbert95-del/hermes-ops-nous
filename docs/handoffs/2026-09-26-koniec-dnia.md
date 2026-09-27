# Handoff — koniec dnia (Hermes Engineer + VPS)

**Data:** 2026-09-26  
**Repo:** akademia `main` `fa7922f`  
**Nie:** `workflow-lab` · plan file · QUI-102 · merge z telefonu · deploy platformy

Ten plik **zastępuje** NEXT w `2026-09-26-hermes-ops-engineer.md` i `2026-09-26-hermes-ops-vps-deploy.md` (ten drugi ma stale `qui_lane_local`).

## Co zrobione

- Audyt Cloud 3290 + HUD 3 strefy + bramka DoR: [#71](https://github.com/wozniaknorbert95-del/akademia/pull/71) → `c7a7a4a`.
- Platforma pętla `/vibeinit→/gate` + strażnik CI: [#124](https://github.com/wozniaknorbert95-del/dsaas-platform-main/pull/124) squash admin (`gates` billing ≠ regresja).
- Papier deployu: [#72](https://github.com/wozniaknorbert95-del/akademia/pull/72).
- `LINEAR_OPS_READ` **SET** w `/opt/akademia/.env` i w `akademia-vault` (kopia z `/etc/workflow-lab/hermes-engineer.env`, zero sekretów w logach).
- `deploy-ready` PASS na `fa7922f`. Deploy VPS (pack `main` → `/opt/akademia`). Nested `deploy-ready` w `deploy-akademia-vps.sh` na Windows bywa flake (`OSError 22` na `DASHBOARD.html`) — po udowodnionym PASS: integralność git + `--force` (tylko pack/setup).
- Fałszywy LOCAL: zakres „zero VPS” łapał marker `vps `. Fix: [#73](https://github.com/wozniaknorbert95-del/akademia/pull/73) → `fa7922f`, redeploy.

## Co live

- Public: `https://akademia.quietforge.flexgrafik.nl/ops` HTTP 200 (basic auth → `CREDENTIALS.local.txt`).
- Vault `127.0.0.1:8097`: `/health` ok, `/ops/diag` `tick_alive`, `ops_cmd_state=file`, timer+path **active**.
- HUD: `chip-dor` + `Cloud: /gate`; Tokens/Cost nie ma.
- DoR **po #73:** `dor.ok=true` `code=ok` **QUI-93**. Pulse 3: QUI-100, QUI-101, QUI-93.
- Compose v1: nie `--force-recreate`; `down` + `up -d` (`setup-akademia-vps.sh`).
- PWA: manifest 200, HTML bez hasła 401.

## Co zablokowane

- **Start na QUI-93 obudzi Cloud** (DoR zielony). #115 nadal brudny vs `main`. Właściciel: Dowódca — nie tapaj bez GO.
- QUI-102 Blocked + worktree — nie ruszać (`aktywne_zadanie`).
- QUI-100 / QUI-101: `hitl:approval-required` — Start 400 `qui_hitl`.
- Czat Akademii: `llm=false` (`ACADEMY_HERMES_*` puste) — nie ta fala.
- Platforma: kod na `main`, **brak** deployu produktu.
- Lab git: nie ruszany.

## Następny krok

**Jeden TERAZ:** rano otwórz `/ops` na telefonie, **nie** Start, dopóki nie ma GO na Cloud QUI-93. Commit tego handoffa = osobne GO (mały chore-PR).

## Komendy weryfikacji

```
ssh root@185.243.54.115 'bash /opt/akademia/scripts/smoke-hermes-ops-vps.sh'
ssh root@185.243.54.115 'curl -fsS http://127.0.0.1:8097/ops/status'
# oczekuj: dor.ok true, id QUI-93, code ok; pulse 3; LINEAR SET w kontenerze
docker exec akademia-vault python -c "import os; v=os.environ.get('LINEAR_OPS_READ',''); print('LINEAR', 'SET' if v.strip() else 'EMPTY')"
```

Lokalnie przed kolejnym deployem:

```
bash scripts/deploy-ready-hermes-ops.sh
```

## Pliki (sesja)

Akademia `main`: #71 HUD/DoR · #72 handoff VPS · #73 `ops_linear_dor.py` + test vault.  
Platforma `main`: #124.  
Host: `/opt/akademia/.env` (`LINEAR_OPS_READ`) + vault recreate.  
Ten plik: `docs/handoffs/2026-09-26-koniec-dnia.md` (lokalnie, nie na `main` aż do chore-PR).
