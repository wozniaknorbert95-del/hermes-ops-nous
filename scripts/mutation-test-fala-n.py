#!/usr/bin/env python3
"""Mutation guards Fala N: QUI-70 — koniec fałszywego RUNNING / dispatch /diag."""
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
    "ops": ROOT / "OPS.html",
    "contract": ROOT / "docs" / "ops" / "CONTRACT-OPS-STATUS.md",
    "runbook": ROOT / "docs" / "ops" / "RUNBOOK-OPS-WIRING.md",
}

ORIG_BYTES = {k: p.read_bytes() for k, p in WATCHED.items()}
ORIG = {k: v.decode("utf-8").replace("\r\n", "\n") for k, v in ORIG_BYTES.items()}


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
        "N1 brak derive_dispatch",
        "ops-qui70: brak derive_dispatch",
        [("vault", "def derive_dispatch(", "def derive_dispatch_gone(")],
    ),
    (
        "N2 brak /ops/diag",
        "ops-qui70: brak GET /ops/diag",
        [("vault", 'parsed.path == "/ops/diag"', 'parsed.path == "/ops/diag-gone"')],
    ),
    (
        "N3 start bump_updated wraca (fałszywy wiek ticka)",
        "ops-qui70: start musi patchować status bez bump_updated",
        [("vault", "bump_updated=False,", "bump_updated=True,")],
    ),
    (
        "N3b default bump_updated wraca na True (Pause fałszuje tick)",
        "ops-qui70: patch_ops_status default bump_updated musi być False (I1)",
        [("vault", "bump_updated: bool = False", "bump_updated: bool = True")],
    ),
    (
        "N4 brak dispatch-banner",
        "ops-qui70: brak #dispatch-banner",
        [("ops", 'id="dispatch-banner"', 'id="dispatch-gone"')],
    ),
    (
            "N5 brak copy STALLED",
            "ops-qui70: brak copy STALLED",
            [
                ("ops", "STALLED — tick nie odpowiada", "WARN — tick nie odpowiada"),
                ("ops", "STALLED — tick nie odpowiada", "WARN — tick nie odpowiada"),
            ],
        ),
    (
        "N6 send() bez optymistycznego QUEUED",
        "ops-qui70: send() musi optymistycznie stawiać QUEUED",
        [("ops", "lastStatus.status='QUEUED'", "lastStatus.status='RUNNING'")],
    ),
    (
        "N7 brak CONTRACT-OPS-STATUS",
        "ops-qui70: brak CONTRACT-OPS-STATUS.md",
        [("contract", "**Fail-closed:**", "**Soft-open:**")],
    ),
    (
        "N8 brak RUNBOOK",
        "ops-qui70: brak RUNBOOK-OPS-WIRING.md",
        [("runbook", "systemctl is-active hermes-ops.timer", "systemctl is-active hermes-ops.GONE")],
    ),
    (
        "N9 brak utf-8-sig (BOM łamie cache)",
        "ops-qui70: odczyt ops JSON musi znosić BOM",
        [("vault", 'encoding="utf-8-sig"', 'encoding="utf-8"')],
    ),
    (
        "N10 main bez ensure_ops_cmd_file",
        "ops-qui70: main() musi wołać ensure_ops_cmd_file()",
        [("vault", "    ensure_ops_cmd_file()\n    server = ThreadingHTTPServer", "    pass  # no-ensure\n    server = ThreadingHTTPServer")],
    ),
    (
        "N11 health bez ops_cmd_state",
        "ops-qui70: /health musi raportować ops_cmd_state",
        [("vault", '"ops_cmd_state": ops_cmd_path_state()', '"ops_cmd_gone": ops_cmd_path_state()')],
    ),
    (
        "N12 diag nie rozróżnia idle od STALLED",
        "ops-qui70: /ops/diag musi rozróżniać idle od STALLED",
        [("vault", "Brak komendy — idle", "Brak komendy — stalled-ish")],
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
                print(f"  POMINIĘTE     | {nazwa} | anchor nie znaleziony")
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
        # integrity: watched files restored
        for k, p in WATCHED.items():
            if hashlib.sha256(p.read_bytes()).hexdigest() != hashlib.sha256(ORIG_BYTES[k]).hexdigest():
                print(f"FAIL: plik {k} nie przywrócony")
                return 1
        print(f"\nZLAPANE: {zlapane}/{len(MUTATIONS)}   PRZEPUSZCZONE: {len(przepuszczone)}   NIENAUZYTE: {len(nieuzyte)}")
        print("PLIKI PRZYWRÓCONE: TAK")
        if przepuszczone or nieuzyte or zlapane != len(MUTATIONS):
            return 1
        return 0
    finally:
        restore()


if __name__ == "__main__":
    sys.exit(main())
