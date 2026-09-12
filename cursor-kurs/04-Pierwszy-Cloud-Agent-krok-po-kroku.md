# 🚀 LEKCJA 04 — Warsztat: pierwszy Cloud Agent krok po kroku
### Rób to przy komputerze. Na końcu będziesz mieć pierwszy MR zrobiony w chmurze.

---

## 0. Checklist wymagań (zanim zaczniesz)

- [ ] **Płatny plan Cursor** (bez niego runy nie wystartują)
- [ ] Konto **GitHub / GitLab / Azure DevOps / Bitbucket** z uprawnieniami **odczyt+zapis** do repo
      (potrzebne także do dependent-repo i submodułów, jeśli masz)
- [ ] GitLab.com? → wymagany **Premium/Ultimate** (patrz decyzja poniżej)
- [ ] Repo z testami (choć minimalnymi) i README jak „odpalić projekt”
- [ ] Skopiowane szablony: `AGENTS.md` do korzenia repo, `.cursor/rules/` (z `szablony/`)

### Decyzja 1: gdzie trzymasz repo **[akt. 07.09.2026 — z oficjalnych stron]**

| Sytuacja | Wybór |
|---|---|
| „Mam wolne ręce” | **GitHub Free** — integracja Cursor działa w pełni, zero kosztów |
| „Chcę GitLaba ZA DARMO i mam VPS” | **GitLab CE self-managed $0** — docs.gitlab.com: project access tokens dostępne w każdej licencji self-managed → test integracji = punkt 2 tej lekcji; to najtańsza pełna opcja |
| „Chcę GitLaba w chmurze + Cloud Agents” | gitlab.com **Premium $29** (na gitlab.com tokeny = Premium/Ultimate) |
| „Chcę wszystko u Cursora” | **Origin** (beta, od planu Pro) — hosting gita od Cursora; działa z Cloud Agents i automatyzacjami; może mirrorować GitHuba |

Uwaga: **gitlab.com Free** jako zwykły host gita (repo, MR, CI, Cursor desktop) działa świetnie za $0 —
ograniczenie dotyczy tylko oficjalnej integracji Cloud Agents/Bugbot, bo na gitlab.com wymaga ona
project access tokens (płatne plany).

> Dla nauki możesz zrobić osobne, małe repo-testowe. Nie ćwicz na produkcyjnym projekcie.

---

## 1. Podłącz providera (jednorazowo, robi admin konta Cursor)

1. Wejdź na `cursor.com/dashboard/integrations`
2. Kliknij **Connect** przy GitHub/GitLab → przejdź instalację
3. Po powrocie: **Manage → Sync Repos**
4. Sprawdź, że repo jest widoczne w dashboardzie

*(GitLab: wymaga roli Maintenera na GitLabie + admin Cursor; opcjonalnie można zabezpieczyć
„Protected Git Scope” — przypięcie grupy GitLab do Twojej organizacji Cursor; wymaga roli Ownera.)*

---

## 2. Utwórz środowisko (guided setup — lekcja 03, ścieżka A)

1. `cursor.com/dashboard/cloud-agents` → **Environments → New environment**
2. Wybierz repo (lub grupę repo przy multi-repo)
3. Dodaj zmienne/sekrety potrzebne do instalacji i uruchomienia
4. Uruchom setup agenta → **obserwuj wspólny terminal** (~10 min): agent instaluje zależności,
   sprawdza build/testy
5. Po sukcesie: zapisz Build → commitnij `.cursor/environment.json` do repo (setup agent potrafi
   zaproponować zmiany nawet jako PR)

✅ Test: zakładka **Builds** → „Test build” / zielony status.

---

## 3. Ustaw limit wydatków

Przy pierwszym starcie Cursor poprosi o **spend limit** — ustaw (na naukę np. niski).
To Twój airbag finansowy: jak zużycie go dobije, runy się zatrzymają zamiast generować rachunek-niespodziankę.

---

## 4. Zadanie zerowe — celowo MALE

Pierwszy run ma pokazać Ci CAŁY obieg, nie zrobić wielką robotę. Przykład (dostosuj do repo):

> „W pliku README.md dodaj sekcję 'Jak zgłosić błąd' z 3 punktami i linkiem do zakładki Issues.
> Nie zmieniaj żadnego innego pliku. Zrób to na nowej gałęzi i otwórz MR.”

Dlaczego małe: zobaczysz start VM, pracę, artefakty, gałąź, MR — całość w parę minut, za grosze.

**Formuła dobrego zadania (6 pól):** ① Cel ② Kontekst (gdzie/po co) ③ Wymagania
④ Ograniczenia („nie ruszaj X, Y”) ⑤ Kryteria akceptacji ⑥ Jak zweryfikować (testy, screenshot).
Więcej: `szablony/PROMPTY-DLA-AGENTOW.md`.

---

## 5. Odpal agenta

- **Desktop:** w polu agenta przestaw **Local → Cloud**, wklej zadanie, Enter
- **Web/telefon:** `cursor.com/agents` → nowy agent, wybierz repo, wklej zadanie
- Wybierz model (na proste zadania tańszy) i rozmiar okna kontekstu jeśli dostępny

Odpal i... **nic nie rób 5 minut.** Patrz, jak pracuje: transkrypt, komendy, edycje.

---

## 6. Review — Twoje 15% pracy, które robi 100% różnicy

Gdy agent skończy:

1. **Artefakty:** obejrzyj screenshoty/wideo — czy zmiana WYGLĄDA i DZIAŁA?
2. **Diff:** przejrzyj zmienione pliki (mały MR = spokojnie przeczytasz całość)
3. **Środowisko:** najedź na nazwę repo na stronie runu → zobaczysz, jakiego środowiska/Buildu użył
4. **Remote desktop (opcjonalnie):** przejmij VM, poklikaj apkę sam
5. **CI:** pipeline musi być zielony (lint, testy, build)
6. Dopiero wtedy: **Approve + Merge** (Ty / człowiek — zawsze)

💡 Chcesz poprawkę? Piszesz follow-up **w tym samym runie** („dodaj jeszcze test dla przypadku pustego
e-maila”) — agent kontynuuje na tej samej gałęzi.

---

## 7. Drugie zadanie — prawdziwe, ale rozmiaru S/M

Naprawdę użyteczne, ale wciąż zamknięte w ~1 pliku/1 obszarze. Przykłady:
- „Dodaj brakujące testy do funkcji X — pokryj przypadki brzegowe A, B, C. Nie zmieniaj implementacji.”
- „Napraw bug: przy pustym polu Y leci 500. Dodaj walidację + test regresyjny.”
- „Zaktualizuj zależność Z i napraw co się wysypie; wszystkie testy muszą przejść.”

**Skala zadań:** S i M → od razu agentowi. L → najpierw zadanie „zbadaj i zaproponuj plan
(bez zmian w kodzie)”, potem implementacja etapami albo rozbicie na issue’y.

---

## 8. Zasady bezpieczeństwa — wypisz sobie nad biurko

1. **Gałąź `main` jest chroniona** (protected branch, merge tylko przez MR) — w repo providera.
2. Agent zawsze pracuje na własnej gałęzi → MR → CI → człowiek. **Nigdy auto-merge do main.**
3. Sekrety tylko przez zakładkę Secrets. W kodzie/komendach nigdy.
4. Spend limit ustawiony; raz w tygodniu zerkasz na usage/costs.
5. Nowi ludzie w zespole: podpinają własne konto git (dostęp do runów jest weryfikowany per-repo).
6. Duże uprawnienia agenta (np. produkcyjna baza przez sekrety) — tylko gdy NAPRAWDĘ potrzebne.

---

## 9. Troubleshooting warsztatu

| Objaw | Co zrobić |
|---|---|
| „Agent runs are not starting” | płatny plan? provider podpięty? uprawnienia RW do repo? |
| Setup nie przechodzi builda | popraw `install`/Dockerfile wg logu z zakładki Builds; pamiętaj: install z roota projektu, ścieżki build względem `.cursor` |
| Agent „głupieje” przy odpalaniu apki | dopisz do AGENTS.md sekcję „Cursor Cloud specific instructions” (lekcja 03) |
| Agent nie widzi sekretu | dodaj sekret → odpal NOWY run |
| Zmiana wygląda OK, testy przechodzą, ale apka nie | brak kryterium weryfikacji w zadaniu → dodaj „otwórz stronę X i pokaż screenshot” |

---

## 10. Co dalej

- [ ] Powtórz punkt 7 na 2–3 realnych zadaniach rozmiaru S
- [ ] Skopiuj pełny zestaw szablonów do głównego repo (lekcja 05)
- [ ] Włącz pierwszą automatyzację: **Bugbot** na PR-y (lekcja 05)
- [ ] Przeczytaj swój plan 30 dni (lekcja 06)

**Następna lekcja:** `05-Profesjonalny-workflow-autonomia.md` — pętla IDEA→PRODUKCJA,
automatyzacje i telefon jako panel dyrektora.
