# Raport audytu — Akademia (`/`)

**Data:** 2026-09-24  
**Plan:** [`AUDYT-PLAN-AKADEMIA-2026-09-24.md`](AUDYT-PLAN-AKADEMIA-2026-09-24.md) (GO Dowódcy)  
**Branch naprawczy:** `cursor/vibe-init-hermes-docs-577c` (PR #63)  
**Kontrakt docelowy:** UX **v4.1** (6 zakładek) + `schema/academy-progress.v0.json` 0.1.0

---

## Executive summary (głos „ojca-inżyniera”)

Akademia miała **dobry szkielet profesjonalizmu** (vault, mutacje, jedno TERAZ, uczciwy Hermes read-only, split `/ops`), ale **regresja IA po split Ops** schowała najważniejszą „szafkę z kluczami” — zakładki **WORKFLOW** i **NARZĘDZIA**. Kod (`renderWorkflow`, `renderTools`, `TOOL_DATA`) nadal żył w pliku, lecz **nie był podpięty do nawigacji** — klasyczny błąd: dokumentacja mówi „używaj narzędzi”, a UI nie daje do nich drzwi.

W tej sesji **przywrócono 6 zakładek**, zaktualizowano guardy CI (A3, hermes-dual, Fala 0/L/M), spec UX v4.1 oraz plan audytu (faza A8). Automatyka: pełna linia `testy:` z `AGENTS.md` — **PASS** lokalnie.

**Merge PR #63 → `main`:** wymaga zielonego `academy-gate` na GitHubie po pushu tego commitu (wcześniej blokada: mutacja D7b + guard 4 vs 6 zakładek).

---

## Metody

| Faza | Wynik |
| --- | --- |
| A1 IA 6 zakładek | PASS po fix — walidator + inspekcja `renderMainPanel` |
| A2 TERAZ | PASS — mutacje D/I (I15), jeden `#nowcard` |
| A3 DZIEŃ | PASS — `test_progress_vault.py` |
| A4 Sync | PASS — `validate-academy-export.py` |
| A5 Intent | PASS — `test_hermes_intent.py` (8 kanarków) |
| A6 Docs vs UI | **PARTIAL → naprawione** w PR (UX spec, plan; INSTRUKCJA/ROLE w tym commicie) |
| A7 CI / mutacje | PASS lokalnie (Fala 0–N, 0 PRZEPUSZCZONE) |
| A8 NARZĘDZIA/WORKFLOW | **FAIL → FIXED** — główny finding P0 |

Manual 360px (WORKFLOW/NARZĘDZIA): zalecany smoke po merge (`python -m http.server 8765`).

---

## Findingi

### P0 — brak zakładki NARZĘDZIA / WORKFLOW w UI (naprawione w PR #63)

| | |
| --- | --- |
| **Objaw** | Użytkownik nie widział kart narzędzi, instrukcji „jak używać”, statusów PARKED/AKTYWNY; WORKFLOW playbooków poza accordionem KURS. |
| **Przyczyna** | Po redukcji do 4 zakładek `ACADEMY_TABS` nie zawierało `workflow`/`tools`; `renderMainPanel` nie wywoływało `renderWorkflow()` / `renderTools()`. |
| **Dowód** | Martwy kod vs brak gałęzi w `renderMainPanel` przed fixem; guard A3 wymusza teraz 6 id. |
| **Naprawa** | Przywrócono `ACADEMY_TAB_COUNT=6`, podpięto render, mapa ról w WORKFLOW linkuje INSTRUKCJA + NARZĘDZIA. |
| **Lekcja (nauczanie)** | **Nie usuwaj zakładki, która uczy procedury** — nawet jeśli „da się to w KURS”. KURS to treść; NARZĘDZIA to **operacyjna higiena** (kiedy NIE używać Slacka, jak nie zepsuć vaulta). |

### P1 — rozjazd dokumentacji (4 vs 6 zakładek)

| Plik | Problem | Status |
| --- | --- | --- |
| `docs/ACADEMY-UX-SPEC.md` | v4.0 opisywała 4 zakładki | → **v4.1** w PR |
| `docs/ops/AKADEMIA-INSTRUKCJA.md` | nagłówek „4 zakładki” | → aktualizacja w PR |
| `docs/ops/HERMES-ROLE-CONTRACT.md` | „4 zakładki” | → aktualizacja w PR |
| `docs/handoffs/*` | historyczne 4/7 zakładek | OK jako archiwum; nie mylić z bieżącym kontraktem |

### P1 — profesjonalne wskazówki narzędziowe (częściowo OK, do pogłębienia)

| | |
| --- | --- |
| **Co działa** | `TOOL_DATA` + rozwijane `<details>` per narzędzie (zasady, 5 kroków, gotcha); karta Hermes Engineer z uczciwym PARTIAL gdy brak E2E. |
| **Luka** | Karta powitalna nadal uczy tylko TERAZ → lab → PWA; **nie wspomina**, że po A1 warto odwiedzić NARZĘDZIA (Cursor, Linear, vault). |
| **Rekomendacja P2** | Jedna linia w welcome + pierwszy krok w INSTRUKCJI: „Przed labem: NARZĘDZIA → Cursor / Linear — przeczytaj Instrukcję”. |

### P2 — ton „profesjonalista” w Hermesie (monitoring, nie regres)

| | |
| --- | --- |
| **Mocne** | Intent nie obiecuje merge/MCP; chips „Jak używać?”; `/ops` na TERAZ; mutacje K/L/M pilnują copy. |
| **Do rozważenia** | Więcej **checklist operacyjnych** w NARZĘDZIA (np. „przed push: vault zielony, brak sekretu w eksporcie”) — bez duplikowania całego handbooku L3 (`ops/workflow-marzen/`). |

### P2 — legacy `active_tab`

Stare wartości `guide|hermes|dsaas` → KURS; `workflow|tools` są **prawdziwymi** id zakładek — poprawne. Guard A5 w mutacji Fala 0 zsynchronizowany z kodem.

---

## Checklist zgodności AGENTS.md

| Reguła | Status |
| --- | --- |
| Jedno ▶ TERAZ | OK |
| Eksport v0.1.0 / `_scratch` | OK (testy vault) |
| Brak 7. działu / iframe Kokpitu | OK |
| Brak sekretów w `academy_url` | OK (mutacje D6/E) |
| `/ops` osobno | OK (mutacje M/N) |

---

## Następne kroki (priorytet)

1. **Merge PR #63** po zielonym CI — dokumentacja Hermes Ops + IA v4.1.
2. **P2:** welcome + INSTRUKCJA — explicit „NARZĘDZIA przed głębokim labem”.
3. **Osobno:** audyt Hermes Ops ([`docs/ops/AUDYT-PLAN-HERMES-OPS-2026-09-24.md`](ops/AUDYT-PLAN-HERMES-OPS-2026-09-24.md)).
4. **Deploy VPS:** tylko na GO Dowódcy; smoke `/` + `/progress`.

---

## Załączniki (dowód techniczny)

```text
validate-academy-export.py  → PASS
test_progress_vault.py      → PASS
test_hermes_intent.py       → PASS
mutation-test-fala-*.py     → PASS (0 PRZEPUSZCZONE, sesja 2026-09-24)
```

**Podpis audytu:** Cloud Agent (sesja vibe-init + GO audyt Akademia 2026-09-24).
