# Plan domknięcia — Cloud + DSAAS + deploy 2026-09-24

**GO Dowódcy:** merge + deploy (Zasada 11).  
**Cel:** jeden `main`, zero zduplikowanych PR, VPS = ten `main`, testy pro, handoff.

## Stan wejścia

| PR / gałąź | Co ma | Luka |
| --- | --- | --- |
| `main` `b9faade` | vault I1, SIGPIPE setup | brak UX v5, DSAAS nav, dział H |
| #64 `cursor/akademia-dzial-h-577c` | H | duplikat; bez UX v5, bez DSAAS restore, bez SIGPIPE |
| #67 `cursor/ux-quiet-landing-577c` | UX U1–U5 + H + deploy plan | **bez** `renderDsaas` / local-gate / SIGPIPE (#66) |
| `feat/restore-dsaas-local-gate` | DSAAS + local-gate + H + SIGPIPE | **bez** UX v5 CSS/guardów |

## Kroki (kolejność)

1. **Scalenie kodu** — merge UX v5 **w** `feat/restore-dsaas-local-gate`. Konflikty: DSAAS zostaje (`title:'DSAAS'`, `renderDsaas()`), UX v5 (chips none, `--nav-active`, calm, winda open only) zostaje.
2. **Testy** — pełna linia `testy:` AGENTS.md PASS.
3. **GitHub** — wypchnąć komplet na `cursor/ux-quiet-landing-577c` (aktualizacja #67); zamknąć **#64** (duplikat H); #67 ready → merge do `main`.
4. **Deploy** — `deploy-ready-hermes-ops.sh` → `deploy-akademia-vps.sh` (GO).
5. **Smoke** — macierz z `docs/DEPLOY-PLAN-AKADEMIA-2026-09-24.md` + I1 Pause + `/hermes/chat` 410 + PWA 200/200/401 + UX: tab DSAAS + H1.
6. **Handoff** — SHA, smoke, otwarte PR = 0 draftów Cloud.

## DoD

- [ ] Jeden merge do `main` zawiera: I1 vault (już), SIGPIPE, DSAAS, UX v5, H, local-gate, deploy plan
- [ ] PR #64 closed
- [ ] PR #67 merged (lub zastąpiony 1:1 i closed)
- [ ] `HEAD == origin/main` po merge
- [ ] VPS smoke PASS
- [ ] Browser: DSAAS mermaidy + quiet landing
- [ ] Handoff w `docs/handoffs/`
