#!/usr/bin/env python3
"""Mutation guards Fala P: 7 tabów, TERAZ brief, zębate, firstOpen B, brak renderOpsCta na now."""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
VAL = ROOT / "scripts" / "validate-academy-export.py"

WATCHED = {"dash": ROOT / "DASHBOARD.html"}

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
        "P1 ósma zakładka wraca",
        "zakladek zamiast 7",
        [
            (
                "dash",
                "ACADEMY_TABS=[{id:'now'",
                "ACADEMY_TABS=[{id:'extra',title:'EXTRA',accent:'#888',desc:'x'},{id:'now'",
            )
        ],
    ),
    (
        "P2 renderOpsCta wraca na TERAZ",
        "TERAZ znowu dokłada CTA /ops",
        [("dash", "if(tab==='now')html=renderNowTab();", "if(tab==='now')html=renderNowTab()+renderOpsCta();")],
    ),
    (
        "P3 firstOpen znowu H-first",
        "firstOpen znowu H-first",
        [("dash", "var KURS_DZIAL_ORDER=['B','C','D','E','F','G'];", "var KURS_DZIAL_ORDER=['H','G','B','C','D','E','F','A'];")],
    ),
    (
        "P4 zabrano koło zębate",
        "brak koła zębatego",
        [("dash", 'id="gear-btn"', 'id="settings-btn"')],
    ),
    (
        "P5 work_log w tracks",
        "work_log wyciekł do tracks",
        [
            (
                "dash",
                "tracks:{W:{percent:pct,completed_ids:done.slice()},F:{percent:pct,completed_ids:done.slice()}}",
                "tracks:{W:{percent:pct,completed_ids:done.slice(),work_log:[]},F:{percent:pct,completed_ids:done.slice()}}",
            )
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
                    print("    stdout:", (result.stdout or "")[:320].replace("\n", " | "))
    finally:
        restore()

    zgodne = all(hashlib.sha256(p.read_bytes()).hexdigest() == HASHES[k] for k, p in WATCHED.items())
    print()
    print(f"ZLAPANE: {zlapane}/{len(MUTATIONS)}   PRZEPUSZCZONE: {len(przepuszczone)}   NIENAUZYTE: {len(nieuzyte)}")
    print("PLIKI PRZYWRÓCONE:", "TAK" if zgodne else "NIE — SPRAWDZ GIT!")
    return 0 if (zlapane == len(MUTATIONS) and zgodne) else 1


if __name__ == "__main__":
    sys.exit(main())
