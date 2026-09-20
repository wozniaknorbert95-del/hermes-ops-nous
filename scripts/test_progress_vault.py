#!/usr/bin/env python3
"""Minimal vault tests — stdlib only."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "host" / "progress_vault.py"


def force_utf8_streams() -> None:
    """Windows cp1252 → polskie znaki w komunikatach wysadzają print."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def wait_url(url: str, timeout: float = 8.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    return
        except Exception:
            time.sleep(0.15)
    raise RuntimeError(f"timeout waiting for {url}")


def req(method: str, url: str, body: dict | None = None, token: str = "") -> tuple[int, dict | str]:
    data = None
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=5) as resp:
            raw = resp.read().decode("utf-8")
            try:
                payload: dict | str = json.loads(raw)
            except Exception:
                payload = raw
            return resp.status, payload
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8")
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {"error": raw}
        return exc.code, payload


def main() -> int:
    force_utf8_streams()
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        data_dir = Path(tmp) / "data"
        env = os.environ.copy()
        env.update(
            {
                "ACADEMY_BIND": "127.0.0.1",
                "ACADEMY_PORT": "18097",
                "ACADEMY_DATA_DIR": str(data_dir),
                "ACADEMY_STATIC_ROOT": str(ROOT),
                "ACADEMY_PROGRESS_TOKEN": "test-token-xyz",
                "ACADEMY_VAPID_PUBLIC_KEY": "test-vapid-public-key",
            }
        )
        proc = subprocess.Popen([sys.executable, str(VAULT)], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        base = "http://127.0.0.1:18097"
        try:
            wait_url(f"{base}/health")
            code, payload = req("GET", f"{base}/progress")
            if code != 401:
                errors.append(f"GET without token expected 401, got {code}")
            code, payload = req("GET", f"{base}/progress", token="wrong")
            if code != 401:
                errors.append("GET with wrong token expected 401")
            code, env_default = req("GET", f"{base}/progress", token="test-token-xyz")
            if code != 200 or env_default.get("source") != "academy-os":
                errors.append("GET with token failed")
            bad = {"schema_version": "0.0.0", "tenant_id": "x", "updated_at": "x", "source": "bad"}
            code, _ = req("PUT", f"{base}/progress", body=bad, token="test-token-xyz")
            if code != 400:
                errors.append("PUT bad schema expected 400")
            good = {
                "schema_version": "0.1.0",
                "tenant_id": "quietforge",
                "updated_at": "2026-09-13T08:00:00+00:00",
                "source": "academy-os",
                "academy_url": "https://akademia.quietforge.flexgrafik.nl/",
                "now_card": "test",
                "tracks": {"W": {"percent": 0, "completed_ids": []}, "F": {"percent": 0, "completed_ids": []}},
                "_scratch": {"A1_pass": True},
            }
            code, put = req("PUT", f"{base}/progress", body=good, token="test-token-xyz")
            if code != 200:
                errors.append(f"PUT good expected 200, got {code}: {put}")
            code, got = req("GET", f"{base}/progress", token="test-token-xyz")
            if got.get("_scratch", {}).get("A1_pass") is not True:
                errors.append("round-trip scratch mismatch")
            static_code, static_body = req("GET", f"{base}/DASHBOARD.html")
            if static_code != 200 or "Command Dashboard v3.1" not in str(static_body):
                errors.append("static DASHBOARD.html not served")
            head_code, _ = req("HEAD", f"{base}/DASHBOARD.html")
            if head_code != 200:
                errors.append(f"HEAD DASHBOARD.html expected 200, got {head_code}")
            sw_code, sw_body = req("GET", f"{base}/sw.js")
            if sw_code != 200 or "notificationclick" not in str(sw_body) or "addEventListener('push'" not in str(sw_body):
                errors.append("service worker sw.js not served or missing push handlers")

            # --- Web Push (Fala 4) ---
            pk_code, pk = req("GET", f"{base}/push/public-key")
            if pk_code != 200 or pk.get("publicKey") != "test-vapid-public-key":
                errors.append(f"GET /push/public-key expected the public key, got {pk_code}: {pk}")
            anon_code, _ = req("POST", f"{base}/push/subscribe", body={"endpoint": "https://x/y"})
            if anon_code != 401:
                errors.append(f"POST /push/subscribe without token expected 401, got {anon_code}")
            bad_sub = {"endpoint": "http://insecure.example/x", "keys": {"p256dh": "a", "auth": "b"}}
            bad_code, _ = req("POST", f"{base}/push/subscribe", body=bad_sub, token="test-token-xyz")
            if bad_code != 400:
                errors.append(f"POST /push/subscribe with http endpoint expected 400, got {bad_code}")
            shadow_code, _ = req("POST", f"{base}/push/subscribe", body={"endpoint": "https://push.example/e1"}, token="test-token-xyz")
            if shadow_code != 400:
                errors.append(f"POST /push/subscribe without keys expected 400, got {shadow_code}")
            sub = {"endpoint": "https://push.example/e1", "keys": {"p256dh": "BAbc", "auth": "Zx9"}}
            ok_code, ok_payload = req("POST", f"{base}/push/subscribe", body=sub, token="test-token-xyz")
            if ok_code != 200 or ok_payload.get("subscriptions") != 1:
                errors.append(f"POST /push/subscribe expected 1 subscription, got {ok_code}: {ok_payload}")
            req("POST", f"{base}/push/subscribe", body=sub, token="test-token-xyz")
            _, again = req("POST", f"{base}/push/unsubscribe", body={"endpoint": "https://nope.example/e"}, token="test-token-xyz")
            if again.get("subscriptions") != 1:
                errors.append(f"dedupe by endpoint failed, got {again}")
            unsub_code, unsub = req("POST", f"{base}/push/unsubscribe", body={"endpoint": "https://push.example/e1"}, token="test-token-xyz")
            if unsub_code != 200 or unsub.get("subscriptions") != 0:
                errors.append(f"POST /push/unsubscribe expected 0, got {unsub_code}: {unsub}")
            _, after_push = req("GET", f"{base}/progress", token="test-token-xyz")
            if after_push.get("_scratch", {}).get("A1_pass") is not True:
                errors.append("push endpoints mutated progress _scratch — they must not touch it")
            subs_raw = (data_dir / "push-subscriptions.json")
            if subs_raw.exists() and "private" in subs_raw.read_text(encoding="utf-8").lower():
                errors.append("push-subscriptions.json holds something private — must never happen")
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
    if errors:
        print("FAIL:")
        for item in errors:
            print(f" - {item}")
        return 1
    print("PASS: progress vault tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
