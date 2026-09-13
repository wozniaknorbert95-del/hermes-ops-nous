#!/usr/bin/env bash
# Wait for DNS then enable HTTPS for Akademia (run on VPS or via ssh).
set -euo pipefail

TARGET="${AKADEMIA_TARGET:-/opt/akademia}"
HOST="${ACADEMY_HOST:-akademia.quietforge.flexgrafik.nl}"
VPS_IP="${AKADEMIA_VPS_IP:-185.243.54.115}"
EMAIL="${ACADEMY_LE_EMAIL:-ops@flexgrafik.nl}"
NGINX_SITE="/etc/nginx/sites-available/akademia-quietforge"

dns_ok() {
  dig +short "${HOST}" A | grep -qx "${VPS_IP}"
}

echo "Waiting for DNS A ${HOST} -> ${VPS_IP} ..."
for i in $(seq 1 60); do
  if dns_ok; then
    echo "DNS OK after ${i} attempts"
    break
  fi
  sleep 10
done

if ! dns_ok; then
  echo "FAIL: DNS still missing. Add A record in Cyberfolks panel."
  exit 1
fi

if [[ ! -d "/etc/letsencrypt/live/${HOST}" ]]; then
  certbot --nginx -d "${HOST}" --non-interactive --agree-tos -m "${EMAIL}" --redirect
fi

cp "${TARGET}/host/nginx-akademia.conf" "${NGINX_SITE}"
nginx -t
systemctl reload nginx

USER="$(grep '^user=' "${TARGET}/CREDENTIALS.local.txt" | cut -d= -f2-)"
PASS="$(grep '^password=' "${TARGET}/CREDENTIALS.local.txt" | cut -d= -f2-)"
curl -fsSI -u "${USER}:${PASS}" "https://${HOST}/DASHBOARD.html" | head -5
echo "OK: https://${HOST}/ live"
