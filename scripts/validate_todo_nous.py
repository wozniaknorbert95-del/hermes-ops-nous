#!/usr/bin/env python3
"""Validate hermes-ops-nous/todo.json — Control Plane SoT, not platform queue."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODO_PATH = ROOT / "todo.json"
REPO = "hermes-ops-nous"
HON_RE = re.compile(r"^HON-[A-Z0-9-]+$")
PLATFORM_WORDS = (
    "kokpit",
    "demand os",
    "quietforge tenant",
    "provision map",
    "dsaas-platform",
)
ACTIVE_TASK = frozenset({"TODO", "IN_PROGRESS"})
PHASE_ACTIVE = "ACTIVE"


def fail(msg: str) -> int:
    print(f"FAIL: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    if not TODO_PATH.is_file():
        return fail(f"missing {TODO_PATH}")
    try:
        data = json.loads(TODO_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"JSON: {exc}")
    if not isinstance(data, dict):
        return fail("root must be object")

    meta = data.get("meta")
    if not isinstance(meta, dict):
        return fail("meta missing")
    if meta.get("repo") != REPO:
        return fail(f"meta.repo must be {REPO!r}, got {meta.get('repo')!r}")

    active = str(meta.get("aktywne_zadanie") or "").strip()
    if active and not HON_RE.match(active):
        return fail(f"meta.aktywne_zadanie must match HON-*, got {active!r}")

    fazy = data.get("fazy")
    if not isinstance(fazy, list) or not fazy:
        return fail("fazy must be non-empty list")

    active_phases = [f for f in fazy if isinstance(f, dict) and f.get("status") == PHASE_ACTIVE]
    if len(active_phases) != 1:
        return fail(f"exactly one ACTIVE phase required, got {len(active_phases)}")

    phase = active_phases[0]
    nazwa = str(phase.get("nazwa") or "").lower()
    for word in PLATFORM_WORDS:
        if word in nazwa:
            return fail(f"ACTIVE phase name looks like platform work: {phase.get('nazwa')!r}")

    tasks = phase.get("zadania")
    if not isinstance(tasks, list):
        return fail("ACTIVE phase zadania must be list")
    open_tasks = [
        t
        for t in tasks
        if isinstance(t, dict) and str(t.get("status") or "") in ACTIVE_TASK
    ]
    idle = str(meta.get("nastepne_todo") or "").strip().upper().startswith("IDLE")
    if not open_tasks and not idle:
        return fail("ACTIVE phase needs >=1 TODO|IN_PROGRESS task (or meta.nastepne_todo starts with IDLE)")

    if active:
        found_status = None
        for f in fazy:
            if not isinstance(f, dict):
                continue
            for t in f.get("zadania") or []:
                if isinstance(t, dict) and t.get("id") == active:
                    found_status = str(t.get("status") or "")
                    break
            if found_status is not None:
                break
        if found_status is None:
            return fail(f"meta.aktywne_zadanie {active} not found in fazy")
        if found_status not in ACTIVE_TASK:
            return fail(
                f"meta.aktywne_zadanie {active} status={found_status} "
                f"(want TODO|IN_PROGRESS)"
            )

    for f in fazy:
        if not isinstance(f, dict) or f.get("status") != PHASE_ACTIVE:
            continue
        for t in f.get("zadania") or []:
            if not isinstance(t, dict):
                continue
            title = str(t.get("tytul") or "").lower()
            for word in PLATFORM_WORDS:
                if word in title:
                    return fail(f"ACTIVE task looks like platform: {t.get('id')}")

    decisions = meta.get("decyzje_dowodcy")
    if isinstance(decisions, list) and len(decisions) > 15:
        return fail(f"decyzje_dowodcy length {len(decisions)} > 15")

    log = data.get("log")
    if isinstance(log, list) and len(log) > 30:
        return fail(f"log length {len(log)} > 30")

    print("PASS: todo.json ok")
    print(f"  tor={meta.get('aktywny_tor')} active={active}")
    print(f"  phase={phase.get('id')} open_tasks={len(open_tasks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
