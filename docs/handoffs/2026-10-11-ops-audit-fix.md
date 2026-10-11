# Handoff — audyt + plan naprawczy Hermes Ops (2026-10-11)

**Repo:** `hermes-ops-nous`  
**Branch:** `fix/ops-blocked-start-ux`  
**Deploy:** nie (Zasada 11)

## Zrobione

1. **Fala 1 UX** — `OPS.html`: Otwórz Linear przy zablokowanym Start, copy PL, Zatrzymaj i przejmij, Jak zacząć, refuse-aware Retry; `host/auth-gate-ops.html` + nginx `/ops`; smoke setup sprawdza „Hermes Ops”.
2. **Fala 2 vault** — `scripts/test_progress_vault.py` (stdlib); `AGENTS.md` `testy:`; `deploy-ready-hermes-ops.sh` woła vault test.
3. **Fala 3 docs** — `AUDYT-WYNIK-HERMES-OPS-2026-10-11.md`, DEPLOY-READY + README.

## Bramka

```bash
python scripts/test_progress_vault.py
# → OK — vault gate PASS
```

## NEXT

1. Merge PR do `main`.
2. GO Dowódcy → `bash scripts/deploy-akademia-vps.sh`.
3. Re-walk live `/ops`: Start+Linear, 401 Hermes Ops, Retry ukryty przy cap refuse.
