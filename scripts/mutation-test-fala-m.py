#!/usr/bin/env python3
"""Mutation guards Fala M: split Academy / Ops (4 taby, 410, /ops)."""
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
    "ops": ROOT / "OPS.html",
    "man": ROOT / "manifest.webmanifest",
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
        "M1 piata zakladka akademii",
        "ACADEMY_TABS != 4",
        [("dash", "{id:'day',title:'DZIEŃ'", "{id:'extra',title:'EXTRA'},{id:'day',title:'DZIEŃ'")],
    ),
    (
        "M2 czat modelu wraca na TERAZ",
        "TERAZ znowu dokłada czat modelu",
        [("dash", "renderNowTab()+renderOpsCta()", "renderNowTab()+renderNowAskHermes()")],
    ),
    (
        "M3 POST /hermes/chat znowu 200",
        "POST /hermes/chat nie jest emerytowany",
        [("vault", "HTTPStatus.GONE", "HTTPStatus.OK")],
    ),
    (
        "M4 manifest bez /ops",
        "manifest bez shortcut /ops",
        [("man", '"./ops"', '"./DASHBOARD.html"')],
    ),
    (
        "M5 OPS.html bez panelu Kolejka",
        "OPS.html bez panelu Kolejka",
        [("ops", "Kolejka Linear", "Lista zadan")],
    ),
    (
        "M6 kontrakt bez Linear-first",
        "kontrakt bez zdania kanonicznego",
        [("contract", "Decyzja jest w Linear, nie na GitHubie.", "Decyzja jest na GitHubie.")],
    ),
    (
        "M7 OPS bez 44px",
        "OPS.html bez celów 44px",
        [("ops", "min-height:44px;min-width:44px", "min-height:32px;min-width:32px")],
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

    zgodne = all(hashlib.sha256(p.read_bytes()).hexdigest() == HASHES[k] for k, p in WATCHED.items())
    print()
    print(f"ZLAPANE: {zlapane}/{len(MUTATIONS)}   PRZEPUSZCZONE: {len(przepuszczone)}   NIENAUZYTE: {len(nieuzyte)}")
    print("PLIKI PRZYWRÓCONE:", "TAK" if zgodne else "NIE — SPRAWDZ GIT!")
    return 0 if (zlapane == len(MUTATIONS) and zgodne) else 1


if __name__ == "__main__":
    sys.exit(main())
