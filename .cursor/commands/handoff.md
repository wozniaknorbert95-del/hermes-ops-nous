---
description: Handoff sesji akademii — docs/handoffs/, fakty, zero sekretów, bez commit
---

Komenda **`/handoff`**. Koniec sesji. Argument opcjonalny: `$ARGUMENTS` (krótki tytuł pliku, kebab-case).

## Wejście

1. `git status` i lista plików dotkniętych — bez tego FAIL.
2. Szablon: skopiuj **ostatni** plik z `docs/handoffs/` i podmień sekcje (nie zmyślaj nowego layoutu).
3. Zapisz `docs/handoffs/YYYY-MM-DD-krotki-tytul.md`.

## Sekcje (obowiązkowe)

- Co zrobione (fakty, nie plany)
- Co live (URL, smoke) — albo „nie deployowano”
- Co zablokowane (blocker + właściciel)
- Następny krok (**jeden** TERAZ)
- Komendy weryfikacji (copy-paste)
- Pliki dotknięte (lista)

## Zakres

- TAK: jeden plik handoff + ewentualnie aktualizacja docs wskazana w sesji.
- NIE: commit, push, deploy, PR — chyba że Dowódca **w tej sesji** o to poprosił.

## Zakazy

- `/deploy` `/publish` `/skip-gate` `/force-merge`. Nie kopiuj szablonu EV/`todo.json` z palety platformy.
- Hasła, tokeny, zawartość `.env` — w handoffie tylko wskazówka „VPS CREDENTIALS.local.txt”.
- `academy_url` z OIDC. Fałszywe „live”, gdy nie było smoke.

## PASS / FAIL

- PASS: plik w `docs/handoffs/`, status git w treści, jeden NEXT, zero sekretów.
- FAIL: brak `git status`; NEXT jako lista pięciu rzeczy; commit bez prośby; hasło w markdownie.
