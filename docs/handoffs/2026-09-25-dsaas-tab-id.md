# Handoff — prawdziwa zakładka DSAAS + ścieżka H

**Data:** 2026-09-25  
**Gałąź:** `feat/dsaas-tab-id` (nie zmergowana, nie deploy)  
**Baza:** `main` `aedbb69`

## Co

Nav **DSAAS** ma `id:'dsaas'` i panel `panel-dsaas` (`renderKurs → renderDsaas`).  
`firstOpen` chodzi po `KURS_DZIAL_ORDER` (H→G→B…→A): pusty start H1, po `H1_pass` TERAZ = **H2** (nie A1).  
Dział A tylko w WORKFLOW. Guardy walidator + mutacje A6–A8.

## Testy

Pełna linia `testy:` AGENTS.md PASS (Fala E: zatrzymać `python -m http.server` na Windows — lock `DASHBOARD.html` → OSError 22).

Browser 360px localhost:8765: tab DSAAS selected, `#dsaas` + `#dsaas-flows` + `#dzial-H` open + 13 mermaid, `dzial-A` nie na DSAAS. Po `H1_pass` TERAZ pokazuje H2.

## Nie zrobione (świadomie)

- Deploy VPS — czeka na GO (Zasada 11).  
- P2 Dowódca: widełki SKU + H2 ×10 outreach.  
- Commit / PR — nie proszone.

## Następny krok

Review gałęzi → commit/PR na Twoje GO → `deploy-ready` → GO deploy.
