# Fala H — świeże urządzenie kasowało zapis Dowódcy (P0)

Data: 2026-09-20 · Poprzednia sesja: [sync + Basic Auth](../handoffs/2026-09-20-akademia-sync-basic-auth-fala-g.md)

## Co się stało

Dowódca napisał „przetestowałem". Sprawdziłem log Nginx i **backup faktycznie zaczął działać** —
pierwsze w historii projektu `PUT /progress` z telefonu: 9 udanych zapisów z Androida Chrome,
wszystkie HTTP 200. W vaultcie leżały jego dane: `day_teraz`, `day_linear_proj`, `hermes_seen`.

Ale przy okazji sprawdzania kształtu zapisu zauważyłem **zagnieżdżony `_scratch`**
(`_scratch._scratch`). Chciałem udowodnić, że odtwarzanie z vaulta działa — i zamiast
potwierdzenia znalazłem P0.

## P0: backup niszczył backup

**Scenariusz: nowy telefon albo wyczyszczone dane przeglądarki.**

Odtworzyłem to deterministycznie: prawdziwy `DASHBOARD.html` po HTTPS (mini-vault), świeży origin
(pusty `localStorage`), vault zasiewany **dokładnym** payloadem z produkcji (664 B, dwa odhaczone
kroki rytuału).

```
PRZED:  GET /progress (200, 664 B z pracą)  →  PUT /progress 412 B (PUSTY)
        vault: 664 B → 412 B.  Dwa kroki Dowódcy SKASOWANE.

PO:     GET /progress (200, 664 B z pracą)  →  BRAK PUT
        vault: 664 B bez zmian, kroki ODTWORZONE w UI.
```

To najgorszy możliwy wariant awarii: użytkownik instaluje PWA na nowym telefonie i **traci cały
kurs z serwera**.

### Przyczyna

`initApp()` woła `initDay()` **przed** `pullProgress()`, a `initDay()` stemplował czas:

```javascript
function initDay(){var t=todayISO();if(!state.day_stamp){
  state.day_stamp=t;
  touchLocalUpdated();   // ← „mój stan jest z 12:05" na ŚWIEŻYM urządzeniu
  saveLocal();return;}
```

Świeże urządzenie deklarowało więc stan z `12:05:39`, a zapis w vaultcie miał `12:03:00`.
Reguła „nowszy wygrywa":

```
remoteAt (12:03:00) < localAt (12:05:39)  →  „zdalny jest starszy"  →  NADPISZ
```

Poprzednie guardy (F1–F3) tego nie łapały, bo `hasContent` liczy `active_tab` i `day_stamp`
jako treść — a to książkowość, nie postęp. Więc `remoteHasContent(env)` było `true`
i pusty stan lokalny spokojnie wygrywał.

## Naprawa — dwie warstwy

**1. Gwarancja (defense in depth): treść bije znaczniki.**

Nowy `hasWork(obj)` liczy wyłącznie realną pracę: `_pass` rozdziałów, kroki labów, kroki rytuału
dnia, linie `today/tomorrow first`, `day_closed`. `mergeRemote` rozstrzyga teraz tak:

```javascript
var rWork=hasWork(env._scratch),lWork=hasWork(state);
if(rWork&&!lWork){applyRemote(env);return;}                                  // treść wygrywa
if(!rWork&&lWork){SYNC.remoteUpdatedAt=remoteAt;schedulePush();saveLocal();return;}
if(remoteAt>localAt){applyRemote(env);}else if(remoteAt<localAt){schedulePush();}
```

Znaczniki decydują **tylko** gdy praca jest po obu stronach. Puste urządzenie nie może już
zniszczyć niepustego zapisu — niezależnie od zegara.

**2. Przyczyna: `initDay()` przestał stemplować czas.** Inicjalizacja dziennika to nie praca
Dowódcy. Postęp stempluje `save()`.

## Dowód, że oba kierunki nadal działają

| Scenariusz | Log serwera | Vault |
|---|---|---|
| Świeże urządzenie | `GET` — zero PUT | 664 B **nietknięte**, kroki odtworzone w UI |
| Klik Dowódcy | `PUT 637 B` | `day_one_issue` **dopisany**, poprzednie kroki **zachowane** |

Merge jest additywny — restore nie gubi niczego, write nie cofa.

## Guardy (Fala H)

`H1` (brak reguły „treść bije znaczniki"), `H1b` (brak liczenia pracy po obu stronach),
`H2` (`initDay` stempluje na starcie), `H3` (`hasWork` znika). Wszystkie zweryfikowane mutacją:
**26/26 złapane** w `mutation-test-fala-e.py`, plus Fala 0 (10/10) i Fala D (19/19) bez regresji.

Poprawka walidatora: `merge_fn` cięte było na 1400 znaków — komentarze tej naprawy wydłużyły
funkcję, więc guardy patrzyłyby na niepełny kod (fałszywa zieleń). Okno podniesione do 2600.

## Wnioski dla kolejnych sesji

1. **Zagnieżdżony `_scratch` to nie błąd.** `envelope()` robi `_scratch = Object.assign({},state)`,
   a `state` sam zawiera `_scratch` — stąd poziom zagnieżdżenia i dlatego `_scratch._scratch: {}`.
   Nie „naprawiać" tego bez zrozumienia.
2. **Backup, który nie został przetestowany na świeżym urządzeniu, nie jest backupem.**
   Test „odhacz i odśwież" na tym samym telefonie nie wykryje klasy błędów „puste nadpisuje pełne" —
   tam `localStorage` jest pełny. Trzeba czyścić origin.
3. **Testuj scenariusz nowego telefonu przed każdą zmianą w sync.** To jedyny scenariusz,
   w którym użytkownik naprawdę potrzebuje vaulta.
