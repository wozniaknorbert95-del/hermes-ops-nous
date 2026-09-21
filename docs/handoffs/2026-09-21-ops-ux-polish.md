# Handoff — Hermes Ops UX polish 2026-09-21

**Repo:** akademia · gałąź `feat/ops-ux-polish`

## Co

Polerka `/ops` pod telefon (operator console, nie kurs):

- HUD: osobne pille **engine** + **mode**; PAUSED = amber, RUNNING = pulse, UNKNOWN = szary
- CTA: Start vs Run next zależnie od trybu/stanu; eyebrow Live / Next
- Kolejka: max 4 karty + „Pokaż jeszcze N”; truncate tytułów; poprawione empty copy
- Live: pasek S1–S6 (pass/fail/run); Approval z kind badges
- Dashboard: 4 kafelki + tokens/cost w jednej linii mini; Active agents chip
- a11y: progressbar ARIA, aria-pressed na trybach; krótszy copy sterowania

## Testy

- `validate-academy-export.py` PASS
- Fala M 8/8
- `test_progress_vault.py` PASS

## Świadomie nie

- Merge z telefonu, fałszywy $, nowy worker dropdown.
