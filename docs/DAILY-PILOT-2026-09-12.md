# Daily pilot — Academy Command Dashboard (2026-09-12)

**Cel:** 1 doba pracy z dashboardem local-first. Bez API, bez tokenów.

## Przebieg (skrót)

- Rano: `▶ TERAZ` → 1 krok z bieżącego modułu; checklist Dzień (digest/board/runy); 1 priorytet ręcznie.
- W dzień: lekcje wyłącznie po klikalnych linkach; lab w `workflow-lab`, nie w Akademii.
- Wieczorem: 3 checkboxy domknięcia + 1 zdanie „co pierwsze jutro".
- Piątek: formularz lokalny (koszt/lekcja/porządek) + eksport JSON.

## Wynik weryfikacji (potwierdzone)

- `scripts/validate-academy-export.py` = PASS.
- Inline JS dashboardu: `node --check` = OK.
- Eksport/import: komunikaty inline (sukces/błąd), brak `alert()`, brak przeładowania strony przy imporcie.
- Blokada modułów: pola zablokowanych modułów są `disabled`, bieżący rozwija się sam.
- Telefon: jedna kolumna, przyciski min. 44px, `prefers-reduced-motion` respektowany.
- `file://`: lekcje m1–m3 klikalne; dla pełnej nawigacji zalecane `python -m http.server`.

## Potwierdzone poprawki wpisane w ten PR

1. Jedna karta `▶ TERAZ` jako prawdziwy przycisk prowadzący do bieżącego modułu.
2. Strefy Dzień / Platforma (ręcznie) / Piątek jako lokalne checklisty.
3. Klikalne biblioteki m1–m3 + instrukcja `python -m http.server`.
4. Progressbar ARIA + tekst „X% (N z 6)", fokus klawiatury, skip link, `<main>`.
5. Eksport: kopiuj + pobierz JSON + widoczny status; import z błędem inline.

## Nie potwierdzone (nie wpisane)

- Live status z GitHub/Linear — odłożony jako osobny projekt (auth/backend/audyt).
- Widget postępu w Kokpicie — kontrakt istnieje, konsument w platformie nie istnieje.
