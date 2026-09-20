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

## 8. Push (Web Push / VAPID) — Fala 4

Łańcuch musi być kompletny: **klucz → subskrypcja → wysyłka**. Jeśli brakuje ogniwa,
push jest *cicho* martwy (subskrypcja się zapisze, ale nic nie dojdzie).

### 8.1 Klucze (raz na VPS, rotacja = świadoma decyzja)

```bash
bash /opt/akademia/scripts/generate-vapid-keys.sh    # tworzy /etc/akademia/vapid.env (chmod 600)
bash /opt/akademia/scripts/setup-akademia-vps.sh     # dociąga klucz PUBLICZNY do .env + recreate vaulta
```

Skrypt **odmówi** nadpisania istniejącego pliku (rotacja unieważnia wszystkie subskrypcje).
W repo nigdy nie ma klucza prywatnego — pilnuje tego `validate-academy-export.py`.

### 8.2 Wysyłka (systemd timer, instalowany przez setup)

- `/etc/systemd/system/akademia-push.service` + `akademia-push.timer`
- `OnCalendar=*-*-* 07:00:00`, `Persistent=true` (dogania po przerwie VPS)
- venv: `/opt/akademia/.venv` z `pywebpush`
- Jedna wysyłka dziennie pilnuje `already_sent_today()` → timer może odpalać częściej bez spamu

```bash
systemctl list-timers akademia-push.timer       # kiedy następny strzał
/opt/akademia/.venv/bin/python /opt/akademia/scripts/push-send.py --dry-run   # treść bez wysyłki
systemctl start akademia-push.service           # wymuś teraz (SKIP gdy już poszło dziś)
```

Rollback samego pusha (Akademia działa dalej):

```bash
systemctl disable --now akademia-push.timer && rm -f /etc/systemd/system/akademia-push.{service,timer}
```

### 8.3 Weryfikacja, że push NAPRAWDĘ działa

1. Na telefonie: otwórz dashboard → **HERMES** → panel *Push*: `service worker` = wspierany,
   `VAPID public` = **ustawiony** (klient sam pobiera klucz z `/push/public-key`).
2. *Włącz powiadomienia* → zgoda → `/push/subscribe` **200**; w panelu `subskrypcja` = zapisana.
3. *Test powiadomienia* → powiadomienie ma się pokazać (SW potwierdza przez `MessageChannel`).
4. Dodaj do ekranu głównego, zamknij PWA, a potem wymuś wysyłkę z VPS powyżej dziennego limitu:
   `/opt/akademia/.venv/bin/python /opt/akademia/scripts/push-send.py --force` → powiadomienie ma dojść
   przy **zamkniętej** PWA (iOS ≥ 16.4 po instalacji, Android).

## 9. Co vault oddaje po HTTP (i czego NIGDY nie odda)

Vault serwuje statyki z `STATIC_ROOT` = **całe repo** (`/app/static`), czyli obok treści kursu leżą tam
`.env`, `CREDENTIALS.local.txt`, `host/.htpasswd` i `data/push-subscriptions.json`. Dlatego
`safe_static_path()` ma **białą listę rozszerzeń** treści kursu:
`.html .md .png .svg .webmanifest .json .js .css .ico .woff2`.

Dodatkowo 404 dostają: każdy plik/katalog z kropką (`.env`, `.git/`, `.venv/`), katalogi `data/`,
`host/`, `scripts/` (także jako sam katalog) oraz `CREDENTIALS.local.txt`.

Incydent 2026-09-20: przed tą białą listą `/.env`, `/CREDENTIALS.local.txt` i `/host/.htpasswd`
zwracały **200** za hasłem Basic Auth — jedno `curl -u` dzieliło więc hasło nginx i bearer vaulta.

Sprawdzenie po każdym deployu (na VPS, hasło nie opuszcza serwera):

```bash
cd /opt/akademia
PASS=$(grep '^password=' CREDENTIALS.local.txt | cut -d= -f2-)
for p in /.env /CREDENTIALS.local.txt /host/.htpasswd /host/env.example /scripts/push-send.py /data/; do
  printf '%-30s %s\n' "$p" "$(curl -s -o /dev/null -w '%{http_code}' -u "academy:$PASS" "https://akademia.quietforge.flexgrafik.nl$p")"
done   # oczekiwane: 404 dla wszystkich
curl -s -o /dev/null -w '%{http_code}\n' -u "academy:$PASS" https://akademia.quietforge.flexgrafik.nl/DASHBOARD.html  # 200
```

Zmiana tej listy = zmiana kontraktu bezpieczeństwa: `scripts/validate-academy-export.py` pilnuje,
żeby reguły nie zniknęły, a `scripts/test_progress_vault.py` sprawdza je na dekojach **istniejących na dysku**
(404 z braku pliku nie liczy się jako dowód).

