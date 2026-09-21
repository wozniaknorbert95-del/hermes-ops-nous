#!/usr/bin/env python3
"""Mutation test guardow Fala 0 (kanal poranny + integralnosc deployu, 2026-09-20).

Trzy ciche awarie znalezione przy audycie:
  A1 powiadomienie 07:00 gubilo zakladke — `client.focus()` AKTYWUJE okno i nie
     ustawia hasha, wiec `hashchange` nie poleci i openHashTarget() sie nie uruchomi
  A2 `#day` to ID ZAKLADKI, a `getElementById('day')` zwraca null — push byl martwy
     nawet przy zimnym starcie (dwie niezalezne awarie nalozone na siebie)
  A3 `main` bez ochrony i 0 workflow: deploy pakuje WORKING COPY, wiec na produkcje
     mogl trafic kod spoza main (PR #17 byl OTWARTY, a jego 6 commitow zylo na VPS)
  A5 raz zapisany zly `active_tab` w localStorage zostawal NA ZAWSZE — panel pusty
     i zadna zakladka nieaktywna, bez wyjscia poza reczna naprawe localStorage

Kazda mutacja cofa JEDNA naprawe. Guard, ktory jest dekoracja, przepusci mutacje.
Skrypt zawsze przywraca oryginaly (try/finally) i na koncu to weryfikuje po hashu.
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
    "dash": ROOT / "DASHBOARD.html",
    "sw": ROOT / "sw.js",
    "deploy": ROOT / "scripts" / "deploy-akademia-vps.sh",
    "ci": ROOT / ".github" / "workflows" / "academy-gate.yml",
}

ORIG_BYTES = {k: p.read_bytes() for k, p in WATCHED.items()}
ORIG = {k: v.decode("utf-8").replace("\r\n", "\n") for k, v in ORIG_BYTES.items()}
HASHES = {k: hashlib.sha256(v).hexdigest() for k, v in ORIG_BYTES.items()}


def restore() -> None:
    """Bajt w bajt — inaczej gubimy konce linii plikow .sh."""
    for k, p in WATCHED.items():
        p.write_bytes(ORIG_BYTES[k])


def apply(muts: list[tuple[str, str, str]]) -> bool:
    """Podmiany SEKWENCYJNIE na kopii roboczej (ta sama nazwa klucza = kilka zmian).

    Zwraca False, gdy ktorys anchor nie istnieje (mutacja nienauzyta).
    """
    work = dict(ORIG)
    for k, old, new in muts:
        if old not in work[k]:
            return False
        work[k] = work[k].replace(old, new, 1)
    for k in {m[0] for m in muts}:
        WATCHED[k].write_bytes(work[k].encode("utf-8"))
    return True


# --- mutacje: (nazwa, oczekiwany fragment komunikatu, podmiany) --------------

MUTATIONS = [
    (
        "A1 powrot do client.focus() bez nawigacji (push gubi zakladke)",
        "notificationclick bez client.navigate",
        [("sw", "client.navigate(target)", "client.focus()")],
    ),
    (
        "A1b usuniety openWindow (zimny start nie otworzy celu)",
        "zimny start nie otworzy celu",
        [("sw", "if (self.clients.openWindow) return self.clients.openWindow(target);\n", "")],
    ),
    (
        "A2b openHashTarget ufa fallbackowi tabDef (smieciowy hash psuje panel)",
        "ufa fallbackowi tabDef",
        [("dash", "if(t0&&t0.id===id){", "if(t0){")],
    ),
    (
        "A2 openHashTarget bez rozpoznawania ID zakladek (#day martwy)",
        "nie zna ID zakladek",
        [("dash", "if(!el){var t0=tabDef(id);if(t0&&t0.id===id){if(id!==currentTab()){state.active_tab=id;renderAll();alignPanelToNav();}return;}}", "")],
    ),
    (
        "A3 piata zakladka (swiadome 4: TERAZ+KURS+NOTATKI+DZIEN)",
        "zakladek zamiast 4",
        [("dash", "ACADEMY_TABS=[{id:'now'", "ACADEMY_TABS=[{id:'extra',title:'EXTRA',accent:'#888',desc:'x'},{id:'now'")],
    ),
    (
        "A4 deploy bez bramki integralnosci (kod spoza main na produkcje)",
        "brak bramki integralnosci",
        [("deploy", 'MAIN_SHA="$(git -C "${SRC}" rev-parse origin/main 2>/dev/null || echo brak)"', 'MAIN_SHA="${HEAD_SHA}"')],
    ),
    (
        "A4c bramka bez fail-closed (poza repo git przechodzi MILCZACO)",
        "bez fail-closed",
        [("deploy", 'if ! git -C "${SRC}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then', 'if false; then')],
    ),
    (
        "A4b bramka integralnosci bez obejscia --force (zablokuje awaryjny deploy)",
        "bez swiadomego obejscia --force",
        [
            ("deploy", "    --force) FORCE=1 ;;\n", ""),
        ],
    ),
    (
        "A5 load() bez odsiewania zlego active_tab (zatruty stan = pusty panel na zawsze)",
        "nie odsiewa nieprawidlowego active_tab",
        [
            ("dash", "if(state.active_tab&&!ACADEMY_TABS.some(function(t){return t.id===state.active_tab;}))state.active_tab='now';", ""),
        ],
    ),
    (
        "A5b currentTab() ufa stanowi bez walidacji (nieznana zakladka renderuje pustke)",
        "ufa stanowi bez walidacji",
        [
            ("dash", "function currentTab(){var t=state.active_tab;if(t&&tabDef(t).id===t)return t;return 'now';}", "function currentTab(){return state.active_tab||'now';}"),
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
    print()
    print(f"ZLAPANE: {zlapane}/{len(MUTATIONS)}   PRZEPUSZCZONE: {len(przepuszczone)}   NIENAUZYTE: {len(nieuzyte)}")
    print("PLIKI PRZYWRÓCONE:", "TAK" if zgodne else "NIE — SPRAWDZ GIT!")
    if przepuszczone:
        print("Przepuszczone mutacje:", ", ".join(przepuszczone))
    return 0 if (zlapane == len(MUTATIONS) and zgodne) else 1


if __name__ == "__main__":
    sys.exit(main())
