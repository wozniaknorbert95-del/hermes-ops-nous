# Tool mastery — Akademia (NARZĘDZIA)

**SoT:** [`PLAN-AKADEMIA-START-2026-09-26.md`](PLAN-AKADEMIA-START-2026-09-26.md) · spec v7.  
**UI:** zakładka NARZĘDZIA w `DASHBOARD.html`. Ten plik = treść kart po GO na UI. Live karty (`TOOL_DATA`) zostają do tego GO.  
**Zasada:** pełna karta = codzienny warsztat. PARKED = „nie startuj”, nie wiki. Blog dostawcy ≠ dowód (wyjątek: jawny autor branżowy). Max 3 linki producenta na kartę.

Lekcja Hermesa Ops (30 s, 6 pól, Pause/Stop/Take over, Approval ≠ Merge) żyje **tylko** na karcie Hermes Engineer.

---

## Szablon pełnej karty

1. **Po co tutaj** — 1 zdanie w tym ekosystemie.
2. **Kiedy tak / kiedy nie.**
3. **Producent** — max 3 oficjalne URL.
4. **Praktyka** — 1–2 nazwane źródła ludzi, którzy tym pracują.
5. **Gotcha** — jedna, której nie wolno pominąć w sesji.
6. **Dowód „umiem”** — zrobione, nie „przeczytałem”.
7. **Status** — AKTYWNY / PARTIAL / PARKED / FUTURE.

---

## Fala 1 — codzienny warsztat (pełne)

### Linear CO

- **Status:** AKTYWNY. Dowód: `workflow-lab/docs/LINEAR.md`, DOD W-03.
- **Po co tutaj:** jedyne wejście zadania. Issue z 6 polami = kolejka. Czat nie jest zadaniem.
- **Kiedy tak:** każdy pomysł, rano In Review / blocked, etykieta mówi czyja piłka. **Kiedy nie:** drugi workspace, sprawa bez issue, board dsaas jako „gaduła”.
- **Producent:** [Linear Docs](https://linear.app/docs) · [API](https://developers.linear.app/docs) · [Method](https://linear.app/method).
- **Praktyka:** szablon 6 pól w `LINEAR.md` (lab). Platforma: [`LINEAR-PLATFORM.md`](LINEAR-PLATFORM.md) — 8 widoków Wave 2, to mapa DSAAS, nie karta poranka.
- **Gotcha:** brak issue = nie startujesz. WIP: max 3 runy agenta, max 5 In progress. Slug workspace = `quietforge`.
- **Umiem:** otwieram issue z 6 polami i etykietą `agent` w 30 s (telefon albo laptop).

### Cursor local

- **Status:** AKTYWNY. Dowód: `workflow-lab/docs/DOD-WORKFLOW.md`.
- **Po co tutaj:** laptop loop — branch, agent, lint/test/build, PR, auto-merge po zielonym CI.
- **Kiedy tak:** jesteś przy laptopie; S/M; auth/billing/migracja tylko małymi krokami. **Kiedy nie:** kod na main, „szybka poprawka” z telefonu jako IDE, PR z czerwonym CI i nadzieja na ręczny merge.
- **Producent:** [Cursor Docs](https://docs.cursor.com) · [Rules](https://docs.cursor.com/context/rules) · [Agent](https://docs.cursor.com/chat/agent).
- **Praktyka:** Conventional Commits + `CONTRIBUTING.md` labu. Jedna myśl = jeden MR; >400 linii = podział.
- **Gotcha:** agent nie decyduje o merge, deploy, sekretach, architekturze. Czerwone CI naprawia agent na branchu, nie admin-override.
- **Umiem:** `feat/…` → trzy bramki npm → PR `Closes #…` → nie czekam na zielone, biorę następne.

### Cursor Cloud Agents

- **Status:** AKTYWNY (lab + pack platformy). Dowód: `W2-CLOUD-AGENTS.md`, QUI-92, D-NO-DSAAS-FALLBACK.
- **Po co tutaj:** jedyny executor kodu w Telefon loopie. Klony **repo GitHub issue**, nie pole Linear `repo`.
- **Kiedy tak:** S/M z telefonu po `/ops` Start. **Kiedy nie:** deploy, SSH, sekrety, `workflow_dispatch`; `LANE=UNKNOWN` albo STOP.
- **Producent:** [Cloud Agents](https://docs.cursor.com/background-agent) · [Bugbot](https://docs.cursor.com/en/integrations/bugbot) · [Dashboard](https://docs.cursor.com).
- **Praktyka:** platforma = `.cursor/README.md` + `python scripts/session-preflight.py`. Lab = npm. UNKNOWN ≠ PASS.
- **Gotcha:** 403 na `dsaas-platform-main` = REFUSED, nie „otwórz issue w labie”. PAT musi mieć Issues write na platformie. OAuth Integrations ≠ GitHub App — diagnozuj osobno.
- **Umiem:** issue `agent` + 6 pól w **tym** repo co kod; Start z `/ops`; PR READY FOR REVIEW (nie draft).

### Hermes Engineer

- **Status:** PARTIAL / SETUP aż e2e.json. Dowód: ten plik + [`HERMES-OPS-HOWTO.md`](HERMES-OPS-HOWTO.md) + [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md).
- **Po co tutaj:** Control Plane `/ops`. Autopilot bierze kolejkę. Ty: Start / Run next / Pause / Stop / Take over. Kod nadal robi Cloud Agent.
- **Kiedy tak:** ruszyć Linear z telefonu; widzieć S1–S6. **Kiedy nie:** merge z telefonu; deploy z `/ops`; Run next przy UNKNOWN; mylić z czatem Akademii.
- **Producent:** brak trzeciego vendora — SoT to ten repo: HOWTO, kontrakt ról, `/ops`.
- **Praktyka:** Approval ≠ Merge. Pause nie ożywia ticka. Brak `ops-cmd.json` po ACK = idle.
- **Gotcha:** 30 sekund: (1) Linear `agent` + 6 pól (2) otwórz `/ops` (3) Start (4) nie merguj (5) deploy lokalnie. Take over = Pause + laptop, zero `@cursor`.
- **Umiem:** z telefonu odpalam jedno issue i wiem, czy pill jest PASS, FAIL czy UNKNOWN.

### GitHub

- **Status:** AKTYWNY. Dowód: `workflow-lab/DECISIONS.md` D-W0-ORIGIN, branch protection.
- **Po co tutaj:** origin kodu labu i platformy. Merge tylko przez PR. Issues = ziarno Cloud Agenta **w tym samym repo**.
- **Kiedy tak:** zawsze jako SoT kodu. **Kiedy nie:** push do main; dual-origin; kod platformy w labie i odwrotnie „bo 403”.
- **Producent:** [GitHub Docs](https://docs.github.com) · [Protecting branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches) · [Pull requests](https://docs.github.com/en/pull-requests).
- **Praktyka:** Conventional Commits. Lab publiczny = zero danych tenanta.
- **Gotcha:** GitHub App ≠ Integrations OAuth. Cloud może kodować przez App i nie otworzyć PR przy martwym OAuth.
- **Umiem:** `git remote -v` pokazuje jeden origin; PR z wymaganymi checkami; zero admin-override.

### CI

- **Status:** AKTYWNY. Lab: validate + execute. Platforma: policy-gates, security, gitleaks, db-rls.
- **Po co tutaj:** bramka merge. Przeczucie nie merguje.
- **Kiedy tak:** każdy PR i push do main. **Kiedy nie:** komenda spoza AGENTS.md §2; filtr ścieżek w triggerze (brakujący check); admin-override.
- **Producent:** [GitHub Actions](https://docs.github.com/actions) · [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) · [Required checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging).
- **Praktyka:** CI parity: AGENTS.md §2 = package.json / komendy platformy = yaml. Docs-only PR ma być zielony.
- **Gotcha:** UNKNOWN nigdy nie jest zielone. Notebook execute jest opt-in (path w kroku, nie w triggerze).
- **Umiem:** lokalnie te same komendy co CI; umiem wskazać required check na PR platformy i labu.

### Gitleaks

- **Status:** AKTYWNY. Dowód: `gitleaks.yml` platformy + lab.
- **Po co tutaj:** zero sekretów w repo, logach, eksporcie Akademii.
- **Kiedy tak:** CI; każdy plik, który „wygląda jak token”. **Kiedy nie:** commit `.env`; token w komentarzu PR; wyłączenie skanu „na chwilę”.
- **Producent:** [gitleaks](https://github.com/gitleaks/gitleaks) · [Config](https://github.com/gitleaks/gitleaks#configuration) · [Gitleaks GitHub Action](https://github.com/gitleaks/gitleaks-action).
- **Praktyka:** riposta „wystawi klucze” = case + `gitleaks detect` na dsaas (dział C). `.env.example` = nazwy bez wartości.
- **Gotcha:** usunięcie z pliku nie czyści historii. Unieważnij klucz u dostawcy.
- **Umiem:** `gitleaks detect` na platformie = 0 trafień **albo** umiem powiedzieć, czemu czerwone i co unieważniłem.

---

## Fala 2 — krócej (AKTYWNY, ale nie codzienny fold)

### Jupyter Notebook (lab)

- **Status:** AKTYWNY W LABIE / OPT-IN.
- **Po co:** dowód liczbowy (koszt, CI), nie opinia. Zero wpływu na Node core.
- **Producent:** [Jupyter](https://docs.jupyter.org/) · [nbstripout](https://github.com/kynan/nbstripout).
- **Gotcha:** outputs i sekrety w komórkach nie idą do gita. Mieszanie `greet` z notebookiem = regresja warstw.
- **Nie startuj w sesji platformy** chyba że DoD A7.

### Bugbot

- **Status:** PARTIAL (`bugBotEnabled:true` ≠ komentarze).
- **Producent:** [Bugbot](https://docs.cursor.com/en/integrations/bugbot).
- **Gotcha:** pokrycie 0% = nigdy nie ruszy. Nie jest bramką merge. Billing = decyzja Dowódcy.
- **Nie startuj** jako „review zastępuje mnie”.

### Automations (digest / sweep / issue-agent)

- **Status:** AKTYWNE W LABIE. Dowód: `W4-AUTOMATIONS.md`.
- **Producent:** [Actions](https://docs.github.com/actions).
- **Gotcha:** Cursor Automation ≠ pewny pisarz. SoT digestu = workflow. Sweep max 1 issue / tydzień ISO.
- **Nie dodawaj** digestu platformy „przy okazji” — osobna fala.

### Grok BADACZ

- **Status:** AKTYWNY. Dowód: `docs/grok-bots/BADACZ.md`.
- **Producent:** [xAI](https://docs.x.ai/).
- **Gotcha:** nie pisze kodu. „Jak to zaimplementować” = Cloud Agent. Blog dostawcy ≠ fakt.

---

## PARKED / FUTURE — nie startuj

| Narzędzie | Status | Warunek odblokowania | Jedna linia |
| --- | --- | --- | --- |
| Grok PM | PARKED | Gdy wskażesz, co doda ponad daily digest | Duplikuje digest — zostaw wyłączone |
| Tailscale | AIRBAG | Awaria VPS / origin | Nie jest pętlą; dual-origin zakazany |
| OpenCode | OPCJONALNE | Eksperyment CLI | Te same bramki repo; nie SoT |
| Hermes / Agent OS | OPCJONALNE | HITL na :8080/:3000 | Nie deployuje; nie zastępuje Linear |
| GitLab CE | FUTURE / HUMAN-STOP | Checklist W0 + GO Dowódcy | Nie teraz; pierwszy 502 jest normalny |

Producent (gdy odblokujesz, nie wcześniej): [Tailscale KB](https://tailscale.com/kb) · [OpenCode](https://opencode.ai/docs) · [GitLab Docs](https://docs.gitlab.com).

---

## Guard UI (po GO, nie teraz)

Karty NARZĘDZIA renderują pola z tego pliku. Zakaz ściany 16 encyklopedii above-fold: fala 1 otwarta, fala 2 i PARKED w `<details>` albo drugi rząd. `id="ops-howto"` zostaje na karcie Engineer (mutacja M9), nie na TERAZ.
