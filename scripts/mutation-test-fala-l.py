#!/usr/bin/env python3
"""Mutation test guardów Fala L: Hermes dual-control (Akademia vs Engineer)."""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
VAL = ROOT / "scripts" / "validate-academy-export.py"

WATCHED = {
    "dash": ROOT / "DASHBOARD.html",
    "vault": ROOT / "host" / "progress_vault.py",
    "contract": ROOT / "docs" / "ops" / "HERMES-ROLE-CONTRACT.md",
}

ORIG_BYTES = {k: p.read_bytes() for k, p in WATCHED.items()}
ORIG = {k: v.decode("utf-8").replace("\r\n", "\n") for k, v in ORIG_BYTES.items()}
HASHES = {k: hashlib.sha256(v).hexdigest() for k, v in ORIG_BYTES.items()}


def restore() -> None:
    for k, p in WATCHED.items():
        p.write_bytes(ORIG_BYTES[k])


def apply(muts: list[tuple[str, str, str]]) -> bool:
    work = dict(ORIG)
    for k, old, new in muts:
        if old not in work[k]:
            return False
        work[k] = work[k].replace(old, new, 1)
    for k in {m[0] for m in muts}:
        WATCHED[k].write_bytes(work[k].encode("utf-8"))
    return True


MUTATIONS = [
    (
        "L1 copy HERMES obiecuje PR/MCP",
        "copy HERMES obiecuje wykonanie",
        [("dash", "Nie buduje PR-ów", "MCP i git push budują PR za Ciebie")],
    ),
    (
        "L2 brak karty Engineer / skrócone kroki",
        "karta Engineer — kroki != 6 pathów playbooku",
        [
            (
                "dash",
                "'6 — Auto-merge labu: workflow-lab/DECISIONS.md'",
                "'6 — usuniety krok'",
            ),
        ],
    ),
    (
        "L3 karta AKTYWNY przed e2e",
        "ENGINEER_LOOP_E2E=true bez C4 e2e",
        [
            ("dash", "status:'PARTIAL / SETUP'", "status:'AKTYWNY'"),
            ("dash", "var ENGINEER_LOOP_E2E=false;", "var ENGINEER_LOOP_E2E=true;"),
        ],
    ),
    (
        "L4 ACADEMY_TABS 7 elementów",
        "ACADEMY_TABS != 6",
        [
            (
                "dash",
                "{id:'hermes',title:'HERMES'",
                "{id:'extra',title:'EXTRA'},{id:'hermes',title:'HERMES'",
            ),
        ],
    ),
    (
        "L5 /hermes/chat handler z MCP",
        "vault bez zakazu MCP",
        [
            (
                "vault",
                "POST /hermes/chat nie ma narzędzi MCP.",
                "POST /hermes/chat moze wywolac mcp tools.",
            ),
        ],
    ),
    (
        "L6 dryf playbook vs karta Engineer",
        "dryf playbook vs karta Engineer",
        [
            (
                "dash",
                "'6 — Auto-merge labu: workflow-lab/DECISIONS.md'",
                "'6 — Auto-merge labu: workflow-lab/DRIFT-NOPE.md'",
            ),
        ],
    ),
]


def main() -> int:
    zlapane = 0
    przepuszczone: list[str] = []
    nieuzyte: list[str] = []
    try:
        for nazwa, oczekiwane, muts in MUTATIONS:
            if not apply(muts):
                nieuzyte.append(nazwa)
                print(f"  POMIN?        | {nazwa} | anchor nie znaleziony")
                restore()
                continue
            result = subprocess.run(
                [sys.executable, str(VAL)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            restore()
            ok = result.returncode != 0 and oczekiwane in (result.stdout or "")
            if ok:
                zlapane += 1
                print(f"  ZLAPANE       | {nazwa}")
            else:
                przepuszczone.append(nazwa)
                print(f"  PRZEPUSZCZONE | {nazwa} | oczekiwano: {oczekiwane}")
                if result.stdout:
                    print("    stdout:", (result.stdout or "")[:280].replace("\n", " | "))
    finally:
        restore()

    zgodne = all(
        hashlib.sha256(p.read_bytes()).hexdigest() == HASHES[k] for k, p in WATCHED.items()
    )
    print()
    print(f"ZLAPANE: {zlapane}/{len(MUTATIONS)}   PRZEPUSZCZONE: {len(przepuszczone)}   NIENAUZYTE: {len(nieuzyte)}")
    print("PLIKI PRZYWRÓCONE:", "TAK" if zgodne else "NIE — SPRAWDZ GIT!")
    return 0 if (zlapane == len(MUTATIONS) and zgodne) else 1


if __name__ == "__main__":
    sys.exit(main())
