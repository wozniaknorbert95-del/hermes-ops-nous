# Handoff — spec nawigacji i kontroli `/ops` — 2026-09-28

**Status:** Spec w repo. Zero zmian `OPS.html`. Nie deployowano.

## Co zrobione

Katalog wszystkich gestów i linków na Hermes Ops + docelowa IA + backlog P0–P3.

- `docs/ops/PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md` — spec (Pokazuje / Robi / Nie robi / Stan)
- `docs/ops/README.md` — jedna linia w „Plan i audyt”
- `docs/ops/UX-SPEC-HERMES-OPS-ENTERPRISE.md` — wskaźnik „następna iteracja”

Enterprise UX-SPEC z 27.09 zostaje SoT **już wdrożonych** pikseli.

## Co live

Bez zmian. VPS nie ruszany.

## Co zablokowane

Implementacja P0 (linki Linear w kolejce + `recommended_issue`) czeka na GO Dowódcy.

## Następny krok

Po GO: atom P0 #1 — `OPS.html` `renderLane` / `renderPulse` jako linki Linear (nie udawany Run).

## Komendy weryfikacji (copy-paste)

```
python scripts/validate-academy-export.py
```

Oczekiwane: `PASS: academy export contract`. Mutacji nie odpalano (docs-only).

## Pliki dotknięte

- `docs/ops/PLAN-UX-NAV-CONTROL-HERMES-OPS-2026-09-28.md` (added)
- `docs/ops/README.md` (modified)
- `docs/ops/UX-SPEC-HERMES-OPS-ENTERPRISE.md` (modified)
- `docs/handoffs/2026-09-28-ops-nav-control-spec.md` (added)
