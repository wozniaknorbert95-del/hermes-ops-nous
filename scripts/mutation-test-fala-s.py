#!/usr/bin/env python3
"""Mutation guards Fala S: Hermes conductor — WAITING-GO, jeden mózg, testy ze strumienia."""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
VAL = ROOT / "scripts" / "test_hermes_intent.py"

WATCHED = {
    "ops": ROOT / "OPS.html",
    "howto": ROOT / "docs" / "ops" / "HERMES-OPS-HOWTO.md",
    "contract": ROOT / "docs" / "ops" / "CONTRACT-OPS-STATUS.md",
    "vault": ROOT / "host" / "progress_vault.py",
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
        "S1 WAITING-GO zawsze widoczny",
        "hermes-conductor: WAITING-GO zawsze widoczny",
        [("ops", "cb.hidden=!!sessUrl;", "cb.hidden=false;")],
    ),
    (
        "S2 dwa mózgiki",
        "hermes-conductor: dwa różne modele w conductora",
        [("ops", "conductor", "deepseek")],
    ),
    (
        "S3 brak WAITING-GO w howto",
        "hermes-conductor: howto nie wspomina WAITING-GO",
        [("howto", "WAITING-GO", "GOTOWE")],
    ),
    (
        "S4 contract zakazuje drugiego S2",
        "hermes-conductor: contract nie zakazuje drugiego S2",
        [("contract", "drugi S2", "S2")],
    ),
    (
        "S5 vault woła Cursor API",
        "hermes-conductor: vault woła Cursor API (drugi S2)",
        [("vault", "cursor", "api")],
    ),
    (
        "S6 Live ukrywa UNKNOWN testów",
        "hermes-conductor: Live nie pokazuje UNKNOWN testów",
        [("ops", "UNKNOWN", "HIDDEN")],
    ),
    (
        "S7 Live ukrywa UNKNOWN testów",
        "hermes-conductor: Live nie pokazuje UNKNOWN testów",
        [("ops", "unknown", "hidden")],
    ),
    (
        "S8 karta Engineer bez banera",
        "hermes-conductor: karta Engineer bez banera WAITING-GO",
        [("ops", 'id="engineer-waiting-go"', 'id="engineer-ready"')],
    ),
    (
        "S9 dispatch running bez run_url",
        "hermes-conductor: derive_dispatch running bez run_url",
        [("vault", "session_url = _safe_url", "session_url = str")],
    ),
    (
        "S10 chip work_mode bez persistencji",
        "ops-steer: brak persistencji work_mode (localStorage)",
        [("ops", "ops-work-mode", "ops-work-gone")],
    ),
    (
        "S11 STOPPED znowu czerwone",
        "ops-steer: STOPPED znowu czerwone jak FAIL",
        [
            (
                "ops",
                "if(u==='PAUSED'||u==='STALLED'||u==='STOPPED')return 'warn';",
                "if(u==='PAUSED'||u==='STALLED')return 'warn';",
            )
        ],
    ),
    (
        "S12 paint FAIL nad Pause",
        "ops-steer: paint() FAIL wygrywa nad PAUSED/STOPPED",
        [("ops", "operator-halt-wins-fail", "operator-halt-gone")],
    ),
    (
        "S13 WAITING-GO chowa się na zdrowym ticku",
        "ops-steer: WAITING-GO chowa się gdy health OK",
        [("ops", "cb.hidden=!!sessUrl;", "cb.hidden=!banner.hidden;")],
    ),
    (
        "S14 Live bez local_remaining",
        "ops-steer: Live bez local_remaining z conductora",
        [("ops", "local_remaining", "local_pending")],
    ),
    (
        "S15 Retry zawsze widoczny",
        "ops-steer: Retry znowu zawsze widoczny (trup)",
        [("ops", "retry-not-corpse", "retry-always-on")],
    ),
    (
        "S16 Live przy leftover PAUSED",
        "ops-steer: Live znowu przy PAUSED leftover",
        [("ops", "live-eyebrow-not-fake", "live-eyebrow-always")],
    ),
    (
        "S17 banner JSON na static 404",
        "ops-steer: banner JSON znowu na static 404",
        [("ops", "json-banner-not-static", "json-banner-always")],
    ),
    (
        "S18 Retry chowa się po FAIL+PAUSED",
        "ops-hud: Retry znowu chowa się po FAIL+PAUSED",
        [("ops", "retry-on-fail-paused", "retry-paused-hides")],
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
                print(f"  POMINIETE   | {nazwa} | anchor nie znaleziony")
                restore()
                continue
            result = subprocess.run(
                [sys.executable, str(VAL)],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            restore()
            if result.returncode == 0:
                przepuszczone.append(nazwa)
                print(f"  PRZEPUSZCZONE | {nazwa} | oczekiwano: {oczekiwane}")
            else:
                zlapane += 1
                print(f"  ZLAPANE     | {nazwa}")
    finally:
        restore()
    print()
    print(f"ZLAPANE: {zlapane}/{len(MUTATIONS)}   PRZEPUSZCZONE: {len(przepuszczone)}   NIENAUZYTE: {len(nieuzyte)}")
    print("PLIKI PRZYWROCONE: TAK")
    return 0 if zlapane == len(MUTATIONS) else 1


if __name__ == "__main__":
    sys.exit(main())
