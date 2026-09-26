# Plan Akademii — start (Cloud SoT, kontrakt)

**Status:** dokument 2026-09-26. **HTML v7 WYKONANE.** Deploy = osobne GO (Zasada 11).  
**Spec:** [`docs/ACADEMY-UX-SPEC.md`](../ACADEMY-UX-SPEC.md) **v7**.  
**Narzędzia:** [`TOOL-MASTERY.md`](TOOL-MASTERY.md).  
**Role:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md).  
**Live HTML:** 7 tabów (`ACADEMY_TAB_COUNT=7`).  
**Deploy:** WAITING-GO.

Cloud: ten plik nadpisuje [`PLAN-AKADEMIA-SZTAB-2026-09-25.md`](PLAN-AKADEMIA-SZTAB-2026-09-25.md) jako SoT reguł. Sztab v6 zostaje historią.

---

## Pięć zasad

1. **Sukces = zamknięty DoD, nie godziny.** Pasek, który rośnie, to **18 DoD** działów B–G. Pasek godzin na TERAZ jest diagnostyką (`local` / `ops` / `phone`). Brak stempla = 0. Zakaz liczenia z gita.
2. **Dwa Hermesy, dwa miejsca.** Hermes Akademii uczy (szablon, 0 tokenów). Hermes Ops (`/ops`) dowozi kolejkę. Lekcja `/ops` = karta NARZĘDZIA. Na TERAZ: jedna linia stanu + link.
3. **Głębokość = jak często tego używasz.** Pełna karta tylko dla codziennych narzędzi. PARKED = „nie startuj”.
4. **Pamięć gnije bez powtórki.** Zaliczenie = głos bez notatek + demo w `dsaas-platform-main`. Co rano jedno pytanie z `lab` już zaliczonego rozdziału.
5. **Brak pliku = „nie wiem”.** Doradca cytuje ścieżkę. Dopisywanie DoD z głowy = slop.

## Gdzie jest kurs

Kurs **nie ma osobnego przycisku**. Jest **całą zakładką DSAAS**.

Sześć działów (kolejność z pliku „działy do opanowania”, nie H-first):

| Plik | Dział UI | Zdanie z tożsamości |
|---|---|---|
| 4 Orkiestracja | **B** (start) | AI wykonuje; człowiek klika (HITL) |
| 1 Bezpieczeństwo | **C** | Zero wycieków; auth po stronie serwera |
| 3 Fundamenty LLM | **D** | Model nie myśli; RAG vs nie |
| 2 Dane i izolacja | **E** | Company brain; RLS/Cedar, nie filtr w aplikacji |
| 5 Architektura | **F** | 30/6/3/1; UI = projekcja |
| 6 Domena i dostawa | **G** | Proces MKB bez żargonu; retainer gdy działa |

**A** = siłownia labu (WORKFLOW, details). **H** = pieniądz (MONETYZACJA). Nie są roadmapą „kim jestem”.

Zaliczenie rozdziału bez obu dowodów jest błędem produktu.

## Nawigacja (kontrakt 7 tabów)

Bez zgody Dowódcy nie dodajesz i nie usuwasz tabów. Kokpit = 6 działów. `/ops` nie jest tabem.

| # | `id` | Title | Pytanie |
|---|---|---|---|
| 1 | `now` | TERAZ | Co dziś? Poranek + jeden ruch. Wchłania DZIEŃ. |
| 2 | `workflow` | WORKFLOW | Jakie twarde zasady, zanim koduję? |
| 3 | `tools` | NARZĘDZIA | Jak opanować narzędzie tej sesji? |
| 4 | `dsaas` | DSAAS | Czego się uczę, żeby być tym kim jestem? 18 DoD. |
| 5 | `money` | MONETYZACJA | Jak wziąć pieniądze? H1–H4. Nie start szkoły. |
| 6 | `sources` | ŹRÓDŁA | Co otwieram dziś? 3 karty. |
| 7 | `notes` | NOTATKI | Egzamin przy id rozdziału. |

`day` w stanie i hash `#day` → `now`.  
`TAB_BY_DZIAL`: A→`workflow`, B–G→`dsaas`, H→`money`.  
`load()`: `kurs` / `guide` / `hermes` → `dsaas`.  
`firstOpen()` dla TERAZ i „dziś”: **B→C→D→E→F→G**, nie H. H dostępne zawsze w zakładce, nie zajmuje jedynego ruchu.

Chrome każdej strony: `Akademia` · `Hermes Ops →` (drzwi, nie lekcja) · koło zębate · mapa A–H · 7 tabów.  
Mapa: fill per-dział. A siłownia, B–G kurs, H pieniądz. Brak morału „zostało N rozdziałów” na foldzie.  
360px: taby 2 rzędy (4+3 albo wrap), `min-height: 44px`.

## TERAZ

Above-fold, ta kolejność:

1. `❯ HERMES PRZYGOTOWAŁ PORANEK` + data. Jedno zdanie: policzone / nie wiem. Wieczór tym samym wzorem, **niżej, po południu**.
2. **Jeden ruch** na `dsaas-platform-main`: otwarty DoD albo pierwszy niezaliczony B–G. Przycisk → ten rozdział na DSAAS.
3. **Jedno pytanie z pamięci** z zaliczonego rozdziału (puste, jeśli zero zaliczeń). Odpowiedź → NOTATKI przy id.
4. **Pasek 18 DoD.** Obok cienkie kreski A i H (widać, nie mylą z platformą).
5. **Pasek czasu** (dziś + tydzień): `local` | `ops` | `phone`. Trzy „Zaczynam”, jeden aktywny. Wieczór zamyka stempel.
6. **Jedna linia pracownika:** `Kolejka: N · PASS|FAIL|UNKNOWN` + Otwórz `/ops`. Zero kroków.

Rytuał ręczny (checkboxy, Today first, LOCK) w `<details>` „Ręcznie”. LOCK dalej blokuje następny rozdział. Odpoczynek (zero śladu) nie jest LOCK-iem.

**Znika z TERAZ:** `renderOpsCta()`, stopka vault/eksport, biblioteka jako ściana, lekcja H jako jedyny ruch.

Drzwi pieniądza: jedna linia „Pieniądz: Hn” pod paskiem — nie lekcja.

## Koło zębate

Eksport AcademyProgress, pobierz JSON, import, sync vault, zdanie o `schema/academy-progress.v0.json`, PWA. Nie nauka.

## Biblioteka

Karta na górze DSAAS + link z TERAZ „Jak zaliczam”:

- 1 sesja = 1 rozdział, 30–45 min
- jeden mechanizm, jeden plik
- egzaminator pyta z `lab`
- demo na żywo w repo
- DONE = oba dowody; „rozumiem” nie zalicza

Kolejność B→G. Reszta w `<details>`.

## WORKFLOW

Chip Telefon | Laptop → **jeden** mermaid. Drugi w `<details>`.  
Pod diagramem twarde zasady, potem pliki jako dowód:

- Linear jest kolejką; decyzja nie jest na GitHubie
- CI zielone albo stoisz; UNKNOWN nie jest zielone
- telefon nie merguje
- deploy tylko lokalnie (Zasada 11)
- nie vibe-coding: lint+test+build zanim „gotowe”

Węzeł mermaid → kotwica akapitu zasady.  
A1–A7, onboarding 10 kroków, layers notebooków → `<details>` „Siłownia labu”.

## NARZĘDZIA

Szablon i karty: [`TOOL-MASTERY.md`](TOOL-MASTERY.md).  
Lekcja Hermesa Ops (30 s, 6 pól, Pause/Stop/Take over, Approval ≠ Merge) **tylko** na karcie Hermes Engineer.

## DSAAS

Above-fold:

1. Kim jesteś ≤6 linii (architekt OS dla MKB 1–15; nie programista na godziny; nie agencja stron; model proponuje, Ty klikasz; kod od dnia 1 u klienta; zastępowalny).
2. Ścieżka B→C→D→E→F→G. Otwarty = pierwszy niezaliczony. W środku jeden rozdział: plik, LEARN, dwa dowody, DoD.
3. Jeden mermaid + 7 chipów. Zakaz siatki 7 diagramów.

**Linear — widoki platformy (Wave 2)** tutaj (`docs/ops/LINEAR-PLATFORM.md`), pod F albo pod roadmapą w `<details>` — nie na TERAZ.

Below-fold: biblia plik→obowiązek→psuje tenant, scoreboard, mastery, misja. A i H nie wracają.

## MONETYZACJA

H1–H4: winda+SKU, ciepłe wejście, pieniądz przed budową, retainer.  
Zakaz DoD: pole EUR, 10 maili, 20 firm, LinkedIn, darmowy POC, „jeszcze jeden moduł”.  
H zawsze otwarte w zakładce. Nie start `firstOpen`. Nie kłódka „najpierw 18 DoD”.

## ŹRÓDŁA

3 karty: dziś (plik bieżącego B–G, albo H jeśli jesteś na money) · pętla (jedna reguła dnia) · bramka (jeden spec).  
Archiwum A–H w `<details>`, max 1 grupa open. Blog ≠ dowód.

## NOTATKI

Jedna notatka na id otwartego rozdziału. Archiwum zwinięte. Wolny tekst na dole. `_scratch`; Kokpit nie czyta jako track.

## Hermes (skrót)

Pełny kontrakt: [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md).

- Akademii: poranek i jeden ruch = szablon z danych. Pytanie z `lab`. 0 tokenów. Nie zapisuje postępu, nie merguje, nie deployuje.
- Ops: brief kolejki zanim usiądziesz. Nocny merge tylko przy `agent` + CI zielone + brak R7. Deploy u Dowódcy. Telefon nie merguje. Run all default OFF.

## UI — WYKONANE (deploy osobno)

HTML v7 jest na laptopie. Guardy Fala 0/L/M/O/P w tym samym diffie.

Deploy = WAITING-GO. Ten plik opisuje **obowiązujące** reguły.

## Poza scope

Godziny jako ocena wartości. Encyklopedia PARKED. Czat „Hermes wie wszystko” na TERAZ. 7. dział Kokpitu. iframe. Deploy bez GO. Edycja HTML/walidatora/mutacji bez GO na UI.
