---
description: Start sesji akademii — TERAZ, jeden plik, bramka export+vault
---

Jesteś agentem w repo **akademia** (szkoła + Hermes Ops `/ops`). Komenda **`/vibeinit`**.

To **nie** jest `dsaas-platform-main` ani `workflow-lab`. Nie ładuj palety 38 komend platformy (`/autopilot`, `/gate`, `session-preflight`, QUI, `todo.json`).

Argument opcjonalny: `$ARGUMENTS` (np. nazwa jednego pliku albo „ops”).

## Wejście (kolejność twarda, read-only)

1. Przeczytaj `AGENTS.md`, `README.md`, `docs/OPERATING-MODEL.md` (§1–3, §1.1 split).
2. Jeśli sesja dotyka `/ops`, vaulta lub tick: `docs/ops/README.md` → `HERMES-ROLE-CONTRACT.md` → `RUNBOOK-OPS-WIRING.md`.
3. Otwórz `DASHBOARD.html` — zakładka TERAZ = jedyny „co teraz” kursu. Praca agentowa = `/ops` (osobna PWA, nie 8. tab).
4. Dev: `python -m http.server 8765` → `http://localhost:8765/DASHBOARD.html` i `http://localhost:8765/ops`.
5. Gate (przed kodem, jeśli drzewo ma zmiany w kontrakcie UI/vault):

```
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
```

## Zakres

- TAK: jeden atomowy krok, jeden plik (albo para plik+test, gdy kontrakt tego wymaga).
- NIE: deploy VPS, SSH z hasłem, sekrety w `academy_url`, druga karta TERAZ, 8. tab, iframe Kokpitu.

## Zakazy

- `/deploy` `/publish` `/skip-gate` `/force-merge` — nie instrukować, nie dodawać tu 5. rytuału z palety platformy.
- Push na `main`. Commit tylko na prośbę Dowódcy.
- Mieszanie kursu (`DASHBOARD.html`) z Control Plane (`OPS.html`) w jednym „przy okazji”.

## Raport startu (maks. 15 linii)

```
REPO: akademia
TERAZ: <co w ▶ TERAZ / firstOpen>
OPS: tak | nie  (czy sesja dotyka /ops, vault, tick)
PLIK: <jeden plik>
GATE: validate+vault PASS | SKIP (czyste drzewo, tylko docs) | FAIL
STOP: <brak albo jeden blocker>
NEXT: <jeden atomowy krok>
```

## PASS / FAIL

- PASS: raport wypełniony, jeden plik, zasady z `AGENTS.md` znane.
- FAIL: zgadywanie TERAZ bez otwarcia dashboardu; start od palety platformy; brak gate przy zmianie HTML/schema/vault.
