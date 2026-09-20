#!/usr/bin/env bash
# Run ON VPS as root after files land in /opt/akademia.
set -euo pipefail

TARGET="${AKADEMIA_TARGET:-/opt/akademia}"
HOST="${ACADEMY_HOST:-akademia.quietforge.flexgrafik.nl}"
VPS_IP="${AKADEMIA_VPS_IP:-185.243.54.115}"
EMAIL="${ACADEMY_LE_EMAIL:-ops@flexgrafik.nl}"
USER="${ACADEMY_BASIC_USER:-academy}"

cd "${TARGET}"

if [[ ! -f host/.htpasswd ]]; then
  PASS="$(openssl rand -base64 18 | tr -d '/+=' | head -c 20)"
  htpasswd -bc host/.htpasswd "${USER}" "${PASS}"
  chmod 755 "${TARGET}" "${TARGET}/host"
  chmod 640 host/.htpasswd
  chgrp www-data host/.htpasswd
  umask 077
  cat > CREDENTIALS.local.txt <<EOF
# Akademia VPS credentials — chmod 600, nie commituj.
host=${HOST}
user=${USER}
password=${PASS}
created=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF
  chmod 600 CREDENTIALS.local.txt
  echo "CREATED credentials: ${TARGET}/CREDENTIALS.local.txt"
fi

if [[ ! -f .env ]]; then
  umask 077
  cat > .env <<EOF
ACADEMY_HOST=${HOST}
ACADEMY_LE_EMAIL=${EMAIL}
ACADEMY_BASIC_USER=${USER}
ACADEMY_PROGRESS_TOKEN=
EOF
  chmod 600 .env
fi

# VAPID (Fala 4): klucz publiczny z /etc/akademia/vapid.env -> .env (idempotentnie).
# Klucz prywatny zostaje tam, gdzie jest — czytają go tylko scripts/push-send.py.
if [[ -f /etc/akademia/vapid.env ]]; then
  PUB="$(grep -E '^VAPID_PUBLIC_KEY=' /etc/akademia/vapid.env | head -n1 | cut -d= -f2- || true)"
  if [[ -n "${PUB}" ]]; then
    if grep -qE '^ACADEMY_VAPID_PUBLIC_KEY=' "${TARGET}/.env"; then
      sed -i "s|^ACADEMY_VAPID_PUBLIC_KEY=.*|ACADEMY_VAPID_PUBLIC_KEY=${PUB}|" "${TARGET}/.env"
    else
      echo "ACADEMY_VAPID_PUBLIC_KEY=${PUB}" >> "${TARGET}/.env"
    fi
    echo "==> VAPID public key -> ${TARGET}/.env"
  fi
else
  echo "WARN: brak /etc/akademia/vapid.env — push nieaktywny. Wygeneruj: bash scripts/generate-vapid-keys.sh"
fi

mkdir -p data
cd host
docker rm -f akademia-vault >/dev/null 2>&1 || true
docker-compose -p akademia --env-file "${TARGET}/.env" up -d vault

echo "==> vault health"
curl -fsS "http://127.0.0.1:8097/health" | head -c 200
echo

NGINX_SITE="/etc/nginx/sites-available/akademia-quietforge"
if [[ ! -f "${NGINX_SITE}" ]]; then
  cp "${TARGET}/host/nginx-akademia-http.conf" "${NGINX_SITE}"
  ln -sf "${NGINX_SITE}" /etc/nginx/sites-enabled/akademia-quietforge
fi
nginx -t
systemctl reload nginx

dns_ok() {
  dig +short "${HOST}" A | grep -qx "${VPS_IP}"
}

if dns_ok; then
  echo "==> DNS OK for ${HOST}"
  if [[ ! -d "/etc/letsencrypt/live/${HOST}" ]]; then
    certbot --nginx -d "${HOST}" --non-interactive --agree-tos -m "${EMAIL}" --redirect
    cp "${TARGET}/host/nginx-akademia.conf" "${NGINX_SITE}"
    nginx -t
    systemctl reload nginx
  fi
  echo "==> HTTPS smoke"
  PASS="$(grep '^password=' "${TARGET}/CREDENTIALS.local.txt" | cut -d= -f2-)"
  curl -fsS -o /dev/null -u "${USER}:${PASS}" "https://${HOST}/DASHBOARD.html"
  curl -fsS -u "${USER}:${PASS}" "https://${HOST}/progress" | head -c 120
  echo
else
  echo "WARN: DNS brak — dodaj A ${HOST} -> ${VPS_IP} w Cyberfolks, potem:"
  echo "  certbot --nginx -d ${HOST} && cp ${TARGET}/host/nginx-akademia.conf ${NGINX_SITE} && nginx -t && systemctl reload nginx"
fi

echo "OK: akademia vault running on 127.0.0.1:8097"

# ---------------------------------------------------------------------------
# Push: wrażliwość na "cichą porażkę". Sama subskrypcja nic nie da — ktoś musi
# WYSŁAĆ. Ten blok jest best-effort: gdy się nie uda, deploy Akademii i tak
# kończy się sukcesem, ale wypisujemy DOKŁADNIE co zrobić ręcznie.
# ---------------------------------------------------------------------------
if [[ -f /etc/akademia/vapid.env ]]; then
  if [[ ! -x "${TARGET}/.venv/bin/python" ]]; then
    echo "==> push: tworzę venv + pywebpush (potrzebne tylko do wysyłki)"
    if python3 -m venv "${TARGET}/.venv" >/dev/null 2>&1; then
      "${TARGET}/.venv/bin/pip" install --quiet --disable-pip-version-check pywebpush >/dev/null 2>&1 \
        || echo "WARN: pip install pywebpush nie powiódł się — push nie wyśle (subskrypcje zostaną zapisane)"
    else
      echo "WARN: nie udało się utworzyć venv — push nie wyśle"
    fi
  fi

  if "${TARGET}/.venv/bin/python" -c "import pywebpush" >/dev/null 2>&1; then
    cat > /etc/systemd/system/akademia-push.service <<EOF
[Unit]
Description=Akademia — jeden kawal (Web Push)
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
WorkingDirectory=${TARGET}
Environment=VAPID_ENV=/etc/akademia/vapid.env
Environment=ACADEMY_DATA_DIR=${TARGET}/data
ExecStart=${TARGET}/.venv/bin/python ${TARGET}/scripts/push-send.py --once
EOF
    cat > /etc/systemd/system/akademia-push.timer <<'EOF'
[Unit]
Description=Akademia push — codziennie 07:00 (dogania, gdy VPS spał)

[Timer]
OnCalendar=*-*-* 07:00:00
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
EOF
    systemctl daemon-reload
    systemctl enable --now akademia-push.timer >/dev/null 2>&1 || true
    echo "==> push: timer aktywny — $(systemctl list-timers akademia-push.timer --no-legend 2>/dev/null | head -n1)"
    echo "    podglad: ${TARGET}/.venv/bin/python ${TARGET}/scripts/push-send.py --dry-run"
  else
    echo "WARN: brak pywebpush w ${TARGET}/.venv — timer NIE zainstalowany."
    echo "  Ręcznie: python3 -m venv ${TARGET}/.venv && ${TARGET}/.venv/bin/pip install pywebpush"
  fi
else
  echo "WARN: push pominięty — brak /etc/akademia/vapid.env (bash ${TARGET}/scripts/generate-vapid-keys.sh)"
fi
