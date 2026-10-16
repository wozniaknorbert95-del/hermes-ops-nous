#!/usr/bin/env python3
"""Minimal vault regression gate for hermes-ops-nous (stdlib only).

Covers: derive_run halt-wins-FAIL, derive_dispatch states, I1 pause/stop,
POST forbid deploy/merge, DoR gate 400, ops_cmd directory trap,
POST /ops/chat facts, POST /hermes/chat 410.
"""
from __future__ import annotations

import importlib
import json
import os
import shutil
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FAILS = 0


def _ok(name: str, cond: bool, detail: str = "") -> None:
    global FAILS
    if cond:
        print(f"  PASS  {name}")
    else:
        FAILS += 1
        print(f"  FAIL  {name}" + (f" — {detail}" if detail else ""))


def _write(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_vault(data_dir: Path):
    os.environ["ACADEMY_DATA_DIR"] = str(data_dir)
    os.environ["HERMES_OPS_STATUS"] = str(data_dir / "ops-status.json")
    os.environ["HERMES_OPS_CMD"] = str(data_dir / "ops-cmd.json")
    os.environ["LINEAR_OPS_READ"] = "test-linear-fixture"
    os.environ.pop("ACADEMY_PROGRESS_TOKEN", None)
    for p in (str(ROOT / "host"), str(ROOT / "scripts")):
        if p not in sys.path:
            sys.path.insert(0, p)
    if "ops_linear_dor" in sys.modules:
        importlib.reload(sys.modules["ops_linear_dor"])
    if "progress_vault" in sys.modules:
        return importlib.reload(sys.modules["progress_vault"])
    import progress_vault as pv  # noqa: WPS001

    return pv


def _iso(offset: int = 0) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + offset))


def test_derive_run_halt_wins(pv: Any, data_dir: Path) -> None:
    print("==> derive_run operator halt")
    status = {
        "ok": True,
        "status": "PAUSED",
        "engine": "PAUSED",
        "updated_at": _iso(-60),
        "live": {
            "issue": "QUI-113",
            "title": "leftover",
            "steps": [
                {"step": 1, "status": "PASS"},
                {"step": 2, "status": "PASS"},
                {"step": 3, "status": "FAIL"},
            ],
        },
    }
    _write(data_dir / "ops-status.json", status)
    if (data_dir / "ops-cmd.json").exists():
        (data_dir / "ops-cmd.json").unlink()
    run = pv.derive_run(status, now=time.time())
    _ok("halt_wins_fail -> paused", run.get("verdict") == "paused", str(run))
    _ok("halt reason operator_halt", run.get("reason") == "operator_halt", str(run))

    done = dict(status)
    done["live"] = {
        "issue": "QUI-1",
        "pr_number": 42,
        "done": True,
        "steps": [{"step": i, "status": "PASS"} for i in range(1, 7)],
    }
    done["status"] = "PAUSED"
    run_done = pv.derive_run(done, now=time.time())
    _ok("T1.1 DONE wins over PAUSED", run_done.get("verdict") == "done", str(run_done))


def test_derive_dispatch(pv: Any, data_dir: Path) -> None:
    print("==> derive_dispatch")
    now = time.time()
    fresh = _iso(-30)
    old = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 30 * 60))

    idle = pv.derive_dispatch({"updated_at": fresh}, {}, now=now)
    _ok("idle", idle.get("state") == "idle", str(idle))

    # cmd newer than status + tick alive
    status_mid = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 120))
    cmd_newer = {"id": "c2", "action": "run_next", "at": _iso(-5)}
    queued = pv.derive_dispatch({"updated_at": status_mid}, cmd_newer, now=now)
    _ok("queued", queued.get("state") == "queued", str(queued))

    cmd_stale = {"id": "c3", "action": "run_next", "at": _iso(-5)}
    stalled = pv.derive_dispatch({"updated_at": old}, cmd_stale, now=now)
    _ok("stalled (tick dead)", stalled.get("state") == "stalled", str(stalled))

    # tick alive + cmd older than OPS_NO_ACK_SEC without ack
    status_alive = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 60))
    cmd_old_enough = {
        "id": "c4b",
        "action": "run_next",
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - pv.OPS_NO_ACK_SEC - 10)),
    }
    no_ack = pv.derive_dispatch({"updated_at": status_alive}, cmd_old_enough, now=now)
    _ok("no_ack", no_ack.get("state") == "no_ack", str(no_ack))

    refuse_id = "cref"
    _write(
        data_dir / f"refuse-{refuse_id}.json",
        {"cmd_id": refuse_id, "reason": "cap_OPS_MAX_RUNS_PER_DAY", "at": fresh},
    )
    refused = pv.derive_dispatch(
        {"updated_at": fresh},
        {"id": refuse_id, "action": "run_next", "at": fresh},
        now=now,
    )
    _ok("refused", refused.get("state") == "refused", str(refused))

    running = pv.derive_dispatch(
        {
            "updated_at": fresh,
            "status": "RUNNING",
            "ack": {"cmd_id": "crun", "at": fresh},
            "live": {
                "issue": "QUI-70",
                "agent": {"run_url": "https://cursor.com/agents/abc"},
            },
        },
        {"id": "crun", "action": "run_next", "at": fresh},
        now=now,
    )
    _ok("running", running.get("state") == "running", str(running))


def test_http_ops(pv: Any, data_dir: Path) -> None:
    print("==> HTTP /ops/run")
    _write(
        data_dir / "ops-status.json",
        {
            "ok": True,
            "status": "PAUSED",
            "engine": "PAUSED",
            "updated_at": "2026-10-01T12:00:00Z",
            "mode": "AUTOPILOT",
            "lanes": {
                "autopilot": [
                    {
                        "id": "QUI-70",
                        "title": "ready",
                        "url": "https://linear.app/quietforge/issue/QUI-70",
                    }
                ]
            },
            "next": {"id": "QUI-70", "title": "ready"},
        },
    )
    # incomplete DoR fixture for QUI-BAD; todo active matches so gate returns qui_dor_not_ready
    _write(data_dir / "ops-todo-fixture.json", {"meta": {"aktywne_zadanie": "QUI-BAD"}})
    _write(
        data_dir / "ops-linear-fixture.json",
        [
            {
                "id": "QUI-70",
                "title": "ready fixture",
                "description": (
                    "cel: x\nkontekst: y\nwymagania: z\nograniczenia: a\n"
                    "kryteria akceptacji\n- [ ] ok\nweryfikacja: t\n"
                    "Zakres środowiska: repo\n"
                ),
                "estimate": 2,
                "labels": ["agent"],
                "project": "hermes-ops",
                "url": "https://linear.app/quietforge/issue/QUI-70",
            },
            {
                "id": "QUI-BAD",
                "title": "no dor",
                "description": "brak pol",
                "estimate": None,
                "labels": [],
                "project": "hermes-ops",
            },
        ],
    )

    server = ThreadingHTTPServer(("127.0.0.1", 0), pv.Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"

    def post(body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        req = urllib.request.Request(
            base + "/ops/run",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8")
            try:
                return exc.code, json.loads(raw)
            except json.JSONDecodeError:
                return exc.code, {"raw": raw}

    try:
        before = json.loads((data_dir / "ops-status.json").read_text(encoding="utf-8"))
        stamp = before.get("updated_at")
        code, body = post({"action": "pause"})
        _ok("pause 200", code == 200 and body.get("ok") is True, f"{code} {body}")
        after = json.loads((data_dir / "ops-status.json").read_text(encoding="utf-8"))
        _ok("I1 pause no bump updated_at", after.get("updated_at") == stamp, after.get("updated_at"))

        code, body = post({"action": "stop"})
        after2 = json.loads((data_dir / "ops-status.json").read_text(encoding="utf-8"))
        _ok("stop 200", code == 200 and body.get("ok") is True, f"{code} {body}")
        _ok("I1 stop no bump updated_at", after2.get("updated_at") == stamp, after2.get("updated_at"))

        code, body = post({"action": "run_next", "issue_id": "QUI-BAD", "deploy": True})
        _ok("deploy_denied 403", code == 403 and body.get("code") == "ZASADA_11", f"{code} {body}")

        code, body = post({"action": "merge", "issue_id": "QUI-70"})
        # merge not in allowed set -> 400; vault also has explicit 403 LINEAR_FIRST if it ever lands
        merge_ok = (code == 400 and body.get("error") == "unknown action") or (
            code == 403 and body.get("code") in ("LINEAR_FIRST", "merge_not_from_phone")
        )
        _ok("merge_denied", merge_ok, f"{code} {body}")

        code, body = post({"action": "run_next", "issue_id": "QUI-BAD"})
        _ok(
            "DoR not ready 400",
            code == 400 and body.get("code") == "qui_dor_not_ready",
            f"{code} {body}",
        )

        # directory trap
        cmd_path = data_dir / "ops-cmd.json"
        if cmd_path.is_file():
            cmd_path.unlink()
        cmd_path.mkdir()
        try:
            code, body = post({"action": "pause"})
            _ok(
                "ops_cmd directory 409",
                code == 409 and "ops_cmd_path_is_directory" in str(body),
                f"{code} {body}",
            )
        finally:
            if cmd_path.is_dir():
                shutil.rmtree(cmd_path)
    finally:
        server.shutdown()
        server.server_close()


def test_ops_chat(pv: Any, data_dir: Path) -> None:
    print("==> HTTP /ops/chat + /hermes/chat 410")
    _write(
        data_dir / "ops-status.json",
        {
            "ok": True,
            "status": "STOPPED",
            "engine": "STOPPED",
            "updated_at": "2026-10-16T12:00:00Z",
            "mode": "AUTOPILOT",
            "reason": "stopped",
            "live": {
                "issue": "QUI-43",
                "agent": {"run_url": "https://cursor.com/agents/bc-test", "id": "bc-test"},
            },
            "next": {"id": "QUI-43", "title": "brand-kit"},
            "lanes": {"autopilot": [], "local": []},
        },
    )
    unit = pv.ops_chat_reply("co robić?", pv.ops_status_view())
    _ok("ops_chat_reply ok", unit.get("ok") is True and unit.get("engine") == "ops_facts", str(unit))
    _ok("ops_chat_reply mentions status", "STOPPED" in str(unit.get("reply") or "") or "Start" in str(unit.get("reply") or ""), str(unit))
    deny = pv.ops_chat_reply("zrób deploy teraz", {})
    _ok("ops_chat_reply zasada11", deny.get("code") == "ZASADA_11", str(deny))
    deny_m = pv.ops_chat_reply("merge?", {})
    _ok("ops_chat_reply merge", deny_m.get("code") == "LINEAR_FIRST", str(deny_m))

    server = ThreadingHTTPServer(("127.0.0.1", 0), pv.Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"

    def post(path: str, body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        req = urllib.request.Request(
            base + path,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8")
            try:
                return exc.code, json.loads(raw)
            except json.JSONDecodeError:
                return exc.code, {"raw": raw}

    try:
        code, body = post("/ops/chat", {"message": "url sesji"})
        _ok(
            "ops/chat 200 url",
            code == 200 and "cursor.com" in str(body.get("reply") or ""),
            f"{code} {body}",
        )
        code, body = post("/ops/chat", {"message": "merge na github"})
        _ok(
            "ops/chat merge refuse",
            code == 200 and body.get("code") == "LINEAR_FIRST",
            f"{code} {body}",
        )
        code, body = post("/hermes/chat", {"message": "hello"})
        _ok(
            "hermes/chat still 410",
            code == 410 and body.get("reason") == "academy_llm_retired",
            f"{code} {body}",
        )
    finally:
        server.shutdown()
        server.server_close()


def main() -> int:
    print("test_progress_vault — hermes-ops-nous")
    data_dir = Path(tempfile.mkdtemp(prefix="ops-vault-test-"))
    try:
        pv = _load_vault(data_dir)
        test_derive_run_halt_wins(pv, data_dir)
        test_derive_dispatch(pv, data_dir)
        test_http_ops(pv, data_dir)
        test_ops_chat(pv, data_dir)
    finally:
        shutil.rmtree(data_dir, ignore_errors=True)
    print("")
    if FAILS:
        print(f"NOT READY — {FAILS} fail(s)")
        return 1
    print("OK — vault gate PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
