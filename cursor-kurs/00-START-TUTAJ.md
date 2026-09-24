# 🎓 KURS: Cursor + Cloud Agents jak profesjonalista
### Wyjaśnione prosto („jak dla 10-latka”), ale do poziomu pro

> 📌 **Ten kurs to BIBLIOTEKA podręcznikowa Akademii.** Interfejs nauki, kolejka „co teraz”
> i checkpointi mieszkają w **`akademia/DASHBOARD.html`** — zaczynaj każdy dzień od niego,
> a do lekcji poniżej wracasz, gdy dashboard Cię tu wyśle (lub gdy chcesz głębiej).

> 🔧 **Praca z agentami (issue → PR → CI) to osobny produkt:** **`/ops`** (Hermes Ops) w tym samym
> repo co Akademia. Nauka = `/`; sterowanie pętlą Linear-first = [`docs/ops/HERMES-OPS-HOWTO.md`](../docs/ops/HERMES-OPS-HOWTO.md).

---

## Co to jest?

To jest Twój kurs z Cursora i Cloud Agents. Czytaj lekcje **po kolejce** (00 → 06).
Każda lekcja to 10–20 minut czytania. Po lekcji 04 uruchomisz pierwszego prawdziwego
agenta w chmurze. Po lekcji 06 będziesz mieć wdrożony profesjonalny workflow.

| Lekcja | Temat | Czego się nauczysz |
|---|---|---|
| `00-START-TUTAJ.md` | Jesteś tutaj | Wielki obraz + słownik pojęć |
| `01-Cursor-model-myslenia.md` | Jak myśleć o Cursorze | 6 trybów Cursora i kiedy którego używać |
| `02-Cloud-Agents-od-A-do-Z.md` | Cloud Agents | Jak to naprawdę działa, ile kosztuje, **twoje klucze API** |
| `03-Srodowiska-i-environment-json.md` | Środowiska | Najważniejsza lekcja — serce całego systemu |
| `04-Pierwszy-Cloud-Agent-krok-po-kroku.md` | Praktyka | Uruchamiasz pierwszego agenta |
| `05-Profesjonalny-workflow-autonomia.md` | Workflow pro | Automatyzacje, Bugbot, telefon jako panel sterowania |
| `06-Twoj-plik-auuu-i-plan-30-dni.md` | Twój dokument | `auuu.txt` przetłumaczone na ludzki + plan wdrożenia |
| `szablony/` | Gotowe pliki | Kopiujesz do swojego repo i działasz |

---

## 🧠 Jedna jedyna rzecz do zapamiętania

Wyobraź sobie, że **zatrudniasz programistę-zdalnego**.

- **Cursor na Twoim laptopie** = siedzisz SAM przy biurku, a obok siedzi AI i pomaga Ci pisać. Ty trzymasz kierownicę.
- **Cloud Agent** = dostajesz pracownika zdalnego z WŁASNYM komputerem w chmurze. Dajesz mu zadanie („napraw logowanie”), idziesz na spacer, a on: odpala swój komputer, pobiera kod, pisze poprawkę, uruchamia testy, nagrywa Ci wideo z dowodem i zostawia propozycję zmian do Twojej akceptacji. Twój laptop może być wyłączony.

To jest cała magia. Reszta kursu to szczegóły.

```
TY (telefon / web / desktop / Slack)
        │  dajesz zadanie po polsku lub angielsku
        ▼
┌─────────────────────────────┐
│  CLOUD AGENT (VM w chmurze) │
│  • klonuje repo             │
│  • pracuje na OSOBNEJ gałęzi│
│  • pisze kod, odpala testy  │
│  • klika w przeglądarce     │
│  • nagrywa wideo z efektu   │
└─────────────┬───────────────┘
              ▼
   GitHub / GitLab  →  Pull/Merge Request
              ▼
   CI/CD (automatyczne testy) → ✅ / ❌
              ▼
        TY: review → MERGE
```

---

## ⚡ Szybkie odpowiedzi na Twoje pytania

Sprawdzone z oficjalną dokumentacją Cursora (stan: wrzesień 2026).

### 1. „Czy Cloud Agents działają na moich darmowych kluczach API?”
**NIE.** I to jest najważniejsza odpowiedź w całym kursie:

- Cloud Agents działają na **serwerach Cursora** i używają **modeli udostępnianych przez Cursora**. Twoje klucze API (OpenAI, Anthropic, Gemini…) siedzą w ustawieniach Twojej lokalnej aplikacji — agent w chmurze ich nie widzi i nie może ich użyć.
- Za Cloud Agents płacisz **wg cennika API wybranego modelu** (tzw. API pricing), z puli Twojego konta Cursor. Przy pierwszym uruchomieniu Cursor każe Ci ustawić **limit wydatków (spend limit)** — to Twój hamulec bezpieczeństwa.
- Wymagany jest **płatny plan Cursor** (od Pro wzwyż).
- Własne klucze API (BYOK – „bring your own key”) działają **wyłącznie** dla zwykłego czatu w aplikacji desktopowej (nie dla Tab, nie dla trybu Agent z „custom models”, nie dla Cloud Agents) — i również wymagają planu Pro+. **Nie istnieje metoda, żeby używać Cloud Agents „za darmo” na darmowych kluczach.**

### 2. „Ile to kosztuje?”
- Abonament Cursor (dla Cloud Agents potrzebny jest płatny plan, np. Pro).
- Zużycie Cloud Agents = cena API modelu × zużyte tokeny. Proste zadanie to zwykle ułamki dolarów do kilku dolarów; duże zadania (duży kontekst, dużo iteracji) kosztują więcej. Większe okno kontekstu = drożej.
- Kontrolujesz to **limitem wydatków** + wyborem tańszego modelu do prostych zadań.

### 3. „Czy muszę mieć GitLab Premium?” — **[akt. 07.09.2026, z oficjalnych stron]**
Najpierw ważne rozróżnienie, bo tu rodzi się 90% nieporozumień:

- **GitLab JEST darmowy** (o tym niżej nie ma dyskusji): gitlab.com Free $0 daje repo, MR, CI (400 min),
  10 GiB; a **GitLab CE self-managed** jest darmowy bez limitów na własnym serwerze (about.gitlab.com/pricing).
- **Płatność dotyczy WYŁĄCZNIE jednej rzeczy: oficjalnej integracji Cursor↔GitLab pod Cloud Agents
  i Bugbot.** Ona potrzebuje *project access tokens*. I tu jest haczyk:
  - na **gitlab.com** tokeny te wymagają Premium/Ultimate (docs.gitlab.com + cursor.com/docs/integrations/gitlab),
  - na **GitLab self-managed** tokeny są „available with any license” — **czyli też w darmowym CE**
    (docs.gitlab.com). Forum Cursora (09.2026) wskazuje, że dokumentacja Cursora jest tu zbyt restrykcyjna.

| Opcja | Cena GitLab | Cloud Agents działają? | Kiedy wybrać |
|---|---|---|---|
| **GitHub Free** | $0 | ✅ od ręki | Najprostszy start, zero administracji |
| **GitLab CE self-hosted (Twój VPS)** | **$0** | ‼️ najpewniej ✅ — test 15 min potwierdzi | Masz VPS; chcesz GitLaba za darmo i pełną kontrolę |
| **gitlab.com Free** | $0 | ❌ (lokalny Cursor działa normalnie) | GitLab w chmurze bez agentów w chmurze |
| **gitlab.com Premium** | $29/user/mc | ✅ oficjalnie | GitLab.com + Cloud Agents, bez self-hostingu |
| **Origin** (git-hosting od Cursora, beta) | w cenie planu Cursor | ✅ | Wszystko w jednym ekosystemie |

### 4. „Czy mogę sterować tym z telefonu?”
**TAK.** Aplikacja Cursor na iOS; na Androidzie — wejdź na `cursor.com/agents` w Chrome i zainstaluj jako apkę (PWA). Do tego Slack/Linear opcjonalnie. Telefon staje się Twoim „panelem dyrektora”.

---

## 📖 Słownik pojęć — „jak dla 10-latka”

| Pojęcie | Co to naprawdę jest |
|---|---|
| **Agent** | Programista-robot. Dajesz mu zadanie → on je wykonuje krok po kroku. |
| **Cloud Agent** | Robot, który ma **własny wypożyczony komputer w chmurze**, a nie używa Twojego laptopa. |
| **VM (maszyna wirtualna)** | Ten wypożyczony komputer. Odizolowany — robot nie widzi Twoich plików ani innych agentów. |
| **Środowisko (environment)** | „Wyposażone biurko” robota: sklonowane repo, zainstalowane programy i biblioteki, hasła (sekrety), komendy startowe. **Bez tego robot jest jak pracownik bez komputera.** |
| **Build / snapshot** | „Zdjęcie” gotowego, skonfigurowanego dysku. Dzięki temu agent startuje w sekundy, zamiast za każdym razem instalować wszystko od zera. |
| **Branch (gałąź)** | Kopia kodu „do grzebania”. Agent zawsze pracuje na osobnej gałęzi, żeby nie zepsuć głównej wersji (`main`). |
| **Commit** | Zapisany punkt w historii zmian — jak zapis gry. |
| **PR / MR** (Pull/Merge Request) | „Proszę, sprawdź moje zadanie domowe i — jeśli jest dobre — włącz je do wersji głównej”. Agent kończy pracę wystawiając PR/MR. |
| **CI/CD** | Automatyczny „kontroler jakości” na GitHubie/GitLabie: po każdej zmianie sam odpala testy, lint, build. Zielone ✅ = można mergować. |
| **Sekret** | Sejf na hasła i klucze. Wpisujesz raz w dashboardzie Cursora; agent je dostaje, ale **nigdy nie trafiają do kodu ani logów**. |
| **AGENTS.md** | Plik w głównym katalogu repo: „instrukcja obsługi firmy” dla KAŻDEGO agenta AI. Robot czyta ją zanim cokolwiek zrobi. |
| **Rules** (`.cursor/rules`) | Dodatkowe zeszyty z zasadami — np. „w plikach frontendowych rób X”. Mogą działać zawsze albo tylko w konkretnych plikach. |
| **Skill** | Gotowa „procedura firmowa”, np. *jak-robimy-migracje-bazy*. Agent sięga po nią, gdy jej potrzebuje. |
| **Hook** | Miniaturowy strażnik: automatycznie odpala komendę w konkretnym momencie (np. formatuje kod po każdej edycji agenta). |
| **MCP** | „Port USB dla AI” — standard podpinania zewnętrznych narzędzi i danych (baza danych, Jira, GitLab, Slack). |
| **Automatyzacja (Automation)** | Budzik / czujnik ruchu: odpala Cloud Agenta **sama** — wg harmonogramu („codziennie 8:00”) albo gdy coś się wydarzy („otwarto nowy PR”, „event z GitLaba”, webhook). |
| **Artifact (artefakt)** | Dowód pracy agenta: zrzuty ekranu, wideo, logi. Obejrzysz je zanim zaakceptujesz zmiany. |
| **Remote desktop** | „Przejęcie myszki” komputera agenta — możesz sam poklikać aplikację, którą agent zmodyfikował, i oddać sterowanie. |
| **Review Apps / Staging** | „Przymierzalnia” — tymczasowa działająca wersja aplikacji z daną zmianą, do kliknięcia przed wdrożeniem. |

---

## Jak pracować z kursem

1. Przeczytaj lekcje 01–03 (teoria, ~45 min).
2. Zrób lekcję 04 **przy komputerze** — to warsztat.
3. Skopiuj pliki z `szablony/` do swojego repo (instrukcja w lekcji 04 i 05).
4. Lekcja 06 zamienia Twój dokument `auuu.txt` w plan 30 dni — to Twoja mapa drogowa.

> 📎 Oficjalne źródła, na których oparty jest kurs:
> `cursor.com/docs/cloud-agent` (Overview, Setup, Builds, Automations, Mobile),
> `cursor.com/docs/integrations/gitlab`, `cursor.com/docs/origin`. Linki padają też w lekcjach.
