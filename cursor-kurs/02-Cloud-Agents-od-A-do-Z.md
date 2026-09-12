# 🤖 LEKCJA 02 — Cloud Agents od A do Z
### Najważniejsza lekcja teoretyczna. Czytaj powoli.

Źródło: oficjalna dokumentacja `cursor.com/docs/cloud-agent` (+ Setup, Builds, Automations, Mobile).

---

## 1. Co to jest Cloud Agent — dokładnie

Cloud Agent to **autonomiczny programista AI działający na odizolowanej maszynie wirtualnej (VM)
w chmurze Cursora**. Nie na Twoim laptopie. Na tej VM-ce ma środowisko jak prawdziwy developer:
sklonowane repo, zainstalowane zależności, sekrety, komendy startowe, dostęp do sieci.

Kluczowe właściwości:
- **Laptop nie musi być włączony.** Agent pracuje, gdy Ty śpisz / jesteś na mieście.
- **Równolegle.** Możesz odpalić wiele agentów naraz — każdy na własnej VM i własnej gałęzi.
- **Pełne zapętlenie pracy:** nie tylko pisze kod, ale go **uruchamia, testuje i klika w przeglądarce** (computer use — steruje desktoplem VM-ki).
- **Dowody pracy (artefakty):** kończy zwykle z gotowym PR/MR + screenshotami, wideo i logami.
- **MCP:** cloud agent może używać serwerów MCP skonfigurowanych dla Twojego zespołu
  (dostęp np. do baz, API, zewnętrznych usług) — zarządzasz nimi z `cursor.com/agents`.

---

## 2. Anatomia jednego „runu” — co się dzieje krok po kroku

```
1.  Ty piszesz zadanie        „Napraw walidację e-maila w formularzu rejestracji + dodaj testy”
2.  Cursor startuje VM        z aktywnego Buildu Twojego środowiska (szybko, bo gotowy dysk)
3.  Klonowanie repo           + przełączenie na NOWĄ gałąź (np. cursor/fix-email-validation-3f2a)
4.  Przygotowanie             start/terminals: odpalenie dev-serwera, bazy itp. (lekcja 03)
5.  Agent czyta zasady        AGENTS.md, .cursor/rules, sekcję "Cursor Cloud specific instructions"
6.  Praca                     edycja plików, terminal, testy, przeglądarka, desktop
7.  Samoweryfikacja           uruchamia testy/apkę i sprawdza, czy naprawił
8.  Artefakty                 screenshoty/wideo/logi z dowodem działania
9.  Push gałęzi               do GitHuba/GitLaba → otwiera PR/MR (lub przygotowuje zmiany)
10. Ciebie woła               powiadomienie → Ty robisz review → MERGE (Ty decydujesz!)
```

Dwie ważne obserwacje:
- Agent **nigdy nie powinien** pchąć prosto do `main` — pracuje na swojej gałęzi. MR = Twoja brama.
- Na stronie agenta możesz **najechać na nazwę repo**, żeby zobaczyć, jakiego środowiska i Buildu użył.

---

## 3. Skąd odpalisz agenta — 8 „drzwi”

| Wejście | Jak |
|---|---|
| **Cursor Desktop** | w polu agenta wybierz **Cloud** zamiast Local |
| **Cursor Web** | `cursor.com/agents` — działa na każdym urządzeniu z przeglądarką |
| **iOS** | natywna aplikacja Cursor (start + zarządzanie + powiadomienia) |
| **Android** | `cursor.com/agents` w Chrome → **Install App** (PWA) |
| **Slack** | komenda `@cursor` + zadanie |
| **GitHub / Bitbucket** | komentarz `@cursor` pod PR lub issue (GitHub) / pod PR (Bitbucket) |
| **Linear** | `@cursor` w issue |
| **API** | programowe odpalanie agentów (jest też CLI/SDK Cursora) |

⚠️ Uwaga precyzyjna: komentarz `@cursor` jako wyzwalacz jest udokumentowany dla
**GitHuba i Bitbucketa**. GitLaba obsługujesz przez web/desktop/Slack/API oraz
**automatyzacje reagujące na eventy GitLaba** (lekcja 05). Na GitLabie **nie** licz na wyzwalacz
`@cursor` pod MR-em.

---

## 4. Co agent potrafi wewnątrz VM-ki

- Terminal: buduje, odpala testy, skrypty, migracje.
- **Przeglądarka + desktop (computer use):** uruchamia Twoją apkę i klika w nią jak człowiek —
  i Ty dostajesz z tego nagranie. (Computer use wymaga obrazu bazowego Debian/Ubuntu — lekcja 03.)
- **Artefakty:** screenshoty, wideo, logi — to Twój materiał do szybkiego review.
- **Remote desktop control:** możesz **przejąć sterowanie** pulpitem agenta, samemu poklikać
  zmodyfikowaną aplikację i oddać sterowanie agentowi. Ogromne: testujesz bez lokalnego checkoutu.
- **MCP:** narzędzia zewnętrzne (HTTP i stdio, z OAuth), plus wbudowany **Cursor Cloud MCP**
  do diagnostyki runów (transkrypty, eventy, logi środowiska).
- **Hooks z repo:** `.cursor/hooks.json` działa w chmurze (np. auto-formatowanie po edycji).
  Hookie z `~/.cursor/hooks.json` (Twojego kompa) — nie, bo VM nie widzi Twojego home.

---

## 5. Równoległość — Twój mnożnik

Możesz mieć jednocześnie:
- agenta A: naprawia bug z listy,
- agenta B: pisze testy do modułu Y,
- agenta C: robi research „jak dodać feature Z” (bez zmian w kodzie),
- automatyzację: przegląda nowe PR-y (Bugbot — lekcja 05).

Każdy na osobnej gałęzi, każdy kończy PR-em. **Ty przestajesz być wąskim gardłem — Twoim zadaniem
jest tylko: dobrze opisać zadania i robić dobre review.**

---

## 6. Modele

Cloud Agents używają **wybranej przez Cursora listy modeli**; dla części modeli możesz wybrać
**rozmiar okna kontekstu**. Większe okno = więcej tokenów = **wyższy koszt**. Praktyka:
- proste zadania (typo, mały fix, testy) → tańszy model / mniejsze okno,
- skomplikowane refaktory → mocniejszy model.

---

## 7. 💸 ROZLICZENIA i Twoje klucze API — cała prawda

**Jak płacisz za Cloud Agents:**
1. Potrzebujesz **płatnego planu Cursor** (bez płatnego planu runy się nie startują).
2. Samo zużycie: **API pricing wybranego modelu** — tyle, co tokeny kosztują u dostawcy, naliczane
   z Twojego konta/puli Cursor. Przy pierwszym użyciu ustawiasz **spend limit**.
3. Automatyzacje (lekcja 05) rozliczają się tak samo — jak zwykłe runy cloud agentów.

**Czy da się używać własnych/darmowych kluczy API? — NIE, i oto dlaczego:**

| Gdzie jesteś | Czy BYOK (własny klucz) działa? |
|---|---|
| Czat w desktopowym Cursorze (zwykłe pytania do modeli) | ✅ tak (i tak wymaga planu Pro+) |
| Tab / custom models Cursora / Agent-mode w desktopie | ❌ nie |
| **Cloud Agents** | ❌ **nie** — VM jest po stronie Cursora, nie widzi Twoich lokalnych kluczy; modele i ich rozliczenie idą przez Cursora |

Konsekwencja praktyczna: **„darmowe klucze” (np. darmowe limity Gemini) nie zasila Ci Cloud Agents.**
Jedyna droga do taniości to dobra ekonomia zadań: małe zadania, gotowe środowisko (szybszy start
= mniej tokenów na „rozkręcanie się”), dobre AGENTS.md (mniej iteracji), tańszy model do prostych rzeczy.

---

## 8. Sekrety i sieć (skrót — szczegóły w lekcji 03)

- Sekrety wpisujesz w dashboardzie (`cursor.com/dashboard/cloud-agents` → Secrets); agent dostaje je
  jako zmienne środowiskowe **na starcie runu** (po dodaniu sekretu uruchom NOWEGO agenta — działający
  go nie zobaczy).
- Możesz ograniczać domeny wychodzące (allowlist) i łączyć agenta z prywatną siecią
  (Tailscale / Cloudflare Tunnel / PrivateLink).
- Istnieje opcja **Self-Hosted Machines** (agent na Twoim sprzęcie) oraz **Cursor Origin**
  (własny git-hosting Cursora, beta, od planu Pro) — wspominam dla pełności; nie potrzebujesz na start.

---

## 9. Współdzielenie z zespołem

Link do runu możesz wysłać koledze — zobaczy rozmowę, diffy i artefakty (read-only).
Warunek: ten sam zespół Cursor + podpięte własne konto source-control z dostępem do repo.
Admin może włączyć **team follow-ups** — wtedy koledzy mogą dopisywać agentowi kolejne polecenia.

---

## 10. Czego Cloud Agent NIE jest

- ❌ To nie VPS do hostowania produkcji. VM żyje na czas zadania.
- ❌ To nie magik: bez dobrego środowiska (lekcja 03) agent „pisze na ślepo”.
- ❌ To nie zastępstwo review: **zawsze** patrzysz na diff + artefakty + zielone CI.
- ⚠️ Środowiska multi-repo: działają (agent robi zmiany w kilku repo naraz i otwiera PR-y w każdym),
  ale „long-running” nie jest dla nich jeszcze dostępny.

---

## 11. Mini-troubleshooting (z dokumentacji)

| Problem | Przyczyna / lek |
|---|---|
| Runy się nie startują | brak płatnego planu; niepodpięty provider repo; brak uprawnień do repo |
| Agent nie widzi sekretu | sekrety wstrzykują się na starcie runu → odpal NOWEGO agenta; sprawdź właściwy zespół/workspace |
| Nie widzisz zakładki Secrets | brak uprawnień w zespole |
| Agent nie umie odpalić apki | środowisko nie skonfigurowane → lekcja 03 to naprawia |
| Kolega nie widzi mojego runu | musi być w zespole + podpiąć własne konto git z dostępem do repo |

---

**Następna lekcja:** `03-Srodowiska-i-environment-json.md` — to jest 80% Twojego sukcesu
z Cloud Agents. Nie pomijaj.
