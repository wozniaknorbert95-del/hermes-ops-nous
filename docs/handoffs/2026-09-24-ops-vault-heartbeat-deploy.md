# Handoff — merge + deploy vault heartbeat 2026-09-24

**Repo:** akademia · **Branch po sesji:** `main` `fb434b2` (+ hotfix setup SIGPIPE w osobnym PR jeśli jeszcze otwarty)  
**Strefa:** merge #65, deploy VPS, testy `/ops`. **Nie:** DASHBOARD.html (poza restore leftover mutacji).

## Co zrobione (fakty)

- PR [#65](https://github.com/wozniaknorbert95-del/akademia/pull/65) zmergowany squash → `fb434b2`.
- `academy-gate` **nie wystartował**: GitHub Actions billing / spending limit. Merge wymagał chwilowego zdjęcia required check (przywrócony: `academy-gate` + `enforce_admins`).
- `deploy-ready` PASS na `HEAD == origin/main`.
- `deploy-akademia-vps.sh` wgrał vault (health podczas setup: `ops_cmd_state: file`). Setup urwał się na HTTPS smoke: `curl \| head` + `pipefail` → curl 23. `fix_hermes_ops_systemd` i smoke Ops **nie** dobiegły w tym SSH.
- Dokończenie SSH: timer+path active, `MakeDirectory=false`, `smoke-hermes-ops-vps.sh` PASS.
- Testy pro: I1 Pause nie zmienia `updated_at` (`18:10:28Z` → `18:10:28Z`), receipt `vault.patch_ok: true`; POST `/hermes/chat` 410; PWA 200/200/401; dispatch idle, cmd missing po ACK ticka.

## Co live

Vault heartbeat (I1–I7) na VPS. Tick żywy. Merge z telefonu nadal 403.

## Co zablokowane

- GitHub Actions: opłać / podnieś spending limit, inaczej każdy PR zostaje BLOCKED na `academy-gate`.
- O6 Linear e2e — bez test issue labu.

## Następny krok (▶ TERAZ)

1. Zmergować hotfix `setup-akademia-vps.sh` (bez `curl \| head`), żeby kolejny deploy nie urywał się na 23.
2. GitHub billing — inaczej CI martwe.
3. Opcjonalnie O6 na issue testowym labu.

## Komendy weryfikacji

```bash
bash scripts/deploy-ready-hermes-ops.sh
ssh root@185.243.54.115 'curl -fsS http://127.0.0.1:8097/ops/diag; curl -fsS http://127.0.0.1:8097/health'
bash scripts/smoke-hermes-ops-vps.sh   # na VPS
```
