# 🏗️ WORKFLOW MARZEŃ v2 — Instrukcja obsługi systemu (element po elemencie)

Format każdego rozdziału: **CO TO · PO CO · KONFIGURACJA · CZEGO NIE · KOSZT/TOKENY · JAK WSPÓŁPRACUJE**.
Wdrażasz w kolejności Faz z `00-PLAN-DZIALANIA.md`. Do szablonów plików patrz `cursor-kurs/szablony/`.

---

## 1️⃣ GIT — mechanizm cofania czasu

**CO TO:** system wersji. **PO CO:** agent może szaleć odważnie, bo każdy eksperyment da się cofnąć.
**KONFIGURACJA:**
1. `main` = protected branch (merge tylko przez MR, wymagane zielone CI).
2. Konwencja gałęzi: `feat/` `fix/` `chore/` + Conventional Commits (już w szablonach rules).
**CZEGO NIE:** pracy na main, „szybkich commitów wprost”, siłowego pusha.
**KOSZT:** $0.
**WSPÓŁPRACA:** każdy run agenta = osobna gałąź → MR. `git reset`/revert to Twoje CTRL+Z dla agentów.

---

## 2️⃣ HOST REPO — źródło prawdy (GitHub / GitLab / Origin)

**CO TO:** miejsce, gdzie żyje prawda o kodzie. **PO CO:** laptop przestaje być sercem systemu.
**KONFIGURACJA (po decyzji D1):**
- **GitHub Free:** utwórz repo → w Cursor dashboard Integrations → Connect GitHub → Sync Repos.
- **GitLab Premium:** jak wyżej; wymagana rola Maintainer + admin Cursor; opcjonalnie Protected Git Scope.
- Sekrety CI trzymasz w zmiennych CI/CD hosta; sekrety dla agentów — w zakładce Secrets Cursora.
**CZEGO NIE:** dwóch hostów naraz „na wszelki wypadek” (mirror tylko, jeśli świadomie).
**KOSZT:** GitHub $0 / GitLab Premium $29 / Origin: w planie Cursor (beta).
**WSPÓŁPRACA:** z niego korzystają Cloud Agents (klonują, branchują, pushują), tu odpala się CI, tu żyją MR-e,
na niego patrzą Automations (eventy) i Bugbot.

---

## 3️⃣ CURSOR DESKTOP — Twój kokpit

**CO TO:** IDE + agent lokalny. **PO CO:** praca „przy biurku” i zarządzanie całością.
**KONFIGURACJA:**
1. Settings → włącz **Privacy Mode** (SEC S6).
2. Agents Window — centrum dowodzenia runami (też cloud).
3. Model: domyślnie **Auto**; frontier wybierasz świadomie dla L/XL.
4. Z repo ładuje AGENTS.md + `.cursor/rules` + skills + hooks.
**CZEGO NIE:** wielkich zadań „bez planu” — L/XL zawsze z Plan/research run.
**KOSZT/TOKENY:** lokalny agent je z Twojej puli planu; zużycie rośnie z wielkością kontekstu —
nie otwieraj 40 plików „na wszelki wypadek”; używaj @-odniesień chirurgicznie.
**WSPÓŁPRACA:** stąd odpalasz: agenta lokalnego, Cloud Agenta (przełącznik Cloud), przeglądasz MR-y.

---

## 4️⃣ AGENTS.md + RULES + SKILLS — pamięć i kultura pracy

**CO TO:** konstytucja + reguły + procedury. **PO CO:** mnożnik jakości każdego agenta (i najtańsza „optymalizacja modelu” jaka istnieje).
**KONFIGURACJA:**
1. Skopiuj `cursor-kurs/szablony/AGENTS.md` → uzupełnij każde [UZUPEŁNIJ] (komendy MUSZĄ być prawdą).
2. `.cursor/rules/*.mdc` z szablonów; `alwaysApply` tylko dla fundamentów.
3. Skills: zacznij od 3: `dodaj-endpoint`, `migracja-db`, `review-bezpieczenstwa` (każdy: kroki + checklist + przykład z repo).
4. Sekcja „Cursor Cloud specific instructions” — jak odpalić projekt, testy, dev-server, jak robić screenshot.
**CZEGO NIE:** literatury („pisz dobry kod”), sprzecznych reguł, reguł których sam nie przestrzegasz.
**KOSZT/TOKENY:** dobra konstytucja = mniej iteracji agenta = realnie taniej o dziesiątki procent.
**WSPÓŁPRACA:** czytana przez agenta lokalnego, Cloud Agents, a zasady „treść zewnętrzna = dane” chronią przed prompt-injection.

---

## 5️⃣ CLOUD AGENTS + środowisko — Twoi pracownicy zdalni

**CO TO:** autonomiczni agenci na VM-kach Cursora. **PO CO:** praca bez Twojego laptopa; równoległość.
**KONFIGURACJA:** (szczegóły: `cursor-kurs` lekcje 02–04)
1. Guided setup środowiska → zielony Build → commit `environment.json` (parity rule!).
2. Sekrety do zakładki Secrets; environment-scoped przy multi-repo.
3. **Spend limit ustawiony.**
4. Pierwszy run = zadanie zerowe (README), potem zadania S/M z `szablony/PROMPTY-DLA-AGENTOW.md`.
**CZEGO NIE:** odpalania L/XL bez runu planistycznego; sekretów w kodzie; „przeczytaj całe repo”.
**KOSZT/TOKENY:** wg cennika API modelu; tańszy model na S/M; Builds skracają start (mniej tokenów na setup).
**WSPÓŁPRACA:** zasilany z Linear/Web/Slack/API; ląduje jako MR w host-cie repo; oblany przez Bugbota; Ty oglądasz artefakty i merdżujesz.

---

## 6️⃣ CI/CD — kontroler jakości, który nie śpi

**CO TO:** pipeline na host-cie repo. **PO CO:** GitLab/GitHub ma ostatnie słowo techniczne, nie agent.
**KONFIGURACJA:**
1. Szablon `cursor-kurs/szablony/.gitlab-ci.yml` (GitHub: analogiczny workflow).
2. **Parity rule (O1):** komendy CI ≡ komendy w AGENTS.md ≡ komendy w package.json/Makefile.
3. Start: lint → typecheck → test → build na każdy MR + main.
**CZEGO NIE:** 15 stage’ów na starcie; security-scan zanim masz cokolwiek wrażliwego; deploymentu bez bramki.
**KOSZT:** darmowe minuty hostów wystarczają solo na start.
**WSPÓŁPRACA:** MR od agenta → CI ✅ → dopiero AI review i Ty. Padła CI → agent naprawia w follow-upie.

---

## 7️⃣ MR + AI REVIEW (Bugbot / Security Agents / PR Routing) — bramka jakości

**CO TO:** Cursor-managed agenci przeglądający MR-y. **PO CO:** drugi (trzeci) recenzent zanim przeczytasz diff.
**KONFIGURACJA:**
1. Ze strony Automations włącz Bugbota i Security Agents na repo.
2. Uwagi Bugbota → follow-up w runie agenta („napraw uwagi z review”).
3. PR Routing & Approval — NIE włączamy na start (autopilota approve’ów nie chcesz bez metryk).
**CZEGO NIE:** traktowania AI review jako zamiennika Twojego review (to warstwa PRZED Tobą);
ignorowania powtarzających się uwag — idą do AGENTS.md (C6).
**KOSZT:** usage-based jak cloud runs — mierzysz w piątkowym rytuale (F4).
**WSPÓŁPRACA:** konsumuje MR-y z pętli; karmi AGENTS.md powtarzalnymi lekcjami.

---

## 8️⃣ LINEAR — „CO zrobić?” (backlog)

**CO TO:** system zadań. **PO CO:** jedno wejście, pamięć organizacji, kryteria akceptacji dla agentów.
**KONFIGURACJA:**
1. Workspace → 1 projekt = 1 repo. Etykiety: `agent` (gotowe dla agenta), `review` (czeka na Ciebie), `blocked`.
2. Szablon issue = nasz „szablon zadania dla agenta” (Cel/Zakres/Kryteria/Ograniczenia/Weryfikacja).
3. Integracja Cursor↔Linear: z Linear odpalisz/zreferencujesz zadania do agentów; linki do MR automatycznie.
**CZEGO NIE:** opisywania w issue JAK napisać kod (to rola agenta+docs); robienia zadań spoza boardu.
**KOSZT:** Free (250 issue) — wystarcza; Basic $10 gdy urośniesz.
**WSPÓŁPRACA:** Slack wrzuca pomysły → stają się tu zadaniami; automatyzacje mogą reagować na nowe issue;
Grok-PM raportuje status; Ty rano robisz triage.

---

## 9️⃣ AUTOMATIONS — agenci, którzy budzą się sami

**CO TO:** cloud agenci odpalani harmonogramem/eventami (GitHub/GitLab/Slack/Linear/webhooki). 
**PO CO:** system pracuje, gdy Ty nie pamiętasz.
**KONFIGURACJA (startowa trójka):**
1. **Daily digest** (codziennie 7:30): podsumowanie wczorajszych MR-ów, padniętych CI, nowych issue → Slack.
2. **Weekly security sweep** (poniedziałek 8:00): przegląd podatności → raport jako issue.
3. **Issue→plan** (event: nowe issue z etykietą `agent`): agent przygotowuje plan implementacji w komentarzu.
Możesz je też stworzyć opisem: skill `/automate` → „co tydzień w piątek podsumuj koszt i status…”.
**CZEGO NIE:** automatyzacji wypychających na produkcję (S5); automatyzacji bez zakresu repo;
stawiania 12 automatyzacji w pierwszym tygodniu — metruj każdą.
**KOSZT:** rozliczane jak cloud runs; scope Team Owned (pula zespołu) vs Private (Ty) — solo: Private.
**WSPÓŁPRACA:** jawszą część „zarządzania z telefonu”; wyniki lądują w host-cie repo/Slacku.

---

## 🔟 SLACK — gaduła, nie baza

**CO TO:** komunikacja + powiadomienia + szybkie wejście. **PO CO:** jesteś z telefonu „w biurze”.
**KONFIGURACJA:**
1. Integracja Cursor↔Slack (odpalanie agenta `@cursor`).
2. Powiadomienia: MR zmergowany, CI padł, automatyzacja skończyła.
3. Kanał `#pomysly` — wszystko co strzeli Ci do głowy na mieście (→ ktoś/Ty przenosi do Linear; C5).
**CZEGO NIE:** trzymania tam zadań („hej zrób billing” bez issue = dług).
**KOSZT:** $0.
**WSPÓŁPRACA:** digest z Automations ląduje tu; Grok-PM pinga tu o blockerach.

---

## 1️⃣1️⃣ GROK BOT — Twoi nazwani pracownicy (NOWOŚĆ v2)

**CO TO:** trwałe, nazwane boty Cursora ze **wspólnym chmurowym komputerem** (przeglądarka, pliki,
terminal), pamięcią, umiejętnością uczenia się procedur (skills/routines), koordynacją między botami.
Działa, gdy Twój laptop jest zamknięty. **W cenie płatnego planu Cursor.**
**PO CO:** praca NIE-kodowa, wieloetapowa, „po aplikacjach”: research, przeklikiwanie QA, raportowanie.
**KONFIGURACJA — stwórz dokładnie 2 boty na start:**
1. **BADACZ** — zadanie: „gdy proszę o research, rzuć raportem: opcje +/−, rekomendacja, źródła; kończ pytaniami otwartymi”.
2. **PM** — zadanie: „codziennie 8:00 (rutina) podsumuj Linear: co atakuje termin, co zablokowane, co czeka na moją decyzję; pisz krótko”.
Jeden pokazany proces → zapisujesz jako skill/routine (bot odtwarza na zawołanie/harmonogram).
**CZEGO NIE:** puszczania go do kodu zamiast agentów (od tego są Cloud Agents); logowania botów
do wrażliwych kont produkcyjnych; trzymania sekretów na wspólnym komputerze (wszyscy boty je widzą).
**KOSZT:** limity Twojego planu (bez dodatkowego abonamentu; można podpiąć SuperGrok — nie na start).
**WSPÓŁPRACA:** BADACZ karmi specyfikacje w Linear; PM karmi Twój poranny triage; obaj nie dotykają git.

---

## 1️⃣2️⃣ TAILSCALE + półka specjalistów

**TAILSCALE (airbag):** instalujesz na domowym PC i telefonie; używasz TYLKO awaryjnie
(„muszę coś z lokalnej maszyny”). Nie optymalizuj dostępu do PC — optymalizuj jego zbyteczność.
**PÓŁKA (DevBox/OpenCode/Hermes/inne):** sięgasz gdy pojawi się KONKRETNY problem, którego główny
system nie rozwiązuje. Każde sięgnięcie → notatka w DECISIONS.md („dlaczego główny stack nie dał rady”).

---

## 📌 Mapa „gdzie co mieszka” (naucz na pamięć)

| Rzecz | Mieszka w | NIGDY w |
|---|---|---|
| kod + prawda | host repo | laptop „u mnie działa” |
| zadania / CO | Linear | Slack, głowa |
| zasady / kultura | AGENTS.md + rules + skills | prompty za każdym razem |
| sekrety | Secrets Cursor / CI vars | kod, issue, logi, Slack |
| decyzje / DLACZEGO | DECISIONS.md | czat |
| pomysły-wystrzały | Slack #pomysly → Linear | „zapamiętam” |
| decyzja o merge/deploy | Ty | agent/automat |
| status dnia | Twój triage rano (Linear+Runy) | klikanie wszędzie po kolei |

> Gdy nie wiesz, gdzie coś włożyć — ta tabela odpowiada. Gdy brakuje wiersza: dopisz (i zaktualizuj ten plik).
