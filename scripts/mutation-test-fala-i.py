#!/usr/bin/env python3
"""Mutation test guardow Fala I — „Mój dzień" robi Hermes (deterministyczny), 2026-09-20.

Cel Fali 1: 2 tapniecia, 0 wpisywania. Kazda mutacja ponizej cofa DOKLADNIE jedna
naprawe i sprawdza, czy walidator to zlapie. Guard, ktory jest dekoracja, przepusci
mutacje — i wtedy wiemy, ze nie mamy zabezpieczenia, tylko komentarz.

Mutacje, ktore MUSZA byc zlapane (kazda to realny scenariusz awarii):

  I1  morning_brief wola model          -> werdykt o rytuale przestaje byc policzalny (G-04)
  I2  brief nie odroznia auto/confirmed -> raport przypisuje sobie prace Dowodcy
  I3  brak rozpoznania dnia odpoczynku  -> narzedzie karze za przerwe (F8)
  I4  /hermes/morning bez authorized()  -> dane o pracy Dowodcy publicznie
  I5  push-send znow liczy rytual sam    -> DWIE kopie reguly rozjezdzaja sie cicho
  I6  push-send nie wola morning_brief  -> powiadomienie 07:00 przestaje widziec rytual
  I7  brak mirroru offline              -> poranek umiera bez sieci (a to ma dzialac offline)
  I8  brak approveDay                   -> nie ma jak zatwierdzic poranka
  I9  hermesKawal bez wyjatku rest-day  -> kij za przerwe wraca do karty TERAZ
  I10 approveDay zapisuje 2 razy        -> rozjechany stan albo podwojny push
  I11 brak sladu audytu                 -> zielone jest anonimowe
  I12 formularz wraca na wierzch        -> 8-11 interakcji zamiast 2 tapniec

Jak w Fala E: restore jest BAJT W BAJT. `read_text` normalizuje CRLF→LF, a `write_text`
na Windows zamienia LF→CRLF — taki „niewinny" restore przestawilby DASHBOARD.html na
inne konce linii niz w repo.
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
    "vault": ROOT / "host" / "progress_vault.py",
    "push": ROOT / "scripts" / "push-send.py",
}

ORIG_BYTES = {k: p.read_bytes() for k, p in WATCHED.items()}
ORIG = {k: v.decode("utf-8").replace("\r\n", "\n") for k, v in ORIG_BYTES.items()}
HASHES = {k: hashlib.sha256(v).hexdigest() for k, v in ORIG_BYTES.items()}


def restore() -> None:
    for k, p in WATCHED.items():
        p.write_bytes(ORIG_BYTES[k])


def apply(muts: list[tuple[str, str, str]]) -> bool:
    for k, old, new in muts:
        if old not in ORIG[k]:
            return False
        WATCHED[k].write_bytes(ORIG[k].replace(old, new, 1).encode("utf-8"))
    return True


MUTATIONS = [
    (
        "I1 morning_brief wola model (werdykt przestaje byc policzalny)",
        "morning_brief wola model",
        [("vault", "def morning_brief(progress: Any, today_hint: Any = None) -> dict[str, Any]:",
          "def morning_brief(progress: Any, today_hint: Any = None) -> dict[str, Any]:\n    hermes_call_llm([], None)")],
    ),
    (
        "I1b dzien znow czytany z zegara wewnatrz briefu (kontener UTC vs timer hosta)",
        "brief czyta dzien z zegara",
        [("vault", "today, today_source = human_today(today_hint)",
          'today, today_source = time.strftime("%Y-%m-%d", time.gmtime()), "clock"')],
    ),
    (
        "I1c drugie miejsce czyta dzien z zegara (dwie prawdy o dniu)",
        "miejsca czytaja dzien z zegara",
        [("vault", "rest_day = bool(stale and day_untouched(scratch))",
          'rest_day = bool(stale and day_untouched(scratch))\n    _ = time.strftime("%Y-%m-%d", time.gmtime())')],
    ),
    (
        "I1d brief przestaje mowic, skad wziol dzien (rozjazd niemy)",
        "brief nie mowi, skad wziol dzien",
        [("vault", '        "today_source": today_source,\n', "")],
    ),
    (
        "I2 brief nie odroznia auto od confirmed (przywlaszcza prace Dowodcy)",
        "nie odroznia 'auto' od 'confirmed'",
        [("vault", 'if scratch.get("day_teraz"):', "if False:")],
    ),
    (
        "I3 brak rozpoznania dnia odpoczynku (narzedzie karze za przerwe)",
        "brak rozpoznania dnia odpoczynku",
        [("vault", "rest_day = bool(stale and day_untouched(scratch))", "rest_day = False")],
    ),
    (
        "I4 /hermes/morning bez authorized() (dane Dowodcy publicznie)",
        "/hermes/morning bez authorized()",
        [("vault",
          "            # NIE jest publiczny — to dane o pracy Dowódcy, nie komunikat serwisu.\n"
          "            if not authorized(self.headers):\n"
          "                self.send_response(HTTPStatus.UNAUTHORIZED)\n"
          "                self.end_headers()\n"
          "                return\n",
          "            # NIE jest publiczny — to dane o pracy Dowódcy, nie komunikat serwisu.\n")],
    ),
    (
        "I4b /hermes/morning ignoruje dzien od telefonu (zostaje zegar kontenera)",
        "ignoruje dzien od telefonu",
        [("vault", 'hint = (parse_qs(parsed.query).get("today") or [None])[0]', "hint = None")],
    ),
    (
        "I4c dashboard nie podaje swojego dnia (brief liczy wg zegara kontenera)",
        "dashboard nie podaje swojego dnia",
        [("dash", "/hermes/morning?today='+todayISO()", "/hermes/morning'")],
    ),
    (
        "I4d push 07:00 nie podaje dnia jawnie (inny dzien niz dashboard)",
        "push 07:00 nie podaje dnia jawnie",
        [("push", "day, source = human_today()", 'day, source = None, "clock"')],
    ),
    (
        "I5 push-send znow liczy rytual sam (dwie kopie reguly)",
        "push-send.py znow liczy rytual sam",
        [("push", "def build_payload(progress: dict[str, Any]) -> dict[str, str]:",
          'def build_payload(progress: dict[str, Any]) -> dict[str, str]:\n'
          '    _s = str((progress.get("_scratch") or {}).get("day_stamp") or "")')],
    ),
    (
        "I6 push-send nie wola morning_brief (powiadomienie slepnie na rytual)",
        "push-send.py nie wola morning_brief",
        [("push", "morning_brief_of(progress)", "{}")],
    ),
    (
        "I7 morningBriefLocal siega po siec (poranek umiera offline)",
        "morningBriefLocal siega po siec/model",
        [("dash", "function morningBriefLocal(){", "function morningBriefLocal(){fetch('/x');")],
    ),
    (
        "I8 brak mirroru offline (brak morningBriefLocal)",
        "brak mirror offline",
        [("dash", "function morningBriefLocal(", "function morningBriefLocalOff(")],
    ),
    (
        "I9 hermesKawal bez wyjatku rest-day (kij za przerwe wraca)",
        "hermesKawal pyta o LOCK bez wyjatku",
        [("dash", "if(lk.locked&&!dayUntouched()){return{tag:'DZIEŃ'", "if(lk.locked){return{tag:'DZIEŃ'")],
    ),
    (
        "I10 approveDay zapisuje dwa razy (rozjechany stan / podwojny push)",
        "approveDay zapisuje",
        [("dash", "  save();\n  var n=", "  save();\n  save();\n  var n=")],
    ),
    (
        "I11 brak sladu audytu (zielone staje sie anonimowe)",
        "brak sladu audytu",
        [("dash", "state.day_brief=", "state.day_briefOff=")],
    ),
    (
        "I12 formularz wraca na wierzch (8-11 interakcji zamiast 2)",
        "13 checkboxow nie jest schowanych",
        # Kotwica MUSI byc w `renderDay()`: samo `class="manual-ritual"` trafialo
        # najpierw w `<details>` briefu (zdefiniowany wyzej), wiec mutacja
        # odslaniala formularz... w zupelnie innym miejscu niz sprawdza guard.
        [("dash", '<details class="manual-ritual"><summary>Ręcznie — kroki rano',
          '<details class="manual-ritual-off"><summary>Ręcznie — kroki rano')],
    ),
    (
        "I13 counts obejmuje wieczor (przycisk obiecuje wiecej, niz robi)",
        "liczby poranka obejmuja wieczor",
        [("vault", '        "counts_evening": counts_evening,\n', "")],
    ),
    (
        "I13b brak evening_to_confirm (wieczor bez wlasnego zatwierdzenia)",
        "brak evening_to_confirm",
        [("vault", '        "evening_to_confirm": [c["id"] for c in evening_checks if c["status"] == "unknown"],\n', "")],
    ),
    (
        "I13c approved_by_human liczony po wszystkich krokach (audyt przypisuje wieczor)",
        "approved_by_human liczony po wszystkich krokach",
        [("vault", '[c["id"] for c in morning_checks if c["status"] == "unknown"]',
          '[c["id"] for c in checks if c["status"] == "unknown"]')],
    ),
    (
        "I13d mirror offline bez counts_evening (offline klamie inaczej niz online)",
        "mirror offline nie zwraca counts_evening",
        [("dash", "counts_evening:countsEvening,", "")],
    ),
    (
        "I14 approveEvening zapisuje dwa razy (tapniecie gubi sie albo dubluje zapis)",
        "approveEvening zapisuje",
        [("dash", "  var closed=closeDay();\n  save();", "  var closed=closeDay();\n  save();\n  save();")],
    ),
    (
        "I14b brak renderu wieczoru (wieczor zostaje w Recznie na zawsze)",
        "brak renderu wieczoru",
        [("dash", "function renderEveningBrief(", "function renderEveningBriefOff(")],
    ),
    (
        "I14c brak approveEvening (wieczoru nie da sie zatwierdzic)",
        "brak approveEvening",
        [("dash", "function approveEvening(", "function approveEveningOff(")],
    ),
    (
        "I14d brak sladu audytu wieczoru (zielone wieczorem anonimowe)",
        "brak sladu audytu wieczoru",
        [("dash", "state.day_evening_brief=", "state.day_evening_briefOff=")],
    ),
    (
        "I14e brak evening_verified_by_vault (audyt wieczoru nie wie, co policzyl vault)",
        "brak evening_verified_by_vault",
        [("vault", '        "evening_verified_by_vault": [c["id"] for c in evening_checks if c["status"] == "auto"],\n', "")],
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
