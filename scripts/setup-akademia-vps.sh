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
