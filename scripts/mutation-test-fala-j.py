#!/usr/bin/env python3
"""Mutation test guardu Fala J: regula bez wyzwalacza jest martwa (2026-09-20).

ZMIERZONE przed tym guardem: CI `academy-gate` przechodzilo w 6 SEKUND. Uruchamialo
walidator i testy vaulta, ale ANI JEDNEGO testu mutacyjnego — czyli nie sprawdzalo
tego, co w tym repo jest najcenniejsze: czy guardy w ogole lapia regresje. Zielone CI
czytano jako "wszystko sprawdzone", a znaczylo "sprawdzilem dwie rzeczy z szesciu".
Ironia: sam plik workflow ostrzegal przed falszywa zielenia w `workflow-lab`.

Guard jest testem na TESCIE. Dlatego mutacje nie dotykaja kodu produktu, tylko:
  J1 cofniecie jednego zestawu z CI (bramka zielona, a tego nie mierzy)
  J2 usuniecie calego kroku mutacji z CI
  J3 NOWY zestaw w scripts/ poza CI — dowod, ze guard globuje, a nie trzyma listy
  J4 AGENTS.md gubi zestaw z linii `testy:` (konstytucja rozjezdza sie z CI)

J3 tworzy plik tymczasowy; restore() go kasuje, a test na koncu to weryfikuje.
Bajty, nie tekst — `read_text`/`write_text` na Windows przestawia LF→CRLF.
"""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
VAL = ROOT / "scripts" / "validate-academy-export.py"

WATCHED = {
    "ci": ROOT / ".github" / "workflows" / "academy-gate.yml",
    "agents": ROOT / "AGENTS.md",
}
PROBE = ROOT / "scripts" / "mutation-test-probe-j3.py"

ORIG_BYTES = {k: p.read_bytes() for k, p in WATCHED.items()}
ORIG = {k: v.decode("utf-8").replace("\r\n", "\n") for k, v in ORIG_BYTES.items()}
HASHES = {k: hashlib.sha256(v).hexdigest() for k, v in ORIG_BYTES.items()}


def restore() -> None:
    """Bajt w bajt — inaczej gubimy konce linii plikow .yml i .md."""
    for k, p in WATCHED.items():
        p.write_bytes(ORIG_BYTES[k])
    if PROBE.exists():
        PROBE.unlink()


def apply(muts, extra_files) -> bool:
    """Podmiany SEKWENCYJNIE + opcjonalne pliki tymczasowe.

    Zwraca False, gdy ktorys anchor nie istnieje (mutacja nienauzyta).
    """
    work = dict(ORIG)
    for k, old, new in muts:
        if old not in work[k]:
            return False
        work[k] = work[k].replace(old, new, 1)
    for rel, content in extra_files:
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    for k in {m[0] for m in muts}:
        WATCHED[k].write_bytes(work[k].encode("utf-8"))
    return True


# --- mutacje: (nazwa, oczekiwany fragment komunikatu, podmiany, pliki tymczasowe) ---

MUTATIONS = [
    (
        "J1 CI przestaje uruchamiac jeden zestaw (bramka zielona, a tego nie mierzy)",
        "nie uruchamia mutation-test-fala-i.py",
        [("ci", "          python scripts/mutation-test-fala-i.py\n", "")],
        [],
    ),
    (
        "J2 caly krok mutacji usuniety z CI (powrot do 6-sekundowej zieleni)",
        "nie uruchamia mutation-test-fala-0.py",
        [
            (
                "ci",
                "          python scripts/mutation-test-fala-0.py\n"
                "          python scripts/mutation-test-fala-d.py\n"
                "          python scripts/mutation-test-fala-e.py\n"
                "          python scripts/mutation-test-fala-i.py\n"
                "          python scripts/mutation-test-fala-j.py\n",
                "          echo pominięte\n",
            )
        ],
        [],
    ),
    (
        "J3 nowy zestaw poza CI — glob lapie, lista na sztywno przepuscilaby",
        "nie uruchamia mutation-test-probe-j3.py",
        [],
        [("scripts/mutation-test-probe-j3.py", '"""Prob: nowy zestaw, jeszcze nie w CI."""\n')],
    ),
    (
        "J4 AGENTS.md gubi zestaw z linii 'testy:' (konstytucja rozjezdza sie z CI)",
        "AGENTS.md 'testy:' nie wymienia mutation-test-fala-j.py",
        [("agents", " && python scripts/mutation-test-fala-j.py", "")],
        [],
    ),
]


def main() -> int:
    zlapane = 0
    przepuszczone: list[str] = []
    nieuzyte: list[str] = []
    try:
        for nazwa, oczekiwane, muts, extra in MUTATIONS:
            if not apply(muts, extra):
                nieuzyte.append(nazwa)
                print(f"  POMIN?        | {nazwa} | anchor nie znaleziony")
                restore()
                continue
            result = subprocess.run(
                [sys.executable, str(VAL)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            restore()
            ok = result.returncode != 0 and oczekiwane in (result.stdout or "")
            if ok:
                zlapane += 1
                print(f"  ZLAPANE       | {nazwa}")
            else:
                przepuszczone.append(nazwa)
                print(f"  PRZEPUSZCZONE | {nazwa} | oczekiwano: {oczekiwane}")
    finally:
        restore()

    zgodne = all(
        hashlib.sha256(p.read_bytes()).hexdigest() == HASHES[k] for k, p in WATCHED.items()
    )
    if PROBE.exists():
        zgodne = False
        print("UWAGA: plik probny J3 nie zostal usuniety:", PROBE)
    print()
    print(f"ZLAPANE: {zlapane}/{len(MUTATIONS)}   PRZEPUSZCZONE: {len(przepuszczone)}   NIENAUZYTE: {len(nieuzyte)}")
    print("PLIKI PRZYWRÓCONE:", "TAK" if zgodne else "NIE — SPRAWDZ GIT!")
    if przepuszczone:
        print("Przepuszczone mutacje:", ", ".join(przepuszczone))
    return 0 if (zlapane == len(MUTATIONS) and zgodne) else 1


if __name__ == "__main__":
    sys.exit(main())
