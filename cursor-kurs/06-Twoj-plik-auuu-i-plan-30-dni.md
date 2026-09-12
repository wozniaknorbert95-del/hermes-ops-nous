# 🗺️ LEKCJA 06 — Twój dokument `auuu.txt` + plan 30 dni

## Część 1: Co Twój dokument mówi — w 8 prostych zdaniach

1. „Nie zbieraj narzędzi. Zbuduj **system**, w którym każde narzędzie da się wymienić.”
2. Centrum prawdy o kodzie = **Git** (GitLab/GitHub), a nie Twój laptop.
3. Cursor = Twoje **główne okno do AI**; Cloud Agents = pracownicy w chmurze.
4. Telefon = panel dyrektora; laptop = opcja / warsztat awaryjny.
5. Repo ma być **samouczkiem dla AI** (AGENTS.md, ARCHITECTURE, DECISIONS, rules, skills).
6. Każde zadanie idzie ścieżką: **Issue → Agent → Branch → Testy → MR → Review → Deploy.**
7. Automatyzacje (Bugbot, harmonogramy, zdarzenia) zdejmują z Ciebie pamiętanie o wszystkim.
8. **Im prostszy system — tym potężniejszy.** Każda doklejona „fajna rzecz” to podatek od uwagi.

## Część 2: Weryfikacja faktów z dokumentu (stan: wrzesień 2026)

✅ **Prawda (potwierdzone w oficjalnych źródłach):**
- Cloud Agents: izolowana VM, własna gałąź, PR/MR, przeglądarka/desktop, artefakty, praca z web/mobile.
- **Integracja Cursor↔GitLab na gitlab.com wymaga Premium/Ultimate** — PRAWDA, potwierdzone 07.09.2026
  na oficjalnych stronach: cursor.com/docs/integrations/gitlab (wymaga project access tokens) +
  docs.gitlab.com („On GitLab.com, project access tokens require a Premium or Ultimate subscription”).
- **ALE (istotne uzupełnienie 07.09):** sam GitLab JEST darmowy, a na **GitLab self-managed CE** project
  access tokens są „available with any license” (docs.gitlab.com) — czyli Twoja droga „GitLab za darmo na
  własnym VPS” może dać pełną integrację z Cloud Agents bez $29. Do potwierdzenia 15-min testem przy setupie.
- Automatyzacje Cursora: harmonogram, eventy GitHuba/**GitLaba**, Slack, webhooki — działa.
- GitLab Duo Agent Platform + **Flow Creator w GitLab 19.3** (sierpień 2026): tworzenie flow językiem naturalnym — działa.

⚠️ **Doprecyzowania / rzeczy do ostrożności:**
- „Agent kontroluje Twój komputer domowy” — w oficjalnych docs istnieje **remote desktop control
  VM-ki agenta** (przejmujesz jego chmurowy pulpit). Kontrola Twojego własnego komputera to co innego —
  nie buduj na tym planu; Tailscale zostaje Twoim airbagiem do własnej maszyny.
- Twój dokument milczy o pieniądzach: **Cloud Agents ≠ darmowe klucze API** (lekcja 02) — to zmienia
  ekonomię „pracy z telefonu”: każdy run kosztuje wg cennika API. Limit wydatków = obowiązek.
- **Origin** (beta): Cursor ma własny hosting gita od planu Pro — alternatywa dla GitLab Premium,
  jeśli „zróbmy wszystko u Cursora”.

## Część 3: Pojęcia z dokumentu — tłumaczenie na ludzki

| Pojęcie z auuu.txt | Co to znaczy po ludzku |
|---|---|
| „source of truth” | Jeden sejf z prawdą: Git. Nie laptop, nie czat, nie „u mnie działa”. |
| „agent-agnostic core” | Proces (Issue→MR→CI) zostaje; agentów podmieniasz jak silniki. |
| „AI-native repo” | Repo-tak-napisane, że obcy AI ogarnia je bez pytania Cię o cokolwiek. |
| „Tailscale jako airbag” | Nie optymalizuj zdalnego dostępu do PC — optymalizuj BRAK potrzeby tego dostępu. |
| „operating system firmy” | Po pół roku masz nie tylko kod, ale: wiedzę o produkcie + historię decyzji + procedury + testy + automatykę. To jest warte więcej niż sam kod. |
| „DSAAS Development OS v1” | Twoja własna wersja pętli z lekcji 05, zszyta na Twój konkretny projekt. |

---

## Część 4: PLAN 30 DNI — od czytania do autonomii

> Zasada planu: **najpierw fundamenty (dni 1–10), potem praktyka (11–20), potem automatyka (21–30).**
> Nie przeskakuj. Każdy tydzień kończy się czymś, co DZIAŁA.

### Tydzień 1 — Fundament repo (kod czeka)

| Dzień | Zadanie | Gotowe, gdy… |
|---|---|---|
| 1 | Decyzja: GitHub Free **albo** GitLab Premium **albo** Origin. Załóż/uporządkuj repo. | repo dostępne, `main` = protected branch |
| 2 | Wstaw `szablony/AGENTS.md` → uzupełnij komendy projektu (build/test/run) | agent ma „mapę osiedla” |
| 3 | Skopiuj `.cursor/rules/*` z szablonów; dostosuj do stacku | reguły widoczne dla agenta |
| 4 | Napisz `ARCHITECTURE.md` (1 strona!) + pierwszy wpis w `DECISIONS.md` | jedna strona mapy systemu istnieje |
| 5 | Dopnij `.gitlab-ci.yml` (lub GitHub Actions): lint → testy → build | pipeline zielony na `main` |
| 6–7 | Szablony issue/MR; testowe issue „tylko dla agenta” z szablonu | issue gotowe do zadania |

### Tydzień 2 — Pierwsze runy w chmurze

| Dzień | Zadanie | Gotowe, gdy… |
|---|---|---|
| 8 | Podłącz providera w Cursor (Integrations → Sync Repos); ustaw **spend limit** | repo widoczne w Cloud Agents |
| 9 | Guided setup środowiska (lekcja 03, ścieżka A); obejrzyj cały proces | Build zielony |
| 10 | Commitnij `.cursor/environment.json`; dodaj sekcję „Cursor Cloud specific” do AGENTS.md | konfiguracja w gicie |
| 11 | **Zadanie zerowe** (README) z lekcji 04 → pełny obieg: VM → gałąź → MR → merge | pierwszy MR od agenta ✅ |
| 12–13 | Dwa zadania rozmiaru S (testy / mały fix) — notuj koszt każdego runu | znasz swój „koszt na MR” |
| 14 | Retrospektywa: co agent zepsuł/nie zrozumiał? → **dopisz zasady do AGENTS.md** | konstytucja v2 |

### Tydzień 3 — Automatyką zdejmujesz z siebie pamięć

| Dzień | Zadanie | Gotowe, gdy… |
|---|---|---|
| 15 | Włącz **Bugbota** na wszystkie MR-e | pierwszy AI-review na żywym MR |
| 16 | Automatyzacja #1: daily digest (harmonogram) → Slack/mail | rano masz podsumowanie |
| 17 | Automatyzacja #2: weekly security sweep | raport bezpieczeństwa |
| 18 | Zadanie rozmiaru M z formułą 6 pól → praca agenta bez Twojego PC (odpal z telefonu/web) | MR zrobiony „z ulicy” |
| 19 | Środowisko: dopnij brakujące sekrety/serwisy (dev-server w `terminals`) | agent sam odpala apkę i robi screenshoty |
| 20–21 | Retrospektywa + czyszczenie: martwe reguły out, nowe lekcje in | AGENTS.md v3 |

### Tydzień 4 — Pełna pętla z telefonu

| Dzień | Zadanie | Gotowe, gdy… |
|---|---|---|
| 22 | Zainstaluj iOS app / Android PWA (`cursor.com/agents` → Install App) | start agenta z telefonu działa |
| 23 | Prawdziwy feature: issue → spec → plan-agent → implementacja → CI → Bugbot → Ty: merge | **pełna pętla zamknięta** |
| 24–25 | Staging/review app w CI (choćby najprostszy) | każdy MR ma podgląd na żywo |
| 26 | Zadanie L: „zbadaj i zaproponuj plan, bez zmian w kodzie” → potem implementacja z planu | umiesz dzielić wielkie zadania |
| 27 | Dokument „JAK PRACUJEMY” dla przyszłego siebie/ludzi (1 strona, oparta o lekcję 05) | proces spisany |
| 28–29 | 2–3 normalne dni pracy WYŁĄCZNIE przez pętlę (żadnego grzebania w kodzie ręcznie) | działa bez Ciebie |
| 30 | Rozliczenie miesiąca: koszt/MR, % MR bez poprawek, czas cyklu → plan v2 | metryki znane, decyzje na danych |

---

## Część 5: Checklista „Jestem pro” (odhacz w ciągu 30 dni)

- [ ] Moje repo czyta się jak instrukcja dla AI (AGENTS.md + ARCHITECTURE + DECISIONS)
- [ ] Cloud Agent startuje z gotowego Buildu i odpala mój projekt bez pytań
- [ ] Przynajmniej 5 MR-ów zrobionych przez agenta, w tym 1 w 100% z telefonu
- [ ] CI blokuje złośliwe/zepsute mergowanie (lint+testy+build obowiązkowe)
- [ ] Bugbot/Security robią pierwszą rundę review przede mną
- [ ] Spend limit ustawiony; znam swój koszt na MR
- [ ] Żadnego sekreta w kodzie/historii gita
- [ ] Każde większe zadanie zaczyna się issue z kryteriami akceptacji
- [ ] Zadania L rozbijam: plan-agent → implementacja
- [ ] Uwagi z review wpisuję z powrotem do AGENTS.md (system się uczy)
- [ ] W 10 min potrafię wyjaśnić komuś cały system na 1 kartce (pętla z lekcji 05)

> Jak odhaczysz wszystko — nie potrzebujesz już żadnego kursu. Potrzebujesz tylko więcej issue'ów. 🎯
