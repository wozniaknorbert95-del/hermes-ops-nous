#!/usr/bin/env python3
"""Hermes Ops DoR gate — Linear READ, no secrets in logs.

Parity snapshot of dsaas-platform-main/scripts/check-linear-contract.py
plus workflow-lab 6-field headings. Does not import those repos.

LINEAR_OPS_READ empty → missing token (fail-closed at vault).
LINEAR_OPS_READ=test-linear-fixture → DATA_DIR fixtures (vault tests, no network).
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

QUI_RE = re.compile(r"QUI-\d+", re.I)
IDENT_RE = re.compile(r"^([A-Z]+)-(\d+)$", re.I)
SIX_FIELDS = ("cel", "kontekst", "wymagania", "ograniczenia", "kryteria akceptacji", "weryfikacja")
HITL_LABELS = ("hitl:approval-required", "blocked", "blocked:external")
# Task *requires* a laptop/VPS — not a prohibition written in AC text.
REQUIRE_LOCAL = (
    "go deploy",
    "deploy lab",
    "deploy vps",
    " ssh",
    "vps ",
    "keycloak",
    "cutover",
    "smoke vps",
    "public https",
    "rollback prod",
    "certbot",
    "platform-admin",
)
CACHE_TTL_SEC = 60

LINEAR_GQL = "https://api.linear.app/graphql"


def _data_dir() -> Path:
    return Path(os.environ.get("ACADEMY_DATA_DIR", Path(__file__).resolve().parents[1] / "data"))


def linear_token() -> str:
    return str(os.environ.get("LINEAR_OPS_READ") or "").strip()


def parse_qui(text: str) -> str:
    m = QUI_RE.search(text or "")
    return m.group(0).upper() if m else ""


def _missing_dor(issue: dict[str, Any], *, platform: bool) -> list[str]:
    labels = [str(x).lower() for x in (issue.get("labels") or [])]
    text = " ".join(str(issue.get(k, "")) for k in ("title", "body", "description")).lower()
    missing: list[str] = []
    if not issue.get("estimate"):
        missing.append("estimate")
    if not ("kryteria akceptacji" in text or "acceptance" in text or "- [ ]" in text):
        missing.append("kryteria akceptacji (AC)")
    if "agent" not in labels:
        missing.append("label agent")
    if platform:
        if "severity" not in text and "p0" not in text and "p1" not in text and "p2" not in text and "p3" not in text:
            missing.append("severity")
        if "nc-" not in text and "**nc:**" not in text:
            missing.append("NC")
        if "fala" not in text:
            missing.append("fala")
        if "owner" not in text and "raci" not in text:
            missing.append("owner/RACI")
        if "zakres środowiska" not in text and "zasada 11" not in text:
            missing.append("zakres środowiska")
        if "rollback" not in text:
            missing.append("rollback")
    else:
        for field in SIX_FIELDS:
            if field not in text:
                missing.append(f"6 pól: {field}")
    return missing


def _requires_local(issue: dict[str, Any]) -> bool:
    title = str(issue.get("title") or "").lower()
    desc = str(issue.get("description") or issue.get("body") or "")
    scope = ""
    for line in desc.splitlines():
        low = line.lower()
        if "zakres środowiska" in low or "zakres srodowiska" in low:
            scope = low
            break
    hay = f" {title} {scope} "
    return any(m in hay for m in REQUIRE_LOCAL)


def _labels(issue: dict[str, Any]) -> list[str]:
    return [str(x).lower() for x in (issue.get("labels") or [])]


def evaluate_issue(issue: dict[str, Any], *, todo_active: str = "", dirty: bool = False) -> dict[str, Any]:
    ident = str(issue.get("id") or issue.get("identifier") or "").upper()
    labels = _labels(issue)
    project = str(issue.get("project") or "").lower()
    platform = "dsaas-platform" in project or project.endswith("platform-main")
    missing = _missing_dor(issue, platform=platform if project else True)
    hitl = [x for x in HITL_LABELS if x in labels]
    code = ""
    if hitl and ("blocked" in hitl or "blocked:external" in hitl) and "hitl:approval-required" not in hitl:
        code = "qui_blocked"
    elif "hitl:approval-required" in labels:
        code = "qui_hitl"
    elif _requires_local(issue):
        code = "qui_lane_local"
    elif dirty:
        code = "qui_dirty_pr"
    elif todo_active and ident and ident not in todo_active.upper():
        code = "qui_todo_mismatch"
    elif missing:
        code = "qui_dor_not_ready"
    lane = "LOCAL" if code in ("qui_hitl", "qui_lane_local", "qui_blocked") else ("HERMES" if not code else "STOP")
    return {
        "ok": not code,
        "code": code or "ok",
        "missing": missing,
        "lane": lane,
        "id": ident,
        "title": str(issue.get("title") or ""),
        "url": str(issue.get("url") or ""),
        "project": str(issue.get("project") or ""),
        "todo_active": todo_active,
        "todo_match": (not todo_active) or (ident in todo_active.upper()),
    }


def _fixture_issue(issue_id: str) -> dict[str, Any]:
    path = _data_dir() / "ops-linear-fixture.json"
    if path.is_file():
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, dict) and (not issue_id or str(raw.get("id") or "").upper() == issue_id.upper()):
            return raw
        if isinstance(raw, list):
            for it in raw:
                if str((it or {}).get("id") or "").upper() == issue_id.upper():
                    return it
    iid = (issue_id or "QUI-70").upper()
    return {
        "id": iid,
        "identifier": iid,
        "title": "test fixture",
        "description": (
            "Kryteria akceptacji\n- [ ] x\n**Severity:** P2 · **NC:** NC-3 · **Fala:** TEST · "
            "Owner (RACI): R5\nZakres środowiska: repo\nRollback: revert"
        ),
        "estimate": 3,
        "labels": ["agent"],
        "project": "dsaas-platform-main",
        "url": f"https://linear.app/quietforge/issue/{iid}",
        "state": "Ready",
    }


def _linear_headers(token: str) -> dict[str, str]:
    return {"Authorization": token, "Content-Type": "application/json"}


def _gql(token: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    req = urllib.request.Request(
        LINEAR_GQL,
        data=json.dumps(payload).encode("utf-8"),
        headers=_linear_headers(token),
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None


def _issue_from_node(node: dict[str, Any], ident: str) -> dict[str, Any]:
    labels = [n.get("name") for n in ((node.get("labels") or {}).get("nodes") or []) if isinstance(n, dict)]
    project = ((node.get("project") or {}) or {}).get("name") or ""
    state = ((node.get("state") or {}) or {}).get("name") or ""
    return {
        "id": str(node.get("identifier") or ident),
        "title": node.get("title") or "",
        "description": node.get("description") or "",
        "estimate": node.get("estimate"),
        "url": node.get("url") or "",
        "labels": labels,
        "project": project,
        "state": state,
    }


def fetch_linear_issue(issue_id: str) -> dict[str, Any] | None:
    token = linear_token()
    if not token:
        return None
    if token == "test-linear-fixture":
        return _fixture_issue(issue_id)
    ident = (issue_id or "").strip().upper()
    parsed = IDENT_RE.match(ident)
    if not parsed:
        return None
    team, num = parsed.group(1).upper(), int(parsed.group(2))
    # Linear `issue(id:)` wants UUID. Phone sends QUI-70 — lookup by team key + number.
    payload = {
        "query": (
            "query($team: String!, $num: Float!) { issues(filter: { team: { key: { eq: $team } }, "
            "number: { eq: $num } }, first: 1) { nodes { identifier title description estimate url "
            "state { name } labels { nodes { name } } project { name } } } }"
        ),
        "variables": {"team": team, "num": float(num)},
    }
    body = _gql(token, payload)
    if not body:
        return None
    nodes = (((body.get("data") or {}).get("issues") or {}).get("nodes")) or []
    node = nodes[0] if nodes and isinstance(nodes[0], dict) else None
    if not node:
        return None
    return _issue_from_node(node, ident)


def fetch_pulse() -> list[dict[str, Any]]:
    token = linear_token()
    if token == "test-linear-fixture":
        path = _data_dir() / "ops-pulse-fixture.json"
        if path.is_file():
            raw = json.loads(path.read_text(encoding="utf-8"))
            return raw if isinstance(raw, list) else []
        return [
            {"id": "QUI-76", "title": "quote-clerk", "status": "Ready", "dor": "NOT-READY"},
            {"id": "QUI-93", "title": "nightly", "status": "In Progress", "dor": "READY"},
            {"id": "QUI-98", "title": "Actions $0", "status": "Blocked", "dor": "HITL"},
        ]
    if not token:
        return []
    payload = {
        "query": (
            "query { issues(filter: { team: { key: { eq: \"QUI\" } } }, first: 12, orderBy: updatedAt) "
            "{ nodes { identifier title state { name } labels { nodes { name } } estimate "
            "description project { name } } } }"
        )
    }
    body = _gql(token, payload)
    if not body:
        return []
    nodes = (((body.get("data") or {}).get("issues") or {}).get("nodes")) or []
    ranked: list[dict[str, Any]] = []
    rest: list[dict[str, Any]] = []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        project = str(((node.get("project") or {}) or {}).get("name") or "")
        issue = {
            "id": node.get("identifier"),
            "title": node.get("title"),
            "description": node.get("description"),
            "estimate": node.get("estimate"),
            "labels": [n.get("name") for n in ((node.get("labels") or {}).get("nodes") or []) if isinstance(n, dict)],
            "project": project or "dsaas-platform-main",
        }
        ev = evaluate_issue(issue)
        row = {
            "id": ev["id"],
            "title": ev["title"],
            "status": str(((node.get("state") or {}) or {}).get("name") or ""),
            "dor": "READY" if ev["ok"] else ev["code"],
        }
        low = project.lower()
        if "dsaas" in low or "platform" in low:
            ranked.append(row)
        else:
            rest.append(row)
    out = (ranked + rest)[:3]
    return out


def load_todo_active() -> str:
    token = linear_token()
    path = _data_dir() / "ops-todo-fixture.json"
    if token == "test-linear-fixture" or path.is_file():
        if path.is_file():
            raw = json.loads(path.read_text(encoding="utf-8"))
            meta = raw.get("meta") if isinstance(raw, dict) else {}
            return str((meta or {}).get("aktywne_zadanie") or "")
        return "QUI-70 test"
    status_path = _data_dir() / "ops-status.json"
    if status_path.is_file():
        try:
            raw = json.loads(status_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            raw = {}
        if isinstance(raw, dict):
            for candidate in (
                raw.get("todo_active"),
                (raw.get("tor") or {}).get("aktywne_zadanie") if isinstance(raw.get("tor"), dict) else None,
                (raw.get("meta") or {}).get("aktywne_zadanie") if isinstance(raw.get("meta"), dict) else None,
            ):
                if candidate:
                    return str(candidate)
    return ""


def load_dirty_flag(issue_id: str) -> bool:
    path = _data_dir() / "ops-dirty-fixture.json"
    if path.is_file():
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, dict) and str(raw.get("issue") or "").upper() == (issue_id or "").upper():
            return bool(raw.get("dirty"))
    return False


def gate_start(issue_id: str) -> dict[str, Any]:
    token = linear_token()
    if not token:
        return {
            "ok": False,
            "code": "missing_LINEAR_OPS_READ",
            "missing": ["LINEAR_OPS_READ"],
            "lane": "UNKNOWN",
            "id": issue_id,
            "todo_match": True,
            "pulse": [],
        }
    issue = fetch_linear_issue(issue_id)
    if not issue:
        return {
            "ok": False,
            "code": "qui_dor_not_ready",
            "missing": ["linear issue"],
            "lane": "UNKNOWN",
            "id": issue_id,
            "todo_match": True,
            "pulse": fetch_pulse(),
        }
    todo = load_todo_active()
    dirty = load_dirty_flag(str(issue.get("id") or issue_id))
    ev = evaluate_issue(issue, todo_active=todo, dirty=dirty)
    ev["pulse"] = fetch_pulse()
    return ev


def read_cache() -> dict[str, Any] | None:
    path = _data_dir() / "ops-dor-cache.json"
    if not path.is_file():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    age = time.time() - float(raw.get("at") or 0)
    if age > CACHE_TTL_SEC:
        return None
    return raw


def write_cache(payload: dict[str, Any]) -> None:
    path = _data_dir() / "ops-dor-cache.json"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        blob = dict(payload)
        blob["at"] = time.time()
        path.write_text(json.dumps(blob, ensure_ascii=False), encoding="utf-8")
    except OSError:
        return


def status_overlay(next_id: str) -> dict[str, Any]:
    cached = read_cache()
    if cached and str(cached.get("id") or "") == (next_id or "") and cached.get("pulse") is not None:
        return cached
    token = linear_token()
    if not token:
        overlay = {
            "ok": False,
            "code": "missing_LINEAR_OPS_READ",
            "missing": ["LINEAR_OPS_READ"],
            "lane": "UNKNOWN",
            "id": next_id,
            "todo_match": True,
            "todo_active": "",
            "pulse": [],
            "ci_hint": "",
        }
        return overlay
    if not next_id:
        overlay = {
            "ok": True,
            "code": "idle",
            "missing": [],
            "lane": "HERMES",
            "id": "",
            "todo_match": True,
            "todo_active": load_todo_active(),
            "pulse": fetch_pulse(),
            "ci_hint": "",
        }
        write_cache(overlay)
        return overlay
    overlay = gate_start(next_id)
    overlay["ci_hint"] = ""
    write_cache(overlay)
    return overlay
