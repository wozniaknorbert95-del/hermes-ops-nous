#!/usr/bin/env python3
"""Walidator kontraktu AcademyProgress v0 (stdlib only).

Sprawdza:
1. schema/academy-progress.v0.json istnieje i jest poprawnym JSON Schema draft 2020-12 (składnia).
2. DASHBOARD.html zawiera jedno TERAZ, strefy Dzień/Platforma/Piątek, progressbar ARIA,
   przycisk nowact, status import/eksportu i brak alert().
3. Przykładowy envelope (6 modułów) spełnia wymagane pola schematu.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema" / "academy-progress.v0.json"
DASH = ROOT / "DASHBOARD.html"

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def main() -> int:
    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: schema unreadable: {exc}")
        return 1
    for key in ("schema_version", "tenant_id", "updated_at", "source"):
        if key not in schema.get("required", []):
            fail(f"schema missing required '{key}'")
    if schema.get("properties", {}).get("source", {}).get("const") != "academy-os":
        fail("schema source const != academy-os")

    try:
        html = DASH.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"FAIL: dashboard unreadable: {exc}")
        return 1

    checks = {
        "jedna karta TERAZ (id=nowcard)": html.count('id="nowcard"') == 1,
        "przycisk TERAZ (id=nowact, button)": 'id="nowact"' in html and "<button" in html,
        "progressbar ARIA": 'role="progressbar"' in html and 'aria-valuenow' in html,
        "strefa Dzień": "Mój dzień" in html or "Rano — 10 minut" in html,
        "strefa Platforma": "Platforma — gdzie jest główna praca" in html,
        "strefa Piątek": "Piątek — koszty i porządek" in html,
        "status import/eksport (id=syncmsg)": 'id="syncmsg"' in html,
        "brak alert()": "alert(" not in html,
        "skip link": 'class="skip"' in html,
        "main landmark": "<main>" in html,
        "klikana biblioteka m1": 'href="cursor-kurs/00-START-TUTAJ.md"' in html,
    }
    for name, ok in checks.items():
        if not ok:
            fail(f"dashboard: {name}")

    sample = {
        "schema_version": "0.1.0",
        "tenant_id": "quietforge",
        "updated_at": "2026-09-12T00:00:00+00:00",
        "source": "academy-os",
        "academy_url": "",
        "now_card": "Moduł 1 — test",
        "tracks": {"W": {"percent": 17, "completed_ids": ["m1"]}, "F": {"percent": 17, "completed_ids": ["m1"]}},
        "_scratch": {"m1_pass": True},
    }
    for key in schema.get("required", []):
        if key not in sample:
            fail(f"sample envelope missing '{key}'")

    if errors:
        print("FAIL:")
        for item in errors:
            print(f" - {item}")
        return 1
    print("PASS: academy export contract + dashboard v1 (local-first)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
