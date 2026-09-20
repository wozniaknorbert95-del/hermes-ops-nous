#!/usr/bin/env python3
"""Mutation test guardow Fala E (podlaczenie modelu deepseek-flash, 2026-09-21).

Trzy ciche awarie, ktore bolą dopiero z prawdziwym modelem:
  E1 docker-compose nie przekazuje zmiennych → kod czyta, kontener nie ma
  E2 budzet tokenow za maly na model ROZUMUJACY → pusty content przy trudnym pytaniu
  E3 vault czeka dluzej niz klient → klient przerywa pierwszy i pali tokeny
  E4-E7 sekret w repo / w logach / w publicznym probe

Kazda mutacja cofa JEDNA naprawe. Guard, ktory jest dekoracja, przepusci mutacje.
Skrypt zawsze przywraca oryginaly (try/finally) i na koncu to weryfikuje po hashu.
"""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
VAL = ROOT / "scripts" / "validate-academy-export.py"

# Pliki dotkniete przez Fala E — mutacje siegaja wiecej niz DASHBOARD.html.
WATCHED = {
    "dash": ROOT / "DASHBOARD.html",
    "compose": ROOT / "host" / "docker-compose.yml",
    "vault": ROOT / "host" / "progress_vault.py",
    "env": ROOT / "host" / "env.example",
    "setup": ROOT / "scripts" / "setup-akademia-vps.sh",
    "deploy": ROOT / "scripts" / "deploy-akademia-vps.sh",
}

# UWAGA (2026-09-21): restore MUSI byc bajt w bajt.
# `read_text` normalizuje CRLF→LF, a `write_text` na Windows zamienia LF→CRLF.
# Ten skrypt dotyka plikow *.sh, ktore .gitattributes wymusza na LF, a deploy taruje
# WORKING COPY — czyli taki "niewinny" restore przestawial setup-akademia-vps.sh na CRLF
# i deploy padal na VPS (bash: syntax error near `$'{\r''). Dlatego: bajty, nie tekst.
# Do dopasowania anchorow uzywamy wersji znormalizowanej do LF (w pamieci).
ORIG_BYTES = {k: p.read_bytes() for k, p in WATCHED.items()}
ORIG = {k: v.decode("utf-8").replace("\r\n", "\n") for k, v in ORIG_BYTES.items()}
HASHES = {k: hashlib.sha256(v).hexdigest() for k, v in ORIG_BYTES.items()}

# Celowo UDAWANY klucz do testu guardu E7 — skladany w runtime, zeby jego literał
# nie pasowal do wzorca skanerow sekretow (gitleaks/GitHub secret scanning).
# Wartosc w pamieci nadal pasuje do wzorca `sk-[0-9a-f]{20,}`, wiec mutacja E7 dziala.
FAKE_KEY = "sk-" + "0123456789abcdef" * 2


def restore() -> None:
    """Bajt w bajt — inaczej gubimy konce linii plikow .sh."""
    for k, p in WATCHED.items():
        p.write_bytes(ORIG_BYTES[k])


def apply(muts: list[tuple[str, str, str]]) -> bool:
    """Zwraca False, gdy ktorys anchor nie istnieje (mutacja nienauzyta)."""
    for k, old, new in muts:
        if old not in ORIG[k]:
            return False
        WATCHED[k].write_bytes(ORIG[k].replace(old, new, 1).encode("utf-8"))
    return True


# --- mutacje: (nazwa, oczekiwany fragment komunikatu, podmiany) --------------

MUTATIONS = [
    (
        "E1 compose nie przekazuje BASE_URL (klucz w .env bez efektu)",
        "docker-compose nie przekazuje ACADEMY_HERMES_BASE_URL",
        [("compose", "      ACADEMY_HERMES_BASE_URL: ${ACADEMY_HERMES_BASE_URL:-}\n", "")],
    ),
    (
        "E1b compose nie przekazuje API_KEY",
        "docker-compose nie przekazuje ACADEMY_HERMES_API_KEY",
        [("compose", "      ACADEMY_HERMES_API_KEY: ${ACADEMY_HERMES_API_KEY:-}\n", "")],
    ),
    (
        "E2 budzet tokenow wraca do 700 (za malo na reasoning)",
        "za malo dla modelu rozumujacego",
        [("vault", 'ACADEMY_HERMES_MAX_TOKENS", "2500"', 'ACADEMY_HERMES_MAX_TOKENS", "700"')],
    ),
    (
        "E3 timeout vaulta 45 s (dluzszy niz watchdog klienta)",
        "timeout vaulta",
        [("vault", 'ACADEMY_HERMES_TIMEOUT", "20"', 'ACADEMY_HERMES_TIMEOUT", "45"')],
    ),
    (
        "E3b watchdog klienta 20 s (krotszy niz timeout vaulta)",
        "watchdog klienta",
        [("dash", "},25000);}", "},20000);}")],
    ),
    (
        "E4 env.example z wpisanym kluczem (sekret w repo)",
        "env.example ma niepusty",
        [("env", "ACADEMY_HERMES_API_KEY=\n", f"ACADEMY_HERMES_API_KEY={FAKE_KEY}\n")],
    ),
    (
        "E5 setup nie dopisuje ACADEMY_HERMES_MODEL",
        "nie wywoluje ensure_env_key ACADEMY_HERMES_MODEL",
        [("setup", "ensure_env_key ACADEMY_HERMES_MODEL\n", "")],
    ),
    (
        "E5b ensure_env_key nadpisuje istniejaca wartosc (klucz nie przezyje deployu)",
        "ensure_env_key nadpisuje",
        [("setup", 'if ! grep -qE "^$1=" "${TARGET}/.env"; then', "if true; then")],
    ),
    (
        "E5c setup wypisuje klucz do logow deployu",
        "setup wypisuje ACADEMY_HERMES_API_KEY",
        [("setup", "echo \"OK: akademia vault running", "echo \"klucz=${ACADEMY_HERMES_API_KEY}\"\necho \"OK: akademia vault running")],
    ),
    (
        "E6 /hermes/status zdradza klucz (publiczny probe)",
        "/hermes/status zwraca HERMES_API_KEY",
        [("vault", '"used_today": hermes_usage_today(),', '"used_today": hermes_usage_today(), "key": HERMES_API_KEY,')],
    ),
    (
        "E7 realny klucz API w repo",
        "realny klucz API w repo",
        [("dash", "var VAPID_PUBLIC_KEY='';", f"var VAPID_PUBLIC_KEY='';\n  var LEAK='{FAKE_KEY}';")],
    ),
    (
        "E8 brak bariery kropki w safe_static_path (operacyjne pliki przez HTTP)",
        "brak bariery kropki",
        [("vault", 'if any(part.startswith(".") for part in parts):', 'if any(False for part in parts):')],
    ),
    (
        "E8b deploy tara .opencode (52 MB stanu agenta na produkcje)",
        "tar nie wyklucza .opencode",
        [("deploy", "  --exclude='.opencode' \\\n", "")],
    ),
    (
        "F1 pusty stan niesie biezacy czas (kasuje postep przy 1. synchronizacji)",
        "uzywa BIEZACEGO czasu jako updated_at",
        [("vault", '"updated_at": EMPTY_STATE_AT,', '"updated_at": time.strftime(\'%Y-%m-%dT%H:%M:%SZ\', time.gmtime()),')],
    ),
    (
        "F2 mergeRemote scala pusty zapis zdalny",
        "scala bez sprawdzenia, czy zdalny zapis ma tresc",
        [("dash", "if(!remoteHasContent(env)){SYNC.remoteUpdatedAt=remoteAt;if(hasContent(state))schedulePush();saveLocal();return;}", "")],
    ),
    (
        "F3 pusty stan lokalny zapisywany w kolko",
        "pusty lokalny stan zapisywalby sie w kolko",
        [("dash", "if(hasContent(state))schedulePush();", "schedulePush();")],
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
