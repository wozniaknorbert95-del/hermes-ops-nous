#!/usr/bin/env python3
"""Mutation guards Fala Q: HUD /ops — chipy, 360px, kolejka ≠ Run, P0 href, P1–P3 IA."""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
VAL = ROOT / "scripts" / "validate-academy-export.py"

WATCHED = {"ops": ROOT / "OPS.html"}

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
        "Q1 zabrano chip DoR",
        "brak chipów DoR",
        [("ops", 'id="chip-dor"', 'id="chip-gone"')],
    ),
    (
        "Q2 Tokens/Cost wracają",
        "Tokens/Cost wróciły",
        [("ops", 'id="t-waiting"', 'id="t-tokens"')],
    ),
    (
        "Q3 fold 360px zniknął",
        "brak foldu 360px",
        [("ops", "@media (max-width:360px)", "@media (max-width:361px)")],
    ),
    (
        "Q4 kolejka udaje Run",
        "kolejka znowu udaje Run",
        [("ops", "Kolejka nie udaje Run — otwiera Linear.", "Kolejka startuje Run — otwiera Linear.")],
    ),
    (
        "Q5 kolejka nie jest linkiem",
        "kolejka issue nie jest linkiem",
        [("ops", '<a class="issue"', '<button class="issue"')],
    ),
    (
        "Q6 brak Użyj tego",
        "brak Użyj tego",
        [("ops", 'id="btn-use-rec"', 'id="btn-use-gone"')],
    ),
    (
        "Q7 martwy panel-steer wrócił",
        "martwy #panel-steer",
        [("ops", "<main>", '<main>\n  <section class="panel" id="panel-steer" hidden></section>')],
    ),
    (
        "Q8 dispatch klonuje Retry",
        "dispatch klonuje przyciski",
        [("ops", "var hint='';", 'var hint=\'<div class="act"><button type="button" class="btn ghost">↻</button></div>\';')],
    ),
    (
        "Q9 Take over bez confirm",
        "Take over bez confirm",
        [("ops", "if(!window.confirm('Take over = laptop, zero @cursor. Na pewno?'))return;", "")],
    ),
    (
        "Q10 brak skip-link",
        "brak skip-link do #panel-live",
        [("ops", 'href="#panel-live"', 'href="#gone-live"')],
    ),
    (
        "Q11 collapse bez localStorage",
        "collapse KONTEKST/DZIENNIK bez localStorage",
        [("ops", "ops-fold-", "ops-gone-")],
    ),
    (
        "Q12 brak Enter=Start",
        "brak skrótu Enter=Start",
        [("ops", "e.key==='Enter'", "e.key==='EnterX'")],
    ),
    (
        "Q13 Take over full-bleed",
        "Take over znowu full-bleed",
        [("ops", ".btn.danger{background:rgba(251,113,133,.18);color:#fecdd3;border:1px solid rgba(251,113,133,.4)}", ".btn.danger{background:rgba(251,113,133,.18);color:#fecdd3;border:1px solid rgba(251,113,133,.4);width:100%}")],
    ),
    (
        "Q14 sticky HUD połyka next-card",
        "sticky HUD połyka #next-card",
        [("ops", '<header class="hud" id="hud-chrome">', '<header class="hud" id="hud-chrome"><div id="next-card">')],
    ),
    (
        "Q15 kolejka za Wynikiem",
        "kolejka za Wynikiem",
        [("ops", 'id="panel-queue"', 'id="panel-queue-late"')],
    ),
    (
        "Q16 slot ghost PAUSED blokuje Start",
        "ops-slot: Start zablokowany ghost",
        [("ops", "ok:!slotOccupying(s)", "ok:agents.length===0")],
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
