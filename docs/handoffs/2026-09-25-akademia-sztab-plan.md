# Handoff — plan sztabu Akademii na main

**Data:** 2026-09-25  
**Zakres:** tylko dokument (Fala 0). Zero zmian `DASHBOARD.html`. Zero deploy.

## Co

Kanoniczny plan Cloud: `docs/ops/PLAN-AKADEMIA-SZTAB-2026-09-25.md`  
Spec UX: `docs/ACADEMY-UX-SPEC.md` v6  
Wskaźniki: `AGENTS.md` pkt 8, root `README.md`, `docs/ops/README.md`

## Dlaczego

Dowódca: chrome kradnie uwagę (hero/sync/„Postęp studiów 3%”/layers mermaid), DSAAS to burdel, brak szkoły lisa. Cloud agenci nie czytają `.cursor/plans/` — SoT musi być na `main`.

## Co zostaje na Cloud (PR 1–6 z planu)

Lock 8 tabów → chrome+mapa A–H → DSAAS 3 strefy → `renderMoney` H1–H4 → ŹRÓDŁA 3 karty → testy/360px. Deploy tylko osobne GO.

## Testy tej Fali 0

Docs-only. Bramka `deploy-ready` nie jest wymagana do merge dokumentu, ale nie psuje HTML.

## Stop

Czekaj, aż Cloud weźmie PR1 z promptu na końcu planu. Nie startuj UI w tym samym PR co Fala 0.
