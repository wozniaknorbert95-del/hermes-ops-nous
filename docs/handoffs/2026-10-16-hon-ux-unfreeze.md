# Handoff — F5 polish OPS.html (HON-UX-UNFREEZE)

**Data:** 2026-10-16  
**GO:** F5 polish (atomy A/B/C)  
**Branch:** `feat/f5-polish-ops`

## Atomy

| Atom | DoD | Stan |
| --- | --- | --- |
| **A** viewport | `#hud-truth` dominant; `#run-truth` = jedna meta; `#how-start` ukryty gdy occupying; mobile ≤3 chipy | DONE |
| **B** sesja | pill/eyebrow `CZEKAJ` gdy waiting; `#session-proof` „Otwórz sesję Cloud”; Zapytaj Czekaj bez URL | DONE |
| **C** folds | skip „Przejdź do runu”; KONTEKST/DZIENNIK bez `open` (mobile first visit zwinięte); dispatch copy skrócony | DONE |

## Guardy

- F9: zero cost HUD / Agents Window
- `python scripts/validate_todo_nous.py` PASS
- `python scripts/test_progress_vault.py` PASS (w tym chat Czekaj)

## Deploy

Po merge `main`: `bash scripts/deploy-akademia-vps.sh` → SMOKE + MD5 `OPS.html`.

## NEXT

`IDLE` — Linear produkt / lab QUI-131·129. F9 reject nadal.
