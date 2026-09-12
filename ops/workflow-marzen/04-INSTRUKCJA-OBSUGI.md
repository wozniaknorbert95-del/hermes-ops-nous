# 🧭 04 — INSTRUKCJA OBSŁUGI DOWÓDCY („książka lotnicza”)
### Jak pracować codziennie, by się nie gubić — lokalnie, zdalnie i z telefonu.
### Stack roboczy (decyzje 07.09.2026): GitLab CE (Twój VPS) + Cursor Pro + Linear Free + Slack + Grok Bot.

---

## 1. Trzy zasady ponad wszystko

1. **Jedno wejście:** pomysł → zawsze do Linear (z telefonu 30 sekund). Wyjątek nie istnieje.
2. **Właściciel etapu jest jeden i znany:** patrz „wektor zadania” (sekcja 3). Jeśli nie wiesz, czyja
   jest piłka — patrz na wektor, nie szukaj po czatach.
3. **WIP limit:** max 3 aktywne runy agentów, max 5 issue „In progress”. Przekroczenie = najpierw domykasz.

---

## 2. Rytuały (dokładnie tak prosto, dokładnie codziennie)

### 🌅 Rano — 10 minut (telefon wystarczy)
- [ ] Daily digest (automat, 7:30) — przeczytany
- [ ] Linear: board — co „In review”? (to Twoje jedyne obowiązkowe kliknięcia dziś)
- [ ] Runy agentów: kto skończył / kto czeka na odpowiedź / kto powinien zostać zabity (D3)
- [ ] Wybierz 1–3 priority na dziś → etykiety w Linear

### 🌆 Wieczór — 5 minut
- [ ] każdy MR: approve/merge **albo** komentarz „co poprawić” **albo** zamknięty (D3) — nic nie wisi
- [ ] Linear zaktualizowany o fakty (nie o nadzieje)
- [ ] jutro: 1 zdanie „co pierwsze” w notatce pod ręką

### 🗓️ Piątek — 30 minut (TYLKO ten blok dotyczy pieniędzy i systemu)
- [ ] koszty: $/MR, 3 najdroższe runy → prompt A3 z `03-PROMPTY-SZTABU.md`
- [ ] uwagi Bugbota/inne powtórzone błędy → zasada do AGENTS.md (prompt A2 co potrzeba)
- [ ] Linear: sprzątanie backlogu (starsze niż 30 dni bez ruchu → archiwum albo etykieta)
- [ ] decyzje o upgrade'ach planów — **tylko teraz**, nigdy w „panice limitów”
- [ ] raz w miesiącu: rytuał opieki nad VPS/GitLab CE (sekcja 8 w `05-...`)

---

## 3. Wektor zadania — kto prowadzi piłkę (naucz na pamięć)

```
IDEA(Ty) → SPEC w Linear(Ty) → PLAN(agent: A1/C3) → AKCEPTACJA PLANU(TY!)
→ KOD(agent) → TESTY+CI(automat) → AI-REVIEW(Bugbot/Security)
→ REVIEW(TY) → MERGE(TY) → STAGING(automat) → DEPLOY PROD(TY — bramka)
→ OBSERWACJA(automat/monitoring) → FEEDBACK → IDEA
```
Jeśli pytasz „co teraz?” → znajdź zadanie na wektorze: krok po prawej stronie = następny właściciel.

---

## 4. Drzewo decyzyjne: czym to zrobić?

| Sytuacja | Narzędzie | Dlaczego |
|---|---|---|
| S: typo/test/copy/mały fix, jestem przy laptopie | Agent lokalny | natychmiast, zero kosztu VM |
| S/M: chcę od komputera uciec / po godzinach | **Cloud Agent** | agent ma PC zamiast Ciebie |
| M z telefonu (pomysł→realizacja) | Linear issue → C3 (plan) → „wykonaj” | pełna pętla w panelu |
| L/XL | najpierw run „research/plan” (bez zmian) → akceptujesz → implementacja | tanie łapanie złych założeń |
| research nie-kodowy (konkurencja, opcje, raport) | **Grok Bot BADACZ** | nie pali limitów kodowych |
| „co mnie dzisiaj boli w projekcie?” | Grok Bot PM + digest | status bez klikania |
| cykliczność (digest, sweep, raport) | Automations | nie możesz zapomnieć |
| awaria GitLaba/VPS, coś „u mnie na kompie” | **Tailscale → domowy PC/VPS** | airbag, potem wracasz do pętli |
| sprawa delikatna (auth/billing/DB migracja) | Ty + agent lokalny | pełny nadzór, małe kroki |

---

## 5. Playbooki (najczęstsze scenariusze krok po kroku)

### ▶️ PLAYBOOK A: Nowy feature z laptopa
1. Linear: issue z szablonu (Cel/Kryteria/Ograniczenia). Bez tego nie startujesz.
2. Cursor lokalny: [jeśli M+] A1/C3 „plan, bez zmian” → akceptujesz/poprawiasz plan.
3. „Wykonaj plan na branchu `feat/xxx`” → agent koduje; Ty nie gapisz się — robisz inne zadanie.
4. MR otwarty → CI ✅ → Bugbot ✅ → **Twoje review: diff + artefakty** → Merge.
5. Linear: Done. Staging (gdy skonfigurowany) → Ty: deploy prod = ręczna bramka.

### ▶️ PLAYBOOK B: Pełna pętla z telefonu (bez laptopa)
1. Pomysł → Linear issue (apka/PWA; 2–3 zdania + kryteria).
2. Etykieta `agent` → automat C3 dopisuje plan w komentarzu (powiadomienie).
3. Przeglądasz plan na telefonie → odpowiadasz „wykonaj, bez X”.
4. Cloud Agent pracuje → kończy MR z artefaktami (wideo/screenshot).
5. Oglądasz artefakt + diff na telefonie, CI ✅ → **Merge**. Deploy: Twoje kliknięcie (bramka).
6. ewentualne poprawki: follow-up w runie („dodaj test pustego pola”) — nie nowy run.

### ▶️ PLAYBOOK C: Bug z produkcji
1. Linear: issue `Sev: high` z objawem + logiem/screenshotem.
2. Prompt D2 (hotfix) do agenta lokalnego (pilna sprawa = najkrótsza droga).
3. CI ✅ → review → **Ty mergujesz i deployujesz osobiście**.
4. Po incydencie: 5-minutowy wpis w DECISIONS.md („przyczyna + co zapobiegnie”).

### ▶️ PLAYBOOK D: Review MR za 5 minut (szablon mentalny)
- [ ] diff tylko w plikach z zakresu issue?
- [ ] testy dodane/zmienione sensownie (nie „naprawione” osłabieniem)?
- [ ] brak sekretów/logów debugowych/lockfile-olśnienia bez powodu?
- [ ] CI ✅ + Bugbot bez uwag blokujących + artefakt wygląda dobrze?
- Coś śmierdzi → komentarz → follow-up agenta. 3 rundy bez poprawy → D3 (salvage).

### ▶️ PLAYBOOK E: „Zgubiłem się” (reset w 60 sekund)
1. Otwórz Linear board → to jedyna prawda o stanie świata.
2. Wektor (sekcja 3): każde „In progress” → czyja piłka? U agenta = cierpliwość; u Ciebie = zrób TERAZ.
3. Ponad 3 runy? Zabij najsłabsze (D3). Ponad 5 issue in-progress? Cofnij nadmiar do backlogu.
4. Jutro zacznij rytuał poranny jak zwykle. System nie wymaga spisywania niczego „od nowa”.

### ▶️ PLAYBOOK F: GitLab CE / VPS pada (awaria fundamentu)
1. Lokalny `git remote -v` — masz przecież lokalne klony (prawda zawsze w ≥2 miejscach).
2. Wejdź przez Tailscale na VPS → `docker ps`, `docker logs gitlab` → sekcja 9 w `05-...`.
3. Krytyczna praca musi iść dziś dalej? Tymczasowo: drugi remote (github/gitlab.com darmowy) push
   tylko najnowszego main → pracujesz → po powrocie synchronizujesz z powrotem jako JEDEN MR.
4. Incydent zamykasz wpisem w DECISIONS.md (przyczyna, czas, lekcja: dysk? RAM? update?).

---

## 6. Nazwy i etykiety (żeby nie szukać)

- Gałęzie: `feat/`, `fix/`, `chore/`, `hotfix/`, `revert/` + krótko po angielsku.
- Etykiety Linear: `agent` (gotowe dla agenta — szablon wypełniony), `review` (czeka na Ciebie),
  `blocked` (czeka na kogoś/coś), `Sev: high` (produkcja).
- MR: tytuł jak commit (`feat: …`), link do issue obowiązkowy. Szablon MR: checklist DoD.

---

## 7. Dziesięć przykazań anty-chaos

1. Gaduła ≠ zadanie: nic nie jest zadaniem, dopóki nie ma issue w Linear.
2. Jeden projekt = jedno repo = jeden board. Nie istnieją „drugie miejsca”.
3. Agenty nie decydują o: merge, deploy prod, sekretach, architekturze. Kropka (4 bramki).
4. Zadanie L/XL bez runu planistycznego = zakaz startu.
5. Nigdy nie płacisz za ten sam błąd dwa razy: błąd → zasada w AGENTS.md.
6. Nie kupujesz/nie instalujesz niczego poza piątkowym przeglądem.
7. Slack to wejście pomysłów i wyjście raportów. Nic więcej.
8. Telefon = panel dowodzenia, nie mini-IDE. Kodu z telefonu nie „doklepujesz na szybko”.
9. Spend limit jest święty. Dobity → STOP i decyzja w piątek, nie podbijanie ad hoc.
10. Raz w tygodniu system się uczy (zasady), a Ty odpoczywasz (conajmniej 1 dzień bez runów).

> 📌 Ten plik drukujesz albo trzymasz przypięty. Gdy coś tu nie działa — nie wyrzucasz systemu,
> tylko poprawiasz plik (i powiadasz Sztabowi, co poprawić w pozostałych dokumentach).
