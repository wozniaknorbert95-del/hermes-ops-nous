---
description: Audyt UI Akademii przed merge — spec v7, schema 0.1.0, 360/768
---

Komenda **`/auditread`**. Przed merge albo po większej zmianie UI (`DASHBOARD.html`, schema, sync). Argument opcjonalny: `$ARGUMENTS` (zakładka albo plik).

## Wejście

1. Przeczytaj `docs/ACADEMY-UX-SPEC.md` (v7), `schema/academy-progress.v0.json`, `AGENTS.md`.
2. Uruchom:

```
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
```

3. Sprawdź ręcznie **360px i 768px:** jedno TERAZ, `#nowcard` ukryty, sticky taby, `scroll-margin` kotwic, stany sync-bar / `#tty-sync`.
4. Mermaid: kontrast edgeLabel ≥ 4.5:1; offline = fallback tekstowy jeśli CDN padnie.
5. Eksport JSON: `schema_version` 0.1.0, `source` academy-os, `academy_url` bez tokenów, `_scratch` OK (Kokpit ignoruje).
6. Nav = 7 tabów. `/ops` nie jest 8. tabem. Nie dodawaj/usuwaj tabów bez GO.

Skill opcjonalny: `ux-audit` na `http://localhost:8765/DASHBOARD.html` (pełny sweep, nie zastępuje walidatora).

## Zakres

- TAK: lista findingów z repro + plik.
- NIE: „przy okazji” redesign; deploy; kopiowanie Kokpitu / 7. działu.

## Zakazy

- `/deploy` `/publish` `/skip-gate` `/force-merge`. Nie ładuj `audit-ux` platformy (screen_role / Kokpit).
- Token w `academy_url`. Druga karta TERAZ. Iframe dashboardu w Kokpicie.

## Format wyniku

```
AUDITREAD: PASS | FAIL
GATE: validate+vault <exit>
VIEWPORTS: 360 | 768 | skip
FINDINGS:
- <repro> → <plik>
NEXT: <jeden fix albo merge OK>
```

## PASS / FAIL

- PASS: walidator zielony, 7 tabów, jedno TERAZ, eksport bez sekretów, zero findingów blocker.
- FAIL: walidator czerwony; druga karta TERAZ; 8. tab; finding bez repro.
