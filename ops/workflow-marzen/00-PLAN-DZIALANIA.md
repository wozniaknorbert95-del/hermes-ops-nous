# 🎯 PLAN DZIAŁANIA — Workflow Marzeń v2
**Projekt:** DSAAS Development OS · **Właściciel:** Dowódca (Ty) · **Wykonawca:** Sztab (AI)
**Stan wiedzy:** wrzesień 2026 · **Status:** gotowe do wdrożenia

---

## 1. Cel operacji

Zbudować workflow, w którym **Ty podejmujesz decyzje, a system (Cursor + agenci + CI)** wykonuje
80–90% pracy — lokalnie i zdalnie — przy **najniższym możliwym koszcie stałym**, bez rezygnacji
z profesjonalnych standardów (review, CI, bezpieczeństwo, pamięć organizacji).

**Definition of Done całej operacji:**
> Jesteś w stanie z telefonu zamienić pomysł w wdrożony na produkcję feature
> (idea → issue → agent → MR → CI → review → merge → deploy), nie otwierając laptopa,
> znając koszt każdego kroku i mając zapisane decyzje „dlaczego tak”.

---

## 2. Werdykt Sztabu w 10 punktach (pełny raport: `01-RAPORT-SZTABU.md`)

1. **Twój workflow z `auuu2` jest w 85% poprawny.** Nie zmieniamy architektury — doszlifowujemy.
2. **Pętla zostaje:** IDEA → ISSUE → AGENT → KOD → TESTY → MR → CI → REVIEW(AI) → REVIEW(Ty) → MERGE → DEPLOY → OBSERWACJA.
3. **Podział ról zostaje:** Linear odpowiada „CO”, Cursor „JAK”, Git „PRAWDA”, Slack tylko „GADUŁA”.
4. **Grok Bot ≠ to, co myślał auuu2, ale jest lepszy, niż myślał:** to gotowy produkt Cursora
   (nazwani, trwali boty z własnym chmurowym komputerem) **w cenie Twojego płatnego planu**.
   Dostaje rolę: badacz/QA/PM — dokładnie tę, którą auuu2 dla niego przewidział, za 0 zł ekstra.
5. **Najtańszy pełnoprawny stack to ~$20/mc** (Cursor Pro + GitHub Free + Linear Free).
   **[akt. 07.09]** Istnieje TEŻ wariant „po Twojemu, z GitLabiem” za $0 za repo: **GitLab CE na własnym
   VPS** (sam GitLab jest darmowy; project access tokens są na self-managed w każdej licencji —
   oficjalne docs.gitlab.com). Płatny Premium dotyczy tylko integracji Cloud Agents na gitlab.com.
   Duo (system Credits) odkładamy do Fazy 5 — nie kupuj drugiego mózgu, zanim pierwszy nie jest użyty.
6. **Cloud Agents wymagają płatnego planu i rozliczają się wg cennika API — Twoich darmowych
   kluczy nie użyjesz.** Ekonomię ratuje: Builds, AGENTS.md, drabina modeli (S/M/L/XL), małe MR-e.
7. **Bezpieczeństwo: 4 bramki człowieka** (merge, deploy produkcyjny, sekrety, zmiana architektury).
   Wszystko inne może być automatyczne.
8. **Nowości IX 2026, które włączamy do workflow:** Automations (też z eventów GitLaba),
   Bugbot + Security Agents + PR Routing (review warstwą AI), `/automate` (automatyzacja z opisu),
   multi-repo environments, Cursor Origin (beta — plan B hostingu).
9. **Największe ryzyko to nie narzędzia — to chaos operacyjny:** wdrażamy „system anty-zgubienia”
   (jedno wejście = Linear, limit WIP, rytuały dzienny/tygodniowy). Pełna procedura: `04-INSTRUKCJA-OBSUGI.md`.
10. **Nic nie instalujemy „na zapas”.** K8s, własny orkiestrator, płatny Slack, Jira, Notion — poza planem.

---

## 3. Decyzje, które musisz podjąć (3 fory — reszta jest zdecydowana)

| # | Decyzja | Opcja A (TANIO — rekomendacja Sztabu) | Opcja B (PO TWOJEMU) |
|---|---|---|---|
| D1 | ✅ **WYBRANO 07.09.2026: GitLab CE self-hosted ($0 + własny VPS)** — instrukcja wdrożenia: `05-GITLAB-CE-SELFHOSTED.md` | — | plan B: gitlab.com Premium $29/mc (gdyby CE nie przeszedł testu integracji) |
| D2 | Drugi mózg AI w platformie git | **Nie teraz** (Cursor wystarcza) | GitLab Duo/Agents — rozliczane systemem **GitLab Credits** (dodatek); decyzja po Fazie 5 |
| D3 | Zarządzanie zadaniami | **Linear Free — $0** (250 issue, 2 zespoły, unlimited members) | Linear Basic $10/user/mc, gdy przekroczysz limit |

ℹ️ Wariant „pośrodku”: **Cursor Origin** (beta, w ramach planu Pro) — hosting gita u Cursora;
plan B, gdybyś chciał wszystko w jednym ekosystemie. Nie buduj na becie fundamentu.

> ⚠️ **AKTUALIZACJA 07.09.2026 — mapa D1 przepisana po weryfikacji cen i funkcji NA OFICJALNYCH
> STRONACH** (about.gitlab.com/pricing, docs.gitlab.com, cursor.com/docs/integrations/gitlab,
> github.com/pricing, linear.app/pricing — pełna lista w sekcji „ŹRÓDŁA” na końcu).
> Wcześniejsza wersja sugerowała „GitLab = płatny pod Cloud Agents”. To prawda **tylko dla
> gitlab.com** — sam GitLab JEST darmowy, a kluczowy jest self-managed CE (patrz niżej).

#### Mapa opcji hosta repozytorium (oficjalne źródła, 07.09.2026)

| Opcja | Hosting gita + MR + CI | Cursor desktop / lokalny agent | Cloud Agents + Bugbot (oficjalna integracja Cursor) | Koszt/mc |
|---|---|---|---|---|
| **GitHub Free** | ✅ | ✅ | ✅ pełna — cursor.com/docs/integrations/github | **$0** |
| **gitlab.com Free** | ✅ (400 min CI, 10 GiB) | ✅ normalnie (clone / push / MR) | ❌ — na gitlab.com project access tokens wymagają Premium: docs.gitlab.com *„On GitLab.com, project access tokens require a Premium or Ultimate subscription”* | $0 (ale bez Cloud Agents) |
| **GitLab CE self-managed (własny VPS)** | ✅ (darmowy CE, bez limitów userów) | ✅ | ‼️ **najprawdopodobniej TAK** — docs.gitlab.com: *„On GitLab Self-Managed … project access tokens are available with any license”* (czyli też darmową). Doc Cursora mówi ogólnie „paid plan required”, ale na forum Cursora (09.2026) użytkownicy wskazują, że dla self-managed to nieaktualne. **→ 15-minutowy test w Fazie 3 rozstrzyga.** | **$0 za GitLab** + koszt Twojego VPS + ~1h/mc opieki |
| **gitlab.com Premium** | ✅ | ✅ | ✅ oficjalnie | $29/user (rocznie) |

**Rekomendacja Sztabu po aktualizacji:**
- Masz VPS i godzinę na setup → **GitLab CE self-hosted** — jesteś „po swojemu” na GitLabie za $0
  (dokładnie ta droga, którą wskazałeś). Test integracji z Cursor robimy w Fazie 3.
- Nie masz VPS / nie chcesz administrować → **GitHub Free** (integracja działa „od ręki”).
- Premium ($29) kupujesz TYLKO, gdy test CE się nie powiedzie, a GitLab jest nie do odstąpienia.

**Koszt stały wg decyzji:**

| Wariant | Cursor | Repo | Linear | Slack | Razem/mc |
|---|---|---|---|---|---|
| **Tanio-profesjonalny** | Pro $20 | GitHub $0 | $0 | $0 | **$20** |
| **Po Twojemu ZA DARMO (GitLab CE self-hosted)** ⭐ | Pro $20 | CE $0 (+Twój VPS) | $0 | $0 | **$20** |
| Po Twojemu w chmurze (gitlab.com) | Pro $20 | Premium $29 | $0 | $0 | $49 |
| Pełny auuu2 (Premium + Duo wg Credits) | Pro $20 | Premium $29 + Credits | $0 | $0 | $49 + Credits |
| Drogie korpo (dla porównania) | Ultra $200 | Ultimate: cena custom | $16/user | płatny | $270+ ⚠️ |

⭐ **Po aktualizacji z 07.09.2026 wariant „po Twojemu” też kosztuje $20/mc**, jeśli hostujesz
GitLaba CE na własnym VPS — darmowy GitLab + (prawdopodobnie) pełna integracja z Cursor Cloud Agents.

Do tego **zużycie Cloud Agents/Bugbota wg cennika API** — kontrolowane spend limitem
(szacunkowo kilka–kilkanaście $/mc przy normalnej pracy solo; mierzysz od Fazy 3).

---

## 4. Architektura docelowa v2

```
                        DOWÓDCA (Ty)
        decyzje · priorytety · plan architektury · approval
                             │
        ┌────────────────────┼─────────────────────┐
        │                    │                     │
        ▼                    ▼                     ▼
  📱 PANEL DOWODZENIA   🗣️ SLACK (gaduła)     🤖 GROK BOT
  telefon/web/desktop   pomysły, notyfikacje  badacz / QA / PM
        │                    │                     │
        │                    ▼                     │ raporty
        │               ┌─────────┐                │
        └──────────────►│ LINEAR  │◄───────────────┘
                        │  CO     │
                        └────┬────┘
                             ▼
                        🧑‍💻 CURSOR — JAK
                 ┌───────────┴────────────┐
                 ▼                        ▼
         Agent lokalny             Cloud Agents
         (przy laptopie)     (+ Automations: Bugbot,
                              Security, harmonogramy)
                 │                        │
                 └───────────┬────────────┘
                             ▼
                        GIT → HOST (PRAWDA)
                             │
              ┌──────────────┼───────────────┐
              ▼              ▼               ▼
             CI ✅        MR + review       SECRETS
         (lint/test/   (AI review →      (skarbiec,
          build/sec)    Ty approve)       nie kod)
                             │
                             ▼
                    STAGING → 🛂 TY → PROD
                             │
                        OBSERWACJA → IDEA (pętla)

  🪂 Tailscale = airbag awaryjny do domowego PC (nie uczestniczy w pracy)
  🧰 DevBox/OpenCode/Hermes = półka specjalistów (opcjonalnie)
```

---

## 5. Plan wdrożenia — 6 tygodni, 4 fazy

Każda faza kończy się **działającym artefaktem**, nie „postępem konfiguracji”.

### FAZA 0 — Decyzje + fundamencik (dni 1–2)
- [ ] Decyzje D1–D3 (tabela wyżej) → **D1 rozstrzygnięta: GitLab CE self-hosted**
- [ ] **GitLab CE zainstalowany na VPS wg `05-GITLAB-CE-SELFHOSTED.md`**: domena + HTTPS (Let's Encrypt),
      runner CI zarejestrowany, hasło root zmienione, publiczne rejestracje WYŁĄCZONE
- [ ] Repo utworzone/uporządkowane; `main` = protected branch; merge tylko przez MR
- [ ] Konto Cursor Pro aktywne; **spend limit ustawiony**
- [ ] Linear: workspace + 1 projekt + etykiety (`agent`, `review`, `blocked`)
- ✅ **Kryterium wyjścia:** puste repo na własnym GitLab CE z CI „hello” (na własnym runnerze) i pierwszym issue w Linear

### FAZA 1 — Fundament bezpiecznej produkcji (tydzień 1)
- [ ] Git + CI: pipeline lint → typecheck → test → build (komendy = 1:1 z AGENTS.md)
- [ ] Szablony z `cursor-kurs/szablony/` skopiowane i uzupełnione [UZUPEŁNIJ]
- [ ] `AGENTS.md` v1 w repo; rules `.cursor/rules/*`
- ✅ **Kryterium:** MR ręczny przechodzi CI; agent lokalny cytuje Twoje zasady

### FAZA 2 — Pamięć AI (tydzień 2)
- [ ] `ARCHITECTURE.md`, `PRODUCT.md`, `DECISIONS.md`, `TESTING.md` (po 1 stronie!)
- [ ] 3 pierwsze Skills (np. `dodaj-endpoint`, `migracja-db`, `review-bezpieczenstwa`)
- [ ] Audyt promptem A1 z `03-PROMPTY-SZTABU.md` → poprawki
- ✅ **Kryterium:** agent realizuje issue S/M bez ani jednego pytania o konwencje

### FAZA 3 — Autonomia cz. 1: Cloud Agents (tydzień 3)
- [ ] Guided setup środowiska → zielony Build → `environment.json` w repo
- [ ] Sekrety w zakładce Secrets (nie w kodzie!)
- [ ] 3 realne MR-e zrobione przez Cloud Agenta (jeden 100% z telefonu/web)
- [ ] Bugbot + Security Agents włączone na MR-e
- ✅ **Kryterium:** znasz swój „koszt na MR”; 2 z 3 MR-ów zmergowane bez ręcznych poprawek

### FAZA 4 — Zarządzanie + autonomia cz. 2 (tydzień 4–5)
- [ ] Telefon: Cursor iOS / PWA Android; SLACK podpięty (wejście pomysłów, powiadomienia)
- [ ] Automations: ① daily digest ② weekly security sweep ③ „nowe issue z etykietą `agent` → plan-implementacji”
- [ ] Grok Bot: utwórz 2 boty — **BADACZ** (research/raporty) i **PM** (status Linear, blockery, przypomnienia)
- [ ] Rytuały z `04-INSTRUKCJA-OBSUGI.md` wdrożone (poranny triage 10', wieczorny przegląd 5')
- ✅ **Kryterium:** pełna pętla issue→prod wykonana z telefonu; rano dostajesz raport zamiast szukać

### FAZA 5 — Hardening + metryki (tydzień 6)
- [ ] Staging auto-deploy z `main` + produkcja za ręczną bramką; prosty monitoring (błędy + uptime)
- [ ] Retrospektywa: wpisz lekcje do AGENTS.md (system się uczy)
- [ ] Raport kosztów: $/MR, tokeny/run, najdroższe operacje → plan optymalizacji
- [ ] Decyzja o Duo / upgrade'ach na TWARDYCH danych (nie na hype)
- ✅ **Kryterium:** dashboard kosztów znany; workflow v2.1 zapisany w `DECISIONS.md`

---

## 6. Budżety i drabina modeli („budżet poznawczy” v2)

| Zadanie | Przykład | Model/kontekst | Gdzie |
|---|---|---|---|
| 🟢 S | typo, test, copy, mały fix | auto/tańszy, mały kontekst | lokalny agent lub cloud |
| 🟡 M | endpoint, komponent, bugfix+testy | standard | cloud agent |
| 🔴 L | feature z planem, refaktor modułu | frontier + Plan Mode | cloud agent (plan osobno!) |
| ⚫ XL | zmiana architektury, multi-repo | frontier, duże okno, wcześniej research | cloud, z Twoim nadzorem |

**Guardraile kosztowe (nienegocjowalne):**
- Spend limit USTAWIONY zanim odpalisz pierwszego agenta.
- Zadanie L/XL zawsze zaczyna się od runu „research/plan, bez zmian w kodzie”.
- Zakaz „przeczytaj całe repo” — zadania wskazują pliki/obszary (oszczędza 30–60% tokenów).
- Builds aktualne → agent nie pali tokenów na instalowanie świata.
- Piątek: 10 minut przeglądu kosztów + najdroższy run tygodnia → lekcja do AGENTS.md.

---

## 7. Bramki bezpieczeństwa (4 × TYLKO CZŁOWIEK)

| Bramka | Kto decyduje | Dlaczego |
|---|---|---|
| Merge do `main` | Ty (po CI ✅ + AI review) | ostatnia linia przed prawdą |
| Deploy na produkcję | Ty (manual gate) | pieniądze/użytkownicy |
| Sekrety: dodanie/rotacja | Ty | wyciek = katastrofa |
| Zmiana architektury / nowa zależność-magnat | Ty | długoterminowy dług |

Wszystko poza tym: agent + automatyzacje. AI review (Bugbot/Security) = warstwa PRZED Tobą, nie zamiast Ciebie.

---

## 8. KPI — jedyny „dashboard”, którego pilnujesz (raz w tygodniu)

| Metryka | Start (t. 3) | Cel (t. 6) |
|---|---|---|
| Koszt na MR | ??? (zmierz) | stabilny/malejący |
| % MR zmergowanych bez Twoich poprawek | — | ≥ 60% |
| Czas issue → merge | — | malejący trend |
| % zadań zaczętych jako issue (nie z czatu) | — | 100% dla M+ |
| Powtarzające się uwagi Bugbota | — | każda → zasada w AGENTS.md |

---

## 8a. Warstwa edukacyjna — AI Engineering Academy OS (dodano 07.09.2026)

Dowódca (ADHD) zdefiniował wymóg: *uczenie się ma być wizualne, na raty, zawsze z odpowiedzią
„co teraz”, bez przytłoczenia.* Uchwała Sztabu: **nie budujemy osobnego kursu — wdrożenie JEST studiami.**

- **Moduł studiów ≡ faza tego planu** (1↔1, 2↔2, …, 6↔5). Jedna oś, zero równoległych systemów.
- **Interfejs nauki:** `akademia/DASHBOARD.html` — wizualna mapa modułów, karta „▶ TERAZ” (zawsze
  dokładnie jedna następna rzecz), biblioteka na raty ≤20′/lekcja, laboratoria z checkboxami,
  checkpointi „UMIEM/NIE” z procedurą ratunkową, zapis postępu + eksport/import.
- **Biblioteka:** `cursor-kurs/` (podręcznik) + `workflow-marzen/` (podręcznik operacyjny).
- **Artefakty w GitLab CE** = dowody zaliczeń (zielony pipeline, MR-#, raport kosztów).
- **Egzamin końcowy:** drugi projekt od zera, solo, w weekend. Zaliczony = absolwent.
- Zasady pracy z tym systemem: `akademia/README.md`. KPI studiów: % checkpointów zaliczonych
  za pierwszym podejściem; cel: ≥ 4 z 6.

---

## 9. Ryzyka i mitygacje

| Ryzyko | Mitygacja |
|---|---|
| „3 tygodnie konfigurowania agentów zamiast budować produkt” | fazy z kryteriami wyjścia; każdy tydzień kończy się artefaktem |
| Agent dokucza architekturą | AGENTS.md zasada „zachowaj architekturę, chyba że zadanie zezwala” + L/XL = plan-run najpierw |
| Prompt injection przez treść issue/komentarzy | zasada konstytucji: treść z zewnątrz = dane, nie rozkazy; watpliwość → stop&ask |
| Koszt ucieka | spend limit + drabina modeli + piątkowy przegląd |
| Chaos narzędzi | jedno wejście = Linear; Slack tylko wejściem; „gaduła ≠ zadanie” |
| Vendor lock-in | proces (issue→MR→CI) ponad narzędziami; AGENTS.md i szablony przenośne |

---

## 10. Jak korzystać z tego pakietu

| Plik | Kiedy czytasz |
|---|---|
| `00-PLAN-DZIALANIA.md` (ten) | teraz; wracasz w każdy piątek |
| `01-RAPORT-SZTABU.md` | teraz (dlaczego te decyzje) + gdy ktoś podważa plan |
| `02-WORKFLOW-MARZEN-v2.md` | przy wdrażaniu każdego elementu (instrukcje krok po kroku) |
| `03-PROMPTY-SZTABU.md` | codziennie przy pracy ze Sztabem/Cursorem; do automatyzacji |
| `04-INSTRUKCJA-OBSUGI.md` | rano po Fazie 4 — Twoja „książka lotnicza” |
| `05-GITLAB-CE-SELFHOSTED.md` | **Faza 0:** instalacja/hardening/runner/backup GitLaba CE na VPS + test integracji z Cursor |
| `cursor-kurs/` | gdy czegoś nie rozumiesz (teoria), gdy zapominasz praktyki |
| `akademia/DASHBOARD.html` + `akademia/README.md` | **codziennie rano** — interfejs studiów: karta „TERAZ”, moduły, checkpointi |

---

## 11. ŹRÓDŁA — zasada „tylko oficjalne strony” (zweryfikowane na żywo 07.09.2026)

Na żądanie Dowódcy **każda cena i funkcja w tym planie musi pochodzić z oficjalnej strony narzędzia
i mieć datę pobrania**. Inne źródła (blogi, agregatory) = tylko kontekst, nigdy podstawa decyzji.

| Twierdzenie w planie | Oficjalne źródło |
|---|---|
| Cursor Pro $20 / Pro+ $60 / Ultra $200; cloud agents + Grok Bot w planie; Bugbot usage-based | `cursor.com/pricing` |
| Cloud agents rozliczane wg cennika API; spend limit; wymagany płatny plan | `cursor.com/docs/cloud-agent` (Billing, Troubleshooting) |
| Integracja Cursor↔GitLab: „requires a paid GitLab plan (Premium or Ultimate). Project access tokens … are not available on GitLab Free” | `cursor.com/docs/integrations/gitlab` |
| GitLab: gitlab.com Free $0 (400 min CI, 10 GiB); Premium $29/user (rocznie); Ultimate: cena custom; Self-Managed Free $0 | `about.gitlab.com/pricing` |
| „On GitLab.com, project access tokens require a Premium or Ultimate subscription” ORAZ „On GitLab Self-Managed and GitLab Dedicated, project access tokens are available with any license” | `docs.gitlab.com/user/project/settings/project_access_tokens` |
| Rozjazd doc-vs-rzeczywistość dla self-managed (zgłoszenie 09.2026) | `forum.cursor.com` → wątek o dokumentacji integracji GitLab |
| GitHub Free $0: unlimited public/private repos, 2000 min CI, Dependabot, Issues & Projects | `github.com/pricing` |
| Linear Free $0: unlimited members, 2 zespoły, 250 issue, Agent platform + Linear Agent; Basic $10; Business $16 | `linear.app/pricing` |
| Grok Bot w cenie płatnych planów; trwale boty, wspólny chmurowy komputer | `cursor.com/docs/grok-bot` + `cursor.com/pricing` |
| Automations: triggery (GitLab/GitHub/Slack/webhooki/Linear), `/automate`, rozliczenie jak cloud agents | `cursor.com/docs/cloud-agent/automations` |
| Cursor Origin (beta, od płatnych planów) | `cursor.com/docs/origin` |

Zasada utrzymania: przy każdym piątkowym przeglądzie (Faza 5) — jeśli decyzja dotyczy planu/ceny,
najpierw odśwież corespondujący wiersz powyżej na oficjalnej stronie. Data ostatniego pełnego audytu
cen: **07.09.2026**.
