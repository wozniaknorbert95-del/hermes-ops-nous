#!/usr/bin/env python3
"""Wysyła „jeden kawał" Norberta przez Web Push.

URUCHAMIAJ NA VPS (cron albo systemd timer). Nie na laptopie, nie w CI.

Zasady:
- Klucz prywatny VAPID czytany z pliku poza repo (domyślnie /etc/akademia/vapid.env,
  chmod 600). Ten skrypt go nie zawiera i nie zapisuje.
- Read-only wobec platformy: czyta `data/progress.json` i `data/push-subscriptions.json`,
  niczego poza subskrypcjami nie zapisuje.
- `--dry-run` działa na samym stdlib (bez pywebpush i bez kluczy) — pozwala sprawdzić
  treść powiadomienia lokalnie, przed deployem.

Użycie:
    python3 scripts/push-send.py --dry-run
    python3 scripts/push-send.py
    VAPID_ENV=/etc/akademia/vapid.env python3 scripts/push-send.py --once
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.environ.get("ACADEMY_DATA_DIR", ROOT / "data"))
PROGRESS_FILE = DATA_DIR / "progress.json"
SUBS_FILE = DATA_DIR / "push-subscriptions.json"
STATE_FILE = DATA_DIR / "push-last-sent.json"
VAPID_ENV = Path(os.environ.get("VAPID_ENV", "/etc/akademia/vapid.env"))
SUBJECT = os.environ.get("VAPID_SUBJECT", "mailto:akademia@quietforge.flexgrafik.nl")


def force_utf8_streams() -> None:
    """Windows ma cp1252 na stdout — polskie znaki wysadzają print. Wymuś UTF-8."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def today_utc() -> str:
    return time.strftime("%Y-%m-%d", time.gmtime())


def load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def morning_brief_of(progress: dict[str, Any]) -> dict[str, Any]:
    """JEDNA PRAWDA o rytuale — import tej samej funkcji, którą woła vault.

    Do 2026-09-20 ten plik miał własną KOPIĘ reguły „blokada DZIEŃ bije wszystko".
    Dwie kopie tej samej reguły rozjeżdżają się cicho: zmiana w dashboardzie nie
    zmieniała powiadomienia i nikt tego nie zauważał. Teraz jest jedno źródło.
    """
    host_dir = str(ROOT / "host")
    if host_dir not in sys.path:
        sys.path.insert(0, host_dir)
    from progress_vault import human_today, morning_brief  # type: ignore  # noqa: PLC0415

    # Dzień podajemy JAWNIE. Ten plik chodzi na hoście (timer 07:00), a ta sama
    # funkcja chodzi też w kontenerze (Alpine, bez tzdata → UTC). Bez jawnego dnia
    # powiadomienie i dashboard mogłyby liczyć zaległość względem RÓŻNYCH dni.
    day, source = human_today()
    brief = morning_brief(progress, day)
    brief["today_source"] = source
    return brief


def build_payload(progress: dict[str, Any]) -> dict[str, str]:
    """Treść powiadomienia 07:00 — z werdyktu `morning_brief`, nie z lokalnej kopii.

    Dwie zmiany względem dawnej kopii:
    1. jedno źródło reguły (import z vaulta),
    2. **dzień odpoczynku nie dzwoni.** Dzień bez śladu pracy to odpoczynek, nie zaległość —
       handbook chroni „min. 1 dzień bez runów". Powiadomienie, które karze za odpoczynek,
       zostaje wyłączone w ~2 tygodnie (R5).
    """
    try:
        brief = morning_brief_of(progress)
    except Exception as exc:  # degradacja, nie plan B: nie duplikujemy reguł rytuału
        print(
            f"  ! nie zaimportowałem morning_brief ({type(exc).__name__}: {exc}) — "
            "wysyłam sam kawał, bez werdyktu o rytuale",
            file=sys.stderr,
        )
        brief = {}

    kawal = str(progress.get("now_card") or "").strip() or str(brief.get("kawal") or "").strip()

    if brief.get("stale") and not brief.get("rest_day"):
        stamp = str(brief.get("stamp") or "")
        return {
            "title": "Akademia — Dokończ DZIEŃ",
            "body": f"Rytuał {stamp} nie jest zamknięty na zielono. Następny rozdział czeka w LOCK.",
            "url": "./DASHBOARD.html#day",
            "tag": "akademia-dzien",
        }

    if not kawal:
        return {
            "title": "Akademia OS",
            "body": "Jeden kawał do zrobienia — otwórz Akademię.",
            "url": "./DASHBOARD.html",
            "tag": "akademia-kawal",
        }
    return {
        "title": "Norbert, jeden kawał do zrobienia",
        "body": kawal,
        "url": "./DASHBOARD.html",
        "tag": "akademia-kawal",
    }


def load_vapid() -> tuple[str, str]:
    if not VAPID_ENV.exists():
        raise SystemExit(
            f"BRAK: {VAPID_ENV}. Wygeneruj klucze na VPS: scripts/generate-vapid-keys.sh"
        )
    values: dict[str, str] = {}
    for line in VAPID_ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    if not values.get("VAPID_PRIVATE_KEY") or not values.get("VAPID_PUBLIC_KEY"):
        raise SystemExit(f"BRAK: {VAPID_ENV} nie zawiera VAPID_PRIVATE_KEY / VAPID_PUBLIC_KEY")
    return values["VAPID_PRIVATE_KEY"], values["VAPID_PUBLIC_KEY"]


def already_sent_today() -> bool:
    return str(load_json(STATE_FILE, {}).get("last_sent") or "") == today_utc()


def mark_sent(count: int) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps({"last_sent": today_utc(), "delivered": count}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def send(subscriptions: list[dict[str, Any]], payload: dict[str, str], private_key: str) -> tuple[int, list[str]]:
    try:
        from pywebpush import WebPushException, webpush  # type: ignore
    except ImportError:
        raise SystemExit("BRAK zależności: pip3 install pywebpush   (na VPS — nie w repo)")

    delivered = 0
    dead: list[str] = []
    body = json.dumps(payload, ensure_ascii=False)
    for item in subscriptions:
        endpoint = str(item.get("endpoint") or "")
        try:
            webpush(
                subscription_info={"endpoint": endpoint, "keys": item.get("keys") or {}},
                data=body,
                vapid_private_key=private_key,
                vapid_claims={"sub": SUBJECT},
            )
            delivered += 1
        except WebPushException as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            print(f"  ! {endpoint[:60]}… → {status or exc}", file=sys.stderr)
            if status in (404, 410):
                dead.append(endpoint)
        except (urllib.error.URLError, OSError) as exc:
            print(f"  ! {endpoint[:60]}… → {exc}", file=sys.stderr)
    return delivered, dead


def main() -> int:
    force_utf8_streams()
    parser = argparse.ArgumentParser(description="Akademia — Web Push z jednym kawałem.")
    parser.add_argument("--dry-run", action="store_true", help="pokaż treść, nie wysyłaj, nie potrzebuj kluczy")
    parser.add_argument("--force", action="store_true", help="wyślij mimo dzisiejszego wpisu")
    parser.add_argument("--once", action="store_true", help="jednorazowa wysyłka — alias dla cron/timera (zachowanie domyślne)")
    args = parser.parse_args()

    progress = load_json(PROGRESS_FILE, {})
    if not isinstance(progress, dict):
        progress = {}
    payload = build_payload(progress)

    if args.dry_run:
        print(json.dumps({"payload": payload, "subscriptions": len(load_json(SUBS_FILE, []))}, ensure_ascii=False, indent=2))
        return 0

    if not args.force and already_sent_today():
        print(f"SKIP: dzisiejszy push już poszedł ({today_utc()}). Użyj --force, żeby powtórzyć.")
        return 0

    subscriptions = load_json(SUBS_FILE, [])
    if not isinstance(subscriptions, list) or not subscriptions:
        print("SKIP: brak subskrypcji w data/push-subscriptions.json.")
        return 0

    private_key, _public_key = load_vapid()
    delivered, dead = send(subscriptions, payload, private_key)

    if dead:
        kept = [s for s in subscriptions if str(s.get("endpoint") or "") not in dead]
        SUBS_FILE.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"SPRZĄTANIE: usunięto {len(dead)} martwych subskrypcji (404/410).")

    mark_sent(delivered)
    print(f"OK: {delivered}/{len(subscriptions)} powiadomień wysłanych — „{payload['title']}”.")
    return 0 if delivered else 1


if __name__ == "__main__":
    sys.exit(main())
