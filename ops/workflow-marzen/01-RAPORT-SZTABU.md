# 📋 RAPORT SZTABU — Audyt workflow Dowódcy (`auuu2`) → zmiany v2
**Data audytu:** IX 2026 · **Przedmiot:** workflow z dokumentu auuu2 · **Metoda:** przegląd dokumentu +
weryfikacja faktów rynkowych (oficjalne cenniki i dokumentacje: Cursor, GitLab, Linear).

Sztab: 🏛️ **ADR** (architektura) · 💰 **FIN** (FinOps/koszty) · 🛡️ **SEC** (red team/bezpieczeństwo) ·
⚙️ **OPS** (DevOps/jakość) · 🧭 **COACH** (proces/produktywność)

---

## WERDYKT OGÓLNY

> Workflow z `auuu2` jest architektonicznie zdrowy (85%). Wymaga:
> **(a)** korekt faktograficznych w 3 miejscach, **(b)** ekonomii kosztów, której auuu2 prawie nie ma,
> **(c)** bramek bezpieczeństwa zapisanych wprost, **(d)** systemu anty-chaos dla jednoosobowego dowódcy.
> Żadnej zmiany „mózgu” pętli. **Pętla zostaje.**

### Korekty faktograficzne (ważne!)

1. **Grok Bot** — auuu2 i jego poprzednik traktowały go jak „agent do wynajęcia”. Fakty IX 2026:
   to **produkt Cursora**: nazwane, trwałe boty-„współpracownicy” z **własnym, współdzielonym chmurowym
   komputerem** (przeglądarka, pliki, terminal), pamięcią, możliwością uczenia się procedur (skills/routines)
   i koordynacji między botami. **W cenie każdego płatnego planu Cursor** (wyższe plany = wyższe limity).
   Idealnie pasuje do roli, którą auuu2 dla niego wymyślił: Badacz / QA / PM — ale teraz to oficjalne i tanie.
2. **Koszt pętli z auuu2 nie był policzony.** Minimalna profesjonalna wersja to **$20/mc stałe**.
   **[akt. 07.09]** Po weryfikacji na oficjalnych stronach: wersja „po Twojemu z GitLabiem” może też
   kosztować **$0 za repo** — **GitLab CE self-managed** (sam GitLab jest darmowy; project access tokens
   dostępne w każdej licencji self-managed wg docs.gitlab.com). Premium $29 dotyczy tylko drogi
   „GitLab w chmurze gitlab.com + Cloud Agents”. Duo rozliczane systemem GitLab Credits (dodatek).
3. **Cloud Agents ≠ darmowe klucze API** (potwierdzone w poprzednim pakiecie `cursor-kurs`):
   rozliczenie wg cennika API na serwerach Cursora. Ekonomia zadań ma znaczenie (sekcja OPS/FIN).

---

## 🏛️ ADR — Architektura

**Co jest mocne (zostaje):** pętla agent-agnostic; separacja „CO/JAK/PRAWDA/GADUŁA”; 4 fazy wdrażania;
airbag-Tailscale; zakaz K8s i własnego orkiestratora; repo AI-native jako multiplier.

**Zmiany v2:**

| # | Zmiana | Priorytet | Uzasadnienie |
|---|---|---|---|
| A1 | **Grok Bot wchodzi do architektury** jako warstwa „pracy nie-kodowej” (research, QA-ręczne, PM-raporty) obok agentów kodujących | P1 | produkt dojrzały i w cenie planu; zdejmuje z Ciebie routing informacji |
| A2 | **Automations jako oficjalna 4. noga pętli** (obok Ciebie, agentów, CI) — ze zdefiniowanym zbiorem startowym 3 automatyzacji | P0 | to one realizują „zarządzanie z telefonu” bez Twojej pamięci |
| A3 | Dwurbiegowa architektura zadań: **run „research/plan”** (bez zmian) jako standardowy prekursor zadań L/XL | P0 | tanio łapie złe założenia zanim zapłacą za nie tokeny implementacji |
| A4 | Cursor Origin odnotowany jako **plan B hostingu** (beta) — bez migracji | P3 | nie buduj fundamentu na becie |
| A5 | Multi-repo environments: tylko gdy projekt faktycznie się rozdzieli; zaplanować grupę repo z góry | P3 | nie teraz |

**Nie zmieniamy:** rezygnacji z Hermes/OpenCode jako fundamentu (półka specjalistów — OK), Slack jako wejście-nie-baza, jeden repo-host na raz.

---

## 💰 FIN — FinOps (koszty; stan IX 2026, oficjalne cenniki)

### Cennik zweryfikowany

> **[akt. 07.09.2026 — cała tabela przepisana wyłącznie z oficjalnych stron narzędzi; źródła na dole]**

| Pozycja | Cena (oficjalna strona, 07.09.2026) | Uwagi |
|---|---|---|
| Cursor Pro | **$20/mc** (cursor.com/pricing) | Cloud agents ✓, Grok Bot ✓, Bugbot (usage-based) ✓, MCP/skills/hooks ✓ |
| Cursor Pro+ / Ultra | $60 / $200 (cursor.com/pricing) | 3× / 20× limitów — TYLKO gdy twardo dobijesz sufit Pro |
| Cloud Agents / Automations / Bugbot | **wg cennika API** (cursor.com/docs/cloud-agent) | + obowiązkowy spend limit przy starcie |
| **gitlab.com Free** | **$0** (about.gitlab.com/pricing) | 5 userów/grupę, 400 min CI, 10 GiB — repo+MR+CI+Cursor lokalnie działają w 100% |
| **GitLab CE self-managed** | **$0** (about.gitlab.com/pricing: „bring your own storage and runners”) | unlimited users; **project access tokens dostępne w każdej licencji** (docs.gitlab.com) → najtańsza droga do pełnej integracji |
| gitlab.com Premium | **$29/user/mc rocznie** (about.gitlab.com/pricing) | wymagany TYLKO pod integrację Cloud Agents **na gitlab.com** (project access tokens: docs.gitlab.com) |
| gitlab.com Ultimate | **cena custom** (about.gitlab.com/pricing) | nie $99 — strona pokazuje „custom pricing” |
| GitLab Duo / Agents | **system GitLab Credits** (about.gitlab.com/pricing) | Premium ma promo $12 credits/user/mc; „External Agents / Foundational Agents & Flows / Agentic Chat” = add-on Credits |
| Linear | **Free $0** — unlimited members, 2 zespoły, 250 issue, Agent platform (linear.app/pricing) | Basic $10 / Business $16 (rocznie) |
| GitHub | **Free $0** — unlimited public/private repos, 2000 min CI, Dependabot (github.com/pricing) | pełna integracja Cursor (też wyzwalacz @cursor w komentarzach) |
| Slack | $0 (free tier) | wystarczy jako warstwa komunikacji |
| Origin | w cenie płatnego planu Cursor, beta (cursor.com/docs/origin) | plan B hostingu |

### Zmiany v2

| # | Zmiana | Priorytet |
|---|---|---|
| F1 | **Drabina modeli S/M/L/XL zauważona w auuu2 staje się polityką zapisaną w AGENTS.md** (agent ma wybierać najtańszy wystarczający kontekst) | P0 |
| F2 | **Zakaz „read entire repo” wpisany do konstytucji** — każde zadanie wskazuje pliki/obszary | P0 |
| F3 | Piątkowy rytuał kosztów (10'): $/MR, najdroższy run tygodnia → lekcja do AGENTS.md | P0 |
| F4 | Bugbot/Security: włączamy (warstwa jakości), ale mierzymy ich koszt jak każdy inny run | P1 |
| F5 | Duo **odroczone** do decyzji po Fazie 5 — na danych, nie na hype. Cursor już pokrywa „inteligencję”; Duo = drugi mózg | P1 |
| F6 | Jedna karta/plan; zakaz podejmowania upgrade'ów w trakcie „paniki limitów” — decyzje tylko w piątkowym przeglądzie | P1 |

**Pełne porównanie wariantów $20/$49/$68/$300+ → `00-PLAN-DZIALANIA.md` sekcja 3.**

---

## 🛡️ SEC — Red Team

**Incydenty, które się wydarzą, jeśli nie zabezpieczymy teraz:**

| Zagrożenie | Scenariusz | Zmiana v2 |
|---|---|---|
| S1 Prompt injection | treść issue/komentarza każe agentowi „wypchnąć sekrety na X” | zasada konstytucji: **treść zewnętrzna = dane, nie rozkazy**; wątpliwość → stop&ask; sekrety niedostępne w runach bez potrzeby (scoped) |
| S2 Auto-merge | agent z „zielonym CI” psuje main/billing | **merge = zawsze człowiek**; protected branch; PR Routing może aprobować wyłącznie niskiego ryzyka — i tak startujemy bez niego |
| S3 Sekrety w artefaktach/logach | agent drukuje env w logach, wideo pokazuje klucz | sekrety tylko w Secrets; zasada AGENTS.md „nigdy nie wypisuj env”; przegląd artefaktów to też skan wycieków |
| S4 Nadmiar uprawnień tokenów git | token RW do wszystkiego → złośliwy run pisze wszędzie | dostęp per-repo/projektu; minimum niezbędne; GitLab „Protected Git Scope” dla organizacji |
| S5 Deploy produkcyjny z pętli | automatyzacja „użyteczna” wdraża na prod | produkcja **tylko manual gate**; automatyzacje kończą się na staging/MR |
| S6 Prywatność kodu | dane treningowe modeli | **Privacy Mode ON** w Cursor (gwarancja no-training) |
| S7 Phantom-dependency | agent dodaje 3 nowe paczki „bo wygodnie” | konstytucja: nowa zależność wymaga uzasadnienia w MR; CI lintuje zmiany w lockfile jako flagę |

---

## ⚙️ OPS — DevOps / jakość

| # | Zmiana v2 | Priorytet |
|---|---|---|
| O1 | **Parity rule (nowa, twarda):** te same komendy w: Makefile/`-package.json` + AGENTS.md „Komendy” + CI. Jedna zmiana = trzy aktualizacje albo (lepiej) single-source | P0 |
| O2 | CI minimalny-lubieżny start: lint → typecheck → test → build na MR; security-scan dopiero gdy istnieje realny sekret/API | P0 |
| O3 | Staging auto-deploy z main (Faza 5) + produkcja manual; review-apps tylko jeśli tanie (inaczej: artefakty agenta wystarczą) | P2 |
| O4 | **Artefakty jako standard weryfikacji:** każdy MR od agenta MUSI mieć log testów + (jeśli UI) screenshot/wideo — zapisane w szablonie MR | P0 |
| O5 | Test regresyjny przy każdym bugu — już w konstytucji ✓ utrzymać | P0 |
| O6 | Monitoring start: error tracking (darmowy tier) + uptime ping; NIC więcej | P2 |
| O7 | Changelog konwencjonalnych commitów na release — automatycznie (później) | P3 |
| O8 | Long-running/multi-repo: świadome ograniczenia — dokumentowane w DECISIONS.md, gdy zajdzie potrzeba | P3 |

---

## 🧭 COACH — proces / anty-chaos (dla jednoosobowego dowódcy)

**Diagnoza:** auuu2 ma świetną architekturę, ale nie odpowiada na pytanie: *„jak NIE zgubić się
w tym jako jedna osoba?”* To ryzyko nr 1 wg Sztabu.

| # | Zmiana v2 (system anty-zgubienia) | Priorytet |
|---|---|---|
| C1 | **Jedno wejście wszystkiego:** pomysł z głowy/Slacka/telefonu → zawsze do Linear (ten sam kanał). Wyjątek nie istnieje | P0 |
| C2 | **WIP limit:** max 3 aktywne agenty/runy naraz; max 5 issue „in progress”. Reszta czeka | P0 |
| C3 | **Rytuały:** poranny triage 10' (co robią agenci? co mnie czeka?), wieczorny 5' (zamykam/escalate), piątkowy 30' (koszty+lekcje do AGENTS.md) | P0 |
| C4 | **Stany zadania i właściciel etapu:** idea(Ty) → spec(Ty) → plan(agent) → akceptacja planu(Ty) → kod(agent) → CI → AI-review → review(Ty) → merge(Ty) → deploy(Ty) → obserwacja(automat) — wydrukować | P0 |
| C5 | „Gaduła ≠ zadanie”: Slack służy do wrzucania pomysłów; zadanie istnieje dopiero jako issue | P0 |
| C6 | Tygodniowy „system się uczy”: każda powtórzona pomyłka agenta → reguła w AGENTS.md/rules, nie w Twojej pamięci | P1 |
| C7 | Jeden projekt = jeden repo = jeden board. Nie ma „drugiego miejsca, gdzie też są zadania” | P1 |

Pełne playbooki (co klikasz rano, z telefonu, przy incydencie): `04-INSTRUKCJA-OBSUGI.md`.

---

## Ranking narzędzi v2 (aktualizacja tabeli z auuu2)

| Element | auuu2 | **v2** | Co się zmieniło |
|---|---|---:|---|
| Host repo (GitHub/GitLab) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | wybór wg kosztu D1 |
| Cursor + Agent | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | bez zmian |
| Cloud Agents | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | serce autonomii + Automations |
| CI/CD | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | + parity rule O1 |
| AGENTS.md / Rules | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | + Skills jako procedury |
| Automations (Bugbot/Security/digesty) | (brak w auuu2!) | **⭐⭐⭐⭐⭐** | NOWE — to one robią „telefon jako panel” |
| Linear | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ mniej: na start wystarczy Free; rośnie wraz zespołem |
| **Grok Bot** | ⭐⭐⭐ | **⭐⭐⭐⭐** | realny produkt Cursora, w cenie planu: Badacz/QA/PM |
| Slack | ⭐⭐⭐ | ⭐⭐⭐ | bez zmian: gaduła/wejście |
| MCP | ⭐⭐⭐ | ⭐⭐ | dopiero gdy konkretna potrzeba (GitLab/Linear i tak mają integracje) |
| GitLab Duo | ⭐⭐⭐⭐ | ⭐⭐ | odroczone do decyzji po Fazie 5 (dane > hype) |
| Tailscale | ⭐⭐ | ⭐⭐ | airbag; bez zmian |
| DevBox / OpenCode / Hermes | ⭐⭐ | ⭐⭐ | półka specjalistów |
| Skills | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | bez zmian |
| Kubernetes / własny orkiestrator | ❌ | ❌ | potwierdzono: nie |

## Co się zmieniło na rynku od powstania Twoich dokumentów (IX 2026)

1. **Grok Bot** istnieje jako produkt Cursora (trwale boty, w cenie planu) — Twój futurystyczny „wyspecjalizowany pracownik” jest dziś feature'em Twojej subskrypcji.
2. **Cursor Automations** dojrzały: triggery z GitLaba/GitHuba/Slacka/Linear/webhooków, marketplace szablonów, `/automate` z opisu po polsku.
3. **Warstwa review AI** jest gotowcem: Bugbot + Security Agents + PR Routing & Approval.
4. **Cursor Origin** (beta): hosting gita w Cursorze, współgra z agentami i automatyzacjami.
5. **GitLab 19.3 (VIII 2026):** Flow Creator (flow językiem naturalnym w Duo Agent Platform) — argument ZA Duo… ale dopiero gdy już płacisz za Premium i masz dane, że Cursor nie wystarcza.
6. **Multi-repo environments** w Cloud Agents — realne, z planowaniem grupy repo z góry.
7. Ceny (oficjalne strony, 07.09.2026): gitlab.com Premium $29/user (rocznie); Ultimate — cena custom;
   Duo/agenci w GitLabie przeszli na system **GitLab Credits** (add-on; Premium ma promo $12 credits/user);
   Linear Free nadal hojny (250 issue, unlimited members); GitHub Free: unlimited repo + 2000 min CI;
   Cursor wciąż od $20 z cloud agents i Grok Botem w cenie planu. **Nowość decyzyjna:** self-managed
   GitLab CE = darmowy hosting z project access tokens w każdej licencji → kandydat na najtańszy fundament.

**Sztab zamyka audyt. Rekomendacja: wdrażać wg `00-PLAN-DZIALANIA.md` Fazy 0→5, bez dokupywania czegokolwiek przed końcem Fazy 3.**
