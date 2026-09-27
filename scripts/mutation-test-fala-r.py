#!/usr/bin/env python3
"""Mutation guards Fala R: bramka DoR przed @cursor (LINEAR_OPS_READ + gate_start + CONTRACT)."""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
VAL = ROOT / "scripts" / "validate-academy-export.py"

WATCHED = {
    "vault": ROOT / "host" / "progress_vault.py",
    "setup": ROOT / "scripts" / "setup-akademia-vps.sh",
    "contract": ROOT / "docs" / "ops" / "CONTRACT-OPS-STATUS.md",
    "dor": ROOT / "scripts" / "ops_linear_dor.py",
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
        "R1 vault bez gate_start",
        "POST /ops/run bez gate_start",
        [("vault", "gate = ops_linear_dor.gate_start(issue_id)", "gate = {\"ok\": True}")],
    ),
    (
        "R2 setup bez LINEAR_OPS_READ",
        "setup nie woła ensure_env_key LINEAR_OPS_READ",
        [("setup", "ensure_env_key LINEAR_OPS_READ\n", "")],
    ),
    (
        "R3 CONTRACT gubi qui_todo_mismatch",
        "CONTRACT bez reason DoR",
        [("contract", "`qui_todo_mismatch`", "`qui_todo_gone`")],
    ),
    (
        "R4 _NEG_ENV gubi 'dotyczy' (nie dotyczy VPS)",
        "nie dotyczy VPS",
        [("dor", "dotycz", "dotyc")],
    ),
    (
        "R5 _NEG_ENV gubi 'dostępu do' (bez dostępu do VPS)",
        "bez dostępu do VPS",
        [("dor", "dost[ęe]pu", "dost[u]pu")],
    ),
    (
        "R6 _NEG_ENV gubi 'deployment'",
        "kwantyfikator 'deployment'",
        [("dor", "deployment", "deploymen")],
    ),
    (
        "R7 setup bez timera raportu Ops",
        "setup bez timera raportu Ops",
        [("setup", "OnCalendar=*:0/15", "OnCalendar=*:0/99")],
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
                    print("    stdout:", (result.stdout or "")[:400].replace("\n", " | "))
    finally:
        restore()

    zgodne = all(hashlib.sha256(p.read_bytes()).hexdigest() == HASHES[k] for k, p in WATCHED.items())
    print()
    print(f"ZLAPANE: {zlapane}/{len(MUTATIONS)}   PRZEPUSZCZONE: {len(przepuszczone)}   NIENAUZYTE: {len(nieuzyte)}")
    print("PLIKI PRZYWRÓCONE:", "TAK" if zgodne else "NIE — SPRAWDZ GIT!")
    return 0 if (zlapane == len(MUTATIONS) and zgodne) else 1


if __name__ == "__main__":
    sys.exit(main())
