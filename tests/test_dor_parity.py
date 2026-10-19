"""QUI-154: hermes-ops-nous DoR parity vs platform dor-v1-fixtures (+ SHA-256)."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "docs" / "ops" / "contracts" / "dor-v1-fixtures.json"
SHA_FILE = ROOT / "docs" / "ops" / "contracts" / "dor-v1-fixtures.sha256"
DOR = ROOT / "scripts" / "ops_linear_dor.py"
CONTRACT = ROOT / "docs" / "ops" / "HERMES-ROLE-CONTRACT.md"


def _load_dor():
    spec = importlib.util.spec_from_file_location("ops_linear_dor", DOR)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_fixture_sha256_matches_recorded():
    raw = FIXTURES.read_bytes()
    recorded = SHA_FILE.read_text(encoding="utf-8").split()[0].strip()
    assert hashlib.sha256(raw).hexdigest() == recorded


def test_fixture_sha256_fails_when_tampered():
    raw = FIXTURES.read_bytes()
    recorded = SHA_FILE.read_text(encoding="utf-8").split()[0].strip()
    tampered = raw + b"\n"
    assert hashlib.sha256(tampered).hexdigest() != recorded


def test_missing_dor_matches_all_fixtures():
    dor = _load_dor()
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    assert len(data["cases"]) >= 12
    for case in data["cases"]:
        got = dor._missing_dor(case["issue"], platform=True)
        expect = list(case["expect_missing"])
        assert sorted(got) == sorted(expect), f"{case['id']}: got={got} expect={expect}"


def test_s3_branch_convention_matches_k9():
    text = CONTRACT.read_text(encoding="utf-8")
    # S3 row must mention both Cloud cursor/* and laptop feat/fix/chore
    assert "cursor/*" in text
    assert "feat/*" in text and "fix/*" in text and "chore/*" in text
    # No lone "PR `cursor/*`" as the only S3 rule without laptop forms nearby
    idx = text.find("| S3 |")
    assert idx >= 0
    row = text[idx : idx + 200]
    assert "cursor/*" in row
    assert "feat/*" in row or "laptop" in row.lower()
