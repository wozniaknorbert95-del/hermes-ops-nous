# AGENTS.md — akademia

You are editing the **school**, not the QuietForge platform and not `workflow-lab`.

1. One ▶ TERAZ. Do not add a second “now” card.
2. Progress export must match `schema/academy-progress.v0.json` (`schema_version` 0.1.0, `source` academy-os).
3. Keep `_scratch` for DASHBOARD checkboxes. Kokpit ignores `_scratch`.
4. Do not iframe this HTML into the Kokpit. Do not add a 7th department.
5. Track W points at `workflow-lab`. Track F maps onto existing Kokpit departments + Taca only.
6. No secrets. No OIDC tokens in `academy_url`.
7. Handbook L3 lives in `ops/workflow-marzen/`.

## Komendy projektu (must-have)

```
instalacja:     (brak — stdlib Python 3, zero npm)
dev lokalny:    python -m http.server 8765
                → http://localhost:8765/DASHBOARD.html
testy:          python scripts/validate-academy-export.py && python scripts/test_progress_vault.py && python scripts/test_hermes_intent.py && python scripts/mutation-test-fala-0.py && python scripts/mutation-test-fala-d.py && python scripts/mutation-test-fala-e.py && python scripts/mutation-test-fala-i.py && python scripts/mutation-test-fala-j.py && python scripts/mutation-test-fala-k.py && python scripts/mutation-test-fala-l.py && python scripts/mutation-test-fala-m.py && python scripts/mutation-test-fala-n.py
test jedn.:     python scripts/test_progress_vault.py
# Testy mutacyjne = dowod, ze guardy lapia regresje (nie dekoracja). CI uruchamia ten
# sam zestaw (academy-gate.yml) — guard Fala J w walidatorze pilnuje, by kazdy nowy
# plik scripts/mutation-test-*.py byl wpiety do CI i do tej linii w tym samym PR.
lint:           (brak — walidator eksportu = kontrakt UI)
typecheck:      (brak — vanilla JS w DASHBOARD.html)
build:          (brak — statyczny HTML; deploy = rsync/tar na VPS)
deploy VPS:     bash scripts/deploy-akademia-vps.sh
TLS po DNS:     bash scripts/finish-akademia-tls.sh   # na VPS lub przez ssh
DNS awaryjnie:  powershell -ExecutionPolicy Bypass -File scripts/fix-akademia-dns-local.ps1  # Admin
smoke VPS:      curl -fsS http://127.0.0.1:8097/health
smoke ops VPS:  bash scripts/smoke-hermes-ops-vps.sh
smoke ops loop: curl -fsS http://127.0.0.1:8097/ops/status && curl -fsS http://127.0.0.1:8097/ops/diag
smoke public:   curl -fsS -u academy:HASLO https://akademia.quietforge.flexgrafik.nl/progress
                curl -fsS -u academy:HASLO https://akademia.quietforge.flexgrafik.nl/ops
                curl -fsS -u academy:HASLO https://akademia.quietforge.flexgrafik.nl/ops/diag
```

**Dwa produkty w tym repo:** nauka = `/` (`DASHBOARD.html`); praca = `/ops` (`OPS.html`). Indeks docs Ops: `docs/ops/README.md`.

Rytuały Cursor (prompty): `docs/CURSOR-WORKFLOW.md` — vibeinit, rootcause, auditread, handoff.

Handoff zespołu: `docs/handoffs/` — jeden plik na zamkniętą sesję.

Role Hermesa (Akademia vs Engineer vs Cursor): `docs/ops/HERMES-ROLE-CONTRACT.md`.
