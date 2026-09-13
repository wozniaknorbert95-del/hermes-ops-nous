# Handoff — Akademia #5+#6 live + deploy-ready close

**Data:** 2026-09-13  
**Repo:** `akademia`  
**Sesja:** merge #5→#6, GO deploy VPS, PENE live DASHBOARD  
**Gałąź close:** `chore/deploy-lf-head`

---

## Co zrobione

- Akademia **#5** zmergowane (`9139def`) — Wave 2 DZIEŃ (WF-P6, 8 widoków Linear).
- Akademia **#6** zrebase’owane na `main` po #5, konflikt `DASHBOARD.html` złożony (vault/PWA + Wave 2), zmergowane (`286aea6`).
- **GO deploy** na VPS `/opt/akademia` (Zasada 11 — jawny GO Dowódcy).
- PENE live: HTTPS DASHBOARD 200, `/progress` 200 + 401 bez auth, TERAZ = A1, DZIEŃ = WF-P6 (nie WF-P9).
- Deploy-ready leftover: `HEAD` na vault (było 501 na `curl -I`), LF w `.sh` (CRLF psuło `pipefail` na VPS), `.gitattributes`.

## Co live

| Element | Wartość |
|---------|---------|
| URL | https://akademia.quietforge.flexgrafik.nl/DASHBOARD.html |
| Treść | `main` #5+#6: vault + WF-P6 + widoki Linear |
| Vault | `127.0.0.1:8097` healthy; envelope `0.1.0` / `academy-os` |
| Hasło | `/opt/akademia/CREDENTIALS.local.txt` (nie w gicie) |

## Co zablokowane

Brak na Akademii. ENT-12 / kod platformy = poza tym repo. Deploy Kokpitu = nie.

## Następny krok (jeden TERAZ)

Nic na Akademii. Poranny rytuał: zakładka **DZIEŃ** na live (WF-P6). Soft: Ctrl+F5 jeśli cache pokazuje WF-P9.

## Komendy weryfikacji

```
python scripts/validate-academy-export.py
python scripts/test_progress_vault.py
curl -fsS http://127.0.0.1:8097/health
```

Publicznie: Basic Auth `academy` + hasło z VPS — GET `/DASHBOARD.html` i `/progress`.

## Pliki tej sesji (close)

- `host/progress_vault.py` — `do_HEAD`
- `scripts/setup-akademia-vps.sh` — recreate vault bez `--force-recreate`, smoke GET
- `scripts/test_progress_vault.py` — test HEAD
- `scripts/*.sh` — LF
- `.gitattributes` — `*.sh text eol=lf`
- ten handoff
