#!/usr/bin/env python3
"""Mutation test guardow Fala D (test uzytkownika 2026-09-20).

Kazda mutacja cofa JEDNA naprawę z DASHBOARD.html. Guard, ktory jest dekoracja,
przepusci mutacje — i taki guard nie jest dowodem, tylko ozdoba.
Skrypt zawsze przywraca oryginal (try/finally), a na koncu to sprawdza.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
DASH = ROOT / "DASHBOARD.html"
VAL = ROOT / "scripts" / "validate-academy-export.py"

# Bajt w bajt (2026-09-21): `read_text` normalizuje CRLF→LF, a `write_text` na Windows
# zamienia LF→CRLF — czyli restore potrafil zmienic konce linii pliku. Tutaj dotyczy to
# tylko DASHBOARD.html (nie .sh), ale ten sam blad w mutation-test-fala-e.py przestawial
# setup-akademia-vps.sh na CRLF i wywalal deploy na VPS. Trzymamy sie jednej, bezpiecznej reguly.
ORIG_BYTES = DASH.read_bytes()
ORIG = ORIG_BYTES.decode("utf-8").replace("\r\n", "\n")


def restore() -> None:
    DASH.write_bytes(ORIG_BYTES)


def _swap(h: str, old: str, new: str) -> str:
    if old not in h:
        return h
    return h.replace(old, new, 1)


def m_no_align(h: str) -> str:
    return _swap(h, "alignPanelToNav();}", "}")


def m_scroll_top(h: str) -> str:
    return _swap(h, "alignPanelToNav();}", "window.scrollTo({top:0,behavior:'auto'});}")


def m_msg_no_toast(h: str) -> str:
    return _swap(h, "}toast(text,ok);}", "}}")


def m_nextlab_renamed(h: str) -> str:
    return _swap(h, "function nextLabIdx(", "function nextLabIdxOff(")


def m_nowcard_ignores_idx(h: str) -> str:
    return _swap(h, "var ni=nextLabIdx(fo);ntask.textContent", "var ni=0;ntask.textContent")


def m_no_afterdata(h: str) -> str:
    return _swap(h, "function afterDataChange(key){checkRitualBanners();renderNowCard();", "function afterDataChange(key){checkRitualBanners();")


def m_no_next_chapter(h: str) -> str:
    return _swap(h, "var nx=firstOpen();var el=nx?", "var nx=null;var el=nx?")


def m_wrong_scroll_target(h: str) -> str:
    return _swap(h, "gentleScroll(document.getElementById('roz-'+rid));return;}", "gentleScroll(b.closest('.box'));return;}")


def m_no_secret_refusal(h: str) -> str:
    return _swap(h, "Nie podam — i nie mam czego podać.", "Nie wypowiadam sie.")


def m_secret_after_export(h: str) -> str:
    start = h.find("    /* Próba wyciągnięcia sekretu")
    end = h.find("    if(/instalac|", start)
    if start < 0 or end < 0:
        return h
    block = h[start:end]
    rest = h[:start] + h[end:]
    marker = "refs:refs([{label:'eksport w zakładce TERAZ',href:'#tabs'}])};\n    }"
    i = rest.find(marker)
    if i < 0:
        return h
    i += len(marker)
    return rest[:i] + "\n" + block.rstrip("\n") + rest[i:]


def m_no_potrafisz(h: str) -> str:
    return _swap(h, "if(/co potrafisz|co umiesz", "if(true||/co potrafisz|co umiesz")


def m_potrafisz_after_uzywac(h: str) -> str:
    a = h.find("if(/co potrafisz")
    b = h.find("if(/jak u", a)
    if a < 0 or b < 0:
        return h
    block = h[a:b]
    rest = h[:a] + h[b:]
    jak = rest.find("if(/jak u")
    marker = "refs:refs([{label:'TERAZ',href:'#tabs'}])};\n    }"
    i = rest.find(marker, jak)
    if i < 0:
        return h
    i += len(marker)
    return rest[:i] + "\n" + block.rstrip("\n") + rest[i:]


def m_no_fuzzy(h: str) -> str:
    return _swap(h, "function hermesFuzzyHit(", "function hermesFuzzyHitOff(")


def m_fuzzy_unused(h: str) -> str:
    # Router i silnik lokalny muszą oba tracić fuzzy — inaczej mutacja trafia tylko w intent.
    return h.replace("||hermesFuzzyHit(question,g.keys[j])", "")


def m_bad_polish(h: str) -> str:
    return _swap(h, "jest domknięty na zielono", "jest zgrane na zielono")


def m_truncate_missing(h: str) -> str:
    return _swap(h, "dayMissing().slice(0,4)", "dayMissing().slice(0,3)")


def m_no_welcome_jump(h: str) -> str:
    return _swap(h, '<button class="btn" type="button" data-go-tab="now">', '<button class="btn" type="button" data-go-tab-off="now">')


GO_TAB_BIND = "querySelectorAll('[data-go-tab]').forEach(function(b){if(b.dataset.bound)return;b.dataset.bound='1';b.addEventListener('click',function(){activateTab(b.dataset.goTab,false);});});"


def _kill_binding_in_block(h: str, fn_marker: str) -> str:
    """Usuwa podpiecie data-go-tab z funkcji wskazanej po nazwie (nie z pierwszej w pliku).
    Funkcja moze zajmowac kilka linii, dlatego tniemy blok, nie linie."""
    start = h.find(fn_marker)
    if start < 0:
        return h
    end = h.find("\nfunction ", start + len(fn_marker))
    block = h[start:end] if end > start else h[start:]
    if GO_TAB_BIND not in block:
        return h
    return h[:start] + block.replace(GO_TAB_BIND, "void 0;", 1) + (h[end:] if end > start else "")


def m_welcome_jump_dead(h: str) -> str:
    return _kill_binding_in_block(h, "function bindInstall(")


def m_panel_jump_dead(h: str) -> str:
    return _kill_binding_in_block(h, "function bindDayExtras(")


MUTATIONS = [
    ("D1 activateTab bez alignPanelToNav", "nie wola alignPanelToNav", m_no_align),
    ("D1b activateTab przewija na gore", "przewija na gore strony", m_scroll_top),
    ("D2 msg() bez toastu", "msg() nie pokazuje toastu", m_msg_no_toast),
    ("D3 brak nextLabIdx", "brak nextLabIdx", m_nextlab_renamed),
    ("D3b karta TERAZ ignoruje otwarty krok", "nie uzywa nextLabIdx", m_nowcard_ignores_idx),
    ("D4 afterDataChange bez odswiezenia karty", "afterDataChange nie odswieza", m_no_afterdata),
    ("D5 po zaliczeniu brak nastepnego rozdzialu", "brak przejscia do nastepnego rozdzialu", m_no_next_chapter),
    ("D5b blad labu prowadzi w zle miejsce", "nie prowadzi do wlasciwego rozdzialu", m_wrong_scroll_target),
    ("D6 brak odmowy sekretu", "nie odmawia wprost", m_no_secret_refusal),
    ("D6b odmowa sekretu za galezia eksportu", "odmowa sekretu jest ZA galezia eksportu", m_secret_after_export),
    ("D7 brak galezi 'co potrafisz'", "brak osobnej galezi 'co potrafisz'", m_no_potrafisz),
    ("D7b 'co potrafisz' za 'jak uzywac'", "jest za 'jak uzywac'", m_potrafisz_after_uzywac),
    ("D8 brak tolerancji literowek", "brak tolerancji literowek", m_no_fuzzy),
    ("D8b tolerancja nieuzywana", "nie jest uzyta w dopasowaniu", m_fuzzy_unused),
    ("D9 zepsuta polszczyzna", "zepsuta polszczyzna", m_bad_polish),
    ("D10 ucieta lista brakow", "ucina liste brakow", m_truncate_missing),
    ("D11 brak przejscia do TERAZ z karty powitalnej", "nie ma przejscia do TERAZ", m_no_welcome_jump),
    ("D11b przycisk w karcie powitalnej jest martwy", "bindInstall nie podpina data-go-tab", m_welcome_jump_dead),
    ("D11c przyciski 'Dokoncz DZIEN' i 'Pelny czat' sa martwe", "bindDayExtras nie podpina data-go-tab", m_panel_jump_dead),
]


def main() -> int:
    zlapane = 0
    przepuszczone: list[str] = []
    nieuzyte: list[str] = []
    try:
        for nazwa, oczekiwane, fn in MUTATIONS:
            zmutowany = fn(ORIG)
            if zmutowany == ORIG:
                nieuzyte.append(nazwa)
                print(f"  POMIN?   | {nazwa} | mutacja nie zmienila pliku")
                continue
            DASH.write_bytes(zmutowany.encode("utf-8"))
            result = subprocess.run(
                [sys.executable, str(VAL)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            restore()
            ok = result.returncode != 0 and oczekiwane in (result.stdout or "")
            if ok:
                zlapane += 1
                print(f"  ZLAPANE  | {nazwa}")
            else:
                przepuszczone.append(nazwa)
                print(f"  PRZEPUSZCZONE | {nazwa} | oczekiwano: {oczekiwane}")
    finally:
        restore()

    zgodne = DASH.read_bytes() == ORIG_BYTES
    print()
    print(f"ZLAPANE: {zlapane}/{len(MUTATIONS)}   PRZEPUSZCZONE: {len(przepuszczone)}   NIENAUZYTE: {len(nieuzyte)}")
    print("PLIK PRZYWRÓCONY:", "TAK" if zgodne else "NIE — SPRAWDZ GIT!")
    if przepuszczone:
        print("Przepuszczone mutacje:", ", ".join(przepuszczone))
    return 0 if (zlapane == len(MUTATIONS) and zgodne) else 1


if __name__ == "__main__":
    sys.exit(main())
