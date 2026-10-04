# AGENTS.md — hermes-ops-nous

You are editing **Hermes Ops Nous** (Control Plane), not `akademia` and not `workflow-lab`.

1. UI SoT: `OPS.html` — czytelny styl terminala, białe tło, zero gradientów, wszystko klikalne.
2. Kontrakt: `docs/ops/HERMES-ROLE-CONTRACT.md` — Linear-first, auto-merge, deploy lokalny.
3. Orchestrator tick: `workflow-lab` (`scripts/hermes_ops/`), nie ten repo.
4. Vault: `host/progress_vault.py` — sync postępu, heartbeat.
5. No secrets. No OIDC tokens in `academia_url`.
6. Deploy = lokalnie, ręcznie (Zasada 11). Zero `workflow_dispatch`.
7. Telefon nie merguje. Approval na `/ops` ≠ Merge na GitHubie.

## Komendy projektu (must-have)

```
dev lokalny:    python -m http.server 8765
                → http://localhost:8765/ops
testy:          python scripts/smoke-hermes-ops-vps.sh
deploy VPS:     bash scripts/deploy-akademia-vps.sh
TLS po DNS:     bash scripts/finish-akademia-tls.sh
smoke VPS:      curl -fsS http://127.0.0.1:8097/health
smoke ops VPS:  bash scripts/smoke-hermes-ops-vps.sh
smoke ops loop: curl -fsS http://127.0.0.1:8097/ops/status && curl -fsS http://127.0.0.1:8097/ops/diag
```

**Dwa produkty w ekosystemie:** nauka = `akademia` (`DASHBOARD.html`); pracja = `hermes-ops-nous` (`OPS.html`). Indeks docs Ops: `docs/ops/README.md`.

Rytuały Cursor (slash): `.cursor/commands/` — `/ops-audit` · `/ops-deploy`. Indeks: `docs/ops/README.md`.

Handoff zespołu: `docs/handoffs/` — jeden plik na zamkniętą sesję.

## Cursor Cloud specific instructions

- Po starcie runu serwer jest w terminalu `dev` (`.cursor/environment.json`): `python3 -m http.server 8765`.
- UI: `http://localhost:8765/ops`. Screenshot zmienionego widoku, gdy ruszasz HTML.
- Laptop: `python` z sekcji Komendy. Cloud VM: `python3` (ten sam stdlib, zero pip).
- Start sesji: `/ops-audit`. Przed merge UI: `/ops-audit`. Koniec: `/ops-deploy`.
- Nie deployuj (`scripts/deploy-akademia-vps.sh`) bez GO Dowódcy. Zero OIDC / tokenów w `academy_url`.
