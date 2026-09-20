# Handoff — Akademia: deploy na VPS + naprawa wycieku sekretów z vaulta

**Data:** 2026-09-20
**Repo:** `akademia`
**Sesja:** polerka przeddeployowa → deploy na VPS → weryfikacja po deployu → **incydent bezpieczeństwa** (vault oddawał `.env`) → naprawa + drugi deploy
**Plan:** [`docs/ops/PLAN-AKADEMIA-TERMINAL-UX-2026-09-20.md`](../ops/PLAN-AKADEMIA-TERMINAL-UX-2026-09-20.md) (§13.1–13.5)
**Runbook:** [`docs/runbooks/AKADEMIA-VPS.md`](../runbooks/AKADEMIA-VPS.md) (§8 push, §9 co vault oddaje po HTTP)
**Poprzedni handoff:** [`2026-09-20-akademia-terminal-ux-fala-3-4.md`](2026-09-20-akademia-terminal-ux-fala-3-4.md)
**PR:** [#13](https://github.com/wozniaknorbert95-del/akademia/pull/13) (compose v1), [#14](https://github.com/wozniaknorbert95-del/akademia/pull/14) (biała lista statyków) — oba zmergowane do `main`
**Status:** Fala 0–4 **NA PRODUKCJI**. Push **uzbrojony** (klucz VAPID + timer), dostarczenie do zamkniętej PWA do potwierdzenia na urządzeniu Dowódcy.

---

## 1. Co jest na produkcji

| Element | Stan |
|---|---|
| `https://akademia.quietforge.flexgrafik.nl` | **200** z Basic Auth, **401** bez; cert Let's Encrypt do **2026-12-12** |
| Parytet plików VPS ↔ lokalnie | **8/8 md5 identyczne** (`DASHBOARD.html`, `sw.js`, `manifest.webmanifest`, `host/progress_vault.py`, `host/docker-compose.yml`, `scripts/push-send.py`, `scripts/test_progress_vault.py`, `scripts/validate-academy-export.py`) |
| Vault | kontener `healthy`, `/health` OK, dane w bind-mouncie `data/` (poza repo) |
| Klucz VAPID | wygenerowany na VPS: `/etc/akademia/vapid.env` (**600 root**), publiczny **87 znaków** w `/opt/akademia/.env`, zgodny z `/push/public-key` |
| Timer wysyłki | `akademia-push.timer` **enabled + active**, następny strzał 07:0x CEST, `--dry-run` zwraca poprawny payload |
| Subskrypcje push | **0** (nikt jeszcze nie włączył na urządzeniu) |

## 2. Incydent bezpieczeństwa (znaleziony po deployu, naprawiony tego samego dnia)

Pytanie kontrolne „co jeszcze ten vault serwuje?” pokazało, że `safe_static_path()` sprawdzał **tylko traversal**, a `STATIC_ROOT` to całe repo. Za hasłem Basic Auth na produkcji:

| URL | Przed | Po |
|---|---|---|
| `/.env` | **200** (bearer vaulta) | **404** |
| `/CREDENTIALS.local.txt` | **200** (hasło w czystym tekście) | **404** |
| `/host/.htpasswd` | **200** (hash nginx) | **404** |
| `/host/env.example`, `/host/docker-compose.yml`, `/host/progress_vault.py`, `/scripts/push-send.py` | **200** | **404** |
| `/data/` | **200** (fallback `/` → dashboard) | **404** |
| `/data/push-subscriptions.json` | 404 tylko dlatego, że plik nie istniał | **404** |
| `DASHBOARD.html`, `README.md`, `AGENTS.md`, `docs/*.md`, `ops/*.md`, `cursor-kurs/*.md`, `schema/*.json`, `icons/*`, `sw.js`, `manifest` | 200 | **200** |

Naprawa: kropki → 404, katalogi `data/`/`host/`/`scripts/` → 404, nazwy wprost, **biała lista rozszerzeń** treści kursu, fallback `/` tylko dla korzenia. Guardy w walidatorze (6 linii reguł) + testy na dekojach **istniejących na dysku**; mutacje: 10 trafień / FAIL walidatora.

## 3. Błędy znalezione i naprawione w tej sesji

1. **Push był cicho martwy** — klient miał klucz na twardo, compose nie przekazywał `ACADEMY_VAPID_PUBLIC_KEY`, setup nie dowoził go do `.env`. Teraz: `loadVapidKey()` z `/push/public-key`, klucz z `vapid.env` → `.env`, badge sam się przełącza.
2. **CRLF w `scripts/*.sh`** — `bash` na VPS by się wywalił; konwersja do LF + guard na CRLF/BOM w walidatorze (`.gitattributes` nie pomaga, bo deploy pakuje working copy przez `tar`).
3. **`docker-compose` v1 `KeyError: 'ContainerConfig'`** przy recreate → martwy vault (`Exited 137`, port 8097 milczał). Naprawa: `down --remove-orphans` + retry + health-check z 20 s retry i twardym `exit 1`.
4. **Brak timera wysyłki** — subskrypcja bez wysyłki = cicha porażka. Setup tworzy `.venv` + `pywebpush` + `akademia-push.{service,timer}` (best-effort, z instrukcją ręczną, gdy brak zależności).
5. **`push-send.py --once`** był w docstringu, ale nie w `argparse` → jednostka systemd by padła. Dodany + guard.
6. **Martwy link po re-kliku** tego samego hasha (`hashchange` nie odpala) — delegowany handler woła `openHashTarget()`.
7. **Ucinany tekst w DSAAS na 375 px** (`.file-row` bez `min-width:0`) — zawijanie + jedna kolumna na ≤560 px.
8. **SW rejestrował się dopiero po kliku** „Włącz powiadomienia” — `registerSwEarly()` w `initApp()` (PWA installability).
9. **Duplikat `<link rel=icon>`**, brak `meta description`, `#dump` bez dostępnej nazwy — dodane/naprawione + guardy.

## 4. Dowody (zmierzone)

| Co | Metoda | Wynik |
|---|---|---|
| Bramki repo | `validate-academy-export.py` + `test_progress_vault.py` | **PASS / PASS** |
| Biała lista statyków | 13 ścieżek sekretów / 5 ścieżek treści (dekoje na dysku) | **13× None / 5× serwowane** |
| Mutacja reguł vaulta | wyłączone dwie reguły | **FAIL: 10 trafień** → po przywróceniu PASS |
| Mutacja walidatora | usunięta linia `if parts[0] in STATIC_DENY_DIRS:` | **FAIL** → po przywróceniu PASS |
| Produkcja: sekrety (po naprawie) | `curl -u` na 6 ścieżkach w tej samej sekundzie co 200 dla treści | **6× 404 / treść 200** |
| Produkcja: content | `DASHBOARD.html`, `docs/OPERATING-MODEL.md`, `docs/ACADEMY-UX-SPEC.md`, `ops/workflow-marzen/04-INSTRUKCJA-OBSUGI.md`, `cursor-kurs/00-START-TUTAJ.md`, `schema/*.json`, `icons/*`, `sw.js`, `manifest` | **200** (katalogi → 404) |
| Produkcja: TLS/nagłówki | `curl -I` + `openssl s_client` | HSTS, `X-Frame-Options: DENY`, `nosniff`, cert LE do 2026-12-12 |
| Push: ścieżka lokalna (wcześniej) | vault `:8098` + dashboard przez vault | badge „ustawiony”, `GET /push/public-key` 200, `POST /push/subscribe` 200 |
| Push: wysyłka | `push-send.py --dry-run` na VPS | payload „Jeden kawał do zrobienia — otwórz Akademię.” |

## 5. Czego **nie** zrobiłem

- Nie wysłałem realnego pusha na urządzenie — **wymaga telefonu Dowódcy** (zgoda + instalacja PWA). To jedyny niepotwierdzony krok.
- Nie zmieniałem UI (`DASHBOARD.html` bez zmian w tej sesji — hash lokalny == hash na VPS == plik zweryfikowany wcześniej axe/mobile/offline).
- Nie ruszałem `schema_version` ani `source`, nie dodałem iframe'a Kokpitu, nie dodałem 7. działu, zero zmian w `workflow-lab` / `dsaas-platform-main` / `jadzia-core`.
- Nie dodawałem drugiej warstwy w nginx (deny na poziomie proxy) — bariera jest w vaulcie, pokryta testami i guardem; nginx serwuje wyłącznie `proxy_pass`.

## 6. Następny krok (jeden TERAZ — na telefonie, 2 minuty)

1. Otwórz `https://akademia.quietforge.flexgrafik.nl/DASHBOARD.html` (login z `/opt/akademia/CREDENTIALS.local.txt`).
2. **HERMES** → panel *Push*: `VAPID public` = **ustawiony**, *Włącz powiadomienia* → zgoda.
3. Dodaj do ekranu głównego, zamknij PWA, na VPS: `/opt/akademia/.venv/bin/python /opt/akademia/scripts/push-send.py --force`.
4. Powiadomienie ma dojść przy **zamkniętej** PWA (iOS ≥ 16.4 po instalacji, Android).

## 7. Pliki tej sesji

- `host/progress_vault.py` (biała lista statyków + reguły deny)
- `scripts/test_progress_vault.py` (dekoje + bramki HTTP na realnych plikach)
- `scripts/validate-academy-export.py` (guard 6 linii reguł + markery testu)
- `.gitignore` (`data/push-subscriptions.json`, `__pycache__/`)
- `scripts/setup-akademia-vps.sh`, `scripts/deploy-akademia-vps.sh`, `scripts/generate-vapid-keys.sh`, `scripts/push-send.py`, `host/docker-compose.yml`, `host/env.example` (PR #13/#14 i wcześniejsze w tej sesji)
- `DASHBOARD.html` (polerka: VAPID z endpointu, re-klik linku, `meta description`, `aria-label`, SW early, mobile `.file-row`)
- `docs/ops/PLAN-AKADEMIA-TERMINAL-UX-2026-09-20.md`, `docs/runbooks/AKADEMIA-VPS.md`, ten handoff
