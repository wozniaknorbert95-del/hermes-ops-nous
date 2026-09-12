# 📘 LEKCJA 01 — Jak naprawdę myśleć o Cursorze
### (dla kogoś, kto używa Cursora od 2 lat, ale chce poziom pro)

Używasz Cursora od 2 lat, więc podstawy znasz. Ta lekcja jest krótka i nie o guzikach —
jest o **zmianie roli**: przestajesz być pisarzem kodu, stajesz się **dyrektorem technicznym
zespołu robotów**.

---

## 1. Sześć trybów Cursora i kiedy którego używać

| Tryb | Skrót / miejsce | Do czego służy | Kiedy używać |
|---|---|---|---|
| **Tab (autocomplete)** | piszesz, Tab akceptuje | dokańczanie linii/bloków | cały czas, przy ręcznym kodowaniu |
| **Inline Edit** | `Cmd/Ctrl+K` | zmiana w zaznaczonym fragmencie | małe, precyzyjne poprawki „tutaj” |
| **Ask** | panel czatu | pytania o kod (bez zmian) | rozumienie obcego kodu, debugowanie koncepcji |
| **Agent (lokalny)** | tryb Agent w panelu | wieloetapowa praca na Twoim komputerze (edytuje pliki, odpala terminal) | średnie zadania, gdy laptop jest włączony |
| **Plan Mode** | w agencie (plan) | najpierw plan → Twoja akceptacja → dopiero wykonanie | zadania >15 min pracy; zawsze gdy niepewne „jak” |
| **Cloud Agent** | „Cloud” w panelu / web / telefon | w pełni autonomiczny pracownik z własną VM-ką | zadania, które mają się skończyć PR/MR bez Twojego laptopa |

**Zasada pro:** im mniejsze i jaśniejsze zadanie — tym „lżejszy” tryb. Im większe — tym więcej
planowania WRZUCASZ PRZED robotą, a nie po.

---

## 2. Zasada nr 1: jakość wyjścia = jakość kontekstu

Agent nie jest słaby, bo model jest słaby. W 90% przypadków jest słaby, bo **dostał zły kontekst**.
Przykład: powiesz „popraw walidację formularza” — agent nie wie którego, po co, jakie masz reguły,
jakie testy — więc zgaduje. I zgaduje źle.

Kontekst dajesz na 4 poziomach (od najtrwalszego):

```
1. AGENTS.md + .cursor/rules   →  trwałe „prawo firmy”, czytane zawsze
2. Struktura repo + docs        →  czytelne katalogi, ARCHITECTURE.md, DECISIONS.md
3. Issue / opis zadania         →  cel, kryteria akceptacji, ograniczenia
4. Prompt + @-odniesienia       →  to, co piszesz TERAZ
```

Jeśli poziomy 1–2 są słabe, musisz za każdym razem pisać gigantyczne prompty (poziom 4).
**Profesjonalista inwestuje w poziomy 1–2 raz, a potem pisze krótkie prompty.**
To jest cała tajemnica „AI-native repo” z Twojego pliku `auuu.txt` — szerzej w lekcji 05 i 06.

---

## 3. Rules (`.cursor/rules`) + AGENTS.md — „zeszyt zasad dla stażysty”

Wyobraź sobie, że co tydzień zatrudniasz nowego, genialnego stażystę z amnezją.
Nic nie pamięta. Wszystko, czego ma się trzymać, musi być **zapisane**.

- **`AGENTS.md`** (korzeń repo) — branżowy standard. Czytają go także Cloud Agents
  (mają nawet zalecaną sekcję `Cursor Cloud specific instructions`). Jeden plik = jedna konstytucja.
- **`.cursor/rules/*.mdc`** — reguły Cursora, z nagłówkiem `description / globs / alwaysApply`:
  - `alwaysApply: true` → obowiązuje zawsze (fundament),
  - `globs: src/frontend/**` → dokleja się tylko dla pasujących plików,
  - `description` → sam opis kiedy z niej korzystać (agent sam zdecyduje / ręcznie).

Gotowe szablony masz w `szablony/.cursor/rules/` — skopiuj i dostosuj.

---

## 4. Plan Mode — zatrzymaj agenta, zanim popłynie

Dla każdego zadania nieoczywistego: najpierw **plan** → Ty poprawiasz plan → dopiero wykonanie.
Poprawienie planu kosztuje Cię 2 minuty. Poprawianie złej implementacji — godzinę i dolary na tokeny.
To samo dotyczy Cloud Agents: na wielkie rzeczy dawaj zadania typu **„zbadaj i zaproponuj plan
(nie zmieniaj kodu)”**, a implementację osobno. (Szablon takiego promptu: `szablony/PROMPTY-DLA-AGENTOW.md`.)

---

## 5. Subagenty i Hooki — mini-zespoły i strażnicy (w skrócie)

- **Subagenty** — wyspecjalizowani pomocnicy agenta (np. „reviewer”, „badacz”). Użyjesz, gdy zadania
  robią się duże. Na start: nie musisz.
- **Hooks** (`.cursor/hooks.json` w repo) — automatyczne komendy odpalane w kluczowych momentach
  (np. po edycji pliku → formatter; przed komendą shell → blokada niebezpiecznych poleceń).
  **Działają też w Cloud Agents** (repo-hooks; hookie z Twojego komputera `~/.cursor` — nie, bo VM
  nie widzi Twojego katalogu domowego).

---

## 6. Twoja nowa rola — job description

```
BYŁO:                      JEST:
piszę kod                  →  opisuję ZADANIE biznesowo i technicznie
sam szukam błędów          →  CI + testy łapią błędy
czytam cały kod            →  robię REVIEW różnic (diffów) i artefaktów
myślę „jak to napisać”     →  myślę „jak to opisać, opisać testy i zabezpieczyć”
```

Największy skok produktywności nie pochodzi z lepszego modelu, tylko z tego, że:
**Ty określasz CO i JAK SPRAWDZIĆ — robot określa i wykonuje JAK.**

---

## 7. Najczęstsze błędy osoby „średnio zaawansowanej” (2 lata Cursora!)

1. ❌ Za duże zadania od razu („zrób mi cały moduł X”) → chaos. Zamiast: małe MR-e.
2. ❌ Brak `AGENTS.md`/rules → agent za każdym razem zgaduje konwencje.
3. ❌ Brak testów w projekcie → nie masz jak weryfikować pracy agenta bez czytania wszystkiego.
4. ❌ Akceptowanie zmian bez uruchomienia → „wygląda OK” ≠ działa.
5. ❌ Gigantyczne mega-prompty zamiast trwałego kontekstu w repo.
6. ❌ Brak Definition of Done → agent kończy „na 80%”.

**Następna lekcja:** `02-Cloud-Agents-od-A-do-Z.md` — dokładnie jak działa agent w chmurze,
skąd go odpalać i cała prawda o rozliczeniach i Twoich kluczach API.
