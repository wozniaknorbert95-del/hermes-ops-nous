#!/usr/bin/env python3
"""Mutation test guardow Fala K: Hermes zna wlasny produkt (2026-09-20).

ZMIERZONE na produkcji przed tym guardem (bateria 14 pytan, deepseek-flash):
  - przy LOCK model wysylal do ci.yml zamiast do zakladki DZIEN
  - mowil „zapytaj Dowodce", choc rozmowca JEST Dowodca
  - doklejal „nastepny ruch" do pytan nauczycielskich
  - „jak uzywac" opisywalo czat, nie Academie

Kazda mutacja cofa JEDNA naprawe. Guard dekoracja przepusci. Bajty, nie tekst.
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
    "vault": ROOT / "host" / "progress_vault.py",
    "dash": ROOT / "DASHBOARD.html",
    "eval": ROOT / "scripts" / "hermes-eval.py",
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
        "K1 usuniety PRIORYTET RUCHU z promptu (LOCK znow przegrywa z ci.yml)",
        "prompt bez kolejnosci LOCK > rytual > TERAZ",
        [("vault", "PRIORYTET RUCHU", "KOLEJNOSC MIEKKIA")],
    ),
    (
        "K2 prompt nie mowi, ze rozmowca JEST Dowodca",
        "prompt nie mowi, ze rozmowca JEST Dowodca",
        [("vault", "Rozmawiasz Z NIM", "Rozmawiasz O NIM")],
    ),
    (
        "K3 brak ochrony pytan nauczycielskich przed doklejaniem ruchu",
        "prompt nie chroni pytan nauczycielskich przed doklejaniem ruchu",
        [("vault", "NIE doklejaj", "mozna doklejac")],
    ),
    (
        "K4 'jak uzywac' znow opisuje czat, nie Academie",
        "prompt nie rozroznia 'jak uzywac' od 'jak mnie pytac'",
        [("vault", "instrukcja OBSŁUGI Akademii", "instrukcja rozmowy z Hermesem")],
    ),
    (
        "K5 digest bez etykiety PRIORYTET przy LOCK",
        "digest nie stawia etykiety PRIORYTET przy LOCK",
        [("vault", '"PRIORYTET",\n            "LOCK aktywny — jedyny ruch: zakładka DZIEŃ; NIE wysyłaj do rozdziału ani ci.yml",\n', '"info",\n            "jest blokada",\n')],
    ),
    (
        "K6 digest nie etykietuje day_missing jako listy zadan",
        "digest nie etykietuje day_missing jako listy zadan",
        [("vault", 'add("lista do odklikania (day_missing)", state.get("day_missing"))', 'add("braki", state.get("day_missing"))')],
    ),
    (
        "K7 digest nie oznacza kawalu kursu jako zawieszonego",
        "digest nie oznacza kawalu kursu jako zawieszonego",
        [("vault", 'add("kawał kursu (ZAWIESZONY do domknięcia DZIEŃ)", state.get("next"))', 'add("następny kawał", state.get("next"))')],
    ),
    (
        "K8 polecenie 'zaproponuj' wrocilo do pustego digesta",
        "polecenie 'zaproponuj' wrocilo do hermes_state_digest",
        [("vault", 'return "(stan pusty — kurs nierozpoczęty)"', 'return "(stan pusty — kurs nierozpoczęty; zaproponuj rozdział A1 z TERAZ)"')],
    ),
    (
        "K9 snapshot bez dayUntouched (LOCK = kazdy zalegly, takze odpoczynek)",
        "snapshot nie rozroznia LOCK aktywnego od dnia odpoczynku",
        [("dash", "lockActive=!!(lk.locked&&!dayUntouched())", "lockActive=!!lk.locked")],
    ),
    (
        "K10 bateria bez przypadku LOCK",
        "bateria bez przypadku LOCK",
        [("eval", '"id": "12_lock"', '"id": "12_removed"')],
    ),
    (
        "K11 bateria bez --digest-only",
        "bateria bez trybu --digest-only",
        [("eval", 'add_argument("--digest-only"', 'add_argument("--offline-check"')],
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
                if result.stdout:
                    print("    stdout:", (result.stdout or "")[:240].replace("\n", " | "))
    finally:
        restore()

    zgodne = all(
        hashlib.sha256(p.read_bytes()).hexdigest() == HASHES[k] for k, p in WATCHED.items()
    )
    print()
    print(f"ZLAPANE: {zlapane}/{len(MUTATIONS)}   PRZEPUSZCZONE: {len(przepuszczone)}   NIENAUZYTE: {len(nieuzyte)}")
    print("PLIKI PRZYWRÓCONE:", "TAK" if zgodne else "NIE — SPRAWDZ GIT!")
    if przepuszczone:
        print("Przepuszczone mutacje:", ", ".join(przepuszczone))
    return 0 if (zlapane == len(MUTATIONS) and zgodne) else 1


if __name__ == "__main__":
    sys.exit(main())
