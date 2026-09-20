#!/usr/bin/env python3
"""Router Hermes B2 — 8 kanarków (mirror logiki hermesIntent w DASHBOARD.html)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASH = ROOT / "DASHBOARD.html"


def norm(s: str) -> str:
    import unicodedata

    t = unicodedata.normalize("NFD", s.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return t.replace("ł", "l")


GLOSSARY_KEYS = [
    "odcs",
    "hitl",
    "human-stop",
    "ledger",
    "otel",
    "r7",
    "security",
    "owasp",
    "growth",
    "werdykt",
    "tenant",
    "objective",
    "guardrail",
    "mcp",
    "budżet",
    "budzet",
    "złożoności",
    "zlozonosci",
    "cedar",
    "rls",
    "izolacj",
]

STATE_RE = re.compile(
    r"instalac|co dalej|gdzie jestem|lock|rytua|dzie[nń]|jak u[zż]ywa|eksport|sync|mistrzostw|drill",
    re.I,
)
SECRET_RE = re.compile(
    r"(podaj|poka[zż]|daj).*(klucz|token|sekret|vault)",
    re.I,
)


def intent(question: str) -> str:
    q = question.lower()
    qn = norm(question)
    if SECRET_RE.search(q):
        return "state"
    if STATE_RE.search(q):
        return "state"
    if re.search(r"\b([a-h])(\d{1,2})\b", q):
        return "state"
    for key in GLOSSARY_KEYS:
        kn = norm(key)
        if key in q or kn in qn:
            return "fact"
    return "open"


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
    if "intent==='state'||intent==='fact'" not in html.replace(" ", ""):
        if "intent==='state'||intent==='fact'" not in html:
            print("FAIL: hermesAsk nie short-circuituje state/fact przed LLM")
            return 1
    errors: list[str] = []
    for q, exp in CANARIES:
        got = intent(q)
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
