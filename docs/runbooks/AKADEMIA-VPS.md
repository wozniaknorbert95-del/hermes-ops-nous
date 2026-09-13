# Runbook — Akademia VPS (izolowany namespace)

**Host docelowy:** `akademia.quietforge.flexgrafik.nl` → `185.243.54.115`  
**Katalog:** `/opt/akademia`  
**Port loopback vault:** `127.0.0.1:8097`  
**Projekt Docker:** `akademia` (prefix `akademia-`)

## 1. Wymagania

- DNS A: `akademia.quietforge.flexgrafik.nl` → `185.243.54.115` (Cyberfolks, jak `cockpit.quietforge…`)
- Na VPS wolny port loopback `8097` (poza DSaaS `8090–8096`, jadzia `8080`)
- **TLS:** nginx na hoście (port 443) — **nie** Caddy w compose (konflikt z istniejącym nginx)
- Docker + docker-compose v1
- **Zero restartu** `jadzia-core` i **zero** zmian w `dsaas-platform-main/deploy`

## 2. Sekrety na VPS (auto przy pierwszym deploy)

- `/opt/akademia/CREDENTIALS.local.txt` — login/hasło Basic Auth (chmod 600)
- `/opt/akademia/host/.htpasswd` — nginx auth
- `/opt/akademia/.env` — opcjonalny bearer vault (domyślnie pusty; auth = nginx)

Token/hasło **nie** trafiają do gita, **nie** do `academy_url`, **nie** do eksportu Kokpitu.

## 3. Deploy

Z laptopa (Git Bash / WSL):

```bash
export AKADEMIA_REMOTE=root@185.243.54.115
bash scripts/deploy-akademia-vps.sh
```

Skrypt: tar → scp → `/opt/akademia` → `setup-akademia-vps.sh` (vault + nginx + certbot gdy DNS OK).

## 4. Smoke

Na VPS:

```bash
curl -fsS http://127.0.0.1:8097/health
curl -I http://127.0.0.1:8097/DASHBOARD.html
```

Publicznie (Basic Auth):

```bash
curl -I -u academy:HASLO https://akademia.quietforge.flexgrafik.nl/DASHBOARD.html
curl -u academy:HASLO https://akademia.quietforge.flexgrafik.nl/progress
```

PUT/GET `/progress` bez auth → **401**. Z auth → **200** + envelope `schema_version` `0.1.0`, `source` `academy-os`.

## 5. Urządzenia (telefon + laptop)

1. Otwórz HTTPS dashboard, zaloguj Basic Auth.
2. Stopka → **Sync vault** → login/hasło (sessionStorage, raz na sesję przeglądarki).
3. Telefon: **Dodaj do ekranu głównego** (PWA).
4. Odhacz 1 checkbox na telefonie → odśwież laptop → ten sam stan.

## 6. Rollback

```bash
ssh root@185.243.54.115 'cd /opt/akademia/host && docker-compose -p akademia down'
```

- Caddy site off; DNS może zostać.
- DSaaS i jadzia nietknięte.
- Dane: `/opt/akademia/data/progress.json` (+ `.bak`) — backup przed rollbackiem jeśli potrzebny.

## 7. Kontrakt

- Eksport = `schema/academy-progress.v0.json` (`0.1.0`, `source: academy-os`)
- `_scratch` zostaje w pliku; Kokpit ignoruje
- `academy_url` = sam HTTPS dashboardu, **zero tokenów**
- Jedno `#nowcard`; brak iframe Kokpitu
