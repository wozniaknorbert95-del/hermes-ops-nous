# Handoff — weryfikacja merge + deploy (2026-10-16)

**Rytuały:** `/ops-audit` → `/ops-deploy`  
**GO Dowódcy:** tak (chat)  
**Repo:** `hermes-ops-nous` @ `main` `3d4ef09`

## Plan weryfikacji (wykonany)

| Krok | Cel | Wynik |
| --- | --- | --- |
| V0 `/ops-audit` | main sync, PR stan, vault test | PASS |
| V1 merge | lab #104 + #108; nous #4 | PASS |
| V2 `/ops-deploy` | `deploy-akademia-vps.sh` z main | PASS |
| V3 smoke | health/diag/public /ops + Start→URL | PASS |
| V4 handoff | ten plik | PASS |

## Merge

| PR | Repo | SHA | Stan |
| --- | --- | --- | --- |
| [#104](https://github.com/wozniaknorbert95-del/workflow-lab/pull/104) | workflow-lab | `cf32acb` | MERGED — early live + create-on-issue |
| [#108](https://github.com/wozniaknorbert95-del/workflow-lab/pull/108) | workflow-lab | `8b55c80` | MERGED — anti create-spam (`missing_cmd_id`) |
| [#4](https://github.com/wozniaknorbert95-del/hermes-ops-nous/pull/4) | hermes-ops-nous | `3d4ef09` | MERGED — T1c/T3 docs + vault hints |

## Deploy

- Komenda: `bash scripts/deploy-akademia-vps.sh` (Git Bash, HEAD == origin/main)
- Vault: `akademia-vault` Up; `/health` ok
- Public: `GET /ops` HTTP 200; `smoke-hermes-ops-vps.sh` **SMOKE PASS**
- Obraz conductor: `hermes-conductor:local` po #108 (`31509141787d`); rollback tags: `rollback-20261016T0426`, `rollback-20261016T0443`
- Env: `CURSOR_API_KEY=SET`, `OPS_RUN_ALL=1`
- Tick: `hermes-ops.timer` + `hermes-ops-cmd.path` active; `tick_alive=true`

## Incident w trakcie weryfikacji → fix

**Objaw:** po T3 journal spam `conductor created` co ~7s (koszt Cloud).  
**Przyczyna:** handoff z `issue_id` + pusty `cmd_id` → `same_cmd` zawsze false → create w każdej iteracji.  
**Mitigation:** stop service + clear handoff.  
**Fix:** workflow-lab #108 — empty `cmd_id` → `refuse=missing_cmd_id` lub unchanged jeśli URL już jest.  
**Dowód po fix:** idle bez create; potem QUI-131 Start bez pętli (`anti_spam_ok True`).

## Smoke Start po deploy

| Issue | Wynik | create_ms | URL |
| --- | --- | --- | --- |
| QUI-130 | REFUSE `ZASADA_11` | — | tytuł zawierał słowo „deploy” — policy OK |
| QUI-131 | **PASS** | 2814 | `https://cursor.com/agents/bc-fe0a3aae-6569-4190-88ef-38050c8fd0f7` |

ops-status po ticku: `RUNNING` + ten sam https URL. Zero ręcznego bind.

## Czy działa jak oczekiwaliśmy?

| Oczekiwanie | Werdykt |
| --- | --- |
| Merge brain na main + image na VPS | TAK |
| Deploy vault z merged main (Zasada 11) | TAK |
| Start → https `run_url` ≤3 min | TAK (QUI-131) |
| Brak create-spam | TAK po #108 |
| OPS.html freeze / zero polish | TAK |
| T2 kill-switch | N/A (T1 PASS) |

## NEXT

1. Produktowa kolejka Autopilot (nie lab probe) — świadomy Start / `run_all`.
2. Unikać słowa „deploy” w tytułach issue labu (false `ZASADA_11`).
3. Cienki chat HUD — tylko osobne GO po Direction Lock.

## Rollback

```bash
# vault: poprzedni tar nie trzymamy — redeploy starszego main SHA
# conductor:
docker tag hermes-conductor:rollback-20261016T0443 hermes-conductor:local
systemctl restart hermes-conductor
```
