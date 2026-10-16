# AGENTS.md — hermes-ops-nous

You are editing **Hermes Ops Nous** (Control Plane), not `akademia` and not `workflow-lab`.

0. **SoT zadań inżynieryjnych tego repo:** [`todo.json`](todo.json) — tor `NOUS-PRODUCT-LOOP`, `meta.aktywne_zadanie` / `nastepne_todo`. Hierarchia: Direction Lock → `todo.json` → Role Contract / CONTRACT-OPS-STATUS → handoff dnia → historyczne PLAN-/AUDYT-. **Nie** używaj `dsaas-platform-main/todo.json` jako SoT tego workspace. Kolejka Autopilot = Linear (nie ten plik). `qui_todo_mismatch` = `ops-status.todo_active` / todo platformy — nie lokalny `todo.json`. F9 = reject list (nie klon Agents Window).
1. UI SoT: `OPS.html` — czytelny styl terminala, białe tło, zero gradientów, wszystko klikalne. Produkt UX = pętla 5 kroków w `docs/ops/HERMES-OPS-HOWTO.md`.
1a. **DIRECTION LOCK:** T1c/T3 PASS (2026-10-16). Freeze polish/chat HUD **nadal ON** do osobnego GO. Produkt = Nous+Cloud w `workflow-lab`, nie polish HUD. → `docs/ops/DIRECTION-LOCK-2026-10-13.md`
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
testy:          python scripts/test_progress_vault.py
todo SoT:       python scripts/validate_todo_nous.py
smoke VPS:      bash scripts/smoke-hermes-ops-vps.sh
deploy VPS:     bash scripts/deploy-akademia-vps.sh
TLS po DNS:     bash scripts/finish-akademia-tls.sh
health VPS:     curl -fsS http://127.0.0.1:8097/health
smoke ops loop: curl -fsS http://127.0.0.1:8097/ops/status && curl -fsS http://127.0.0.1:8097/ops/diag
```

**Dwa produkty w ekosystemie:** nauka = `akademia` (`DASHBOARD.html`); pracja = `hermes-ops-nous` (`OPS.html`). Indeks docs Ops: `docs/ops/README.md`.

Rytuały Cursor (slash): `.cursor/commands/` — `/ops-audit` · `/ops-deploy`. Indeks: `docs/ops/README.md`.

Handoff zespołu: `docs/handoffs/` — jeden plik na zamkniętą sesję.

## Cursor Cloud specific instructions

- Po starcie runu serwer jest w terminalu `dev` (`.cursor/environment.json`): `python3 -m http.server 8765`.
- UI: `http://localhost:8765/ops`. Screenshot zmienionego widoku, gdy ruszasz HTML.
- Laptop: `python` z sekcji Komendy. Cloud VM: `python3` (ten sam stdlib, zero pip).
- Start sesji: `/ops-audit` (krok 0 = odczyt `todo.json` + Direction Lock NEXT). Przed merge UI: `/ops-audit`. Koniec: `/ops-deploy`.
- Nie deployuj (`scripts/deploy-akademia-vps.sh`) bez GO Dowódcy. Zero OIDC / tokenów w `academy_url`.
