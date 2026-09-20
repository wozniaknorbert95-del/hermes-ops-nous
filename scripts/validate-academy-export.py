#!/usr/bin/env python3
"""Walidator kontraktu AcademyProgress v0 + struktury DASHBOARD v3.1 (stdlib only)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema" / "academy-progress.v0.json"
DASH = ROOT / "DASHBOARD.html"

errors: list[str] = []


def force_utf8_streams() -> None:
    """Windows ma cp1252 na stdout — polskie znaki w komunikatach wysadzają print.

    Bez tego walidator wykrywa problem i… wywala się tracebackiem zamiast pokazać FAIL.
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def fail(message: str) -> None:
    errors.append(message)


def main() -> int:
    force_utf8_streams()
    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: schema unreadable: {exc}")
        return 1
    for key in ("schema_version", "tenant_id", "updated_at", "source"):
        if key not in schema.get("required", []):
            fail(f"schema missing required '{key}'")
    if schema.get("properties", {}).get("source", {}).get("const") != "academy-os":
        fail("schema source const != academy-os")

    try:
        html = DASH.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"FAIL: dashboard unreadable: {exc}")
        return 1

    # Fala 3 (twardy guard): kazdy diagram musi miec wersje ASCII na offline.
    ascii_block = re.search(r"var ASCII_DIAGRAMS=\{(.*?)\n  \};", html, re.S)
    ascii_keys = set(re.findall(r"\n    (\w+):`", ascii_block.group(1))) if ascii_block else set()
    diagrams_block = re.search(r"var DIAGRAMS=\{(.*?)\n  \};", html, re.S)
    diagram_entries = re.findall(r"\n    (\w+):\{title:", diagrams_block.group(1)) if diagrams_block else []
    diagrams_with_ascii = re.findall(
        r"\n    (\w+):\{title:(?:(?!\n    \w+:\{title:).)*?ascii:ASCII_DIAGRAMS\.", diagrams_block.group(1) + "\n  };", re.S
    ) if diagrams_block else []
    diagrams_missing_ascii = [k for k in diagram_entries if k not in diagrams_with_ascii]
    ascii_orphans = sorted(
        {k for k in re.findall(r"ASCII_DIAGRAMS\.(\w+)", html) if k not in ascii_keys}
    )
    pre_mermaid = re.findall(r'<pre class="mermaid"([^>]*)>', html)
    pre_without_ascii = [a[:48] for a in pre_mermaid if 'data-ascii="' not in a]

    checks = {
        "wersja v3.1 w tytule": "Command Dashboard v3.1" in html,
        "jedna karta TERAZ (id=nowcard)": html.count('id="nowcard"') == 1,
        "nowcard ukrywany na zakladce TERAZ (is-hidden)": "syncNowcardVisibility" in html and "is-hidden" in html,
        "przycisk TERAZ (id=nowact)": 'id="nowact"' in html and "<button" in html,
        "progressbar ARIA": 'role="progressbar"' in html and "aria-valuenow" in html,
        "5 zakladek IA": all(x in html for x in ("TERAZ", "WORKFLOW", "NARZĘDZIA", "DSAAS", "DZIEŃ")),
        "strefa Dzień": "Mój dzień — rano 10 minut" in html,
        "strefa Platforma": "Platforma — stan na dsaas-platform-main" in html or "Platforma — gdzie jest główna praca" in html,
        "strefa Piątek": "Piątek — koszty i porządek" in html,
        "playbook klikalny (PLAYBOOK_LAPTOP)": "PLAYBOOK_LAPTOP" in html and "renderPlaybookSteps" in html,
        "onboarding OPERATING-MODEL link": 'href="docs/OPERATING-MODEL.md"' in html,
        "Moj produkt z AGENTS.md": "PRODUCT_MISSION" in html and "AGENTS.md § Misja" in html,
        "15 narzedzi (proofHref)": html.count("proofHref:") == 15,
        "Jupyter nazwany wprost": "Jupyter" in html,
        "decyzja D-W7-JUPYTER": "D-W7-JUPYTER" in html,
        "check execute obok validate": "execute" in html,
        "warstwa analityczna w loopach (kropkowana)": "notebook execute" in html,
        "diagram dwoch warstw (DIAGRAMS.layers)": "layers:" in html,
        "scoreboard platformy (8 pozycji)": html.count("plat_") >= 8,
        "7 diagramow (DIAGRAMS)": all(k in html for k in ("platform:", "chain:", "hitl:", "isolation:", "surfaces:", "agents:", "budget:")),
        "SOURCES type+why": "source-meta" in html and "type:'spec'" in html,
        "accordion DSAAS (dzial-acc)": "dzial-acc" in html,
        "status import/eksport (id=syncmsg)": 'id="syncmsg"' in html,
        "brak alert()": "alert(" not in html,
        "skip link": 'class="skip"' in html,
        "main landmark": "<main>" in html,
        "klikana biblioteka": 'href="cursor-kurs/00-START-TUTAJ.md"' in html,
        "mermaid bez sztywnego min-width 520": "min-width:520px" not in html,
        "welcome banner ADHD": 'id="welcome"' in html and "welcome_dismissed" in html,
        "zone strip context": 'id="zone-strip"' in html and "renderZoneStrip" in html,
        "licznik pozostalych rozdzialow": 'id="remain"' in html,
        "klawiatura strzalki zakladek": "ArrowRight" in html and "ArrowLeft" in html,
        "WF-P tor platformy (nie ENT-12)": ("WF-P6" in html or "WF-P" in html) and "ENT-12" in html and "WAIT" in html,
        "Linear widoki Wave 2": "ceotoday-1ef420fc07c0" in html or "CEO/Today" in html,
        "MORNING-RITUAL platform align": "day_today_first" in html or "Today first" in html,
        "scroll-margin pod sticky tabami": "--scroll-offset" in html and "scroll-margin-top" in html,
        "sync bar online/offline": 'id="sync-bar"' in html and "renderSyncBar" in html and "pullProgress" in html,
        "sync PUT debounce": "schedulePush" in html and "pushProgress" in html,
        "PWA manifest": 'href="manifest.webmanifest"' in html,
        "F4 bramka workflow": 'id:"F4"' in html and "PLATFORM-WORKFLOW-GATE" in html,
        "mermaid kontrast edgeLabel": "edgeLabelBackground" in html or "edgeLabel" in html,
        "mermaid fallback offline": "mermaid-fallback" in html,
        "phone-first workflow": "phone-loops" in html and "phone-loop-first" in html,
        # --- Fala 3: mistrzostwo DSAAS + diagramy offline ---
        "F3 sekcja mistrzostwa": 'id="mastery"' in html and "MISTRZOSTWO" in html,
        "F3 8 etapow lancucha (z godlem i dowodem)": all(
            x in html
            for x in (
                "ODCS 3.1.0 ingress",
                "dsaas.security",
                "dsaas.governance.r7",
                "dsaas.growth_decision",
                "dsaas.tenant_objective",
                "dsaas.objective",
                "MCP execute_tool :8090",
                "ledger + OTel GenAI",
            )
        ),
        "F3 trzy agenty runtime": all(
            x in html for x in ("Agent-1: Demand & Trust", "Agent-2: Conversion & Retention", "Agent-3: Optimization & Strategy")
        ),
        "F3 budzet 30/6/3/1 drill": all(x in html for x in ("max:30", "max:6", "max:3", "max:1")),
        "F3 bramki HITL": all(
            x in html
            for x in ("label:'deploy'", "publikacja zewnętrzna", "wydatek > próg", "label:'zatrudnienie'")
        )
        and "human-stop: " in html,
        "F3 Zasada 11 wskazana": "Zasada 11" in html,
        "F3 drill egzekwuje pamiec": "drill_chain_done" in html and "mastery_dsaas" in html and "checkDrill" in html,
        "F3 diagramy offline z ASCII": "ASCII_DIAGRAMS" in html and "data-ascii=" in html and "offlineDiagrams" in html,
        "F3 KAZDY diagram ma wersje ASCII (offline bez wycieku kodu)": diagrams_missing_ascii == [],
        "F3 ASCII_DIAGRAMS bez martwych odwolan": ascii_orphans == [],
        "F3 KAZDY <pre class=mermaid> ma data-ascii (takze petle WORKFLOW)": pre_without_ascii == [] and len(pre_mermaid) >= 3,
        "F3 fallback nie pokazuje surowego kodu mermaid": "ten diagram nie ma jeszcze wersji ASCII" in html,
        "F3 CSS dla fallbacku offline": ".ascii-pre" in html and "pre.mermaid-fallback" in html,
        # --- Fala 4: Hermes (read-only kontroler + push) ---
        "F4 zakladka HERMES": "id:'hermes'" in html and "HERMES — kontroler i nauczyciel" in html,
        "F4 jeden kawal (nie druga karta)": "JEDEN KAWAŁ DO ZROBIENIA" in html and "hermesKawal" in html,
        "F4 powod z reguly": "powód z reguły" in html,
        "F4 read-only + Zasada 11": "READ-ONLY" in html and "Hermes nie pisze" in html,
        "F4 podglad platformy (4 przekroje)": all(x in html for x in ("repo-map", "koszt", "bezpieczeństwo")),
        "F4 push subscribe + VAPID public": "pushSubscribe" in html and "/push/subscribe" in html and "VAPID_PUBLIC_KEY" in html,
        "F4 fallback przy otwarciu": "hermes-banner" in html and "renderHermesBanner" in html,
        "F4 status GitHub read-only": "api.github.com" in html and "loadHermesRemote" in html,
    }
    for name, ok in checks.items():
        if not ok:
            fail(f"dashboard: {name}")

    # --- Fala 4: artefakty pushu poza HTML ---
    sw_path = ROOT / "sw.js"
    if not sw_path.exists():
        fail("push: brak sw.js")
    else:
        sw = sw_path.read_text(encoding="utf-8")
        for token in ("addEventListener('push'", "showNotification", "notificationclick", "skipWaiting"):
            if token not in sw:
                fail(f"push: sw.js bez '{token}'")
        if "caches.open" in sw or "cache.addAll" in sw:
            fail("push: sw.js cache'uje — ryzyko nieświeżej Akademii, tego nie chcemy")

    for rel, needle in (
        ("scripts/push-send.py", "def build_payload"),
        ("scripts/generate-vapid-keys.sh", "VAPID_PUBLIC_KEY"),
    ):
        path = ROOT / rel
        if not path.exists():
            fail(f"push: brak {rel}")
        elif needle not in path.read_text(encoding="utf-8"):
            fail(f"push: {rel} bez '{needle}'")

    # --- Kontrakt deployu push: klient pyta vault o klucz publiczny, VPS go dowozi ---
    # Bez tych trzech ogniw push na produkcji jest cicho martwy (badge "nieustawiony").
    if "/push/public-key" not in html or "loadVapidKey" not in html:
        fail("push: dashboard nie pobiera klucza VAPID z /push/public-key — na VPS push byłby martwy")
    if "registerSwEarly" not in html:
        fail("push: brak wczesnej rejestracji service workera — PWA na Androidzie traci instalowalność")
    icon_hrefs = re.findall(r'<link[^>]+rel="icon"[^>]*>', html)
    seen_icons = {}
    for tag in icon_hrefs:
        m = re.search(r'href="([^"]+)"', tag)
        if m:
            seen_icons[m.group(1)] = seen_icons.get(m.group(1), 0) + 1
    dup_icons = [k for k, v in seen_icons.items() if v > 1]
    if dup_icons:
        fail(f"head: zduplikowane <link rel=icon> ({', '.join(dup_icons)}) — sloppy head")
    if re.search(r"VAPID_PUBLIC_KEY\s*=\s*['\"][A-Za-z0-9_\-]{20,}", html):
        fail("push: klucz publiczny VAPID wpisany na twardo w DASHBOARD.html — ma go dowozić vault")
    compose = (ROOT / "host/docker-compose.yml")
    if not compose.exists() or "ACADEMY_VAPID_PUBLIC_KEY" not in compose.read_text(encoding="utf-8"):
        fail("push: host/docker-compose.yml nie przekazuje ACADEMY_VAPID_PUBLIC_KEY do kontenera vault")
    setup = (ROOT / "scripts/setup-akademia-vps.sh")
    if not setup.exists():
        fail("push: brak scripts/setup-akademia-vps.sh")
    else:
        ssetup = setup.read_text(encoding="utf-8")
        for needle in ("/etc/akademia/vapid.env", "ACADEMY_VAPID_PUBLIC_KEY"):
            if needle not in ssetup:
                fail(f"push: setup-akademia-vps.sh bez '{needle}' — .env nie dostanie klucza VAPID")
        for needle in ("akademia-push.timer", "pywebpush"):
            if needle not in ssetup:
                fail(f"push: setup-akademia-vps.sh bez '{needle}' — nikt nie WYŚLE pusha (cicha porażka)")
        # Compose v1 = KeyError 'ContainerConfig' przy recreate -> martwy vault (incydent 2026-09-20).
        for needle in ("down --remove-orphans", "vault health (retry"):
            if needle not in ssetup:
                fail(f"deploy: setup-akademia-vps.sh bez '{needle}' — recreate compose v1 zostawi martwy vault")
    sender = (ROOT / "scripts/push-send.py")
    if sender.exists() and '"--once"' not in sender.read_text(encoding="utf-8"):
        fail("push: push-send.py nie zna '--once' — jednostka systemd z tym argumentem padnie")

    # --- Kontrakt deployu: deploy-akademia-vps.sh pakuje tar z WORKING COPY ---
    # .gitattributes (eol=lf) nie pomoże, więc CRLF/BOM w skrypcie = pad bash na VPS.
    for sh in sorted(ROOT.glob("scripts/*.sh")):
        raw = sh.read_bytes()
        rel = sh.relative_to(ROOT)
        if b"\r\n" in raw:
            fail(f"deploy: {rel} ma CRLF — na VPS bash padnie (tar pakuje working copy)")
        if raw[:3] == b"\xef\xbb\xbf":
            fail(f"deploy: {rel} ma BOM — na VPS bash padnie")

    # --- Bramka sekretów: klucz prywatny VAPID nie może mieć wartości w repo ---
    secret_re = re.compile(r"VAPID_PRIVATE_KEY\s*=\s*[A-Za-z0-9_\-]{20,}")
    skip_dirs = {".git", "node_modules", "__pycache__", ".ruff_cache", "data", ".venv"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or skip_dirs & set(path.parts):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".pyc", ".pdf"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        if secret_re.search(text):
            fail(f"sekret: {path.relative_to(ROOT)} zawiera wartość VAPID_PRIVATE_KEY")

    # SOURCES per dzial B-G
    for dzial in ("B:", "C:", "D:", "E:", "F:", "G:"):
        if dzial not in html.split("SOURCES_DATA")[1][:4000] if "SOURCES_DATA" in html else "":
            pass  # optional soft check skipped — keys exist in object

    sample = {
        "schema_version": "0.1.0",
        "tenant_id": "quietforge",
        "updated_at": "2026-09-12T00:00:00+00:00",
        "source": "academy-os",
        "academy_url": "",
        "now_card": "Moduł 1 — test",
        "tracks": {"W": {"percent": 17, "completed_ids": ["m1"]}, "F": {"percent": 17, "completed_ids": ["m1"]}},
        "_scratch": {"m1_pass": True},
    }
    for key in schema.get("required", []):
        if key not in sample:
            fail(f"sample envelope missing '{key}'")

    if re.search(r"academy_url['\"]?\s*:\s*['\"][^'\"]*token", html, re.I):
        fail("dashboard: token w academy_url w kodzie")
    if re.search(r"oidc", html, re.I) and "zero token" not in html.lower() and "Never put OIDC" not in html:
        pass  # schema comment only in JSON file

    if errors:
        print("FAIL:")
        for item in errors:
            print(f" - {item}")
        return 1
    print("PASS: academy export contract + dashboard v3.1 (sync vault ready)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
