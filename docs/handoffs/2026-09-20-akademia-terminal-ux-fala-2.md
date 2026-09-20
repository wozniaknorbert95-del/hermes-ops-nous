# Handoff — Akademia: Terminal UX (Fala 0–2)

**Data:** 2026-09-20
**Repo:** `akademia`
**Sesja:** chrom terminala + 15 manuali narzędzi + strażnik `DZIEŃ` z blokadą
**Plan:** [`docs/ops/PLAN-AKADEMIA-TERMINAL-UX-2026-09-20.md`](../ops/PLAN-AKADEMIA-TERMINAL-UX-2026-09-20.md)
**Status:** kod gotowy i zweryfikowany lokalnie. **Nic nie jest zacommitowane ani zdeployowane.**

---

## Co zrobione w tej sesji

| Fala | Zakres | Bramka |
|---|---|---|
| **0** | Chrom terminala: `--mono`/`--prompt`, prompt `❯` przed tytułami, sticky statusbar `#tty-statusbar`, ASCII dividery `─ ❯ SEKCJA ─`, migający kursor pod `prefers-reduced-motion` | ✅ |
| **1** | `NARZĘDZIA`: 15 kart z rozwijaną **Instrukcją** (`robi` / `kiedy` / `kiedy NIE` / `zasady` / `kroki` ×5 / `gotcha`) + banner „Jak użyć" | ✅ |
| **2** | `DZIEŃ`: każdy krok rytuału linkuje do konkretnej reguły, linie `Today first:` / `Tomorrow first:` sprawdzalne, blokada zaległego dnia | ✅ |

## Fala 2 — co dokładnie zmienione w `DASHBOARD.html`

| Element | Zmiana |
|---|---|
| Dane | `var AKA` (linki do repo akademia) + `var DAY_RULES` — mapa 19 kluczy → `{label, href}` (akademia `AGENTS.md`, `ops/workflow-marzen/04`, `workflow-lab/{AGENTS,CONTRIBUTING}.md`, `MORNING-RITUAL`, `EVENING-RITUAL`, `PLATFORM-WORKFLOW-GATE`) |
| Helper `ckRow(key,text)` | renderuje krok jako `.step` = checkbox + tekst + link `❯ reguła: …` (link jest **poza** `<label>`, żeby nie tworzyć nested-interactive) |
| Stan dnia | `state.day_stamp` (dzień otwartego rytuału), `state.day_closed` (dzień zamknięty na zielono), `state.day_skipped` (świadome pominięcie) — wszystko w `_scratch`, wolno dowolne klucze |
| `initDay()` | **na wejściach** (`initApp()` + po `pullProgress()`), nie w `renderAll()`: jeśli poprzedni dzień był zamknięty na zielono → reset rytuału + `day_stamp = dziś` |
| `dayLock()` | zaległy dzień = `day_stamp !== dziś && day_closed !== day_stamp` |
| `ranoDone()` / `wieczorDone()` | 5 kroków + linia w poprawnym formacie (`Today first:` / `Tomorrow first:` na początku) |
| `closeDay()` | oba półrocza zielone → `day_closed = day_stamp` + `msg(...)` |
| `renderDayStatus()` | banner czerwony (LOCK + lista braków + „Pomiń świadomie") albo zielony („ZAMKNIĘTY NA ZIELONO" + „Zacznij nowy dzień") |
| `nowLockCard()` | **podmienia** treść istniejącej karty TERAZ na „DOKOŃCZ DZIEŃ" — **nie** dodaje drugiej karty |
| `renderChapterCard()` | `blocked = isLocked(id) \|\| dayLock().locked` → `LOCK`, checkboxy labu i przycisk „Zalicz" `disabled` |
| `bindDynamic()` | guard na `[data-pass]`: przy blokadzie przekierowuje na DZIEŃ + `msg(...)` (defense in depth) |
| `bindDataInputs()` | handler tekstowy woła teraz `checkRitualBanners()` — **bugfix** |
| `renderStatusbar()` | przy blokadzie: `❯ TERAZ — DOKOŃCZ DZIEŃ (2026-09-19) · 0%` |
| CSS | `.step`, `.rule-link`, `.day-lock`, `.day-lock-ok`, `.line-row`, `.line-hint.ok/.bad`, `.tpl-row`, `.tpl` |

## Dwa błędy znalezione przez weryfikację (i naprawione)

1. **Dzień się nie zamykał, gdy ostatnią rzeczą była linia.** `bindDataInputs` dla `input[type=text]` robił `save()` bez `checkRitualBanners()`, więc `closeDay()` nigdy nie odpalał. Dowód: po wypełnieniu wszystkich checkboxów i obu linii `day_closed` zostawało `''`. Naprawione.
2. **`initDay()` w `renderAll()` natychmiast przewracał datę** po zamknięciu zaległego dnia → zielony banner i przycisk „Zacznij nowy dzień" były nieosiągalne (dzień przewracał się przy każdym renderze, np. przy przełączeniu zakładki). Przeniesione na wejścia.

## Testy tej sesji

- `python scripts/validate-academy-export.py` → **PASS** (`proofHref == 15`, `id="nowcard"` == 1, brak `alert(`)
- `python scripts/test_progress_vault.py` → **PASS**
- `node --check` na inline JS → **PASS**
- 17/17 kroków rytuału ma link reguły; 0 bez linku; wszystkie hrefy w `wozniaknorbert95-del/*`
- Linia: `Today first: …` → `✓`; `random` → `✗`; sam prefiks → `✗`
- Blokada (symulacja `day_stamp=2026-09-19`, `day_closed=''`): 7/7 „Zalicz" disabled, checkboxy labu disabled, `#nowcard` == 1, title = „DOKOŃCZ DZIEŃ — 2026-09-19"
- Zamknięcie: `day_closed=2026-09-19` → TERAZ odblokowane (`Workflow Lab / A1`), banner zielony + „Zacznij nowy dzień (2026-09-20)" → klik → `day_stamp=2026-09-20`, rytuał pusty
- Wyjście awaryjne: „Pomiń świadomie" → `day_skipped=2026-09-19`, blokada zdjęta
- `ENT-12` nie występuje na zakładce TERAZ (żyje tylko w NARZĘDZIA + DZIEŃ jako `WAIT`)
- axe-core: 0 critical / 0 serious na wszystkich 5 zakładkach. Zostaje **1 `heading-order:moderate`** — pre-existing `<h4>Mój dzień — rano 10 minut</h4>` pod `h2` (znany z Fali 0, świadomie nie ruszałem)
- 375 px: `scrollWidth == innerWidth == 375`, 0 błędów konsoli, taby `.tpl` 32 px (WCAG 2.2 AA ≥ 24 px)
- Eksport: `schema_version 0.1.0`, `source academy-os`, `academy_url` bez tokena

## Co świadomie odłożone (backlog)

- `heading-order` na DZIEŃ: `<h4>` pod `<h2>` w pięciu `.box`. Naprawa = `h3` zamiast `h4` albo dodanie `<h2>` sekcji — to zmiana istniejącej struktury nagłówków, poza zakresem Fali 2.
- `#plat_tor` ma wewnętrzny overflow (długa domyślna wartość `WF-P6 — Rytuały platformy (QUI-14, dzień 2/7)`), ale **strona nie scrolluje poziomo**. Pre-existing.
- Brak `day_stamp`/`day_closed` w `schema/academy-progress.v0.json` — leżą w `_scratch`, który schema traktuje jako free-form. Nie trzeba zmieniać schematu.

## Czego **nie** zrobiłem

- Zero commitów, zero PR, zero deployu. `DASHBOARD.html` + plan + ten handoff są niezacommitowane.
- Nie ruszałem `_scratch` w Kokpicie, nie dodałem iframe'a, nie dodałem 7. działu.
- Stan testowy w `localStorage` na `localhost:8765` został wyczyszczony (`removeItem('aea-os')`) — weryfikacja nadpisała lokalny stan dashboardu, ale postęp kursu był `0%`, więc nie zginęło żadne zaliczone ćwiczenie.

## Następny krok (jeden TERAZ)

**GO Dowódcy na Falę 3 (DSAAS — mistrzostwo)** albo najpierw commit + deploy Fali 0–2 na VPS:

```
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
git add DASHBOARD.html docs/ops/PLAN-AKADEMIA-TERMINAL-UX-2026-09-20.md docs/handoffs/2026-09-20-akademia-terminal-ux-fala-2.md
bash scripts/deploy-akademia-vps.sh     # tylko na GO (Zasada 11)
```

## Pliki tej sesji

- `DASHBOARD.html`
- `docs/ops/PLAN-AKADEMIA-TERMINAL-UX-2026-09-20.md`
- ten handoff
