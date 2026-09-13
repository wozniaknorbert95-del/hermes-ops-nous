# Handoff — Akademia vault/PWA na osobny PR

**Data:** 2026-09-13  
**Repo:** `akademia`  
**Sesja:** vibeinit + Linear OS Wave 2 (EV-335) — wybrano **C**  
**Gałąź:** `feat/progress-vault-pwa`

---

## Co zrobione

- Wybrano **C**, bo **A** i **B** są zablokowane:
  - **A** wymaga merge PR #5 — nadal `open` (`docs/linear-os-wave2-akademia`).
  - **B** wymaga QUI-18 Done — status **In Progress**; filtry §7 i powiadomienia nadal puste (HITL Dowódcy).
- WIP vault/PWA/VPS zdjęty z brudnego lokalnego `main` (był 2 commity za `origin/main` / #4).
- Branch od `origin/main` (z F4 / ENT-12 nie TERAZ) + vault/PWA, bez treści Wave 2 (WF-P6 / 8 widoków).
- Gate: `validate-academy-export.py` PASS, `test_progress_vault.py` PASS.
- Zero deployu (Zasada 11). Zero sekretów w commicie (`.htpasswd` / `CREDENTIALS.local.txt` w `.gitignore`).

## Co live

Bez zmian w tej sesji. Poprzedni smoke VPS: patrz `docs/handoffs/2026-09-13-akademia-vps-sync-deploy.md`.

## Co zablokowane

| Item | Blocker | Właściciel |
|------|---------|------------|
| A — smoke po merge #5 | Human merge #5 | Dowódca |
| B — Faza B checklist | QUI-18 filtry + notyfikacje HITL | Dowódca |
| Platforma Wave 2 | PR #34 `mergeable_state=blocked` | Dowódca |
| DNS publiczny | NXDOMAIN Cyberfolks (hosts tymczasowo) | Dowódca / DirectAdmin |
| Deploy VPS | Zasada 11 — czekaj GO | Dowódca |

## Następny krok (jeden TERAZ)

**Human merge PR vault/PWA** (ten branch) **albo** najpierw #5 — nie oba naraz bez rebase. Po merge #5: smoke DZIEŃ/TERAZ + `validate-academy-export.py` (zadanie A).

## Status PR

| PR | Stan | URL |
|----|------|-----|
| akademia #5 Wave 2 Faza A | open, clean, 0 checks | https://github.com/wozniaknorbert95-del/akademia/pull/5 |
| akademia vault/PWA | ten PR | (uzupełnij po `gh pr create`) |
| platforma #34 Wave 2 | open, **blocked** | https://github.com/wozniaknorbert95-del/dsaas-platform-main/pull/34 |

## Komendy weryfikacji

```
python scripts/validate-academy-export.py
python scripts/test_progress_vault.py
python -m http.server 8765
```

→ http://localhost:8765/DASHBOARD.html — TERAZ = A1 (pusty localStorage); DZIEŃ tor placeholder = WF-P9 vault.

## Pliki dotknięte

- `DASHBOARD.html`, `manifest.webmanifest`, `icons/icon.svg`
- `host/*`, `scripts/*akademia*`, `scripts/test_progress_vault.py`, `scripts/validate-academy-export.py`
- `docs/ACADEMY-UX-SPEC.md`, `docs/CURSOR-WORKFLOW.md`, `docs/runbooks/AKADEMIA-VPS.md`
- `AGENTS.md`, `.gitignore`, `data/.gitkeep`
- ten handoff + `docs/handoffs/2026-09-13-akademia-vps-sync-deploy.md`

## Cursor — restart

vibeinit z `docs/CURSOR-WORKFLOW.md`, potem: po merge #5 zrób **A**; Faza B dopiero po QUI-18 Done.
