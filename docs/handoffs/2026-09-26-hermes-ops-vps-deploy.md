# Handoff — Hermes Ops VPS (GO merge + deploy)

**Data:** 2026-09-26  
**Repo:** akademia `main` `c7a7a4a` (PR #71) · platforma `main` squash PR #124  
**Nie:** `workflow-lab` · plan file · platforma VPS · merge z telefonu

## Co zrobione

- Akademia [#71](https://github.com/wozniaknorbert95-del/akademia/pull/71) zmergowany squash → `c7a7a4a`.
- Platforma [#124](https://github.com/wozniaknorbert95-del/dsaas-platform-main/pull/124) zmergowany squash (admin; `gates` billing ≠ regresja kodu).
- Deploy `/opt/akademia` z `main`; vault recreate z `-p akademia --env-file /opt/akademia/.env`.
- `LINEAR_OPS_READ` skopiowany z tick env (`/etc/workflow-lab/hermes-engineer.env`) → `/opt/akademia/.env` (chmod 600). Wartość **SET** w kontenerze (`len 48`). Zero sekretów w logach.

## Co live

- Vault: `http://127.0.0.1:8097/health` ok; `/ops` 200; `/ops/diag` ok, `tick_alive=true`, timer+path **active**.
- Public: `https://akademia.quietforge.flexgrafik.nl/ops` HTTP 200 (basic auth, hasło tylko `CREDENTIALS.local.txt`).
- HUD: `chip-dor` + `Cloud: /gate`; Tokens/Cost usunięte.
- DoR live: `dor.ok=false` `code=qui_lane_local` (kolejka LOCAL — Start fail-closed, zgodnie z kontraktem).
- Pulse: 3 issue (np. QUI-101 `qui_hitl`). `run.dor` obecny.
- `github.com` w GET `/ops/status` = `live.pr_url` / `github_issue_url` z cache ticka (kontrakt `live.*` pozwala). Pulse overlay **bez** GitHub.

Compose v1 (`1.29.2`): `up --force-recreate` → `KeyError: ContainerConfig`. Ścieżka: `down --remove-orphans` + `rm -f` leftover + `up -d` (jak `setup-akademia-vps.sh`).

## Co zablokowane

- Hermes LLM: jeśli `ACADEMY_HERMES_*` puste w `.env`, czat zostaje na silniku lokalnym (stan sprzed tej sesji).
- Platforma: kod na `main`; **brak** deployu produktu platformy (Zasada 11 — GO był na `/ops`).
- Lab git: nie ruszany.

## Następny krok

Fala papieru zamknięta tym handoffem. Na telefonie `/ops` — chip DoR może pokazać `qui_lane_local` dopóki next nie jest Cloud-ready. Start nie woła `@cursor`. Merge z telefonu = nie. Nie ruszaj QUI-102.

## Komendy weryfikacji

```
ssh root@185.243.54.115 'bash /opt/akademia/scripts/smoke-hermes-ops-vps.sh'
curl -fsS http://127.0.0.1:8097/ops/status
# oczekuj: dor + pulse + run.dor; LINEAR w kontenerze SET
```

## Pliki (ta sesja VPS)

Host: `/opt/akademia/.env` (`LINEAR_OPS_READ`) + recreate `akademia-vault`. Kod: `main` `c7a7a4a`.
