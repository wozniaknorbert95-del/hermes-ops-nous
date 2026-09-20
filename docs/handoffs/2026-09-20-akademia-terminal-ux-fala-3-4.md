# Handoff — Akademia: Terminal UX (Fala 3 + 4)

**Data:** 2026-09-20
**Repo:** `akademia`
**Sesja:** DSAAS mistrzostwo (drill + diagramy offline) + Hermes (read-only kontroler + Web Push) + weryfikacja końcowa
**Plan:** [`docs/ops/PLAN-AKADEMIA-TERMINAL-UX-2026-09-20.md`](../ops/PLAN-AKADEMIA-TERMINAL-UX-2026-09-20.md)
**Poprzedni handoff:** [`2026-09-20-akademia-terminal-ux-fala-2.md`](2026-09-20-akademia-terminal-ux-fala-2.md)
**Status:** wszystkie 4 fale **DONE** i zweryfikowane lokalnie. Kod zacommitowany na `feat/terminal-ux-fala-0-2` (PR #12). **Zero deployu** — `Zasada 11`.

---

## Co zrobione w tej sesji

| Fala | Zakres | Bramka |
|---|---|---|
| **3** | `DSAAS`: drill mistrzostwa (łańcuch ODCS→OPA→objective→MCP→ledger, 3 agenci runtime, budżet 30/6/3/1, bramki HITL + Zasada 11) + diagramy renderowane offline z wersją ASCII | ✅ |
| **4** | `HERMES`: read-only kontroler (stan Akademii + GitHub API labu/platformy) + nauczyciel („jeden kawał") + Web Push (Service Worker + VAPID na VPS) | ✅ |

## Fala 3 — co dokładnie zmienione w `DASHBOARD.html`

| Element | Zmiana |
|---|---|
| Dane `PATH_STAGES` | 8 etapów łańcucha z `role` (rola) + `proof` (plik dowodowy z platformy) |
| Dane `AGENTS3` / `ALL_ENGINES` | 3 agenty runtime i przypisane silniki wzrostu (`a1`=discovery/demand/trust, `a2`=conversion/retention, `a3`=knowledge/optimization) |
| Dane `BUDGET_DRILL` | twarde limity Konstytucji §3.3: `30 / 6 / 3 / 1` |
| Dane `HITL_GATES` / `HITL_DECOYS` | 4 realne bramki człowieka (`deploy`, `publikacja`, `wydatek`, `zatrudnienie`) + 4 pułapki (`refaktor pliku`, `commmit na branch`, `uruchomienie testów`, `odczyt ledgera`) |
| Drill `1/4` | kolejność łańcucha — klik w etapy; zła kolejność **nie** jest przyjmowana (komunikat mówi, co stoi teraz) |
| Drill `2/4` | mapowanie 3 agentów na silniki; po sprawdzeniu pełna mapa `ok` (należy) / `bad` (nie należy) |
| Drill `3/4` | budżet złożoności — pola liczbowe, po sprawdzeniu pokazuje poprawną wartość przy błędzie |
| Drill `4/4` | bramki HITL — dokładnie 4 nieodwracalne decyzje, pułapki odrzucane |
| Bramka | `masteryDone()` = 4/4 drill-e → `state.mastery_dsaas` + klasa `mastery-pass` + „MISTRZOSTWO DSAAS" |
| Ściąga | `<details>` z pełną ścieżką i dowodami plik:linia + **uczciwa notka**, że repo platformy jest prywatne, więc linki nie otworzą się obcemu — dlatego ścieżkę odtwarzamy z pamięci |
| `ASCII_DIAGRAMS` | 8 wersji ASCII (`platform` L1–L9 + Bramka 4.1, `surfaces` Kokpit vs Maszynownia, `layers`, `chain`, `agents`, `budget`, `hitl`, `isolation`) |
| `offlineDiagrams()` | podmienia Mermaid na ASCII (`ascii-pre` + tag „❯ ASCII — wersja offline"); gdy ASCII brak → **uczciwy komunikat** zamiast surowego DSL |
| Pętle WORKFLOW | „Telefon loop" i „Laptop loop" (inline `<pre class="mermaid">`) dostały `data-ascii` ręcznie |

## Fala 4 — co dokładnie zmienione

| Plik | Zmiana |
|---|---|
| `DASHBOARD.html` | zakładka `HERMES` (`id:'hermes'`); `hermesKawal()`, `hermesState()`, `renderHermes()`, `renderHermesRemote()`, `loadHermesRemote()` (GitHub API, cache 10 min, `404` → „repo niedostępne publicznie", błąd sieci łapany per-repo), `renderPushPanel()`, `pushRegister()`/`pushSubscribe()`/`pushTest()` (potwierdzenie z SW przez `MessageChannel`), `renderHermesBanner()`, `bindHermes()` |
| `sw.js` (nowy) | Service Worker: `install`/`activate`/`push`/`notificationclick`/`message`; **nie cache'uje HTML** (zero stale content); odpowiada do klienta po `showNotification` |
| `host/progress_vault.py` | `GET /push/public-key`, `POST /push/subscribe`, `POST /push/unsubscribe`; walidacja subskrypcji, limit `PUSH_MAX_SUBS`, rate-limit, zapis do `push-subscriptions.json` poza repo |
| `scripts/generate-vapid-keys.sh` (nowy) | generuje parę VAPID (`secp256r1`) → `/etc/akademia/vapid.env`, `chmod 600`; drukuje tylko klucz publiczny. **Klucz prywatny nigdy nie wchodzi do repo** |
| `scripts/push-send.py` (nowy) | wysyłka push z `progress.json` + subskrypcji; `--dry-run` (bez VAPID) i `--force` |
| `scripts/validate-academy-export.py` | +guardy F3/F4, skan repo pod kątem `VAPID_PRIVATE_KEY`, `force_utf8_streams()` |
| `scripts/test_progress_vault.py` | +testy `/push/*` (auth, walidacja body, rate-limit), `sw.js` serwowany, `_scratch` nietknięte przez push |

## Błędy znalezione przez weryfikację (i naprawione)

1. **`DIAGRAMS.platform` nie miał wersji ASCII** → offline pokazywał surowy `flowchart LR…`. Po drodze wyszło, że to samo dotyczyło `surfaces` i `layers`.
2. **Pętle „Telefon/Laptop loop"** są inline w `renderWorkflow`, poza `renderDiagram` → bez `data-ascii`. Dodane ręcznie.
3. **`offlineDiagrams()` nie czyścił treści**, gdy ASCII brakowało → wyciekał developerski DSL do UI. Teraz uczciwy komunikat.
4. **`white-space:nowrap` w `.ro-table`** → w HERMES długie ścieżki platformy (`polityki/opa/security_runtime.rego`) dawały **55 px** przelewu poziomego na 375 px. Naprawione `overflow-wrap:anywhere`.
5. **`heading-order` w `DZIEŃ`** (dług z Fali 2: 5× `H4` bez `H3`) → naprawione na `H3` + CSS `#panel-day .box>h3` odtwarzający styl `H4` **1:1** (zmierzone `identical: true`).
6. **Pusty check w walidatorze:** `"diagram dwoch warstw (DIAGRAMS.layers)": "layers:" in html` przechodził nawet gdy diagram nie był renderowany. Zastąpiony twardym guardem.
7. **`UnicodeEncodeError`** przy polskich znakach w `print()` na Windows (`cp1252`) → `force_utf8_streams()` w 3 skryptach.

## Testy tej sesji (zmierzone, nie „na oko")

**Walidatory i kontrakty**

- `python scripts/validate-academy-export.py` → **PASS**
- `python scripts/test_progress_vault.py` → **PASS**
- Kontrakt „jedna karta `TERAZ`": `#nowcard` == **1** (także przy zablokowanym dniu)
- Kontrakt „brak `alert(`": **0**
- Eksport: `schema_version 0.1.0`, `source academy-os`, `academy_url` bez tokena

**Drill mistrzostwa (black-box przez DOM — skrypt jest w IIFE, więc testujemy jak użytkownik)**

- zła kolejność łańcucha → odrzucona, licznik `0/8`; poprawna → `8/8`
- agenci niekompletni → odrzuceni; poprawni → „Trzy agenty odtworzone poprawnie", 7/7 silników `ok`
- zły budżet → odrzucony; `30/6/3/1` → „Budżet 30/6/3/1 odtworzony"
- bramki HITL z pułapką `decoy0` → odrzucone; dokładnie 4 realne → zaliczone
- finalnie: `.mastery` = `mastery mastery-pass`, 8× `.dlog.ok`, 0× `.dlog.bad`

**Diagramy offline (`Network.setBlockedURLs` na 3 CDN-y)**

- 10 diagramów (WORKFLOW 3 · DSAAS 7), **10/10** z niepustym ASCII
- **0** wycieków surowego `flowchart`, **0** poziomego scrolla na 6 zakładkach, **0** błędów konsoli
- online: Mermaid rysuje **7× `<svg>`**, 0× `ascii-pre`, 0× `.ascii-tag`

**Dostępność i mobile**

- axe-core 4.10.2 na **6 zakładkach** (WCAG 2.0/2.1 A/AA + best-practice) → **0 naruszeń** (dług `heading-order` domknięty)
- 375 px: `scrollWidth == 375` na wszystkich zakładkach; sticky tabbar = **2 rzędy** (3+3), `--scroll-offset` = **128 px** (auto-pomiar)

**Guard walidatora udowodniony mutacją**

| Mutacja | Wynik |
|---|---|
| usunięcie `ascii:` z `DIAGRAMS.platform` | **FAIL wykryty** (`['platform']`) |
| martwe `ASCII_DIAGRAMS.nieistnieje` | **FAIL wykryty** (`['nieistnieje']`) |
| oryginał | PASS (8/8 diagramów, 3/3 `data-ascii`) |

## Co świadomie odłożone (backlog)

- **Push na produkcji** wymaga VPS: `bash scripts/generate-vapid-keys.sh` + `ACADEMY_VAPID_PUBLIC_KEY` + `pip install pywebpush`. Lokalnie potwierdzona sama ścieżka SW → `showNotification`; dostarczenie do **zamkniętej** PWA da się sprawdzić tylko na HTTPS z prawdziwym VAPID.
- GitHub API bez tokena ma limit **60 req/h** — przy intensywnym odświeżaniu Hermes degraduje się do samych linków (zachowanie zamierzone, cache 10 min).
- `#plat_tor` ma wewnętrzny overflow (długa wartość domyślna) — pre-existing, strona nie scrolluje poziomo.
- `day_stamp`/`day_closed`/`day_skipped` leżą w `_scratch` (schema traktuje go jako free-form) — brak zmian w schemacie.

## Czego **nie** zrobiłem

- **Zero deployu** na VPS (`Zasada 11` — tylko na GO Dowódcy). Zero zmian w `workflow-lab` i `dsaas-platform-main`.
- Nie ruszałem `_scratch` Kokpitu, nie dodałem iframe'a, nie dodałem 7. działu.
- Nie zmieniałem `schema_version` ani palety `:root`.

## Następny krok (jeden TERAZ)

**GO Dowódcy na deploy Fali 0–4 na VPS** (po merge PR #12), plus — dla pełnego pushu — wygenerowanie kluczy VAPID na serwerze:

```
bash scripts/generate-vapid-keys.sh          # na VPS: /etc/akademia/vapid.env (600)
pip install pywebpush                        # na VPS
python scripts/push-send.py --dry-run        # sanity bez wysyłki
```

## Pliki tej sesji

- `DASHBOARD.html`
- `sw.js` (nowy)
- `host/progress_vault.py`
- `scripts/generate-vapid-keys.sh` (nowy)
- `scripts/push-send.py` (nowy)
- `scripts/validate-academy-export.py`
- `scripts/test_progress_vault.py`
- `docs/ops/PLAN-AKADEMIA-TERMINAL-UX-2026-09-20.md`
- ten handoff
