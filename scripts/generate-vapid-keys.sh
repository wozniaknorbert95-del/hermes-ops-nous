#!/usr/bin/env bash
# VAPID keypair dla Akademii (Web Push, Fala 4).
#
# URUCHAMIAJ WYŁĄCZNIE NA VPS. Ten skrypt nie zawiera żadnego klucza — generuje go
# lokalnie na maszynie i zapisuje w pliku czytelnym tylko dla roota. Klucz prywatny
# nigdy nie trafia do repo, do eksportu JSON ani do HTML-a.
set -euo pipefail

OUT="${AKADEMIA_VAPID_ENV:-/etc/akademia/vapid.env}"

if [ -f "$OUT" ]; then
  echo "ABORT: $OUT już istnieje. Rotacja klucza = świadoma decyzja Dowódcy (unieważnia stare subskrypcje)." >&2
  exit 1
fi

if ! python3 -c "import cryptography" 2>/dev/null; then
  echo "BRAK zależności: pip3 install cryptography   (na VPS — nie w repo)" >&2
  exit 1
fi

umask 077
mkdir -p "$(dirname "$OUT")"

python3 - "$OUT" <<'PY'
import base64
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

out = sys.argv[1]
key = ec.generate_private_key(ec.SECP256R1())
private_raw = key.private_numbers().private_value.to_bytes(32, "big")
public_raw = key.public_key().public_bytes(
    serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint
)


def b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


with open(out, "w", encoding="utf-8") as handle:
    handle.write(f"VAPID_PRIVATE_KEY={b64u(private_raw)}\n")
    handle.write(f"VAPID_PUBLIC_KEY={b64u(public_raw)}\n")

print(f"OK: {out} — klucz prywatny zapisany, chmod 600, tylko root.")
print()
print("Klucz publiczny trafia do /opt/akademia/.env jako ACADEMY_VAPID_PUBLIC_KEY.")
print("scripts/setup-akademia-vps.sh dowozi go tam sam przy każdym deployu.")
print("Ręcznie (gdyby trzeba): ACADEMY_VAPID_PUBLIC_KEY=" + b64u(public_raw))
PY

chmod 600 "$OUT"
ls -l "$OUT"
