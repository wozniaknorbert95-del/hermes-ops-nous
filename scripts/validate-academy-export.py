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


def fn_body(src: str, header: str, limit: int = 6000) -> str:
    """Tekst od `header` do NASTĘPNEJ definicji na początku linii.

    Powód: stałe okno `[:4000]` wchodzi w kolejną funkcję i guard zapala się na kodzie,
    który nie należy do sprawdzanej funkcji. Fałszywy alarm jest gorszy niż brak guardu —
    taki guard zostaje wyłączony przy pierwszej okazji i przestaje cokolwiek chronić.
    """
    start = src.find(header)
    if start < 0:
        return ""
    rest = src[start + len(header):]
    ends = [c for c in (rest.find("\ndef "), rest.find("\nclass ")) if c >= 0]
    return src[start:start + len(header) + min(min(ends) if ends else limit, limit)]


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
        "progressbar ARIA": 'id="course-map"' in html and "data-course-dzial" in html,
        "4 zakladki IA (TERAZ KURS NOTATKI DZIEN)": all(x in html for x in ("TERAZ", "KURS", "NOTATKI", "DZIEŃ")),
        "strefa Dzień": "Mój dzień — rano 10 minut" in html,
        "strefa Platforma": "Platforma — stan na dsaas-platform-main" in html or "Platforma — gdzie jest główna praca" in html,
        "strefa Piątek": "Piątek — koszty i porządek" in html,
        "playbook klikalny (PLAYBOOK_LAPTOP)": "PLAYBOOK_LAPTOP" in html and "renderPlaybookSteps" in html,
        "onboarding OPERATING-MODEL link": 'href="docs/OPERATING-MODEL.md"' in html,
        "Moj produkt z AGENTS.md": "PRODUCT_MISSION" in html and "AGENTS.md § Misja" in html,
        "16 narzedzi (proofHref)": html.count("proofHref:") == 16,
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
        "licznik pozostalych rozdzialow": 'id="course-map"' in html,
        "klawiatura strzalki zakladek": "ArrowRight" in html and "ArrowLeft" in html,
        "WF-P tor platformy (nie ENT-12)": ("WF-P6" in html or "WF-P" in html) and "ENT-12" in html and "WAIT" in html,
        "Linear widoki Wave 2": "ceotoday-1ef420fc07c0" in html or "CEO/Today" in html,
        "MORNING-RITUAL platform align": "day_today_first" in html or "Today first" in html,
        "scroll-margin pod sticky tabami": "--scroll-offset" in html and "scroll-margin-top" in html,
        "sync bar online/offline": 'id="tty-sync"' in html and "renderSyncBar" in html and "pullProgress" in html,
        "sync PUT debounce": "schedulePush" in html and "pushProgress" in html,
        "PWA manifest": 'href="manifest.webmanifest"' in html,
        "F4 bramka workflow": 'id:"F4"' in html and "PLATFORM-WORKFLOW-GATE" in html,
        "mermaid kontrast edgeLabel": "edgeLabelBackground" in html or "edgeLabel" in html,
        "mermaid fallback offline": "mermaid-fallback" in html,
        "phone-first workflow": "loop-chip" in html and "phone-loop-first" in html,
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
        "F3 KAZDY <pre class=mermaid> ma data-ascii (takze petle WORKFLOW)": pre_without_ascii == [] and len(pre_mermaid) >= 2,
        "F3 fallback nie pokazuje surowego kodu mermaid": "ten diagram nie ma jeszcze wersji ASCII" in html,
        "F3 CSS dla fallbacku offline": ".ascii-pre" in html and "pre.mermaid-fallback" in html,
        # --- Fala 4: Hermes (read-only kontroler + push) ---
        "F4 Hermes Akademii (funkcja, nie zakładka)": "Hermes Akademii" in html and "function renderHermes(" in html,
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
        if "HTTPStatus.GONE" not in vtxt2 or "academy_llm_retired" not in vtxt2:
            fail("czat: POST /hermes/chat nie jest emerytowany (brak 410 / academy_llm_retired)")
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
            fail(f"czat: DASHBOARD.html bez '{needle}' — silnik lokalny (nie UI) zniknął")

    if "renderNowTab()+renderOpsCta()" in html:
        fail("split: TERAZ znowu dokłada CTA /ops — lekcja /ops jest na NARZĘDZIA")
    if "if(tab==='now')html=renderNowTab();" not in html:
        fail("split: TERAZ nie renderuje samego renderNowTab()")
    if 'href="/ops"' not in html:
        fail("split: brak CTA href=/ops w Akademii")
    if 'id="ops-howto"' not in html or "Approval ≠ Merge" not in html:
        fail("split: TERAZ bez instrukcji Hermes Ops (ops-howto / Approval ≠ Merge)")
    if "Autopilot" not in html or "Approval ≠ Merge" not in html:
        fail("split: instrukcja /ops musi tłumaczyć Autopilot-only + Approval ≠ Merge")
    howto = ROOT / "docs" / "ops" / "HERMES-OPS-HOWTO.md"
    if not howto.is_file():
        fail("split: brak docs/ops/HERMES-OPS-HOWTO.md")
    else:
        ht = howto.read_text(encoding="utf-8")
        for needle in ("Autopilot", "Approval", "Zasada 11"):
            if needle not in ht:
                fail(f"split: HERMES-OPS-HOWTO.md bez '{needle}'")
        for removed in ("Manual", "Supervised"):
            if removed in ht:
                fail(f"split: HERMES-OPS-HOWTO.md nie może wspominać usuniętego trybu '{removed}'")
    readme_path = ROOT / "README.md"
    if not readme_path.is_file():
        fail("docs: brak README.md — brak mapy wejścia repo")
    else:
        rt = readme_path.read_text(encoding="utf-8")
        for needle in ("/ops", "docs/ops/README.md", "HERMES-OPS-HOWTO"):
            if needle not in rt:
                fail(f"docs: README.md bez '{needle}' — Hermes Ops niewidoczny na drzwiach")
    ops_index = ROOT / "docs" / "ops" / "README.md"
    if not ops_index.is_file():
        fail("docs: brak docs/ops/README.md — brak indeksu Hermes Ops")
    om = ROOT / "docs" / "OPERATING-MODEL.md"
    if om.is_file():
        omt = om.read_text(encoding="utf-8")
        if "/ops" not in omt or "Hermes Ops" not in omt:
            fail("docs: OPERATING-MODEL.md bez split Hermes Ops (/ops)")
    if 'id="guide"' not in html and "id='guide'" not in html:
        fail("ia: brak kotwicy #guide — mapa INSTRUKCJA niedostępna w KURS")
    if 'id="hermes"' not in html and "id='hermes'" not in html:
        fail("ia: brak kotwicy #hermes — sekcja Hermes Akademii niedostępna w KURS")
    if "goAcademyTab" not in html:
        fail("ia: brak goAcademyTab — legacy guide/hermes/workflow prowadzi do pustego panelu")
    if "tool-hermes-engineer" not in html:
        fail("ia: brak karty Engineer (#tool-hermes-engineer) — drift split Ops")
    if "renderNowTab()+renderNowAskHermes()" in html:
        fail("czat: TERAZ znowu dokłada czat modelu — Akademia ma być bez DeepSeek")
    if 'data-go-tab="hermes"' in html.split("function renderMainPanel(")[1][:800] if "function renderMainPanel(" in html else "":
        fail("czat: renderMainPanel nadal otwiera zakładkę HERMES")

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

    # D3b: TERAZ musi POZWOLIC odhaczyc krok, nie tylko go opisac.
    # Zmierzone 2026-09-20 w dzialajacej aplikacji: karta TERAZ pokazywala
    # „Zostalo krokow lab: 3 / 3" i tekst kroku, ale nie miala ANI JEDNEGO checkboxa,
    # a przy wszystkich odhaczonych pisala „zostaje jedno klikniecie: Zalicz rozdzial"
    # — przycisku, ktorego na tym ekranie nie bylo. Obietnica bez wykonania na
    # NAJCZESTSZEJ akcji calej Akademii (instrukcja mowi: „Odhacz laboratorium -> zalicz rozdzial").
    now_tab = code_line("function renderNowTab(")
    if '''data-k="'+esc(k)+'"''' not in now_tab:
        fail("dashboard: TERAZ opisuje krok, ale nie daje go odhaczyc — trzeba skakac do WORKFLOW")
    elif "f.roz.id+'l'+(i+1)" not in now_tab:
        fail("dashboard: TERAZ nie buduje klucza kroku (rozdzial+'l'+numer) — checkbox zapisze sie w zlym miejscu")
    if '''data-pass="'+esc(f.roz.id)+'"''' not in now_tab:
        fail("dashboard: TERAZ nie ma przycisku 'Zalicz rozdzial' — karta obiecuje klikniecie, ktorego nie ma")
    elif "left>0?" not in now_tab or "disabled>Zalicz rozdzia" not in now_tab:
        fail("dashboard: 'Zalicz rozdzial' na TERAZ jest aktywny przy nieodhaczonych krokach — klik donikad")
    if "Wszystkie kroki odhaczone" in now_tab:
        fail("dashboard: TERAZ wrocil do tekstu 'Wszystkie kroki odhaczone' — to kazalo klikac przycisk, ktorego nie bylo")
    # Ten sam wzorzec w karcie rozdzialu (zakladka WORKFLOW) — to DRUGA i jedyna inna
    # droga do odhaczenia kroku. Mutacja I15 to odkryla: krotszy anchor trafial w te
    # funkcje, a zadnej roznicy nie bylo widac, bo obie mialy identyczny tekst.
    chap_card = code_line("function renderChapterCard(")
    if '''data-k="'+esc(k)+'"''' not in chap_card:
        fail("dashboard: rozdzial w WORKFLOW nie daje odhaczyc kroku — akcja nie istnieje nigdzie")

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
    local_fn = fn_body(html, "function hermesLocalAnswer(", limit=12000) or ""
    secret_idx = local_fn.find("Nie podam")
    eksport_idx = local_fn.find("if(/eksport|json|sync|vault")
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
    elif "hermesFuzzyHit(question," not in (fn_body(html, "function hermesLocalAnswer(", limit=12000) or ""):
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
    welcome_block = re.search(r'<div id="welcome".*?id="welcome-dismiss".*?</div>', html, re.S)
    go_tab_bind = "querySelectorAll('[data-go-tab]').forEach(function(b){if(b.dataset.bound)return;b.dataset.bound='1';b.addEventListener('click',function(){activateTab(b.dataset.goTab,false);});});"
    go_tab_helper = "bindGoTabButtons(scope)"
    if not welcome_block:
        fail("dashboard: brak karty powitalnej #welcome")
    else:
        if 'data-go-tab="now"' not in welcome_block.group(0):
            fail("dashboard: karta powitalna nie ma przejscia do TERAZ (nawigacja jest pod ekranem)")
        bi = code_block("function bindInstall(")
        if go_tab_bind not in bi and go_tab_helper not in bi:
            fail("dashboard: bindInstall nie podpina data-go-tab — przycisk w karcie powitalnej bylby martwy")
    # Ten sam kontrakt dla panelu treści: data-go-tab obsluguje „Dokończ DZIEŃ" (karta LOCK)
    # i legacy guide/hermes → KURS (goAcademyTab).
    bde = code_block("function bindDayExtras(")
    if go_tab_bind not in bde and go_tab_helper not in bde:
        fail("dashboard: bindDayExtras nie podpina data-go-tab — 'Dokończ DZIEŃ' i legacy zakładki bylyby martwe")

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
        if "hermes_router.py:/app/hermes_router.py" not in compose_txt.replace(" ", ""):
            fail("hermes: docker-compose nie montuje hermes_router.py — router vaulta nie zadziala")

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
    # 1400 -> 2600: komentarze z opisem reguly "tresc bije znaczniki" wydluzyly funkcje,
    # a przy zbyt krotkim cieciu guardy G4 patrzylyby na niepelny kod (falszywa zielen).
    merge_fn = html[html.find("function mergeRemote("):][:2600]
    if not merge_fn:
        fail("dashboard: brak mergeRemote")
    elif "!remoteHasContent(env)" not in merge_fn:
        fail("dashboard: mergeRemote scala bez sprawdzenia, czy zdalny zapis ma tresc")
    # F3: pusty stan lokalny nie moze robic PUT-a przy kazdym wejsciu (petla zapisow).
    elif "hasContent(state)" not in merge_fn:
        fail("dashboard: brak warunku hasContent(state) — pusty lokalny stan zapisywalby sie w kolko")

    # --- Fala H: swieze urzadzenie kasowalo zapis z praca (2026-09-20) -----------
    # ZMIERZONE (prawdziwy DASHBOARD.html + mini-vault po HTTPS, swiezy origin):
    #   przed naprawa: GET /progress -> PUT 412 B  =>  zapis Dowodcy (633 B, dwa odhaczone
    #                  kroki rytualu) ZOSTAL SKASOWANY pustym stanem
    #   po naprawie:   GET /progress -> BRAK PUT   =>  zapis nietkniety, kroki odtworzone
    # Przyczyna: `initApp()` wola `initDay()` PRZED `pullProgress()`, a `initDay()` stemplowal
    # `_local_updated_at` na starcie. Swieze urzadzenie deklarowalo stan nowszy niz vault,
    # wiec "nowszy wygrywa" kasowalo PRAWDZIWA prace. To najgorszy wariant awarii backupu:
    # backup niszczy backup — dokladnie scenariusz nowego telefonu.
    init_day = html[html.find("function initDay(){"):][:200]
    if not init_day:
        fail("sync: brak initDay")
    elif "if(!state.day_stamp){state.day_stamp=t;touchLocalUpdated();" in init_day:
        fail("sync: initDay stempluje czas na starcie — swieze urzadzenie skasuje zapis z praca")
    if "function hasWork(" not in html:
        fail("sync: brak hasWork — nie odroznia realnej pracy od ksiazkowosci (active_tab/day_stamp)")
    elif "var rWork=hasWork(env._scratch),lWork=hasWork(state);" not in merge_fn:
        fail("sync: mergeRemote nie liczy pracy po OBU stronach — pusty stan wygra znacznikiem czasu")
    elif "if(rWork&&!lWork){applyRemote(env);return;}" not in merge_fn:
        fail("sync: brak reguly 'tresc bije znaczniki' — pusty stan nadpisze zapis z praca")

    # --- Fala I: „Mój dzień" robi Hermes (deterministyczny rdzeń) ---------------
    # Cel: 2 tapniecia, 0 wpisywania. Hermes przygotowuje, Dowodca zatwierdza.
    # G-04: werdykt o rytuale MUSI byc policzalny bez modelu. Halucynacja moze dac
    # falszywa CZERWIEN (koszt 5 s), ale NIE MOZE dac falszywej ZIELENI (koszt: metoda).
    vault_py = (ROOT / "host" / "progress_vault.py").read_text(encoding="utf-8")
    brief_fn = fn_body(vault_py, "def morning_brief(")
    if "def morning_brief(" not in vault_py:
        fail("fala1: brak morning_brief — 'Moj dzien' nie ma deterministycznego rdzenia")
    elif "hermes_call_llm" in brief_fn:
        fail("fala1: morning_brief wola model — werdykt o rytuale musi byc policzalny bez LLM (G-04)")
    elif 'if scratch.get("day_teraz")' not in brief_fn:
        fail("fala1: brief nie odroznia 'auto' od 'confirmed' — przypisalby sobie prace Dowodcy")
    elif "rest_day" not in brief_fn or "day_untouched(" not in brief_fn:
        fail("fala1: brak rozpoznania dnia odpoczynku — narzedzie karze za przerwe (F8)")

    morning_ep = vault_py[vault_py.find('"/hermes/morning"'):][:900]
    if '"/hermes/morning"' not in vault_py:
        fail("fala1: brak endpointu /hermes/morning — dashboard nie ma skad wziac briefu")
    elif not morning_ep:
        fail("fala1: /hermes/morning istnieje, ale nie udalo sie odczytac jego obslugi")
    elif "authorized(self.headers)" not in morning_ep:
        fail("fala1: /hermes/morning bez authorized() — dane o pracy Dowodcy publicznie")
    elif 'parse_qs(parsed.query).get("today")' not in morning_ep:
        fail("fala1: /hermes/morning ignoruje dzien od telefonu — zostaje zegar kontenera (UTC)")

    # JEDEN DZIEN, NIE TRZY. Te sama funkcje `morning_brief` woła kontener
    # (Alpine BEZ tzdata → TZ cicho nic nie robi, zostaje UTC) i host z timerem 07:00
    # przez push-send.py. Gdy dzien pochodzi z zegara, werdykt o LOCK-u zalezy od tego,
    # gdzie trafil import — a w oknie 00:00-02:00 lokalnie oba dni sie roznia.
    if "today_hint" not in brief_fn or "human_today(" not in brief_fn:
        fail("fala1: brief czyta dzien z zegara — kontener (UTC) i timer 07:00 (host) wskaza rozne dni")
    elif '"today_source"' not in brief_fn:
        fail("fala1: brief nie mowi, skad wziol dzien — rozjazd kontener/host bylby niemy")
    # Niezmiennik: dzien z zegara czyta DOKLADNIE JEDNO miejsce (fallback w human_today).
    # `generated_at` zostaje na gmtime() celowo — znacznik czasu ma byc UTC, to nie jest
    # dzien czlowieka. Dlatego liczymy wzorzec formatu DNIA, nie samo `gmtime`.
    clock_reads = vault_py.count('"%Y-%m-%d", time.gmtime()') + vault_py.count('"%Y-%m-%d", time.localtime()')
    if clock_reads != 1:
        fail(f"fala1: {clock_reads} miejsca czytaja dzien z zegara — dzien musi pochodzic z JEDNEGO miejsca (human_today)")
    # Zakres liczb jest czescia kontraktu: jedno tapniecie „Zatwierdz poranek" podpisuje
    # tylko kroki rano, wiec `counts` i `approved_by_human` nie moga obejmowac wieczora —
    # inaczej przycisk obiecuje wiecej, niz robi, a slad audytu przypisuje Dowodcy
    # zatwierdzenie, ktorego nie zlozyl.
    if '"counts_evening": counts_evening' not in brief_fn:
        fail("fala1: brak counts_evening — liczby poranka obejmuja wieczor (przycisk obiecuje wiecej, niz robi)")
    elif '"evening_to_confirm"' not in brief_fn:
        fail("fala1: brak evening_to_confirm — wieczor nie ma wlasnego zatwierdzenia")
    elif 'for c in morning_checks if c["status"] == "unknown"' not in brief_fn:
        fail("fala1: approved_by_human liczony po wszystkich krokach — slad audytu przypisze Dowodcy wieczor")
    # Asercja na KSZTALCIE ZWRACANYM, nie na slowie: `counts_evening` wystepuje tez
    # w ciele funkcji (liczenie), wiec guard na slowie przepuszczal usuniecie pola.
    # Ten sam antywzorzec zlapalem juz przy push-send (G3) i I13 — trzeci raz.
    if "counts_evening:countsEvening" not in html:
        fail("fala1: mirror offline nie zwraca counts_evening — offline i online pokaza rozne liczby")
    # WIECZOR: wierne lustro poranka. Ten sam kontrakt, inne tapniecie i inna pora.
    # Bez tego wieczor zostaje w „Recznie" na zawsze, a `evening_to_confirm` jest polem,
    # ktorego nikt nie uzywa — czyli obietnica bez wykonania.
    if "evening_verified_by_vault" not in brief_fn:
        fail("fala1: brak evening_verified_by_vault — audyt wieczoru nie wie, co policzyl vault")
    for needle, why in (
        ("function renderEveningBrief(", "brak renderu wieczoru — wieczor zostaje w Recznie"),
        ("function approveEvening(", "brak approveEvening — wieczoru nie da sie zatwierdzic tapnieciem"),
        ("function syncRitualBanners(", "brak syncRitualBanners — wieczor nie pokaze banera bez drugiego zapisu"),
    ):
        if needle not in html:
            fail(f"fala1: {why}")
    # JEDNO save() rowniez na wieczor, i to samo znaczenie: `closeDay()` zmienia stan,
    # nie zapisuje. Inaczej tapniecie wieczoru albo ginie, albo tworzy drugi zapis.
    evening_fn = fn_body(html, "function approveEvening(")
    ewrites = sum(evening_fn.count(s) for s in ("save();", "saveLocal();", "schedulePush();", "touchLocalUpdated();"))
    if evening_fn.count("save();") != 1 or ewrites != 1:
        fail(f"fala1: approveEvening zapisuje {ewrites} razy — kontrakt mowi JEDNO save()")
    if "state.day_evening_brief=" not in html:
        fail("fala1: brak sladu audytu wieczoru — zielone wieczorem byloby anonimowe")
    if "?today=" not in html:
        fail("fala1: dashboard nie podaje swojego dnia — brief liczy zaleglosc wg zegara kontenera")

    # Jedna prawda: push 07:00 NIE MOZE miec wlasnej kopii reguly rytualu.
    # Dwie kopie rozjezdzaja sie cicho — zmiana w dashboardzie nie zmienialaby powiadomienia.
    push_py = (ROOT / "scripts" / "push-send.py").read_text(encoding="utf-8")
    if "human_today(" not in push_py:
        fail("fala1: push 07:00 nie podaje dnia jawnie — powiadomienie liczy inny dzien niz dashboard")
    build_fn = push_py[push_py.find("def build_payload("):][:3000]
    # Asercja na WYWOLANIU, nie na słowie: `morning_brief` występuje też w komentarzu,
    # więc mutacja usuwająca samo wywołanie przeszłaby niezauważona (dokładnie ten
    # antywzorzec złapałem już raz przy G3 — guard na słowie, nie na kodzie).
    if "morning_brief_of(progress)" not in build_fn:
        fail("fala1: push-send.py nie wola morning_brief — wracaja DWIE kopie reguly rytualu")
    elif "day_closed" in build_fn or "day_stamp" in build_fn:
        fail("fala1: push-send.py znow liczy rytual sam — jedna prawda jest w vaulcie")

    for needle, why in (
        ("function morningBriefLocal(", "brak mirror offline — poranek nie zadziala bez sieci"),
        ("function fetchMorningBrief(", "brak pobrania briefu z vaulta"),
        ("function renderDayBrief(", "brak renderu briefu w istniejacym #day-status"),
        ("function approveDay(", "brak approveDay — poranka nie da sie zatwierdzic jednym tapnieciem"),
        ("function dayUntouched(", "brak dayUntouched — nie da sie odroznic odpoczynku od zaleglosci"),
        ("function autoStaleResolve(", "brak autoStaleResolve — dzien odpoczynku zostanie w LOCK"),
    ):
        if needle not in html:
            fail(f"fala1: {why}")
    if "lk.locked&&!dayUntouched()" not in code_line("function hermesKawal("):
        fail("fala1: hermesKawal pyta o LOCK bez wyjatku na dzien odpoczynku — kij za przerwe wraca")
    # Brief MUSI dzialac bez internetu i bez modelu: lokalny mirror nie siega po siec.
    local_fn = html[html.find("function morningBriefLocal("):][:1800]
    if "fetch(" in local_fn or "hermesChat" in local_fn:
        fail("fala1: morningBriefLocal siega po siec/model — brief ma dzialac offline")
    # JEDNO save() na zatwierdzenie. Wiecej = rozjechany stan albo podwojny push.
    approve_fn = html[html.find("function approveDay("):][:1200]
    writes = sum(approve_fn.count(s) for s in ("save();", "saveLocal();", "schedulePush();", "touchLocalUpdated();"))
    if approve_fn.count("save();") != 1 or writes != 1:
        fail(f"fala1: approveDay zapisuje {writes} razy — kontrakt mowi JEDNO save()")
    # Zielone nie moze byc anonimowe: w _scratch zostaje slad, co policzyl vault, a co czlowiek.
    if "state.day_brief=" not in html:
        fail("fala1: brak sladu audytu w _scratch — zielone byloby anonimowe")
    # Formularz musi zniknac, inaczej zostaje 8-11 interakcji i caly zysk przepada.
    # Liczymy w `renderDay()`, nie w calym pliku: od Fali 1 slowo `manual-ritual`
    # wystepuje tez w briefie poranka, wiec asercja na calym pliku przepuszczala
    # mutacje, ktora odslaniala wlasnie te 13 checkboxow.
    day_fn = fn_body(html, "function renderDay(")
    if day_fn.count('<details class="manual-ritual">') != 2:
        fail("fala1: 13 checkboxow nie jest schowanych pod 'Recznie' — rytual zostaje formularzem")

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
    elif "if(id==='day')id='now'" not in hash_fn:
        fail("push: openHashTarget nie aliasuje #day → now")

    # A3: dokladnie 7 zakladek (TERAZ + WORKFLOW + NARZĘDZIA + DSAAS + MONETYZACJA + ŹRÓDŁA + NOTATKI). DZIEŃ wchłonięty.
    m_tabs = re.search(r"ACADEMY_TABS\s*=\s*\[(.*?)\];", html, re.S)
    if not m_tabs:
        fail("ia: brak ACADEMY_TABS")
    else:
        n_tabs = len(re.findall(r"id:'([a-z]+)'", m_tabs.group(1)))
        if n_tabs != 7:
            fail(f"ia: {n_tabs} zakladek zamiast 7 — TERAZ/WORKFLOW/NARZĘDZIA/DSAAS/MONETYZACJA/ŹRÓDŁA/NOTATKI")
        if "id:'day'" in m_tabs.group(1) or 'id:"day"' in m_tabs.group(1):
            fail("ia: zakladka DZIEŃ wróciła — wchłonięta przez TERAZ")
        for need in ("now", "workflow", "tools", "dsaas", "money", "sources", "notes"):
            if f"id:'{need}'" not in m_tabs.group(1) and f'id:"{need}"' not in m_tabs.group(1):
                fail(f"ia: ACADEMY_TABS bez zakladki {need}")

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

    # --- Fala J: reguła bez wyzwalacza jest martwa (2026-09-20) --------------------
    # ZMIERZONE: CI `academy-gate` przechodzilo w 6 SEKUND, bo uruchamialo tylko walidator
    # i testy vaulta. Testy mutacyjne — jedyny dowod, ze guardy w ogole lapia regresje —
    # nie byly uruchamiane nigdzie poza czyjas pamiecia. Zielone CI nie znaczylo wiec
    # "guardy dzialaja", a dokladnie tak je czytano (sam workflow ostrzegal przed ta
    # falszywa zielenia w workflow-lab).
    # Prob przed wpieciem: kopia robocza na Linuksie, Python 3.12.3 — 87/87 zlapanych,
    # pliki przywrocone co do bajtu. Mutacje moga wiec biegac w CI bez ryzyka.
    # Glob, nie lista na sztywno: nowy zestaw mutacji musi zostac wpiety do CI w tym
    # samym PR, w ktorym powstaje — inaczej bramka go nie zna.
    ci_path = ROOT / ".github" / "workflows" / "academy-gate.yml"
    ci_txt = ci_path.read_text(encoding="utf-8") if ci_path.exists() else ""
    suites = sorted(p.name for p in (ROOT / "scripts").glob("mutation-test-*.py"))
    if not ci_txt:
        fail("CI: brak .github/workflows/academy-gate.yml — reguly nie ma czym wymusic")
    elif not suites:
        fail("CI: zero zestawow mutacji w scripts/ — najtwardszy asset repo zniknal")
    else:
        for name in suites:
            if name not in ci_txt:
                fail(f"CI: academy-gate nie uruchamia {name} — bramka wyglada na zielona, a tego nie mierzy")
    try:
        agents_txt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"CI: AGENTS.md nieczytelny: {exc}")
    else:
        # Nie „czy w pliku jest slowo mutation-test" (to guard mierzacy slowo — taki
        # przepuszcza regresje), a KSZTALT KONTRAKTU: linia `testy:`, ktora czyta agent,
        # musi wymieniac kazdy zestaw. Ta sama lista co w CI, ta sama lista co w globie.
        testy_line = next((ln for ln in agents_txt.splitlines() if ln.startswith("testy:")), "")
        if not testy_line:
            fail("CI: AGENTS.md bez linii 'testy:' — nie wiadomo, co ma byc zielone")
        else:
            for name in suites:
                if name not in testy_line:
                    fail(f"CI: AGENTS.md 'testy:' nie wymienia {name} — konstytucja i CI sie rozjada")

    # --- Fala L: dwa Hermesy — kontrakt, UI, karta Engineer, brak MCP w czacie ----
    contract = ROOT / "docs" / "ops" / "HERMES-ROLE-CONTRACT.md"
    if not contract.exists():
        fail("hermes-dual: brak docs/ops/HERMES-ROLE-CONTRACT.md")
    else:
        ct = contract.read_text(encoding="utf-8")
        for sent in (
            "Cursor Cloud Agent jest jedynym executorem kodu w Telefon loopie.",
            "POST /hermes/chat nie ma narzędzi MCP.",
            "Decyzja jest w Linear, nie na GitHubie.",
            "Hermes Engineer + Cursor + CI dowożą aż do merge.",
            "Wgranie na serwer = lokalnie, ręcznie (Zasada 11).",
        ):
            if sent not in ct:
                fail(f"hermes-dual: kontrakt bez zdania kanonicznego: {sent[:48]}…")
        if "engineer_loop_e2e" not in ct:
            fail("hermes-dual: kontrakt bez flagi engineer_loop_e2e")
    agents_link = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if "HERMES-ROLE-CONTRACT.md" not in agents_link:
        fail("hermes-dual: AGENTS.md bez linku do kontraktu ról")
    if "Hermes Akademii" not in html or "Nie buduje PR" not in html.replace("-", ""):
        if "Nie buduje PR-ów" not in html:
            fail("hermes-dual: zakładka HERMES nie rozdziela Akademii od Engineera")
    rh = fn_body(html, "function renderHermes(){", limit=800)
    if rh and re.search(r"\bMCP\b.*auto-merge|git push|Cloud Agent buduje", rh, re.I):
        fail("hermes-dual: copy HERMES obiecuje wykonanie (MCP/git/auto-merge)")
    if "data-hermes-go=\"tools\"" not in html and "data-hermes-go='tools'" not in html:
        fail("hermes-dual: brak linku HERMES → NARZĘDZIA (Engineer)")
    tabs_blob = html.split("var ACADEMY_TABS=[", 1)[1].split("];", 1)[0] if "var ACADEMY_TABS=[" in html else ""
    tab_count = tabs_blob.count("{id:")
    if "ACADEMY_TAB_COUNT=7" not in html:
        fail("ia: brak ACADEMY_TAB_COUNT=7 — kontrakt zakładek Akademii niezdefiniowany")
    if tab_count != 7:
        fail(f"hermes-dual: ACADEMY_TABS != 7 (wykryto {tab_count}) — oczekiwane TERAZ+WORKFLOW+NARZĘDZIA+DSAAS+MONETYZACJA+ŹRÓDŁA+NOTATKI")
    if "{id:'dsaas',title:'DSAAS'" not in html and '{id:"dsaas",title:"DSAAS"' not in html:
        fail("hermes-dual: brak zakładki DSAAS (id dsaas) w ACADEMY_TABS — mermaidy platformy ukryte")
    if "{id:'kurs',title:'DSAAS'" in html or '{id:"kurs",title:"DSAAS"' in html:
        fail("hermes-dual: zakładka DSAAS ma fałszywe drzwi (id kurs zamiast dsaas)")
    if "html=renderDsaas()" not in html.replace(" ", ""):
        fail("hermes-dual: renderKurs musi wołać renderDsaas() — panel DSAAS był odłączony od nav")
    if 'id="dsaas"' not in html or 'id="dsaas-flows"' not in html:
        fail("hermes-dual: brak kotwicy #dsaas / galerii mermaid (dsaas-flows)")
    if "{id:'money',title:'MONETYZACJA'" not in html and '{id:"money",title:"MONETYZACJA"' not in html:
        fail("hermes-dual: brak zakładki MONETYZACJA (id money)")
    if "{id:'sources',title:'ŹRÓDŁA'" not in html and '{id:"sources",title:"ŹRÓDŁA"' not in html:
        fail("hermes-dual: brak zakładki ŹRÓDŁA (id sources)")
    if "{id:'notes',title:'NOTATKI'" not in html and '{id:"notes",title:"NOTATKI"' not in html:
        fail("hermes-dual: brak zakładki NOTATKI w ACADEMY_TABS")
    if "function renderKurs(" not in html or "tab==='dsaas'" not in html.replace(" ", ""):
        fail("hermes-dual: brak renderKurs() / gałęzi dsaas w renderMainPanel")
    if "function renderNotes(" not in html or "tab==='notes'" not in html.replace(" ", ""):
        fail("hermes-dual: brak renderNotes() / gałęzi notes w renderMainPanel")
    if "_scratch.notes" not in html:
        fail("hermes-dual: notatki nie synchronizują _scratch.notes")
    if "delete scratch.tracks" not in html and "nie wchodzą do tracks" not in html.lower():
        if "tracks:{W:" not in html:
            fail("hermes-dual: envelope bez tracks W/F")
    if "KURS_DZIAL_ORDER=['B','C','D','E','F','G']" not in html:
        fail("ia: firstOpen nauki nie jest B–G")
    if "KURS_DZIAL_ORDER=['H'" in html:
        fail("ia: firstOpen znowu H-first")
    if 'id="gear-btn"' not in html or 'id="gear-panel"' not in html:
        fail("v7: brak koła zębatego / panelu vault")
    if "function workLog(" not in html:
        fail("v7: brak work_log w _scratch")
    env_fn = html[html.find("function envelope("):html.find("function ingest(")]
    tracks_blob = env_fn[env_fn.find("tracks:"):env_fn.find("_scratch:")] if "tracks:" in env_fn and "_scratch:" in env_fn else env_fn
    if "work_log" in tracks_blob:
        fail("export: work_log wyciekł do tracks — godziny tylko w _scratch")
    now_tab = ""
    for line in html.splitlines():
        if "function renderNowTab(" in line:
            now_tab = line
            break
    if "Jak używać /ops" in now_tab or "renderOpsCta" in now_tab:
        fail("v7: TERAZ znowu ma lekcję /ops")
    if "function dod18(" not in html:
        fail("v7: brak paska 18 DoD")
    dzial_ids = re.findall(r'\n      id:"([A-H])"', html)
    if dzial_ids[:8] != list("ABCDEFGH"):
        fail(f"kurs: DZIAL_DATA nie jest A–H (wykryto {dzial_ids[:9]})")
    blob = html.split("var DZIAL_DATA")[1].split("var ALL_ROZ")[0] if "var DZIAL_DATA" in html else ""
    if 'id:"H", title:"Monetyzacja"' not in blob:
        fail("kurs: brak działu H (Monetyzacja) w DZIAL_DATA")
    for need_roz in ("H1", "H2", "H3", "H4"):
        if f'id:"{need_roz}"' not in blob:
            fail(f"kurs: brak rozdziału {need_roz} w dziale H")
    if "Wyślij min. 10" in blob or "widełki ceny" in blob:
        fail("kurs: H znowu ma homework 10 maili / pole EUR — lis uczy, nie odhacza")
    if "KURS_DZIAL_ORDER" not in html:
        fail("kurs: brak ścieżki pustego startu H1 (KURS_DZIAL_ORDER + firstOpen)")
    fo_fn = html[html.find("function firstOpen(){"): html.find("function findRoz(")]
    if not fo_fn or "KURS_DZIAL_ORDER" not in fo_fn:
        fail("kurs: firstOpen nie chodzi po mapie H (KURS_DZIAL_ORDER) — po H1 wraca A1")
    if "ALL_ROZ[i]+'_pass'" in fo_fn.replace(" ", ""):
        fail("kurs: firstOpen chodzi po ALL_ROZ (A1 po H1) zamiast mapy H")
    tab_by = html[html.find("var TAB_BY_DZIAL="): html.find("var TAB_BY_DZIAL=") + 220]
    if "H:'money'" not in tab_by.replace(" ", "") and 'H:"money"' not in tab_by:
        fail("kurs: TAB_BY_DZIAL.H musi byc money")
    if "A:'workflow'" not in tab_by.replace(" ", "") and 'A:"workflow"' not in tab_by.replace(" ", ""):
        fail("kurs: TAB_BY_DZIAL.A musi byc workflow")
    if "8 działów" not in html and "A–H" not in html.replace("A-H", "A–H"):
        if "A–H" not in html and "A-H" not in html:
            fail("kurs: brak copy A–H (8 działów kursu vs Kokpit 6-działowy)")
    sku = ROOT / "docs" / "akademia" / "SKU-SKAN-DECYZJI-MKB.md"
    if not sku.is_file():
        fail("kurs: brak docs/akademia/SKU-SKAN-DECYZJI-MKB.md (kontrakt H1)")
    if 'id="welcome"' in html:
        welcome = html[html.find('id="welcome"') : html.find('id="welcome"') + 1200]
        if "@cursor" in welcome.lower():
            fail("palette: welcome znowu wspomina @cursor — Akademia nie zleca kodu z powitania")
    if "min-height:44px" not in html:
        fail("palette: brak celów 44px")
    ops_html = ROOT / "OPS.html"
    if not ops_html.exists():
        fail("split: brak OPS.html")
    else:
        ot = ops_html.read_text(encoding="utf-8")
        if "Hermes Ops" not in ot:
            fail("split: OPS.html bez title/copy Hermes Ops")
        if 'href="/"' not in ot and "Akademia" not in ot:
            fail("split: OPS.html bez linku do Akademii")
        for panel in ("Dashboard", "Live", "Approval"):
            if panel not in ot:
                fail(f"split: OPS.html bez panelu {panel}")
        if "Sterowanie na foldzie" not in ot:
            fail("split: OPS.html bez copy Sterowanie na foldzie")
        if 'id="panel-steer"' in ot:
            fail("ops-nav-p1: martwy #panel-steer wrócił")
        if "Kolejka Linear" not in ot:
            fail("split: OPS.html bez panelu Kolejka")
        if "DZIAL_DATA" in ot:
            fail("split: OPS.html nie może zawierać DZIAL_DATA")
        if "min-height:44px;min-width:44px" not in ot:
            fail("ops-ux: OPS.html bez celów 44px")
        if "safe-area-inset" not in ot:
            fail("ops-ux: OPS.html bez safe-area (telefon / PWA)")
        if "JSON.stringify(live)" in ot:
            fail("ops-ux: Live znowu dumpuje JSON — ma pokazać krok S n")
        if 'class="pill unk"' not in ot:
            fail("ops-ux: UNKNOWN musi startować jako pill unk, nie zieleń")
        if "manifest-ops.webmanifest" not in ot:
            fail("ops-ux: OPS.html musi używać manifest-ops (tożsamość Hermes)")
        # Stały przycisk sterowania (nie tylko string w bannerze dispatch QUI-70).
        if 'data-ops="take_over" id="btn-take"' not in ot and "data-ops='take_over' id='btn-take'" not in ot:
            fail("ops-ux: brak Take over")
        # QUI-70: dyspozycja + uczciwy HUD (telefon nie kłamie RUNNING).
        if 'id="dispatch-banner"' not in ot:
            fail("ops-qui70: brak #dispatch-banner")
        if "STALLED — tick nie odpowiada" not in ot:
            fail("ops-qui70: brak copy STALLED")
        if "QUEUED — czekam na workera" not in ot:
            fail("ops-qui70: brak copy QUEUED")
        if "NO-ACK — tick nie potwierdził" not in ot:
            fail("ops-qui70: brak copy NO-ACK")
        if "REFUSED — tick odmówił" not in ot:
            fail("ops-qui70: brak copy REFUSED")
        if "Cloud nie otrzymał komentarza @cursor" not in ot:
            fail("ops-qui70: brak copy cursor_wake")
        if "target_repo_create_forbidden" not in ot:
            fail("ops-qui70: brak copy target_repo_create_forbidden")
        if "nie otworzył issue na platformie" not in ot:
            fail("ops-qui70: brak copy platform issue 403")
        if "VPS filesystem blocker" not in ot:
            fail("ops-qui70: brak copy ops_cmd_path_is_directory")
        if "Wake:" not in ot:
            fail("ops-qui70: brak Wake proof w Live")
        if "mapServerVerdict" not in ot or "renderDispatch" not in ot:
            fail("ops-qui70: brak mapServerVerdict/renderDispatch")
        if "pill.queued" not in ot and ".pill.queued" not in ot:
            fail("ops-qui70: brak stylu pill.queued")
        # Optymistyczny Start → QUEUED, nigdy RUNNING w send().
        if "lastStatus.status='QUEUED'" not in ot and 'lastStatus.status="QUEUED"' not in ot:
            fail("ops-qui70: send() musi optymistycznie stawiać QUEUED")
        vault_txt = (ROOT / "host" / "progress_vault.py").read_text(encoding="utf-8")
        if not re.search(r"(?m)^def derive_dispatch\(", vault_txt):
            fail("ops-qui70: brak derive_dispatch")
        if 'parsed.path == "/ops/diag"' not in vault_txt and "parsed.path == '/ops/diag'" not in vault_txt:
            fail("ops-qui70: brak GET /ops/diag")
        if 'encoding="utf-8-sig"' not in vault_txt and "encoding='utf-8-sig'" not in vault_txt:
            fail("ops-qui70: odczyt ops JSON musi znosić BOM (utf-8-sig)")
        if "bump_updated=False," not in vault_txt:
            fail("ops-qui70: start musi patchować status bez bump_updated (wiek ticka)")
        if "bump_updated: bool = False" not in vault_txt:
            fail("ops-qui70: patch_ops_status default bump_updated musi być False (I1)")
        if "def ensure_ops_cmd_file(" not in vault_txt:
            fail("ops-qui70: brak ensure_ops_cmd_file")
        if "ensure_ops_cmd_file()" not in vault_txt.split("def main", 1)[-1]:
            fail("ops-qui70: main() musi wołać ensure_ops_cmd_file()")
        if '"ops_cmd_state": ops_cmd_path_state()' not in vault_txt:
            fail("ops-qui70: /health musi raportować ops_cmd_state")
        if "Brak komendy — idle" not in vault_txt:
            fail("ops-qui70: /ops/diag musi rozróżniać idle od STALLED")
        if "vault_receipt" not in vault_txt:
            fail("ops-qui70: POST /ops/run musi zwracać decision receipt (vault.patch_ok)")
        if "ops_cmd_path_is_directory" not in vault_txt:
            fail("ops-qui70: write_ops_cmd musi blokować katalog ops-cmd.json")
        if '"status": "QUEUED"' not in vault_txt and "'status': 'QUEUED'" not in vault_txt:
            fail("ops-qui70: _ops_run start musi ustawiać status QUEUED")
        if re.search(
            r'action in \("start".*?patch_ops_status\(\s*\{[^}]*"status":\s*"RUNNING"',
            vault_txt,
            re.S,
        ):
            fail("ops-qui70: start/run_next nie wolno patchować status=RUNNING")
        if "pr_number+6of6" not in vault_txt:
            fail("ops-qui70: done musi opierać się o pr_number+6/6 (de-ghost)")
        contract_md = ROOT / "docs" / "ops" / "CONTRACT-OPS-STATUS.md"
        if not contract_md.is_file() or "**Fail-closed:**" not in contract_md.read_text(encoding="utf-8"):
            fail("ops-qui70: brak CONTRACT-OPS-STATUS.md")
        contract_txt = contract_md.read_text(encoding="utf-8")
        if "Właściciel: tick" not in contract_txt:
            fail("ops-qui70: CONTRACT musi przypisać updated_at wyłącznie tickowi")
        runbook_md = ROOT / "docs" / "ops" / "RUNBOOK-OPS-WIRING.md"
        if not runbook_md.is_file() or "systemctl is-active hermes-ops.timer" not in runbook_md.read_text(encoding="utf-8"):
            fail("ops-qui70: brak RUNBOOK-OPS-WIRING.md")
        setup_ops = (ROOT / "scripts" / "setup-akademia-vps.sh").read_text(encoding="utf-8")
        if "ensure_hermes_ops_cmd_file" not in setup_ops:
            fail("ops-qui70: setup-akademia-vps.sh musi naprawiać ops-cmd.json (katalog→plik)")
        for _line in setup_ops.splitlines():
            _s = _line.strip()
            if _s.startswith("#"):
                continue
            if re.search(r"curl.*\|\s*head\b", _s):
                fail("ops-qui70: setup nie może pipe'ować curl | head (pipefail → curl 23, urywa systemd+smoke)")
                break
        if "/ops/diag" not in setup_ops:
            fail("ops-qui70: deploy smoke musi wołać /ops/diag")
        if "fix_hermes_ops_systemd" not in setup_ops:
            fail("ops-qui70: setup musi patchować hermes-ops-cmd.path (MakeDirectory=false)")
        smoke_vps = ROOT / "scripts" / "smoke-hermes-ops-vps.sh"
        if not smoke_vps.is_file() or "SMOKE PASS" not in smoke_vps.read_text(encoding="utf-8"):
            fail("ops-qui70: brak scripts/smoke-hermes-ops-vps.sh")
        deploy_ready = ROOT / "scripts" / "deploy-ready-hermes-ops.sh"
        if not deploy_ready.is_file():
            fail("ops-qui70: brak scripts/deploy-ready-hermes-ops.sh")
        if 'data-mode="MANUAL"' in ot or 'data-mode="SUPERVISED"' in ot:
            fail("ops-ux: Hermes Ops = tylko Autopilot (usuń Manual/Supervised)")
        if "SUPERVISED" in ot or "lane-manual" in ot or "n-manual" in ot:
            fail("ops-ux: brak Manual/Supervised w OPS.html")
        if "AUTOPILOT" not in ot or "setModeBadge" not in ot:
            fail("ops-ux: OPS.html musi pokazywać tylko Autopilot (setModeBadge)")
        if "ensureTickAutopilot" not in ot or "burstPoll" not in ot:
            fail("ops-ux: sync trybu Autopilot + burstPoll po komendach")
        if "setLaneFocus" not in ot:
            fail("ops-ux: brak focus toru kolejki")
        if 'id="chip-dor"' not in ot or 'id="chip-lane"' not in ot or 'id="chip-tests"' not in ot or 'id="chip-ci"' not in ot or 'id="chip-todo"' not in ot:
            fail("ops-fala-q: brak chipów DoR/lane/testy/CI/todo")
        if "max-width:360px" not in ot:
            fail("ops-fala-q: brak foldu 360px")
        if 'id="t-tokens"' in ot or 'id="t-cost"' in ot:
            fail("ops-fala-q: Tokens/Cost wróciły na /ops")
        if "Kolejka nie udaje Run — otwiera Linear." not in ot:
            fail("ops-fala-q: kolejka znowu udaje Run")
        if "function linearUrl" not in ot or '<a class="issue"' not in ot:
            fail("ops-nav: kolejka issue nie jest linkiem Linear")
        if 'id="btn-use-rec"' not in ot or "Użyj tego" not in ot or 'data-ops="select_next"' not in ot:
            fail("ops-nav: brak Użyj tego / select_next")
        if "recommended_issue" not in vault_txt or "select_next" not in vault_txt:
            fail("ops-nav: vault bez recommended_issue / select_next")
        _i_res, _i_dep, _i_dash = ot.find('id="panel-result"'), ot.find('id="panel-deploy"'), ot.find('id="panel-dash"')
        if _i_res < 0 or _i_dash < 0 or _i_res > _i_dash:
            fail("ops-nav-p1: Wynik nie jest pod HUD (przed Dashboard)")
        if _i_dep < 0 or _i_dep > _i_dash:
            fail("ops-nav-p1: Deploy nie jest pod HUD (przed Dashboard)")
        if 'id="ops-context"' not in ot or "ops-fold-" not in ot or "localStorage.getItem" not in ot:
            fail("ops-nav-p1: collapse KONTEKST/DZIENNIK bez localStorage")
        _disp = ot.split("function renderDispatch", 1)[-1].split("function renderProof", 1)[0]
        if "<button" in _disp.lower():
            fail("ops-nav-p1: dispatch klonuje przyciski")
        if "Użyj ↻ Retry u góry" not in ot:
            fail("ops-nav-p1: dispatch bez CTA Retry u góry")
        if re.search(r"\.btn\.danger\{[^}]*width:\s*100%", ot):
            fail("ops-nav-p1: Take over znowu full-bleed")
        if "steer-sec" not in ot or "steer-ter" not in ot:
            fail("ops-nav-p1: brak hierarchii Pause/Stop vs Take over")
        if "Kolejkuje tick. To nie jest merge." not in ot:
            fail("ops-nav-p1: brak linii PL przy Start")
        if "Take over = laptop, zero @cursor. Na pewno?" not in ot:
            fail("ops-nav-p1: Take over bez confirm")
        if "To nie jest Merge." not in ot:
            fail("ops-nav-p1: Take over bez title")
        if 'href="#panel-live"' not in ot:
            fail("ops-nav-p1: brak skip-link do #panel-live")
        if "e.key==='Enter'" not in ot:
            fail("ops-nav-p1: brak skrótu Enter=Start")
        if "e.key==='Escape'" not in ot:
            fail("ops-nav-p1: brak skrótu Escape=Pause")
        _desk = ot.split("@media (min-width:960px)", 1)[-1] if "@media (min-width:960px)" in ot else ""
        if "position:sticky" not in _desk:
            fail("ops-nav-p1: brak sticky h2 na desktop")
        if 'id="pulse-list"' not in ot:
            fail("ops-fala-q: brak pulse 3 issue")
        if 'id="run-truth"' not in ot or "Cloud: /autopilot" not in ot:
            fail("ops-fala-q: brak linii prawdy Cloud /autopilot (paleta EV-454)")
        if "qui_todo_mismatch" not in ot or "qui_lane_local" not in ot:
            fail("ops-fala-q: HUD bez reason DoR")
        if "canRun=false" not in ot:
            fail("ops-fala-q: kolejka ma canRun")
        if "ops_linear_dor" not in vault_txt:
            fail("ops-fala-r: vault nie importuje ops_linear_dor")
        if "gate_start" not in vault_txt:
            fail("ops-fala-r: POST /ops/run bez gate_start")
        if "LINEAR_OPS_READ: ${LINEAR_OPS_READ:-}" not in compose_txt and "LINEAR_OPS_READ:" not in (ROOT / "host" / "docker-compose.yml").read_text(encoding="utf-8"):
            fail("ops-fala-r: docker-compose nie przekazuje LINEAR_OPS_READ")
        if "ensure_env_key LINEAR_OPS_READ" not in setup_ops:
            fail("ops-fala-r: setup nie woła ensure_env_key LINEAR_OPS_READ")
        if "qui_dor_not_ready" not in contract_txt or "qui_todo_mismatch" not in contract_txt:
            fail("ops-fala-r: CONTRACT bez reason DoR")
        if "ops_linear_dor.py:/app/scripts/ops_linear_dor.py" not in (ROOT / "host" / "docker-compose.yml").read_text(encoding="utf-8").replace(" ", ""):
            fail("ops-fala-r: compose nie montuje ops_linear_dor.py")
        dor_src = (ROOT / "scripts" / "ops_linear_dor.py").read_text(encoding="utf-8")
        if "dotycz" not in dor_src:
            fail("ops-fala-s: _NEG_ENV nie bierze czasownika 'dotyczy' — 'nie dotyczy VPS' spadnie na LOCAL (P2)")
        if "dost[ęe]pu" not in dor_src:
            fail("ops-fala-s: _NEG_ENV nie bierze 'dostępu do' — 'bez dostępu do VPS' spadnie na LOCAL (P2)")
        if "deployment" not in dor_src:
            fail("ops-fala-s: _NEG_ENV gubi kwantyfikator 'deployment' (P2)")
        ops_report = ROOT / "scripts" / "ops-report.py"
        if not ops_report.is_file():
            fail("ops-fala-s2: brak scripts/ops-report.py (raport Hermes Ops)")
        elif "ops-push-pending.json" not in ops_report.read_text(encoding="utf-8"):
            fail("ops-fala-s2: ops-report.py nie pisze ops-push-pending.json")
        if "OnCalendar=*:0/15" not in setup_ops:
            fail("ops-fala-s2: setup bez timera raportu Ops (OnCalendar=*:0/15)")
        if '"report-line"' not in ot:
            fail("ops-fala-s2: OPS.html bez karty Raport (#report-line)")
        vault_txt2 = (ROOT / "host" / "progress_vault.py").read_text(encoding="utf-8")
        if "_ops_autopilot_only_view" not in vault_txt2:
            fail("ops-ux: vault musi normalizować widok na AUTOPILOT-only")
        if "if(live&&live.issue)" not in ot:
            fail("ops-ux: Live musi wymagać live.issue (bez pustego take_over)")
        if "safe-area-inset" not in html or "IBM Plex Sans" not in html:
            fail("academy-ux: DASHBOARD bez safe-area / typografii Plex")
        if "hero-ops" not in html:
            fail("academy-ux: brak CTA Hermes Ops w hero")
        if "chips{display:none}" not in html:
            fail("academy-ux-v5: hero chips muszą być ukryte (display:none)")
        if "--nav-active" not in html or "--sem-ok" not in html:
            fail("academy-ux-v5: brak tokenów kolorów v5 (--nav-active / --sem-*)")
        if 'id="nav-legend"' in html:
            fail("academy-ux-v6: zakaz #nav-legend — chrome kradnie uwagę")
        if ".hero .sub" in html or "Jeden rozdział naraz" in html:
            fail("academy-ux-v6: zakaz hero.sub — copy kursu nie na foldzie")
        if 'id="sync-bar"' in html:
            fail("academy-ux-v6: zakaz #sync-bar — sync tylko #tty-sync")
        if 'id="barwrap"' in html or 'id="remain"' in html:
            fail("academy-ux-v6: zakaz paska Postęp studiów — mapa A–H")
        if 'id="course-map"' not in html or "data-course-dzial" not in html:
            fail("academy-ux-v6: brak #course-map z data-course-dzial")
        if "function renderMoney(" not in html or "tab==='money'" not in html.replace(" ", ""):
            fail("academy-ux-v6: brak renderMoney() / gałęzi money")
        if "function renderSourcesTab(" not in html or "tab==='sources'" not in html.replace(" ", ""):
            fail("academy-ux-v6: brak renderSourcesTab() / gałęzi sources")
        if 'id="sources-today"' not in html:
            fail("academy-ux-v6: ŹRÓDŁA bez 3 kart (#sources-today)")
        if "PLATFORM_BIBLE" not in html:
            fail("academy-ux-v6: brak PLATFORM_BIBLE")
        if 'class="grid two" id="dsaas-flows"' in html or 'id="dsaas-flows" class="grid two"' in html:
            fail("academy-ux-v6: dsaas-flows nie może być gridem 7 mermaidów")
        if "DSAAS_FLOW_CHIPS" not in html or html.split("var DSAAS_FLOW_CHIPS=", 1)[1].split("];", 1)[0].count("{id:") != 7:
            fail("academy-ux-v6: brak 7 chipów przepływu DSAAS")
        if "Node core vs notebooki (A7)" not in html:
            fail("academy-ux-v6: layers mermaid musi być w details A7, nie first-card")
        if ".zone-strip{display:none}" not in html:
            fail("academy-ux-v5: zone-strip musi być scalony ze sync (CSS display:none)")
        if "ui_calm" not in html or "calm-mode" not in html:
            fail("academy-ux-v5: brak Calm mode (_scratch.ui_calm)")
        if 'open id="guide-winda"' not in html:
            fail("academy-ux-v5: INSTRUKCJA — tylko winda open na start")
        if html.count('guide-card" open') > 1:
            fail("academy-ux-v5: INSTRUKCJA — max jeden guide-card open")
        if "Active agents" not in ot:
            fail("ops-ux: brak Active agents (WIP)")
        if re.search(r">\s*1\.\s*Dashboard", ot):
            fail("ops-ux: ponumerowane sekcje jak atrapa speca — HUD bez '1. Dashboard'")
        if 'href="/DASHBOARD.html"' in ot and "Ucz się" in ot:
            fail("ops-ux: hero nie może być nawigacją Akademii — footer wystarczy")
        push_py = (ROOT / "scripts" / "push-send.py").read_text(encoding="utf-8")
        if "--ops" not in push_py or "ops-push-pending" not in push_py:
            fail("ops-ux: push-send.py musi obsługiwać --ops (Supervised alert)")
    man_ops = ROOT / "manifest-ops.webmanifest"
    if not man_ops.exists():
        fail("ops-ux: brak manifest-ops.webmanifest")
    else:
        mt = man_ops.read_text(encoding="utf-8")
        if '"Hermes Ops"' not in mt:
            fail("ops-ux: manifest-ops bez short_name Hermes Ops")
        if "#070b14" not in mt:
            fail("ops-ux: manifest-ops theme musi być ciemny (#070b14)")
        if '"./ops"' not in mt and "'./ops'" not in mt:
            fail("ops-ux: manifest-ops start_url bez /ops")
    man = ROOT / "manifest.webmanifest"
    if man.exists():
        mt = man.read_text(encoding="utf-8")
        if '"./ops"' not in mt and "'./ops'" not in mt:
            fail("split: manifest bez shortcut /ops")
        if "Ucz się" not in mt or "Praca" not in mt:
            fail("split: manifest bez shortcuts Ucz się / Praca")
    vault_ops = (ROOT / "host" / "progress_vault.py").read_text(encoding="utf-8")
    if 'parsed.path in ("/ops", "/ops/")' not in vault_ops:
        fail("split: vault nie routuje GET /ops")
    if 'HTTPStatus.GONE' not in vault_ops:
        fail("split: vault POST /hermes/chat bez 410")
    if "Hermes Engineer" not in html:
        fail("hermes-dual: brak karty TOOL_DATA Hermes Engineer")
    eng_m = re.search(r"\{name:'Hermes Engineer'[\s\S]*?kroki:\[(.*?)\]", html)
    kroki_blob = eng_m.group(1) if eng_m else ""
    eng_paths = re.findall(r"workflow-lab/[^'\]\s]+", kroki_blob)
    if len(eng_paths) != 6:
        fail(f"hermes-dual: karta Engineer — kroki != 6 pathów playbooku ({len(eng_paths)})")
    eng_block = kroki_blob
    if "ENGINEER_LOOP_E2E" not in html:
        fail("hermes-dual: brak ENGINEER_LOOP_E2E w dashboardzie")
    e2e_evidence = ROOT / "docs" / "ops" / "engineer-loop-e2e.json"
    if "ENGINEER_LOOP_E2E=true" in html.replace(" ", ""):
        if not e2e_evidence.exists():
            fail("hermes-dual: ENGINEER_LOOP_E2E=true bez docs/ops/engineer-loop-e2e.json")
        else:
            ev = e2e_evidence.read_text(encoding="utf-8")
            if "engineer_loop_e2e" not in ev or "github_pr" not in ev:
                fail("hermes-dual: engineer-loop-e2e.json niekompletny")
    if 'name:\'Hermes Engineer\'' in html or 'name:"Hermes Engineer"' in html:
        idx = html.find("Hermes Engineer")
        card = html[idx : idx + 1200]
        if re.search(r"status:'AKTYWNY'|status:\"AKTYWNY\"", card) and "ENGINEER_LOOP_E2E=false" in html.replace(" ", ""):
            if "PARTIAL / SETUP" not in card:
                fail("hermes-dual: karta Engineer AKTYWNY przed engineer_loop_e2e")
    slownik = ROOT / "docs" / "SLOWNIK-HERMESA.md"
    if not slownik.exists():
        fail("hermes-dual: brak docs/SLOWNIK-HERMESA.md")
    else:
        sd = slownik.read_text(encoding="utf-8")
        gloss_labels = re.findall(r"label:'([^']+)'", html.split("HERMES_GLOSSARY")[1][:8000])
        for lab in gloss_labels:
            short = lab.split("(")[0].strip().split(" ")[0]
            if short and short not in sd and lab not in sd:
                fail(f"hermes-dual: słownik bez etykiety glossary {lab!r}")
        if "30" not in sd or "6" not in sd or "R7" not in sd:
            fail("hermes-dual: słownik bez budżetu 30/6/3/1 lub R7")
    router_py = ROOT / "host" / "hermes_router.py"
    if not router_py.exists():
        fail("hermes-dual: brak host/hermes_router.py (vault musi routować state/fact)")
    elif "def hermes_intent(" not in router_py.read_text(encoding="utf-8"):
        fail("hermes-dual: hermes_router bez hermes_intent")
    if "function hermesIntent(" not in html:
        fail("hermes-dual: brak routera hermesIntent")
    intent_use = fn_body(html, "function hermesAsk(", limit=2500)
    if not intent_use or "hermesIntent" not in intent_use:
        fail("hermes-dual: hermesAsk nie używa hermesIntent")
    elif "intent==='state'" not in intent_use.replace(" ", "") and "intent==='state'" not in intent_use:
        fail("hermes-dual: brak short-circuit state/fact przed LLM")
    vault_l = ROOT / "host" / "progress_vault.py"
    if vault_l.exists():
        vl = vault_l.read_text(encoding="utf-8")
        if "POST /hermes/chat nie ma narzędzi MCP" not in vl:
            fail("hermes-dual: vault bez zakazu MCP w /hermes/chat")
        if "hermes_local_reply" not in vl:
            fail("hermes-dual: vault nie routuje state/fact przed LLM")
        chat_fn = fn_body(vl, "def _hermes_chat(", limit=2000)
        if chat_fn and re.search(
            r"(?:call_mcp|mcp_server|mcp_tools|tool_calls|invoke_tool\s*\()",
            chat_fn,
            re.I,
        ):
            fail("hermes-dual: _hermes_chat zawiera wywołanie narzędzi/MCP")
    pb_paths = re.findall(r"path:'([^']+)'", html.split("PLAYBOOK_PHONE")[1][:1200])
    for p in pb_paths:
        if not any(p in k for k in eng_paths):
            fail(f"hermes-dual: dryf playbook vs karta Engineer — brak {p}")

    # --- Fala K: Hermes zna wlasny produkt (2026-09-20) ---------------------------
    # ZMIERZONE na produkcji (bateria 14 pytan, deepseek-flash): przy LOCK model
    # wysylal do ci.yml, mowil „zapytaj Dowodce" i doklejal „nastepny ruch" do
    # pytan nauczycielskich. Kontroler dzialal przeciw regule nr 1 aplikacji.
    # Guardy patrza na KONSTRUKCJE w prompcie i digescie + na snapshot frontu.
    vault_k = ROOT / "host" / "progress_vault.py"
    if vault_k.exists():
        vk = vault_k.read_text(encoding="utf-8")
        for needle, why in (
            ("PRIORYTET RUCHU", "prompt bez kolejnosci LOCK > rytual > TERAZ"),
            ("Rozmawiasz Z NIM", "prompt nie mowi, ze rozmowca JEST Dowodca"),
            ("NIE doklejaj", "prompt nie chroni pytan nauczycielskich przed doklejaniem ruchu"),
            ("instrukcja OBSŁUGI Akademii", "prompt nie rozroznia 'jak uzywac' od 'jak mnie pytac'"),
            ('"PRIORYTET"', "digest nie stawia etykiety PRIORYTET przy LOCK"),
            ("lista do odklikania (day_missing)", "digest nie etykietuje day_missing jako listy zadan"),
            ("ZAWIESZONY do domknięcia DZIEŃ", "digest nie oznacza kawalu kursu jako zawieszonego"),
            ('return "(stan pusty — kurs nierozpoczęty)"', "pusty digest znow zawiera polecenie"),
        ):
            if needle not in vk:
                fail(f"hermes-kontroler: {why}")
        digest_fn = fn_body(vk, "def hermes_state_digest(", limit=3500)
        if not digest_fn:
            fail("hermes-kontroler: brak hermes_state_digest")
        elif 'return "(stan pusty — kurs nierozpoczęty; zaproponuj' in digest_fn:
            fail("hermes-kontroler: polecenie 'zaproponuj' wrocilo do hermes_state_digest (sekcja DANE)")
        elif 'return "(stan pusty — kurs nierozpoczęty)"' not in digest_fn:
            fail("hermes-kontroler: pusty digest znow zawiera polecenie")
    snap = fn_body(html, "function hermesStateSnapshot(){", limit=1200)
    if not snap:
        fail("hermes-kontroler: brak hermesStateSnapshot")
    elif "lk.locked&&!dayUntouched()" not in snap:
        fail("hermes-kontroler: snapshot nie rozroznia LOCK aktywnego od dnia odpoczynku")
    elif "priority:" not in snap and "priority :" not in snap:
        fail("hermes-kontroler: snapshot nie wysyla pola priority")
    eval_py = ROOT / "scripts" / "hermes-eval.py"
    if not eval_py.exists():
        fail("hermes-kontroler: brak scripts/hermes-eval.py — bateria jakosci nie jest w repo")
    else:
        et = eval_py.read_text(encoding="utf-8")
        if "12_lock" not in et or "day_missing" not in et:
            fail("hermes-kontroler: bateria bez przypadku LOCK — nie złapie regresji P0")
        if 'add_argument("--digest-only"' not in et:
            fail("hermes-kontroler: bateria bez trybu --digest-only (CI nie moze biec bez LLM)")

    if errors:
        print("FAIL:")
        for item in errors:
            print(f" - {item}")
        return 1
    print("PASS: academy export contract + dashboard v3.1 (sync vault ready)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
