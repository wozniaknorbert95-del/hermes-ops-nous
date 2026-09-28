# Raport użyteczności — `/ops` — 2026-09-28

**Persona:** Dowódca, telefon 390×844, 2 minuty, ADHD-first. Job: **zobaczyć zadania** i ruszyć albo otworzyć Linear.

**WERDYKT (przed): Fail. Po poprawce + polish: Conditional Pass** na foldzie (kolejka widoczna). Live po deploy.

Cursor-browser nie doszedł do `localhost` (inna maszyna) ani do live `/ops` (401 bez hasła). Dowód: headless Edge na laptopie, `http://127.0.0.1:8766/OPS.html`.

## Interaction (skrót, nie pełny 11-scenario ux-audit)

- Otwarto `/OPS.html` 390×844 i 1440×900.
- Zmierzone: sticky `.hud` zawierał całą kartę Next + 6 checków pre-flight (~viewport).
- Scroll: treść pod HUD istniała (kolejka), ale na 844px była **przysłonięta** sticky overlay.
- Kolejka była **trzecia** w `main` (po Wynik i Kontekst).
- `ensureTickAutopilot` na starcie POST `/ops/run` → przy HTML zamiast JSON: `SyntaxError` na foldzie.

## Findings (przed)

| ID | Sev | Co | Gdzie |
|---|---|---|---|
| C1 | Critical | Sticky HUD wyższy niż ekran — scroll „nie działa”, klik trafia w overlay | `OPS.html` `.hud` + `#next-card` w `<header>` |
| C2 | Critical | Zadań nie widać — kolejka pod Wynikiem, w Kontekście | `#panel-queue` |
| H1 | High | Pre-flight 6 wierszy zawsze otwarty | `#preflight` |
| H2 | High | Pause / Take over obcięte na 844px | ten sam HUD |
| M1 | Medium | `SyntaxError: Unexpected token '<'` na foldzie | `send()` catch + POST zanim JSON status |

## Poprawka w tej gałęzi

- HUD = pille + raport (krótki sticky). `#next-card` **poza** headerem.
- Pre-flight = `<details>` (`Zanim ruszysz · N ✗`).
- **Kolejka pierwsza** w `main`.
- Sticky h2 desktop zdjęty.
- Błąd sieci: „Vault nie odpowiedział JSON”. Autopilot POST dopiero po JSON `/ops/status`.
- Guardy Q14/Q15.

**Po (390×844):** Pause/Stop/Retry/Take over + nagłówek **Kolejka Linear** w pierwszym ekranie.

## TOP 5

1. C1 sticky HUD  
2. C2 kolejka za foldem  
3. H1 pre-flight  
4. M1 SyntaxError  
5. H2 obcięte tertiary  

Hold: przed poprawką to był panel sterowania, który **siedział na zadaniach**. Po: widać kolejkę; na live z danymi pojawią się QUI-*.

## Następny krok

Zmergowane i wdrożone w tej sesji (commit + PR + deploy).
