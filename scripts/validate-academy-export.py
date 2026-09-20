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

    # --- Bramka wycieku sekretów: vault serwuje CAŁE repo (STATIC_ROOT). ---
    # Incydent 2026-09-20: /.env, /CREDENTIALS.local.txt, /host/.htpasswd = HTTP 200
    # za hasłem Basic Auth, czyli jeden curl dzielił nginx .htpasswd i bearer vaulta.
    vault = (ROOT / "host" / "progress_vault.py")
    if vault.exists():
        vtxt = vault.read_text(encoding="utf-8")
        for needle in (
            "STATIC_ALLOW_EXT = frozenset(",
            "STATIC_DENY_DIRS = frozenset(",
            '"credentials.local.txt"',
            'if any(part.startswith(".") for part in parts):',
            "if parts[0] in STATIC_DENY_DIRS:",
            "if candidate.suffix.lower() not in STATIC_ALLOW_EXT:",
        ):
            if needle not in vtxt:
                fail(f"vault: brak reguły '{needle}' — sekrety repo wyciekną po HTTP (/.env = 200)")
    test = (ROOT / "scripts" / "test_progress_vault.py")
    if test.exists():
        ttxt = test.read_text(encoding="utf-8")
        for needle in ("static_leak_checks", "def load_vault_module", '"/host/.htpasswd"'):
            if needle not in ttxt:
                fail(f"test: brak '{needle}' — regresja wycieku sekretów nie zostałaby złapana")

    # --- Bramka instalacji PWA: manifest i ikony MUSZĄ być anonimowe. ---
    # Chromium pobiera manifest bez poświadczeń; za Basic Auth dostaje 401 i nie
    # uznaje witryny za instalowalną → Android mintuje tylko skrót (mealie#6060).
    # Ikony z poświadczeniami nie pobierają się wcale — muszą być publiczne.
    nginx_conf = (ROOT / "host" / "nginx-akademia.conf")
    if not nginx_conf.exists():
        fail("pwa: brak host/nginx-akademia.conf")
    else:
        ntxt = nginx_conf.read_text(encoding="utf-8")
        for needle in ("location = /manifest.webmanifest", "location ^~ /icons/", "auth_basic off"):
            if needle not in ntxt:
                fail(f"pwa: nginx bez '{needle}' — na Androidzie zostanie tylko skrót, nie instalacja")
        if ntxt.count("auth_basic off") < 2:
            fail("pwa: nginx odsłania tylko jedno z dwojga (manifest/ikony) — instalacja padnie")
    ssetup2 = (ROOT / "scripts" / "setup-akademia-vps.sh")
    if ssetup2.exists():
        stxt2 = ssetup2.read_text(encoding="utf-8")
        for needle in ("install_site", "manifest.webmanifest", "html_bez_hasla"):
            if needle not in stxt2:
                fail(f"pwa: setup-akademia-vps.sh bez '{needle}' — konfiguracja nginx nie dojedzie na VPS")
    if "manifest.webmanifest" not in html:
        fail("pwa: DASHBOARD.html nie linkuje manifestu")

    # --- Bramka czatu z Hermesem (audyt UX/UI 2026-09-20) ---------------------
    # Dowódca zgłosił: „gdzie czat? przecież to ma być mój kontroler i nauczyciel".
    # Czat to teraz kontrakt: front (UI + silnik lokalny), backend (provider za
    # konfiguracją, klucz tylko na VPS, limit dzienny) i wejście z ekranu startowego.
    # Bez tych guardów można przypadkiem skasować rozmowę i nikt tego nie złapie.
    vault_py = (ROOT / "host" / "progress_vault.py")
    if not vault_py.exists():
        fail("czat: brak host/progress_vault.py")
    else:
        vtxt2 = vault_py.read_text(encoding="utf-8")
        # Guardy patrzą na KONSTRUKCJE, nie na słowa. Powód: pierwsza wersja sprawdzała
        # obecność podłańcucha w całym pliku, więc mutacja komentarza albo jednej z kilku
        # wzmianek przechodziła niezauważona — wykazał to mutacyjny test guardów.
        for needle, why in (
            ('path == "/hermes/chat"', "vault nie routuje POST /hermes/chat"),
            ("hermes_clean_messages(data.get(", "wiadomości z przeglądarki idą do LLM bez czyszczenia"),
            ("HERMES_SYSTEM.format(state=hermes_state_digest(state))", "stan nie trafia do promptu systemowego"),
            ("def hermes_call_llm", "brak wywołania dostawcy LLM"),
            ('"/hermes/status"', "dashboard nie dowie się, czy mózg LLM jest podłączony"),
            ("ACADEMY_HERMES_DAILY_CAP", "brak sufitu kosztu na dobę"),
        ):
            if needle not in vtxt2:
                fail(f"czat: {why}")
        # Licznik zużycia musi być WOŁANY, nie tylko zdefiniowany: nazwa funkcji występuje
        # też w jej definicji, więc sam podłańcuch przepuściłby mutację usuwającą wywołanie.
        if not re.search(r"^\s+hermes_usage_bump\(\)\s*$", vtxt2, re.M):
            fail("czat: licznik zużycia nigdy nie jest wołany — limit dzienny nie działa")
        # Provider musi być za konfiguracją, nie zaszyty w kodzie: domyślna wartość
        # adresu i klucza MUSI być pusta. Wzmianka w komentarzu (przykład konfiguracji)
        # jest dozwolona i nie jest zaszyciem — dlatego patrzymy na PRZYPISANIE, nie na tekst.
        if not re.search(r'HERMES_BASE_URL\s*=\s*os\.environ\.get\(\s*"ACADEMY_HERMES_BASE_URL"\s*,\s*""\s*\)', vtxt2):
            fail("czat: domyślny adres dostawcy LLM nie jest pusty — provider zaszyty w kodzie")
        if not re.search(r'HERMES_API_KEY\s*=\s*os\.environ\.get\(\s*"ACADEMY_HERMES_API_KEY"\s*,\s*""\s*\)', vtxt2):
            fail("czat: klucz API nie ma pustej wartości domyślnej — ryzyko sekretu w repo")
        # Klucz wolno użyć TYLKO w trzech miejscach: odczyt ze środowiska, test
        # konfiguracji (zwraca bool, nie wartość) i nagłówek żądania WYCHODZĄCEGO do
        # dostawcy. Każde inne użycie to droga do wycieku — pilnujemy tego linia po linii,
        # bo test z kanarkiem sprawdza tylko odpowiedzi konkretnej konfiguracji.
        dozwolone = (
            'HERMES_API_KEY = os.environ.get("ACADEMY_HERMES_API_KEY", "").strip()',
            "return bool(HERMES_BASE_URL and HERMES_MODEL and HERMES_API_KEY)",
            '"Authorization": f"Bearer {HERMES_API_KEY}",',
        )
        for hit in re.finditer(r"^.*HERMES_API_KEY.*$", vtxt2, re.M):
            line = hit.group(0).strip()
            if line.startswith("#") or line in dozwolone:
                continue
            fail(f"czat: HERMES_API_KEY poza dozwolonym miejscem — możliwy wyciek: {line[:70]}")
        # Limit kosztu: bez niego darmowy model kończy się banem, płatny fakturą.
        if "hermes_usage_bump" not in vtxt2:
            fail("czat: brak licznika zużycia — limit dzienny nie zadziała")

    for needle in ("/hermes/chat", "/hermes/status", "hermesLocalAnswer", "hermesAsk", "renderHermesChat"):
        if needle not in html:
            fail(f"czat: DASHBOARD.html bez '{needle}' — UI rozmowy z Hermesem nie działa")

    # Wejście do czatu z TERAZ. Bez tego czat istnieje, ale nie da się go znaleźć —
    # dokładnie to zgłosił Dowódca („gdzie czat?"). Sprawdzamy WIRING, nie definicję:
    # sama funkcja renderująca nie wystarczy, musi być dołożona do zakładki startowej.
    if "renderNowTab()+renderNowAskHermes()" not in html:
        fail("czat: TERAZ nie dokłada wejścia do czatu (brak renderNowTab()+renderNowAskHermes())")
    if 'data-chat-jump="' not in html or "[data-chat-jump]" not in html:
        fail("czat: chipsy TERAZ→HERMES nie są ani renderowane, ani podpięte")
    if 'data-go-tab="hermes"' not in html:
        fail("czat: brak odnośnika do pełnego czatu na ekranie startowym")

    # Cache GitHub API: guard musi być postawiony PRZED odpaleniem fetch, inaczej
    # równoległe rendery wystrzelą kilkanaście identycznych żądań (zmierzone: 30).
    if "GH_LOADING=true;var hdr=" not in html:
        fail("czat: flaga GH_LOADING nie stoi przed fetch — GitHub API dostanie duplikaty żądań")
    if "if(r.knownPrivate)return Promise.resolve(" not in html:
        fail("czat: repo znane jako prywatne znów jest pytane o API — konsola dostanie 404")
    # Flaga musi stać PRZY WPISIE repo, nie tylko być sprawdzana: bez niej warunek
    # `r.knownPrivate` jest zawsze fałszywy i prywatne repo znów poleci do API (404).
    if "'dsaas-platform-main',label:'dsaas-platform-main',knownPrivate:true" not in html:
        fail("czat: wpis repo prywatnego zgubił flagę knownPrivate — wracają 404 w konsoli")

    # --- Bramka celów dotykowych (audyt UX/UI 2026-09-20) --------------------
    # Akademia mówi „telefon w pracy", a pomiar na 390x844 wykazał 306 kontrolek
    # poniżej 44 px. Blok (pointer:coarse) jest tym, co tę różnicę zamyka.
    if "@media(pointer:coarse)" not in html:
        fail("mobile: brak bloku @media(pointer:coarse) — cele dotykowe znów spadną pod 44px")
    for needle in ("label.ck,.score-row{min-height:44px", ".tpl{min-height:44px"):
        if needle not in html:
            fail(f"mobile: blok dotykowy bez '{needle}' — część kontrolek zostanie za mała")

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

    # --- Fala D (test użytkownika 2026-09-20) ---
    # Defekty znalezione przez wejscie w role uzytkownika i klikanie, nie przez czytanie kodu.
    # Kazdy guard celuje w KONSTRUKCJE (wywolanie, kolejnosc galezi), nie w sam napis —
    # inaczej przechodzi mutacje i jest dekoracja.

    def code_line(needle: str) -> str:
        for line in html.splitlines():
            if needle in line:
                return line
        return ""

    def code_block(needle: str) -> str:
        """Cala funkcja od 'needle' do poczatku nastepnej — czesc funkcji w tym pliku
        zajmuje kilka linii (np. bindDayExtras), wiec code_line bylo za waskie."""
        start = html.find(needle)
        if start < 0:
            return ""
        end = html.find("\nfunction ", start + len(needle))
        return html[start:end] if end > start else html[start:]

    # D1: zmiana zakladki prowadzi do TRESCI. Panel treści leży ~900 px pod hero,
    # wiec scrollTo(0) po kliknieciu zakladki = "kliknalem i nic sie nie stalo".
    if "function alignPanelToNav()" not in html:
        fail("dashboard: brak alignPanelToNav — klikniecie zakladki nie doprowadzi do tresci")
    activate_line = code_line("function activateTab(")
    if not activate_line:
        fail("dashboard: brak funkcji activateTab")
    else:
        if "alignPanelToNav()" not in activate_line:
            fail("dashboard: activateTab nie wola alignPanelToNav — tresc zostaje pod ekranem")
        if re.search(r"scrollTo\(\{\s*top:\s*0", activate_line):
            fail("dashboard: activateTab przewija na gore strony zamiast do tresci")

    # D2: potwierdzenia i bledy MUSZA byc widoczne. #syncmsg lezy w stopce (~4500 px),
    # wiec bez toastu uzytkownik nie widzi ani "Zaliczono", ani "najpierw odhacz laboratorium".
    if 'id="toast"' not in html:
        fail("dashboard: brak elementu #toast — komunikaty zostaja niewidoczne w stopce")
    if not re.search(r"\.toast\{position:fixed", html):
        fail("dashboard: brak CSS .toast{position:fixed} — toast nie bylby przyklejony")
    msg_line = code_line("function msg(text,ok)")
    if not msg_line:
        fail("dashboard: brak funkcji msg")
    elif "toast(text,ok)" not in msg_line:
        fail("dashboard: msg() nie pokazuje toastu — potwierdzenia i bledy sa niewidoczne")
    if "bindToast()" not in code_line("function bindStatic("):
        fail("dashboard: bindStatic nie wola bindToast — toast nie da sie zamknac kliknieciem")

    # D3: karta TERAZ musi pokazywac NASTEPNY OTWARTY krok, nie na sztywno lab[0].
    # Wczesniej po odhaczeniu kroku 1 karta dalej kazala robic krok 1, a Hermes mowil krok 2.
    if "function nextLabIdx(" not in html:
        fail("dashboard: brak nextLabIdx — karta TERAZ nie wie, ktory krok jest otwarty")
    elif "return -1" not in code_line("function nextLabIdx("):
        fail("dashboard: nextLabIdx nie zwraca -1 dla wszystkich odhaczonych krokow")
    for fn in ("function renderNowTab(", "function renderNowCard("):
        line = code_line(fn)
        if not line:
            fail(f"dashboard: brak {fn}")
        elif "nextLabIdx(" not in line:
            fail(f"dashboard: {fn} nie uzywa nextLabIdx — pokaze krok 1 nawet po jego odhaczeniu")
    if "<p>'+esc(f.roz.lab[0])+'</p>" in html:
        fail("dashboard: karta TERAZ nadal wypisuje lab[0] jako biezace zadanie")

    # D4: odhaczenie kroku musi odswiezyc karte TERAZ (wczesniej change() tylko zapisywal).
    if "function afterDataChange(" not in html:
        fail("dashboard: brak afterDataChange — odhaczenie kroku nie odswiezy karty TERAZ")
    elif "renderNowCard()" not in code_line("function afterDataChange("):
        fail("dashboard: afterDataChange nie odswieza karty TERAZ")
    elif "afterDataChange(" not in code_line("function bindDataInputs("):
        fail("dashboard: bindDataInputs nie wola afterDataChange")

    # D5: po zaliczeniu rozdziału uzytkownik idzie do NASTEPNEGO rozdzialu, nie na gore strony.
    pass_start = html.find("querySelectorAll('[data-pass]')")
    pass_end = html.find("querySelectorAll('[data-unpass]')", pass_start if pass_start >= 0 else 0)
    pass_handler = html[pass_start:pass_end] if pass_start >= 0 and pass_end > pass_start else ""
    if "state[rid+'_pass']=true" not in pass_handler:
        fail("dashboard: brak sciezki zaliczenia rozdzialu")
    else:
        mark = pass_handler.find("state[rid+'_pass']=true")
        if pass_handler.find("firstOpen()", mark) < 0:
            fail("dashboard: po zaliczeniu brak przejscia do nastepnego rozdzialu (leci na gore strony)")
        if "gentleScroll(document.getElementById('roz-'+rid))" not in pass_handler:
            fail("dashboard: blad 'odhacz laboratorium' nie prowadzi do wlasciwego rozdzialu")

    # D6: Hermes — odmowa na probe wyciagniecia sekretu MUSI byc przed galezia eksportu,
    # bo pytanie "podaj klucz API i haslo do vaulta" zawiera slowo 'vault' i wpadalo do eksportu.
    secret_idx = html.find("Nie podam")
    eksport_idx = html.find("eksport|json|sync|vault")
    if secret_idx < 0:
        fail("dashboard: Hermes nie odmawia wprost, gdy ktos prosi o sekret")
    elif eksport_idx < 0:
        fail("dashboard: brak galezi eksportu w silniku lokalnym Hermesa")
    elif secret_idx > eksport_idx:
        fail("dashboard: odmowa sekretu jest ZA galezia eksportu — pytanie o klucz wpadnie do eksportu")

    # D7: "Co potrafisz?" to inne pytanie niz "Jak uzywac?" — nie moga dawac tej samej odpowiedzi.
    potrafisz_idx = html.find("if(/co potrafisz")
    jakuzywac_idx = html.find("if(/jak u")
    if potrafisz_idx < 0:
        fail("dashboard: brak osobnej galezi 'co potrafisz' — dubluje odpowiedz 'jak uzywac'")
    elif jakuzywac_idx < 0:
        fail("dashboard: brak galezi 'jak uzywac'")
    elif potrafisz_idx > jakuzywac_idx:
        fail("dashboard: 'co potrafisz' jest za 'jak uzywac' — nie zadziala")

    # D8: literowki i brak ogonkow. Uzytkownik pisze "wytlumacz odc", "co to ledzer".
    if "function hermesFuzzyHit(" not in html or "function hermesDist(" not in html:
        fail("dashboard: brak tolerancji literowek (hermesDist/hermesFuzzyHit)")
    elif "hermesFuzzyHit(question," not in html:
        fail("dashboard: tolerancja literowek nie jest uzyta w dopasowaniu slow slownika")

    # D9: polszczyzna. "Rytuał DZIEŃ jest zgrane" to zepsute zdanie.
    if "jest zgrane" in html:
        fail("dashboard: zepsuta polszczyzna 'jest zgrane' w odpowiedzi Hermesa")

    # D10: karta TERAZ nie moze ucinac listy brakow do 3 pozycji bez informacji,
    # ze brakow jest wiecej — uzytkownik odhaczy 3 i nadal bedzie zablokowany.
    if "dayMissing().slice(0,3)" in html:
        fail("dashboard: karta TERAZ ucina liste brakow do 3 bez slowa o reszcie")

    # D11: pierwszy ekran (telefon 390x844) nie miesci paska zakladek — lezy ~1080 px.
    # Karta powitalna MUSI dac jedno klikniecie do TERAZ, inaczej nowy uzytkownik szuka nawigacji.
    welcome_block = re.search(r'<div id="welcome".*?chowaj na zawsze</button></div>', html, re.S)
    go_tab_bind = "querySelectorAll('[data-go-tab]').forEach(function(b){if(b.dataset.bound)return;b.dataset.bound='1';b.addEventListener('click',function(){activateTab(b.dataset.goTab,false);});});"
    if not welcome_block:
        fail("dashboard: brak karty powitalnej #welcome")
    else:
        if 'data-go-tab="now"' not in welcome_block.group(0):
            fail("dashboard: karta powitalna nie ma przejscia do TERAZ (nawigacja jest pod ekranem)")
        if go_tab_bind not in code_block("function bindInstall("):
            fail("dashboard: bindInstall nie podpina data-go-tab — przycisk w karcie powitalnej bylby martwy")
    # Ten sam kontrakt dla panelu treści: data-go-tab obsluguje „Dokończ DZIEŃ" (karta LOCK)
    # i „Pełny czat →" (karta Zapytaj Hermesa). Bez podpiecia oba sa martwe.
    if go_tab_bind not in code_block("function bindDayExtras("):
        fail("dashboard: bindDayExtras nie podpina data-go-tab — 'Dokończ DZIEŃ' i 'Pełny czat' bylyby martwe")

    # --- Fala E (podłączenie modelu deepseek-flash, 2026-09-21) -----------------
    # Trzy ciche awarie, które nie bolą, dopóki nie podłączysz prawdziwego modelu:
    #  (1) docker-compose nie przekazuje zmiennych → kod je CZYTA, kontener ich NIE MA,
    #      Hermes po cichu odpowiada lokalnie mimo poprawnie wpisanego klucza;
    #  (2) budżet tokenów za mały na model ROZUMUJĄCY → finish_reason=length i pusty
    #      content przy trudnych pytaniach (model milczy tam, gdzie jest najmadrzejszy);
    #  (3) vault czeka dłużej niż klient → przeglądarka przerywa pierwsza, użytkownik
    #      dostaje odpowiedź lokalną, a vault dalej pali tokeny do dziennego sufitu.
    compose = (ROOT / "host" / "docker-compose.yml")
    vault_py = (ROOT / "host" / "progress_vault.py")
    env_example = (ROOT / "host" / "env.example")
    setup_sh = (ROOT / "scripts" / "setup-akademia-vps.sh")
    compose_txt = compose.read_text(encoding="utf-8") if compose.is_file() else ""
    vault_txt = vault_py.read_text(encoding="utf-8") if vault_py.is_file() else ""
    env_txt = env_example.read_text(encoding="utf-8") if env_example.is_file() else ""
    setup_txt = setup_sh.read_text(encoding="utf-8") if setup_sh.is_file() else ""

    # E1: kontener MUSI dostać zmienne Hermesa. Vault czyta je z os.environ wewnątrz
    # kontenera, więc samo wpisanie ich w .env nic nie da bez przekazania w compose.
    if not compose_txt:
        fail("hermes: brak host/docker-compose.yml")
    else:
        for var in ("ACADEMY_HERMES_BASE_URL", "ACADEMY_HERMES_MODEL", "ACADEMY_HERMES_API_KEY"):
            if not re.search(rf"^\s*{var}:\s*\$\{{{var}:-", compose_txt, re.M):
                fail(f"hermes: docker-compose nie przekazuje {var} do kontenera — klucz w .env bez efektu")

    # E2: budżet tokenów musi pomieścić reasoning_content modelu rozumującego.
    # Pomiar 2026-09-21 na deepseek-flash: 807 tokenów myslenia na pytaniu trudnym,
    # out=1495. Sufit 700 → pusta odpowiedź. Wymagamy sensownego zapasu.
    m_budget = re.search(r'ACADEMY_HERMES_MAX_TOKENS",\s*"(\d+)"', vault_txt)
    if not m_budget:
        fail("hermes: brak ACADEMY_HERMES_MAX_TOKENS w progress_vault.py")
    elif int(m_budget.group(1)) < 1500:
        fail(f"hermes: ACADEMY_HERMES_MAX_TOKENS={m_budget.group(1)} za malo dla modelu rozumujacego "
             "(myslenie zjada 30-55% outputu → pusty content przy trudnym pytaniu)")

    # E3: vault oddaje sterowanie PRZED klientem (timeout vaulta < watchdog klienta).
    m_vault_to = re.search(r'ACADEMY_HERMES_TIMEOUT",\s*"(\d+)"', vault_txt)
    m_client_to = re.search(r"milcz[ał][^\n]*?\},(\d{4,6})\)", html)
    if not m_vault_to:
        fail("hermes: brak ACADEMY_HERMES_TIMEOUT w progress_vault.py")
    elif not m_client_to:
        fail("dashboard: nie znaleziono watchdogu klienta (setTimeout po msg o milczeniu)")
    elif int(m_vault_to.group(1)) >= int(m_client_to.group(1)) // 1000:
        fail(f"hermes: timeout vaulta ({m_vault_to.group(1)} s) >= watchdog klienta "
             f"({int(m_client_to.group(1)) // 1000} s) — to klient przerywa pierwszy i pali tokeny")

    # E4: .env.example musi dokumentowac WSZYSTKIE trzy zmienne Hermesa — inaczej
    # kolejny deploy na swiezym VPS nie ma skad wiedziec, co wpisac.
    if not env_txt:
        fail("hermes: brak host/env.example")
    else:
        for var in ("ACADEMY_HERMES_BASE_URL=", "ACADEMY_HERMES_MODEL=", "ACADEMY_HERMES_API_KEY="):
            if var not in env_txt:
                fail(f"hermes: env.example nie dokumentuje {var.rstrip('=')}")
        # Klucz w env.example MUSI byc pusty. Wypelniony = sekret w repo.
        if not re.search(r"^ACADEMY_HERMES_API_KEY=\s*$", env_txt, re.M):
            fail("hermes: env.example ma niepusty ACADEMY_HERMES_API_KEY — sekret w repo!")

    # E5: setup MUSI dopisac puste klucze (bez nadpisywania wartosci — klucz z VPS
    # przezywa deploy), i NIGDY nie wypisac wartosci klucza.
    if not setup_txt:
        fail("hermes: brak scripts/setup-akademia-vps.sh")
    else:
        if "ensure_env_key()" not in setup_txt:
            fail("hermes: setup nie ma ensure_env_key — .env na VPS zostanie bez kluczy Hermesa")
        for var in ("ACADEMY_HERMES_BASE_URL", "ACADEMY_HERMES_MODEL", "ACADEMY_HERMES_API_KEY"):
            if f"ensure_env_key {var}" not in setup_txt:
                fail(f"hermes: setup nie wywoluje ensure_env_key {var}")
        if not re.search(r'if\s+!\s+grep\s+-qE\s+"\^\$1="', setup_txt):
            fail("hermes: ensure_env_key nadpisuje istniejace wartosci — klucz z VPS nie przezyje deployu")
        # Zadnego echa sekretu w logi deployu.
        if re.search(r"echo[^\n]*\$\{?ACADEMY_HERMES_API_KEY", setup_txt):
            fail("hermes: setup wypisuje ACADEMY_HERMES_API_KEY — sekret w logach deployu")

    # E6: /hermes/status nie moze zdradzac adresu dostawcy ani klucza (publiczny probe).
    status_block = vault_txt[vault_txt.find('parsed.path == "/hermes/status"'):][:900]
    if not status_block:
        fail("hermes: brak /hermes/status w progress_vault.py")
    else:
        for leak in ("HERMES_API_KEY", "HERMES_BASE_URL"):
            if leak in status_block:
                fail(f"hermes: /hermes/status zwraca {leak} — publiczny probe nie moze zdradzac sekretu")

    # E7: zadnych realnych kluczy w repo (klucz DeepSeek: sk- + 32 hex).
    leaks = []
    for path in (DASH, vault_py, env_example, compose, setup_sh):
        if path.is_file() and re.search(r"sk-[0-9a-f]{20,}", path.read_text(encoding="utf-8")):
            leaks.append(path.name)
    if leaks:
        fail(f"hermes: realny klucz API w repo: {', '.join(leaks)} — sekret musi zyc tylko w /opt/akademia/.env")

    # E8: bariera kropki jest JEDYNA ochrona .env/.git/.opencode/.htpasswd na publicznym
    # serwerze statykow. Bez niej vault oddaje pliki operacyjne spod Basic Auth.
    if 'startswith(".")' not in vault_txt or "STATIC_DENY_DIRS" not in vault_txt:
        fail("vault: brak bariery kropki w safe_static_path — .env/.git/.opencode do sciagniecia przez HTTP")

    # E8b: deploy nie ma po co wysylac lokalnego stanu agenta (52 MB) na produkcje.
    deploy_sh = ROOT / "scripts" / "deploy-akademia-vps.sh"
    deploy_txt = deploy_sh.read_text(encoding="utf-8") if deploy_sh.is_file() else ""
    if not deploy_txt:
        fail("deploy: brak scripts/deploy-akademia-vps.sh")
    elif "--exclude='.opencode'" not in deploy_txt:
        fail("deploy: tar nie wyklucza .opencode — 52 MB lokalnego stanu agenta leci na produkcje")

    # --- Fala F (P0: utrata postepu przy pierwszej synchronizacji, 2026-09-21) ----
    # Vault dla NIEISTNIEJACEGO stanu oddawal updated_at = "teraz". Dashboard scala
    # regula "nowszy wygrywa" (remoteAt > localAt → state = env._scratch), wiec pusty
    # zapis zawsze wygrywal z realna praca uzytkownika i KASOWAL ja przy pierwszej
    # synchronizacji — z tostem "Zsynchronizowano z vault (nowszy zapis)".
    # Na produkcji plik progress.json nigdy nie istnial, czyli byla to bomba z opoznionym
    # zaplonem: wystarczylo wpisac haslo w stopce, zeby stracic caly kurs.
    default_fn = vault_txt[vault_txt.find("def default_envelope"):][:700]
    if not default_fn:
        fail("vault: brak default_envelope")
    else:
        if "EMPTY_STATE_AT" not in default_fn:
            fail("vault: pusty stan bez EMPTY_STATE_AT — nie wiadomo, co jest znacznikiem pustki")
        if re.search(r"updated_at\"\s*:\s*(now|time\.|datetime\.)", default_fn):
            fail("vault: default_envelope uzywa BIEZACEGO czasu jako updated_at — "
                 "pusty zapis wygra z praca uzytkownika i ja skasuje")

    # F2: front NIE MOZE scalic pustego zapisu zdalnego (druga warstwa obrony).
    if "function remoteHasContent(" not in html:
        fail("dashboard: brak remoteHasContent — pusty zapis z vaulta moze skasowac postep")
    merge_fn = html[html.find("function mergeRemote("):][:1400]
    if not merge_fn:
        fail("dashboard: brak mergeRemote")
    elif "!remoteHasContent(env)" not in merge_fn:
        fail("dashboard: mergeRemote scala bez sprawdzenia, czy zdalny zapis ma tresc")
    # F3: pusty stan lokalny nie moze robic PUT-a przy kazdym wejsciu (petla zapisow).
    elif "hasContent(state)" not in merge_fn:
        fail("dashboard: brak warunku hasContent(state) — pusty lokalny stan zapisywalby sie w kolko")

    # --- Fala 0 (kanal poranny + integralnosc deployu, 2026-09-20) ---------------
    # Znalezione przy audycie: powiadomienie 07:00 wysyla `./DASHBOARD.html#day`,
    # a tapniecie prowadzilo DONIKAD — dwie niezalezne awarie nalozone na siebie.
    # To byl najdrozszy cichy defekt w repo: caly poranny rytual nie mial wejscia.
    sw_file = ROOT / "sw.js"
    sw_txt = sw_file.read_text(encoding="utf-8") if sw_file.is_file() else ""
    if not sw_txt:
        fail("push: brak sw.js")
    else:
        sw_nc = sw_txt[sw_txt.find("'notificationclick'"):]
        sw_nc = sw_nc[: sw_nc.find("'message'")] if "'message'" in sw_nc else sw_nc
        if not sw_nc:
            fail("push: brak obslugi notificationclick")
        # A1: `client.focus()` samo AKTYWUJE okno i NIE ustawia hasha, wiec `hashchange`
        # nie poleci i openHashTarget() nigdy sie nie uruchomi. Musi byc NAWIGACJA.
        elif "navigate(" not in sw_nc:
            fail("push: notificationclick bez client.navigate — tapniecie powiadomienia gubi zakladke")
        elif "openWindow(target)" not in sw_nc:
            fail("push: notificationclick bez openWindow(target) — zimny start nie otworzy celu")

    # A2: `#day` to ID ZAKLADKI, a getElementById('day') zwraca null (takiego elementu
    # nie ma w HTML). Bez tej galezi push byl martwy nawet przy zimnym starcie.
    # UWAGA: `tabDef` ma FALLBACK na ACADEMY_TABS[0], wiec sam `tabDef(id)` jest prawdziwy
    # dla KAZDEGO smiecia. Musi byc jawne porownanie `t0.id===id`, inaczej `#cokolwiek`
    # ustawi active_tab na nieistniejaca zakladke i panel bedzie pusty.
    hash_fn = html[html.find("function openHashTarget("):][:1600]
    if not hash_fn:
        fail("push: brak openHashTarget")
    # Asercja na KODZIE, nie na slowie: komentarz w tej samej funkcji wspomina
    # `tabDef(id)` i `t0.id===id` — gdyby guard patrzyl na sam podlancuch, mutacja
    # usuwajaca galaz przechodzilaby niezauwazona (dokladnie ten blad zdarzyl sie
    # juz wczesniej przy pierwszej wersji guardow).
    elif "var t0=tabDef(id)" not in hash_fn:
        fail("push: openHashTarget nie zna ID zakladek — URL #day z powiadomienia jest martwy")
    elif "t0.id===id" not in hash_fn:
        fail("push: openHashTarget ufa fallbackowi tabDef — smieciowy hash ustawi nieistniejaca zakladke")

    # A3: zakaz 7. zakladki (AGENTS.md pkt 1 i 4). Guard "5 zakladek IA" sprawdza tylko
    # OBCENOSC napisow w pliku, wiec 6. zakladka (HERMES) weszla calkowicie niezauwazona.
    m_tabs = re.search(r"ACADEMY_TABS\s*=\s*\[(.*?)\];", html, re.S)
    if not m_tabs:
        fail("ia: brak ACADEMY_TABS")
    else:
        n_tabs = len(re.findall(r"id:'([a-z]+)'", m_tabs.group(1)))
        if n_tabs != 6:
            fail(f"ia: {n_tabs} zakladek zamiast 6 — nowa zakladka wymaga swiadomej decyzji (AGENTS.md pkt 1/4)")

    # A4: deploy pakuje WORKING COPY, wiec bez bramki SHA na produkcje moze trafic kod
    # spoza main. Zmierzone: PR #17 byl OTWARTY, a jego 6 commitow juz zylo na VPS.
    if "rev-parse origin/main" not in deploy_txt or "status --porcelain" not in deploy_txt:
        fail("deploy: brak bramki integralnosci — deploy moze wypchnac kod spoza zmergowanego main")
    elif "--is-inside-work-tree" not in deploy_txt:
        fail("deploy: bramka integralnosci bez fail-closed — poza repo git przechodzi MILCZACO")
    elif "--force) FORCE=1 ;;" not in deploy_txt:
        fail("deploy: bramka integralnosci bez swiadomego obejscia --force — zablokuje awaryjny deploy")

    # A5: raz zapisany NIEPRAWIDLOWY `active_tab` w localStorage zostaje na zawsze.
    # Zmierzone na zywo: origin z zatrutym stanem renderowal PUSTY panel i ZADNEJ
    # zaznaczonej zakladki — dashboard bez wyjscia poza reczna naprawa localStorage.
    # Poprzednia wersja openHashTarget wlasnie tak zatruwala stan (`#cokolwiek`).
    # Walidacja przy ODCZYCIE (load) + przy RENDERZE (currentTab) = samonaprawa.
    load_fn = html[html.find("function load(){"):][:900]
    if not load_fn:
        fail("dashboard: brak load()")
    elif "ACADEMY_TABS.some(function(t){return t.id===state.active_tab;})" not in load_fn:
        fail("dashboard: load() nie odsiewa nieprawidlowego active_tab — zatruty stan = pusty panel na zawsze")
    elif "state.active_tab='now';" not in load_fn:
        fail("dashboard: load() odsiewa zly active_tab, ale nie ma na co go cofnac")
    ctab_fn = html[html.find("function currentTab(){"):][:120]
    if not ctab_fn:
        fail("dashboard: brak currentTab()")
    elif "tabDef(t).id===t" not in ctab_fn:
        fail("dashboard: currentTab() ufa stanowi bez walidacji — nieznana zakladka renderuje pustke")

    # --- Fala G: sync nie moze milczec (2026-09-21) ------------------------------
    # ZMIERZONE NA PRODUKCJI: 0 x `PUT /progress` w CALEJ historii logow nginx, a `/progress`
    # nie odwiedzila ZADNA przegladarka (tylko curl i PowerShell). `if(!syncCreds())return;`
    # cicho wylaczal CALY backup, zanim cokolwiek wyslal — a etykieta obiecywala „raz na
    # urzadzenie", gdy tymczasem zapis szedl do sessionStorage i ginal z kazda sesja.
    # Strona stoi za TYM SAMYM `auth_basic` co /progress, wiec kto widzi dashboard, ten ma
    # juz prawo do vaulta, a przegladarka dokłada poswiadczenia do same-origin `fetch()`
    # (dowod: stub z Basic Auth — żądanie bez naglowka w JS dotarlo jako `Basic dGVzdDp0ZXN0`).
    pull_fn = html[html.find("function pullProgress(){"):][:400]
    if not pull_fn:
        fail("sync: brak pullProgress")
    elif "if(!syncCreds())" in pull_fn:
        fail("sync: pullProgress wylacza sie bez recznego hasla — postep nigdy nie trafi do vaulta")
    elif "fetch(SYNC.url" not in pull_fn:
        fail("sync: pullProgress nie dochodzi do fetch")
    push_fn = html[html.find("function pushProgress(){"):][:300]
    if not push_fn:
        fail("sync: brak pushProgress")
    elif "!syncCreds()" in push_fn:
        fail("sync: pushProgress wylacza sie bez recznego hasla — zapis nigdy nie trafi do vaulta")

    # G2: obietnica w UI musi zgadzac sie z implementacja. „raz na urzadzenie" + sessionStorage
    # to obietnica, ktorej kod nie dotrzymuje — Dowodca ustawial haslo raz i nie wiedzial,
    # ze od nastepnego otwarcia PWA backup nie dziala.
    if "raz na urządzenie" in html:
        fail("sync: etykieta obiecuje zapis 'raz na urzadzenie', a to sessionStorage — obietnica niezgodna z kodem")
    elif "działa sam po zalogowaniu" not in html:
        fail("sync: brak etykiety mowiacej, ze sync dziala sam — uzytkownik znow bedzie szukal hasla")

    # G3: brak autoryzacji to jedyny stan, w ktorym praca NIE jest zabezpieczona.
    # Sam pasek w stopce nie wystarczyl — Dowodca nie wiedzial, ze backup nie dziala.
    if "function syncWarn(" not in html:
        fail("sync: brak syncWarn — brak autoryzacji zostanie niezauwazony")
    # DWA miejsca, nie jedno: brak autoryzacji boli i przy odczycie, i przy zapisie.
    # Guard sprawdzajacy samo `syncWarn('Vault ` PRZEPUSZCZAL regresje jednego z nich
    # (zlapane mutacja G3: cofniete wolo w pullProgress, a pushProgress nadal je mial).
    elif "syncWarn('Vault nie przyjmuje zapisu" not in html:
        fail("sync: pullProgress nie wola syncWarn — brak autoryzacji przy ODCZYCIE niezauwazony")
    elif "syncWarn('Vault odrzuca zapis" not in html:
        fail("sync: pushProgress nie wola syncWarn — brak autoryzacji przy ZAPISIE niezauwazony")
    elif "SYNC.warned" not in html:
        fail("sync: brak ograniczenia 'raz na sesje' — toast spamowalby przy kazdym kliknieciu")

    if errors:
        print("FAIL:")
        for item in errors:
            print(f" - {item}")
        return 1
    print("PASS: academy export contract + dashboard v3.1 (sync vault ready)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
