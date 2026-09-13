# Handoff — Akademia sync vault + VPS deploy

**Data:** 2026-09-13  
**Repo:** `akademia`  
**Sesja:** optymalizacja enterprise, sync telefon+laptop, deploy live VPS  
**Gałąź:** `main` (zmiany **niecommitowane** w momencie handoffu)

---

## Co zrobione

| Obszar | Status |
|--------|--------|
| `DASHBOARD.html` | sync vault (GET/PUT `/progress`), PWA, phone-first, UX gates (scroll-margin, Mermaid kontrast), WF-P9 w DZIEŃ |
| `host/progress_vault.py` | vault stdlib, walidacja v0.1.0, backup, rate-limit |
| Docker + nginx | `akademia-vault` healthy `:8097`; nginx Basic Auth + reverse proxy |
| TLS | Let's Encrypt do 2026-12-12; fix `auth_basic off` na `/.well-known/acme-challenge/` |
| Testy | `validate-academy-export.py` ✅ `test_progress_vault.py` ✅ |
| Runbook | `docs/runbooks/AKADEMIA-VPS.md`, skrypty deploy/setup/finish-tls |
| Cursor workflow | `docs/CURSOR-WORKFLOW.md` + komendy w `AGENTS.md` |
| DNS awaryjny Windows | `scripts/fix-akademia-dns-local.ps1` (hosts, wymaga Admin) |

---

## Co live

| Element | Wartość |
|---------|---------|
| URL | https://akademia.quietforge.flexgrafik.nl/DASHBOARD.html |
| VPS | `185.243.54.115`, `/opt/akademia`, projekt Docker `akademia` |
| Basic Auth login | `academy` |
| Hasło | `/opt/akademia/CREDENTIALS.local.txt` na VPS (**nie w gicie**) |
| Vault | `GET/PUT /progress` przez nginx, envelope `schema_version` `0.1.0`, `source` `academy-os` |

**Smoke (VPS lokalnie):** dashboard + `/progress` przez nginx — OK.  
**Smoke (HTTPS z resolve/hosts):** GET dashboard + progress — OK.

---

## Blockery / ryzyka

1. **DNS autorytatywny Cyberfolks** — rekord `akademia.quietforge` bywa **NXDOMAIN** na `ns1–ns3` mimo potwierdzeń robo_Folks. ISP (UPC) nie widzi domeny → `DNS_PROBE_POSSIBLE` u użytkownika.
   - **Fix trwały:** DirectAdmin → strefa `flexgrafik.nl` → A `akademia.quietforge` → `185.243.54.115`, TTL `300` (wzorzec: `cockpit.quietforge`).
   - **Fix tymczasowy:** hosts / skrypt `fix-akademia-dns-local.ps1` (już użyte na laptopie Dowódcy).

2. **Git:** duży diff na `main`, **brak commita/PR** — świadoma decyzja sesji.

3. **Telefon:** po stabilnym DNS — PWA + sync vault w stopce (login jak VPS).

---

## Następny krok (jeden TERAZ)

**DirectAdmin:** dodać/trwale utrwalić rekord A `akademia.quietforge` → `185.243.54.115`, potwierdzić `dig @ns1.cyberfolks.pl`. Potem smoke z telefonu (LTE, bez hosts).

Alternatywa w Akademii (treść): ▶ TERAZ = **WF-P9** — sync vault skonfigurowany na obu urządzeniach.

---

## Komendy weryfikacji (copy-paste)

```bash
# lokal dev
python -m http.server 8765
# → http://localhost:8765/DASHBOARD.html

# gate przed MR
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py

# DNS
nslookup akademia.quietforge.flexgrafik.nl ns1.cyberfolks.pl
nslookup akademia.quietforge.flexgrafik.nl 8.8.8.8

# VPS
ssh root@185.243.54.115 'curl -fsS http://127.0.0.1:8097/health'
ssh root@185.243.54.115 'docker ps --filter name=akademia'

# deploy (manual, Zasada 11)
bash scripts/deploy-akademia-vps.sh
```

```powershell
# Windows — gdy DNS_PROBE (Admin PowerShell)
Set-ExecutionPolicy -Scope Process Bypass -Force
& ".\scripts\fix-akademia-dns-local.ps1"
ipconfig /flushdns
```

---

## Pliki dotknięte (główne)

- `DASHBOARD.html`, `manifest.webmanifest`, `icons/icon.svg`
- `host/progress_vault.py`, `host/docker-compose.yml`, `host/nginx-akademia*.conf`
- `scripts/*.py`, `scripts/*-akademia-vps.sh`, `scripts/fix-akademia-dns-local.ps1`
- `docs/ACADEMY-UX-SPEC.md`, `docs/runbooks/AKADEMIA-VPS.md`
- `docs/CURSOR-WORKFLOW.md`, `AGENTS.md` (komendy)
- `schema/academy-progress.v0.json` (bez zmian schematu — tylko konsument)

---

## Cursor — szybki restart następnej sesji

Wklej blok **vibeinit** z `docs/CURSOR-WORKFLOW.md`, potem:

> Kontynuuj od handoff `docs/handoffs/2026-09-13-akademia-vps-sync-deploy.md`. Priorytet: DNS DirectAdmin, potem sync telefon.
