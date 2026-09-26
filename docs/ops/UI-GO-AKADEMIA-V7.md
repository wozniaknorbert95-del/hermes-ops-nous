# UI GO — Akademia v7 (HTML WYKONANE)

**Status HTML:** WYKONANE 2026-09-26 (`DASHBOARD.html` = 7 tabów, `ACADEMY_TAB_COUNT=7`).  
**Ship:** gałąź `feat/academy-ui-v7` + PR (to GO).  
**Deploy:** **WAITING-GO** (Zasada 11). Nie ruszaj VPS bez jawnego GO Dowódcy.  
Kontrakt: [`PLAN-AKADEMIA-START-2026-09-26.md`](PLAN-AKADEMIA-START-2026-09-26.md).

## Zrobione na laptopie

- Scalenie TERAZ + DZIEŃ; hash `#day` → `now`; `ACADEMY_TAB_COUNT=7`.
- Koło zębate: vault, eksport, import, PWA. Stopka zapisu nie jest na foldzie.
- Kill `renderOpsCta()` na TERAZ; `id="ops-howto"` na karcie Hermes Engineer (M9).
- `firstOpen` nauki: B→C→D→E→F→G. Mapa `is-current` = ten dział (A/H gdy tab).
- WORKFLOW: mermaid + kotwice `#wf-rule-*`; A1–A7 w details „Siłownia labu”.
- NARZĘDZIA: pola z [`TOOL-MASTERY.md`](TOOL-MASTERY.md) (fala 1 above-fold).
- DSAAS: tożsamość + 18 DoD B→G; Wave 2 pod F.
- Paski: 18 DoD + `local|ops|phone` (`_scratch.work_log`).
- Walidator + Fala 0/L/M/O/P. Fala J: `mutation-test-fala-p.py` w workflow i `testy:`.

## Deploy

Osobne GO. Ten plik **nie** odblokowuje `deploy-akademia-vps.sh`.
