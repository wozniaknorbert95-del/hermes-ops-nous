# PLAN — polerka UX (post-audit, post-deploy)

**Status:** WYKONANE w kodzie (Fale A+B+C). Deploy = ten sam PR po `deploy-ready`.
**Data:** 2026-10-03
**Persona:** Dowódca na telefonie — 30 s, zero docs.
**SoT pikseli:** [`../ACADEMY-UX-SPEC.md`](../ACADEMY-UX-SPEC.md) v7 · [`UX-SPEC-HERMES-OPS-ENTERPRISE.md`](UX-SPEC-HERMES-OPS-ENTERPRISE.md)

**Nie jest to:** 8. tab, iframe Kokpitu, zmiana Cloud API, rotacja kluczy, Projects, nowy landing.

---

## 0. Co już jest zamknięte (nie ruszać)

| Finding audytu | Stan |
| --- | --- |
| Naga 401 nginx | Live: branded gate + `WWW-Authenticate` |
| `Live` przy leftover `PAUSED` | Live: `Ostatni run` |
| Retry flash na boot | Live: `hidden` + `body.booting` |
| Rytuał+wieczór na pierwszym ekranie TERAZ | Live: jeden `<details>` zamknięty |
| Brak `h1` / skip < 44px na `/ops` | Live |

Werdykt po re-walku lokalnym + smoke VPS: **Pass** na P0. Polerka = gęstość i duplikaty, nie prawda silnika.

---

## 1. Cel polerki

Ten sam job: **jeden ruch** na TERAZ, **jeden stan** na `/ops`.  
Po Fali A na 375px first-visit (welcome schowane): brief poranka + karta kursu, bez drugiej kopii rytuału i bez listy wieczoru w poranku.

---

## 2. Zasady twarde

1. Kontrakt **7 tabów**. `/ops` nie jest 8.
2. `#nowcard` ukryty. Jedno TERAZ.
3. `approveDay` / `approveEvening` = jedno `save()`. Wieczór ma własne tapnięcie.
4. Zmiana stringu HUD = ten sam PR co `validate-academy-export.py` (+ Fala S gdy kotwica).
5. Zero sekretów. Zero formularza hasła na `auth-gate`.
6. Jeden MR = jedna myśl. Fala A osobno od Fali B.

---

## 3. Fala A — TERAZ bez dubli (P0 polerki, 1 MR)

**Dowód (re-walk 375px, 2026-10-03):** `renderDayBrief()` zostawia zamknięty `<details>` „Wieczór — N kroków” **oraz** `renderRitualFold()` wkleja `renderEveningBrief()` + cały `renderDay()` (poranek, checkboxy, drugi „Zatwierdź poranek”). Fold jest czystszy, ale panel nadal dubluje ten sam rytuał.

| # | Fix | Plik | Guard |
| --- | --- | --- | --- |
| A1 | `renderRitualFold()` = tylko checkboxy `renderDay()` **bez** drugiego briefu wieczoru, gdy brief poranka już wisi; albo tylko `renderEveningBrief()` gdy `ranoDone()` | `DASHBOARD.html` | validate: `renderRitualFold` nie składa `renderEveningBrief` + pełnego `renderDay` naraz |
| A2 | Brief poranka: lista wieczoru znika z `renderDayBrief` (zostaje jedno zdanie + link do foldu). `counts_evening` zostaje w JSON | `DASHBOARD.html` | Fala I: `counts_evening` / `approveEvening` nietknięte; nowy needle: brak `eRows` w `renderDayBrief` |
| A3 | Copy „Ręcznie” w briefie → „Ręcznie / wieczór” (zgodne z foldem i spec) | `DASHBOARD.html` · `ACADEMY-UX-SPEC.md` | string w `renderDayBrief` |

**Poza A:** nie chować welcome (kontrakt ≤3 kroki, first visit). Nie ruszać 7 tabów.

**DoD Fali A:** 375px, welcome schowane: jeden CTA „Zatwierdź poranek”, karta B1, jeden zamknięty details. Zero drugiej listy `? wieczór` nad foldem.

---

## 4. Fala B — `/ops` słowa prawdy (P1, 1 MR)

Silnik już nie kłamie. Zostają etykiety.

| # | Fix | Plik |
| --- | --- | --- |
| B1 | Skip „Przejdź do Live” → „Przejdź do runu” (albo ukryj gdy nie `RUNNING`) | `OPS.html` |
| B2 | `h2` panelu `#panel-live` nie mówi „Live” gdy leftover — „Ostatni run” / „Run” | `OPS.html` |
| B3 | Banner „Vault nie odpowiedział JSON” nie na foldzie przy zwykłym 404 `/ops/run` na static preview — tylko gdy `POST` faktycznie poszedł | `OPS.html` |

Nie zmieniać `eye.textContent` logiki z `live-eyebrow-not-fake`.

---

## 5. Fala C — chrome 360px (P1, tylko po A)

| # | Fix | Uwaga |
| --- | --- | --- |
| C1 | Mapa A–H: na 360px + welcome widoczne → mapa w jednym rzędzie niższym albo pod details „Działy” | Spec: mapa zawsze widoczna — nie usuwać z DOM; można zwinąć |
| C2 | Welcome: jedna linia „NARZĘDZIA przed głębokim labem” (P2 z audytu 2026-09-24) | Nie czwarty krok |

---

## 6. Parked (osobna decyzja, nie ta polerka)

- Rotacja kluczy Cursor / Basic Auth.
- Redesign kart NARZĘDZIA (fala 1/2/PARKED już w `<details>` — to nie jest regresja).
- Projects / nowy landing / zmiana 7 tabów.
- Włączanie Nous LLM na VPS.

---

## 7. Kolejność i testy

1. Fala A → `validate` + vault + Fala I + Fala S (jeśli ruszysz kotwice) → re-walk 360 i 375 → PR mały.
2. Fala B → Fala S + Q (skip-link).
3. Fala C tylko jeśli A nie wystarczy na telefonie.

Bramka: `python scripts/validate-academy-export.py && python scripts/test_progress_vault.py`  
Merge: `bash scripts/deploy-ready-hermes-ops.sh`. Deploy = Zasada 11, osobne GO.

---

## 8. TERAZ

**Fala A.** Nie B i C w tym samym MR.
