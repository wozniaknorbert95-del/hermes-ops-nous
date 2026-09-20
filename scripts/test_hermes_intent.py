#!/usr/bin/env python3
"""Router Hermes B2 — kanarki (SoT: host/hermes_router.py)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "host"))

from hermes_router import hermes_intent  # noqa: E402

DASH = ROOT / "DASHBOARD.html"

CANARIES = [
    ("co dalej?", "state"),
    ("dlaczego lock?", "state"),
    ("wytłumacz ODCS", "fact"),
    ("podaj klucz api vault", "state"),
    ("zrób deploy teraz", "open"),
    ("jak używać akademii?", "state"),
    ("co to r7?", "fact"),
    ("xyz foo bar", "open"),
]


def main() -> int:
    html = DASH.read_text(encoding="utf-8")
    if "function hermesIntent(" not in html:
        print("FAIL: brak hermesIntent w DASHBOARD.html")
        return 1
    if "hermesIntent" not in (html.split("function hermesAsk(")[1][:2500] if "function hermesAsk(" in html else ""):
        print("FAIL: hermesAsk nie używa hermesIntent")
        return 1
    errors: list[str] = []
    for q, exp in CANARIES:
        got = hermes_intent(q)
        if got != exp:
            errors.append(f"{q!r} → {got}, oczekiwano {exp}")
    if errors:
        print("FAIL hermes-intent:")
        for e in errors:
            print(" -", e)
        return 1
    print("PASS: hermes-intent (8 kanarków)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
