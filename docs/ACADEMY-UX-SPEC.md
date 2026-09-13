# Academy Command Dashboard — UX spec (local-first, v3.1)

**Cel:** w 30 sekund wiesz co robisz teraz, gdzie kliknąć i czyja jest piłka. Jeden fokus naraz (ADHD-first).

## 1. Użytkownik i kontekst

- Właściciel (ADHD-friendly): laptop + telefon, potrzebuje spokoju, nie ściany checkboxów.
- Urządzenia: mobile-first (360px), desktop max 1180px. Offline/file:// musi działać.
- Ograniczenia (`AGENTS.md` akademii): jedno TERAZ; eksport v0.1.0; brak iframe Kokpitu; brak 7. działu; zero sekretów.

## 2. Pięć zakładek (IA v3.1)

| Zakładka | Pytanie | Główna akcja |
|---|---|---|
| `TERAZ` | Co robię w tej minucie? | Pełny widok bieżącego rozdziału (karta u góry ukryta) |
| `WORKFLOW` | Jak pracuję (laptop/telefon)? | Playbook z klikalnymi krokami → `#roz-A*` + ścieżka pliku |
| `NARZĘDZIA` | Co działa / co parked? | 14 kart + scoreboard platformy (8 poz.) |
| `DSAAS` | Czego uczę się o platformie? | Accordion: 1 dział otwarty, 1 rozdział otwarty |
| `DZIEŃ` | Jaki rytm dnia? | Rano/wieczór/piątek + tor **WF-P*** (ENT-12 = WAIT, nie TERAZ) |

**Reguła TERAZ:** Na zakładce TERAZ widoczny tylko panel (bez duplikatu `#nowcard`). Na innych zakładkach — kompaktowa karta TERAZ u góry.

## 3. Stany

- Pierwszy start: banner powitalny (3 kroki, dismiss → `welcome_dismissed` w localStorage) + pasek postępu + TERAZ wskazuje A1; reszta zwinięta.
- Pasek strefy pod tabami: nazwa + opis aktywnej zakładki + kolor (ADHD orientacja).
- TERAZ: pill „Zostało kroków lab: N/M”; pod progressbarem: „Do końca kursu: X rozdziałów”.
- Klawiatura: strzałki ←/→ między zakładkami (focus na tab).
- DSAAS/WORKFLOW: `<details>` — otwarty dział = ten z `firstOpen()`; otwarty rozdział = bieżący.
- Zablokowany rozdział: `disabled` na checkboxach i przycisku zaliczenia.
- Import/eksport: `#syncmsg`, bez `alert()`.
- Mobile: taby w 2 rzędach (3+2), diagramy bez poziomego scrolla (mermaid `max-width:100%`).

## 4. Komponenty

- `NowCard`: kompakt na zakładkach ≠ TERAZ; 1 przycisk → rozdział.
- `PlaybookSteps`: numer + link `#roz-*` + `<code>path</code>`.
- `Sources`: `<details>` z `type` + `why` per link (Konstytucja §3.4).
- `ProductQuote`: cytat z `dsaas-platform-main/AGENTS.md § Misja`.
- `Diagrams`: 7 szt. (L1–L9, łańcuch, HITL, izolacja, Kokpit/Maszynownia, 3 agenty, budżet 30/6/3/1).

## 5. Odbiór (DoD v3.1)

- `python scripts/validate-academy-export.py` → PASS v3.1
- Node: składnia inline JS OK
- Walkthrough 360px: 5 zakładek, playbook klikalny, DSAAS accordion
- Eksport/import round-trip bez utraty `_scratch`
