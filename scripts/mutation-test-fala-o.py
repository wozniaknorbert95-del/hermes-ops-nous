#!/usr/bin/env python3
"""Mutation guards Fala O: 8 tabów, chrome kill, lis H, ŹRÓDŁA (sztab v6)."""
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
        "O1 zabrano MONETYZACJA (id money)",
        "bez zakladki money",
        [("dash", "{id:'money',title:'MONETYZACJA'", "{id:'cash',title:'MONETYZACJA'")],
    ),
    (
        "O2 zabrano ZRODLA (id sources)",
        "bez zakladki sources",
        [("dash", "{id:'sources',title:'ŹRÓDŁA'", "{id:'refs',title:'ŹRÓDŁA'")],
    ),
    (
        "O3 przywrócono nav-legend",
        "zakaz #nav-legend",
        [
            (
                "dash",
                '<nav class="tabs" role="tablist" aria-label="Główne zakładki Akademii" id="tablist"></nav>',
                '<nav class="tabs" role="tablist" aria-label="Główne zakładki Akademii" id="tablist"></nav><p class="nav-legend" id="nav-legend">legenda</p>',
            )
        ],
    ),
    (
        "O4 dsaas-flows znowu grid 7 mermaidów",
        "dsaas-flows nie może być gridem",
        [("dash", '\'<div id="dsaas-flows">\'+renderDiagram(DIAGRAMS[id]', '\'<div class="grid two" id="dsaas-flows">\'+renderDiagram(DIAGRAMS[id]')],
    ),
    (
        "O5 usunięto #course-map",
        "brak #course-map",
        [("dash", 'id="course-map"', 'id="cmap"')],
    ),
    (
        "O6 brak H4",
        "brak rozdziału H4",
        [("dash", 'id:"H4"', 'id:"HX"')],
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

    zgodne = all(
        hashlib.sha256(p.read_bytes()).hexdigest() == HASHES[k] for k, p in WATCHED.items()
    )
    print()
    print(f"ZLAPANE: {zlapane}/{len(MUTATIONS)}   PRZEPUSZCZONE: {len(przepuszczone)}   NIENAUZYTE: {len(nieuzyte)}")
    print("PLIKI PRZYWRÓCONE:", "TAK" if zgodne else "NIE — SPRAWDZ GIT!")
    return 0 if (zlapane == len(MUTATIONS) and zgodne) else 1


if __name__ == "__main__":
    sys.exit(main())
