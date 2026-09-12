# 🏆 LEKCJA 05 — Profesjonalny workflow: pętla autonomii
### To jest lekcja „jak pro”. Łączy wszystko: Cursor + Cloud Agents + Git + CI + telefon.

---

## 1. Pętla — jeden diagram, który rządzi wszystkim

```
IDEA → ISSUE → SPECYFIKACJA → (PLAN) → AGENT → BRANCH → KOD → TESTY
      → MR → CI ✅ → REVIEW (AI: Bugbot/Security) → REVIEW (człowiek)
      → MERGE → DEPLOY (staging → produkcja) → OBSERWACJA → FEEDBACK → IDEA ...
```

**Zasada fundamentu: każde większe zadanie zaczyna się jako ISSUE.**
Dlaczego? Bo za 6 miesięcy pytasz AI „dlaczego billing działa tak?” — i masz ślad:
issue → decyzja → MR → kod → testy. To jest **pamięć organizacji**. Prompt w telefonie
„zrób coś” nie zostawia pamięci.

Niezależnie, czy agentem jest Cursor Cloud, GitLab Duo czy coś przyszłego — **pętla zostaje ta sama**.
Dlatego budujesz workflow wokół pętli, nie wokół narzędzia („agent-agnostic core” z Twojego `auuu.txt` — poprawna myśl).

---

## 2. Repo „AI-native” — struktura, która multiplikuje agentów

```
twoje-repo/
├── AGENTS.md                    ← konstytucja (czytają WSZYSTKIE agenty)
├── ARCHITECTURE.md              ← mapa systemu na 1 stronę
├── PRODUCT.md                   ← co budujemy, dla kogo, reguły biznesowe
├── DECISIONS.md                 ← dziennik decyzji (data → decyzja → dlaczego)
├── TESTING.md                   ← jak testujemy (jeśli rozbudowane)
├── SECURITY.md                  ← zasady bezpieczeństwa
├── .cursor/
│   ├── environment.json         ← środowisko cloud agentów (lekcja 03)
│   ├── Dockerfile               ← opcjonalnie
│   ├── rules/                   ← reguły (.mdc) — szablony gotowe
│   └── hooks.json               ← opcjonalnie: strażnicy (formatowanie itd.)
├── .gitlab/ lub .github/
│   ├── issue_templates/         ← szablon zadania „karmy dla agenta”
│   └── merge_request_templates/ ← checklist MR
├── .gitlab-ci.yml (lub .github/workflows/) ← CI: strażnik jakości
└── src/ ...
```

Szablon większości tych plików masz w folderze `szablony/`. Kopiujesz → uzupełniasz sekcje „UZUPEŁNIJ”.

---

## 3. AGENTS.md — Twoja konstytucja. Jak pisać dobrą

Zła konstytucja: „Pisz dobry kod.” (Agent zignoruje — niemierzalne.)
Dobra konstytucja: **zasady wykonywalne i sprawdzalne**. Przykłady z szablonu:

- „Każda zmiana w bazie = plik migracji. Nigdy ręczne UPDATE na produkcji.”
- „Nie usuwaj/nie osłabiaj padającego testu bez udowodnienia, że test jest błędny.”
- „Nie dodawaj zależności bez uzasadnienia w opisie MR.”
- „Przed MR: lint ✅, typecheck ✅, testy ✅, build ✅.”
- „Gdy wymaganie jest dwuznaczne: STOP i zapytaj — nie zgaduj.”

Zasady pisania: rozkazujące zdania, jedna zasada = jedna linia, zero literatury,
sekcja „Cursor Cloud specific instructions” na końcu (lekcja 03), aktualizuj przy KAŻDEJ
zmianie procesu (to żywy dokument, nie muzeum).

### Mapa: czego użyć do czego

| Narzędzie | Do czego | Kiedy się ładuje |
|---|---|---|
| `AGENTS.md` | prawo projektu, komendy, konwencje | zawsze, każdy agent |
| `.cursor/rules/*.mdc` | reguły szczegółowe / per-ścieżka | zawsze albo wg `globs` |
| **Skills** | procedury „jak robimy X” (migracja, release, incident) | agent sięga, gdy temat pasuje |
| **Hooks** | automatyczne komendy (format, lint-fix, blokady) | na zdarzeniach edycji/narzędzi |
| **MCP** | dostęp do systemów zewnętrznych (baza, Jira, GitLab) | gdy agent woła narzędzie |

---

## 4. Automations — agenci, którzy budzą się sami

**Co to:** automatyzacja odpala Cloud Agenta wg **harmonogramu** albo w reakcji na **zdarzenia**:
GitHub, **GitLab**, Slack, webhooki, Linear i inne.

**Jak tworzysz (4 drogi):** Agents Window w desktopie · `cursor.com/automations` ·
skill `/automate` (opisujesz workflow po polsku, Cursor sam konfiguruje triggery, instrukcje
i narzędzia) · gotowe szablony z `cursor.com/marketplace/automations`.

**Konfiguracja w 5 krokach:** ① trigger (np. „gdy otwarto PR” albo „codziennie 8:00”)
② prompt-instrukcja ③ narzędzia (np. wyślij na Slacka, komentuj PR, MCP) ④ repo / wiele repo / bez repo
⑤ zapisz i aktywuj.

**3 wbudowanych agentów Cursora (Cursor-managed, na stronie Automations):**
- **Bugbot** — recenzuje PR-y, łapie bugi i problemy jakości,
- **Security Agents** — skanują PR-y/kod pod kątem podatności,
- **PR Routing & Approval** — kieruje PR-y do recenzentów, może aprobować zmiany niskiego ryzyka.

**Rozliczenia:** automatyzacja = zwykły cloud agent pod spodem (API pricing; automatyzacje używają
maksymalnego okna kontekstu rozwiązań — bez suwaka). Kto płaci zależy od zakresu:
**Team Owned** → pula zespołu (service account); **Private/Team Visible** → Twój limit.

### Trzy automatyzacje, które włączasz najpierw (kolejność pro)

1. **Bugbot na każdy PR/MR** — darmowy drugi recenzent przed Tobą
2. **„Daily digest”** (harmonogram) — codziennie rano podsumowanie zmian w repo
3. **Weekly security sweep** (harmonogram) — przegląd kodu pod kątem podatności
(później: zdarzeniowe — „nowe issue → agent przygotowuje analizę i propozycję planu”)

---

## 5. Dwustopniowe review — profesjonalna branka

```
AGENT pisze kod  → X otwiera MR
        ↓
STOP 1 (AI):    Bugbot + Security Agents recenzują automatycznie
        ↓
STOP 2 (Ty):    czytasz diff + artefakty + wyniki AI-review + zielone CI
        ↓
MERGE (człowiek klika) → deploy
```

Nigdy: agent → auto-merge do `main`. Nigdy: „wygląda OK” bez uruchomienia/artefaktów.

---

## 6. Telefon jako panel dyrektora — scenariusz docelowy (z Twojego pliku)

To jest Cel. Nie „kodowanie z telefonu”, tylko **zarządzanie produkcją z telefonu**:

```
13:10  Ty (iOS app / PWA): „Agent, przeanalizuj problem z onboardingiem.”
13:15  Agent: znalazł 4 problemy + proponuje plan.
13:16  Ty: „Napraw punkty 1–3.”  → branch, zmiany, 17 nowych testów
13:45  GitLab CI: ✅ lint ✅ testy ✅ build ✅ review app
       Bugbot: 2 uwagi poprawione przez agenta
14:00  Ty: oglądasz wideo-artefakt na telefonie, czytasz diff
14:05  Ty: MERGE. Koniec. Laptop cały czas zamknięty.
```

Warunki, żeby to działało: środowisko z lekcji 03 ✅ + AGENTS.md ✅ + CI ✅ + Bugbot ✅
+ zadania dobrze opisane ✅. Bez tego telefon = generator chaotycznych PR-ów.

---

## 7. Anti-wzorce — czego NIE robić (potwierdzam Twój `auuu.txt`)

❌ Trzy „mózgi” naraz jako fundament (Cursor + OpenCode + Hermes) — wybierz jeden interfejs, reszta opcjonalna
❌ SSH do laptopa jako główny workflow; laptop jako source of truth
❌ Ręczne deploye i ręczne „testowanie wszystkiego”
❌ Gigantyczne prompty zamiast AGENTS.md/rules
❌ MCP do wszystkiego + 20 aplikacji + własny orchestrator zanim jest potrzebny
❌ Auto-merge agentów do main; sekrety w kodzie; brak limitu kosztów

✅ Zamiast tego: Git jako źródło prawdy → agenci nad nim → CI jako strażnik → człowiek na bramce →
telefon jako panel. Tailscale = airbag (awaryjny dostęp do domowego PC), nie codzienność.

---

## 8. Mierz jak pro (raz w tygodniu, 10 min)

- **Koszt na MR** — rośnie? skracaj zadania albo schodź do tańszego modelu
- **% MR-ów mergowanych bez Twoich poprawek** — Twoja „jakość kontekstu”; cel: rosnąco
- **Czas cyklu** issue → merge — cel: malejąco
- Uwagi Bugbota, które się powtarzają → **dopisz zasadę do AGENTS.md** (zamykanie pętli nauki!)

---

**Następna lekcja:** `06-Twoj-plik-auuu-i-plan-30-dni.md` — rozumiem Twój dokument,
sprawdzam co w nim prawda, i rozkładam Ci wdrożenie na 4 tygodnie.
