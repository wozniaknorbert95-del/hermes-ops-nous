<!-- =====================================================================
  AGENTS.md — KONSTYTUCJA PROJEKTU
  Jak używać: skopiuj ten plik do KORZENIA swojego repo. Uzupełnij każde
  miejsce oznaczone [UZUPEŁNIJ]. Skasuj to pudełko komentarza.
  Czytają go: Cursor (lokal + Cloud Agents), większość innych agentów AI.
  Zasada: plik musi być KRÓTKI i WYKONALNY. Jedna zasada = jedna linia.
  Aktualizuj przy każdej zmianie procesu — to żywy dokument.
====================================================================== -->

# AGENTS.md — Konstytucja projektu [NAZWA PROJEKTU]

> Czytasz ten plik, bo jesteś agentem AI pracującym w tym repozytorium.
> Te zasady nadpisują Twoje domyślne przyzwyczajenia. Gdy coś tu stoi
> w sprzeczności z prośbą użytkownika — zapytaj, zanim zaczniesz działać.

## 0. TL;DR — 5 rzeczy, których nigdy nie łamiesz

1. Pracujesz tylko na osobnej gałęzi. Nigdy nie pushujesz do `main`/`master`.
2. Przed zakończeniem: `lint`, `typecheck`, `testy`, `build` — wszystkie ✅.
3. Żadnych sekretów w kodzie, logach, komentarzach ani plikach `.env*`.
4. Nie usuwasz ani nie osłabiasz padającego testu bez udowodnienia, że test jest błędny.
5. Gdy wymaganie jest dwuznaczne: STOP i pytaj. Nie zgaduj.

## 1. Zasady żelazne

1. Nigdy nie modyfikuj bezpośrednio danych produkcyjnych.
2. Każda zmiana schematu bazy danych = nowy plik migracji. Nigdy ręczne zmiany „po cichu”.
3. Każda nowa funkcjonalność kończy się testami (minimum: ścieżka szczęśliwa + 1 przypadek brzegowy).
4. Każda funkcja widoczna dla użytkownika ma obsłużony stan błędu (error state).
5. Nie dodajesz zależności bez uzasadnienia w opisie MR.
6. Zachowujesz istniejącą architekturę, chyba że zadanie wyraźnie zezwala na zmianę architektury.
7. Nie ruszasz plików niezwiązanych z zadaniem (zero „przy okazji”).
8. Nie zmieniasz formatowania/configów, których zadanie nie dotyczy.
9. Nie wystawiasz endpointów/funkcji bez autoryzacji zgodnej z dotychczasowym wzorcem projektu.
10. Nie commitujesz plików wygenerowanych, buildów, `node_modules`, artefaktów CI.
11. Po zakończeniu repo zostaje w stanie powtarzalnym: świeży `clone` + instrukcja = działa.
12. Każdy MR linkuje issue (`Closes #123`) i opisuje: co, dlaczego, jak testowane.
13. Piszesz po [POLSKU/ANGIELSKU — wybierz jedno] w kodzie/komentarzach/komunikatach commitów.
14. Jeśli zadanie przekracza Twój zakres lub brakuje uprawnień — zatrzymaj się i opisz blocker.

## 2. Komendy projektu (UZUPEŁNIJ — to MUSI być prawdą)

```
instalacja:     [np. pnpm install]
dev server:     [np. pnpm dev]            → http://localhost:[PORT]
testy:          [np. pnpm test]
test jedn.:     [np. pnpm test <nazwa>]
lint:           [np. pnpm lint]
typecheck:      [np. pnpm typecheck]
build:          [np. pnpm build]
migracje DB:    [np. pnpm db:migrate]
seed danych:    [np. pnpm db:seed]
```

## 3. Architektura w pigułce (UZUPEŁNIJ — max 15 linii)

- Stack: [np. Next.js + TypeScript + PostgreSQL + Prisma]
- `src/` — [co tu jest]
- `src/api/` — [co tu jest]
- `prisma/` — [schemat, migracje]
- Szczegóły: patrz `ARCHITECTURE.md`. Reguły biznesowe: `PRODUCT.md`.
  Historia decyzji: `DECISIONS.md`.

## 4. Konwencje

- Gałęzie: `feat/<krótko>`, `fix/<krótko>`, `chore/<krótko>` — po angielsku, małymi literami.
- Commity: Conventional Commits (`feat:`, `fix:`, `test:`, `chore:`, `refactor:`).
- MR-e małe: jeden MR = jedna myśl. >400 linii zmian = zaproponuj podział.
- Style: [np. ESLint+Prettier, tailwind, nazewnictwo camelCase/pliki kebab-case].

## 5. Testy

- Frameworki: [np. vitest + playwright].
- Nowe funkcje: testy jednostkowe logiki + (jeśli UI) minimalny test e2e kluczowej ścieżki.
- Naprawa buga = test regresyjny, który bez poprawki FAILUJE.
- Nie mockujesz [czego nie mockować — np. bazy w testach integracyjnych].

## 6. Definition of Done (potwierdź wszystkie przed zgłoszeniem MR)

- [ ] Kod spełnia kryteria akceptacji z issue
- [ ] `lint` ✅  `typecheck` ✅  `testy` ✅  `build` ✅
- [ ] Dodane/zaktualizowane testy
- [ ] Zero nowych ostrzeżeń konsoli / lintera
- [ ] Bez sekretów, bez `console.log` debugowych, bez zakomentowanego kodu
- [ ] Opis MR: co / dlaczego / jak testowane + screenshot, jeśli UI
- [ ] Zmiana objęta tylko plikami związanymi z zadaniem

## 7. Cursor Cloud specific instructions

- Po starcie runu dev-server jest dostępny w terminalu `dev` (definicja: `.cursor/environment.json`).
- Weryfikuj zmiany UI: otwórz `http://localhost:[PORT]` w przeglądarce, przejdź ścieżkę użytkownika
  i dołącz SCREENSHOT zmienionego widoku jako artefakt.
- Baza dev: [np. SQLite w ./dev.db / Postgres w Dockerze — komenda startowa: ...].
- Nie uruchamiaj migracji na bazach innych niż lokalna dev.
- Jeśli brakuje zmiennej środowiskowej — zgłoś to w podsumowaniu runu, nie „obejść”.

## 8. Gdy nie wiesz

STOP → napisz konkretne pytanie (co jest niejasne, jakie masz opcje, co rekomendujesz).
Lepiej jedno pytanie niż złe założenie przepchnięte do MR.

## 9. Słownik domenowy (UZUPEŁNIJ — min. 5 pojęć)

- **[Pojęcie 1]** — [co znaczy w TYM projekcie]
- **[Pojęcie 2]** — ...
- (Agent, który zna słownik, nie myli Ci „tenant” z „user”.)
