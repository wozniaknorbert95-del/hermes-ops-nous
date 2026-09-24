# Handoff — DSAAS + local gate + dział H 2026-09-24

**Repo:** akademia · **Branch:** `feat/restore-dsaas-local-gate`  
**Nie:** deploy VPS (brak GO). **Nie:** 7. zakładka. **Nie:** 7. dział Kokpitu.

## T1 GitHub bez kasy — DONE

Płatne `ubuntu-latest` na PR wyłączone (`workflow_dispatch` only). Required check `academy-gate` zdjęty z `main`. Bramka: `bash scripts/deploy-ready-hermes-ops.sh`. Docs: `docs/ops/LOCAL-GATE.md`.

## T2 DSAAS — DONE

`renderDsaas()` był w pliku, ale `renderMainPanel` go nie wołał; `#dsaas` szło do INSTRUKCJI. Nav: **DSAAS** (`id: kurs`). Galeria mermaid + produkt + scoreboard + mastery + B–H. Browser: tab DSAAS selected, diagramy widoczne (ASCII fallback gdy CDN mermaid nie wstanie).

## T3 Cloud PR #64 — wchłonięte

Dział H (H1–H3) + `docs/akademia/*`. Pusty postęp → TERAZ H1. Kurs A–H ≠ Kokpit 6 działów. Konflikty scalone: DSAAS zostaje, H nie kasuje mermaidów.

## DoD

- [x] 6 zakładek
- [x] pełna linia `testy:` AGENTS.md (lokalnie)
- [ ] Merge do `main` — na GO Dowódcy (teraz **można** bez płatnego CI)
- [ ] Deploy VPS — na GO

## ▶ TERAZ

1. Review branch, merge (lokalny `deploy-ready` + `git push`).
2. W SKU wpisać widełki ceny przed outreach (H2).
3. Deploy Akademii na GO.
