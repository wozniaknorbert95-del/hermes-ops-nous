#!/usr/bin/env python3
"""Academy progress vault — stdlib only. GET/PUT /progress + static files."""
from __future__ import annotations

import json
import os
import shutil
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.environ.get("ACADEMY_DATA_DIR", ROOT / "data"))
PROGRESS_FILE = DATA_DIR / "progress.json"
BACKUP_FILE = DATA_DIR / "progress.json.bak"
STATIC_ROOT = Path(os.environ.get("ACADEMY_STATIC_ROOT", ROOT))
MAX_BODY = int(os.environ.get("ACADEMY_MAX_BODY", "262144"))
PUT_WINDOW_SEC = 60
PUT_MAX = int(os.environ.get("ACADEMY_PUT_RATE", "30"))
BEARER = os.environ.get("ACADEMY_PROGRESS_TOKEN", "").strip()
# Web Push (Fala 4). Klucz PUBLICZNY jest jawny z definicji.
# Klucz PRYWATNY VAPID nigdy nie trafia do repo ani do tego procesu — używa go
# wyłącznie scripts/push-send.py na VPS, czytając /etc/akademia/vapid.env (chmod 600).
VAPID_PUBLIC_KEY = os.environ.get("ACADEMY_VAPID_PUBLIC_KEY", "").strip()
SUBS_FILE = DATA_DIR / "push-subscriptions.json"
PUSH_MAX_SUBS = int(os.environ.get("ACADEMY_PUSH_MAX_SUBS", "10"))

REQUIRED = ("schema_version", "tenant_id", "updated_at", "source")
SCHEMA_VERSION = "0.1.0"
SOURCE = "academy-os"

_put_times: list[float] = []


def default_envelope() -> dict[str, Any]:
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return {
        "schema_version": SCHEMA_VERSION,
        "tenant_id": "quietforge",
        "updated_at": now,
        "source": SOURCE,
        "academy_url": "",
        "now_card": "",
        "tracks": {"W": {"percent": 0, "completed_ids": []}, "F": {"percent": 0, "completed_ids": []}},
        "_scratch": {},
    }


def validate_envelope(data: dict[str, Any]) -> str | None:
    if not isinstance(data, dict):
        return "body must be object"
    for key in REQUIRED:
        if key not in data:
            return f"missing required '{key}'"
    if data.get("schema_version") != SCHEMA_VERSION:
        return "schema_version must be 0.1.0"
    if data.get("source") != SOURCE:
        return "source must be academy-os"
    if not isinstance(data.get("tenant_id"), str) or not data["tenant_id"].strip():
        return "tenant_id invalid"
    if not isinstance(data.get("updated_at"), str) or len(data["updated_at"]) < 10:
        return "updated_at invalid"
    url = data.get("academy_url", "")
    if url and (not isinstance(url, str) or "token" in url.lower() or "oidc" in url.lower()):
        return "academy_url invalid"
    scratch = data.get("_scratch")
    if scratch is not None and not isinstance(scratch, dict):
        return "_scratch must be object"
    return None


def read_progress() -> dict[str, Any]:
    if not PROGRESS_FILE.exists():
        return default_envelope()
    try:
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return default_envelope()


def atomic_write(payload: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if PROGRESS_FILE.exists():
        shutil.copy2(PROGRESS_FILE, BACKUP_FILE)
    tmp = PROGRESS_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(PROGRESS_FILE)


def rate_ok() -> bool:
    global _put_times
    now = time.time()
    _put_times = [t for t in _put_times if now - t < PUT_WINDOW_SEC]
    if len(_put_times) >= PUT_MAX:
        return False
    _put_times.append(now)
    return True


def authorized(headers: Any) -> bool:
    if not BEARER:
        return True
    auth = headers.get("Authorization", "")
    if auth == f"Bearer {BEARER}":
        return True
    return False


def read_subs() -> list[dict[str, Any]]:
    if not SUBS_FILE.exists():
        return []
    try:
        data = json.loads(SUBS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []
    return data if isinstance(data, list) else []


def write_subs(subs: list[dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = SUBS_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(subs, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(SUBS_FILE)


def validate_subscription(data: Any) -> str | None:
    if not isinstance(data, dict):
        return "subscription must be object"
    endpoint = data.get("endpoint")
    if not isinstance(endpoint, str) or not endpoint.startswith("https://") or len(endpoint) > 1000:
        return "endpoint invalid"
    keys = data.get("keys")
    if not isinstance(keys, dict):
        return "keys must be object"
    for name in ("p256dh", "auth"):
        value = keys.get(name)
        if not isinstance(value, str) or not value or len(value) > 300:
            return f"keys.{name} invalid"
    return None


def safe_static_path(url_path: str) -> Path | None:
    rel = unquote(url_path.lstrip("/"))
    if not rel or rel.endswith("/"):
        rel = "DASHBOARD.html"
    candidate = (STATIC_ROOT / rel).resolve()
    try:
        candidate.relative_to(STATIC_ROOT.resolve())
    except ValueError:
        return None
    if not candidate.is_file():
        return None
    return candidate


class Handler(BaseHTTPRequestHandler):
    server_version = "AcademyVault/0.1"

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if getattr(self, "_omit_body", False):
            return
        self.wfile.write(body)

    def _file(self, path: Path) -> None:
        data = path.read_bytes()
        ctype = "text/html; charset=utf-8"
        if path.suffix == ".json":
            ctype = "application/json; charset=utf-8"
        elif path.suffix == ".js":
            ctype = "application/javascript; charset=utf-8"
        elif path.suffix == ".css":
            ctype = "text/css; charset=utf-8"
        elif path.suffix == ".svg":
            ctype = "image/svg+xml"
        elif path.suffix == ".webmanifest":
            ctype = "application/manifest+json"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        if getattr(self, "_omit_body", False):
            return
        self.wfile.write(data)

    def do_HEAD(self) -> None:
        self._omit_body = True
        try:
            self.do_GET()
        finally:
            self._omit_body = False

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/progress":
            if not authorized(self.headers):
                self.send_response(HTTPStatus.UNAUTHORIZED)
                self.end_headers()
                return
            self._json(HTTPStatus.OK, read_progress())
            return
        if parsed.path in ("/", "/health"):
            self._json(HTTPStatus.OK, {"ok": True, "service": "academy-vault"})
            return
        if parsed.path == "/push/public-key":
            # Klucz publiczny VAPID — jawny z definicji, zero sekretów.
            self._json(HTTPStatus.OK, {"publicKey": VAPID_PUBLIC_KEY})
            return
        static = safe_static_path(parsed.path)
        if static:
            self._file(static)
            return
        self.send_response(HTTPStatus.NOT_FOUND)
        self.end_headers()

    def do_PUT(self) -> None:
        if urlparse(self.path).path != "/progress":
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()
            return
        if not authorized(self.headers):
            self.send_response(HTTPStatus.UNAUTHORIZED)
            self.end_headers()
            return
        if not rate_ok():
            self._json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "rate limit"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > MAX_BODY:
            self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid body size"})
            return
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid json"})
            return
        err = validate_envelope(data)
        if err:
            self._json(HTTPStatus.BAD_REQUEST, {"error": err})
            return
        try:
            atomic_write(data)
        except Exception as exc:
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
            return
        self._json(HTTPStatus.OK, {"ok": True, "updated_at": data.get("updated_at")})

    def _push_body(self) -> tuple[Any, int, str]:
        if not rate_ok():
            return None, HTTPStatus.TOO_MANY_REQUESTS, "rate limit"
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > MAX_BODY:
            return None, HTTPStatus.BAD_REQUEST, "invalid body size"
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            return None, HTTPStatus.BAD_REQUEST, "invalid json"
        return data, HTTPStatus.OK, ""

    def do_POST(self) -> None:
        """Subskrypcje Web Push. Nigdy nie dotyka /progress ani danych platformy."""
        path = urlparse(self.path).path
        if path not in ("/push/subscribe", "/push/unsubscribe"):
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()
            return
        if not authorized(self.headers):
            self.send_response(HTTPStatus.UNAUTHORIZED)
            self.end_headers()
            return
        data, status, err = self._push_body()
        if data is None:
            self._json(status, {"error": err})
            return
        if path == "/push/unsubscribe":
            endpoint = data.get("endpoint") if isinstance(data, dict) else None
            remaining = [s for s in read_subs() if s.get("endpoint") != endpoint]
            write_subs(remaining)
            self._json(HTTPStatus.OK, {"ok": True, "subscriptions": len(remaining)})
            return
        err = validate_subscription(data)
        if err:
            self._json(HTTPStatus.BAD_REQUEST, {"error": err})
            return
        kept = [s for s in read_subs() if s.get("endpoint") != data["endpoint"]]
        kept.append(
            {
                "endpoint": data["endpoint"],
                "keys": {"p256dh": data["keys"]["p256dh"], "auth": data["keys"]["auth"]},
                "added_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
        )
        kept = kept[-PUSH_MAX_SUBS:]
        try:
            write_subs(kept)
        except Exception as exc:
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
            return
        self._json(HTTPStatus.OK, {"ok": True, "subscriptions": len(kept)})


def main() -> None:
    host = os.environ.get("ACADEMY_BIND", "127.0.0.1")
    port = int(os.environ.get("ACADEMY_PORT", "8097"))
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"academy vault on http://{host}:{port} static={STATIC_ROOT} data={DATA_DIR}")
    server.serve_forever()


if __name__ == "__main__":
    main()
