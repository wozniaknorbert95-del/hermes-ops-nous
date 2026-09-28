# Handoff — deploy P0 nav `/ops` — 2026-09-28

**Status:** Live. HEAD `01afcfe` == origin/main. GO Dowódcy na deploy wykonane.

## Co zrobione

- Bramka: `bash scripts/deploy-ready-hermes-ops.sh` — DEPLOY READY, HEAD == origin/main, drzewo czyste przed deployem.
- Deploy: `bash scripts/deploy-akademia-vps.sh` (bez `--force`) — exit 0. Pakiet `01afcfe`.
- Smoke VPS: `SMOKE PASS: Hermes Ops (vault + diag)`. Public GET `/ops` HTTP 200. `/ops/diag` ok, `tick_alive=true`. systemd timer+path active.
- Live `GET /ops/status`: `recommended_issue` QUI-104, `reason_code=dor_ok`, `selected=true`, URL `https://`. OPS.html na VPS: `linearUrl`, `<a class="issue">`, `#btn-use-rec`, `select_next`.

## Co live

- Nauka: `https://akademia.quietforge.flexgrafik.nl/` (vault `:8097` health ok).
- Praca: `https://akademia.quietforge.flexgrafik.nl/ops` — P0 #1 Linear href + P0 #2 Użyj tego.
- Hasła: VPS `/opt/akademia/CREDENTIALS.local.txt` (nie w repo).

Obserwacja (nie blocker): nginx warn `conflicting server name api.zzpackage.flexgrafik.nl` (inny vhost). Hermes LLM na VPS wyłączony — czat lokalnym silnikiem (klucze `.env` poza tą sesją).

## Co zablokowane

Brak. Backlog P1–P3 (IA, hierarchia przycisków, Take over confirm, klawiatura) czeka na osobne GO.

## Następny krok

GO na **P1 IA** `/ops` (fold + hierarchia) **albo** stop — P0 jest na produkcji.

## Komendy weryfikacji (copy-paste)

```
bash scripts/deploy-ready-hermes-ops.sh
# na VPS:
curl -fsS http://127.0.0.1:8097/health
curl -fsS http://127.0.0.1:8097/ops/diag
bash scripts/smoke-hermes-ops-vps.sh
```

Oczekiwane: DEPLOY READY · health ok · SMOKE PASS.

## Pliki dotknięte

Kod P0 już na `main` (`01afcfe`, PR #84). Po smoke, lokalnie (jeszcze nie commit):

- `docs/ops/PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md` — §9 smoke [x], status LIVE
- `docs/ops/README.md` — PLAN = P0 live
- `docs/ops/UX-SPEC-HERMES-OPS-ENTERPRISE.md` — wskaźnik P0 live
- `docs/handoffs/2026-09-28-ops-p0-deploy.md`

`git status` w chwili zapisu: `main...origin/main`, trzy docs zmodyfikowane + ten handoff (nie commit — `/handoff` nie commituje).
