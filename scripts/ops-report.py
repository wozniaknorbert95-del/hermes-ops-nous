#!/usr/bin/env python3
"""Raport Hermes Ops → data/ops-push-pending.json (tylko gdy jest NOWA treść).

Działa na VPS (systemd timer). Read-only wobec platformy; pisze wyłącznie:
  - data/ops-push-pending.json   (payload dla push-send.py --ops)
  - data/ops-report-last.json    (stan do detekcji delty)

SSoT syntezy: importuje `_build_ops_report` + `derive_run` + `read_ops_status`
z host/progress_vault.py — tę samą linię, którą renderuje karta Raport na /ops.
Jedna prawda o tym, „co Hermes Ops dziś zrobił".

Zdarzenia raportowane (reszta = cisza, nie spam):
  - `done`   → „merge OK (PR #…)"
  - `failed` → „FAILED (step…)"
  - `running`→ „agent pracuje nad QUI-…"

Użycie:
  python3 scripts/ops-report.py --dry-run
  python3 scripts/ops-report.py
  python3 scripts/ops-report.py --force
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.environ.get("ACADEMY_DATA_DIR", ROOT / "data"))
PENDING = DATA_DIR / "ops-push-pending.json"
STATE = DATA_DIR / "ops-report-last.json"

REPORTABLE = {"done", "failed", "running"}


def force_utf8_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def build_report() -> dict[str, Any]:
    host_dir = str(ROOT / "host")
    if host_dir not in sys.path:
        sys.path.insert(0, host_dir)
    from progress_vault import _build_ops_report, derive_run, read_ops_status  # noqa: PLC0415

    status = read_ops_status()
    # derive_run jest pure (bez sieci) — dokłada werdykt done/failed/running do cache ticka.
    status["run"] = derive_run(status)
    return _build_ops_report(status)


def _fingerprint(report: dict[str, Any]) -> str:
    return json.dumps(
        {
            "verdict": report.get("verdict"),
            "runs": report.get("runs"),
            "merged": report.get("merged"),
            "failed": report.get("failed"),
        },
        sort_keys=True,
        ensure_ascii=False,
    )


def _load_state() -> dict[str, Any]:
    if not STATE.is_file():
        return {}
    try:
        raw = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return raw if isinstance(raw, dict) else {}


def _save_state(report: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(
        json.dumps(
            {"fp": _fingerprint(report), "line": report.get("line"), "at": int(time.time())},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def _write_pending(report: dict[str, Any]) -> str:
    payload = {
        "title": "Hermes Ops — raport",
        "body": report["line"],
        "url": "./OPS.html",
        "tag": "hermes-ops-report",
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PENDING.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return json.dumps(payload, ensure_ascii=False)


def main() -> int:
    force_utf8_streams()
    parser = argparse.ArgumentParser(description="Hermes Ops — raport dnia (Web Push).")
    parser.add_argument("--dry-run", action="store_true", help="pokaż, nie pisz")
    parser.add_argument("--force", action="store_true", help="pisz pending mimo braku delty")
    args = parser.parse_args()

    report = build_report()
    verdict = str(report.get("verdict") or "idle")
    fp = _fingerprint(report)
    prev = _load_state()
    changed = fp != prev.get("fp")
    reportable = verdict in REPORTABLE

    if args.dry_run:
        print(
            json.dumps(
                {"verdict": verdict, "reportable": reportable, "changed": changed, "report": report},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if not reportable:
        print(f"SKIP: verdict={verdict} — raport wysyłam tylko na done/failed/running.")
        return 0

    if not changed and not args.force:
        print(f"SKIP: {report.get('line')} — już zgłoszony.")
        return 0

    _save_state(report)
    payload = _write_pending(report)
    print(f"PENDING: {payload}")
    return 0


if __name__ == "__main__":
    sys.exit(main())