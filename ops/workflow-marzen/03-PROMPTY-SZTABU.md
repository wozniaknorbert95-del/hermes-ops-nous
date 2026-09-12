# 📡 PROMPTY SZTABU — protokół komunikacji Sztab ↔ Cursor
### Każda zmiana w systemie idzie promptem (zapisanym tutaj), nie „nastrojową rozmową”.
### Formuła obowiązkowa: ① Cel ② Kontekst ③ Wymagania ④ Ograniczenia ⑤ Kryteria ⑥ Weryfikacja.
### Wklejasz do: agenta lokalnego (A/B/D) albo Cloud Agenta / Automations (C). Miejsca [NAVIASY] uzupełniasz.

---

## A) PROMPTY AUDYTOWE — Sztab bada, Cursor raportuje

### A1. Audyt gotowości repo na AI (raz na start, potem co miesiąc)
```
CEL: Oceń, jak bardzo to repo jest "AI-native".
KONTEKST: Jesteś audytorem. NIE zmieniasz żadnych plików.
SPRAWDŹ: (1) AGENTS.md istnieje i komendy w nim działają — uruchom je i zweryfikuj;
(2) czy README/ARCHITECTURE/PRODUCT/DECISIONS istnieją i nie sprzeczają się kodowi;
(3) czy .cursor/rules nie kłócą się z AGENTS.md; (4) czy CI (`.gitlab-ci.yml`) ma te same
komendy co AGENTS.md (parity rule); (5) czy testy przechodzą z czystego checkoutu.
WYNIK: raport z oceną 0-10 per obszar + listą NAPRAW posortowaną wg wpływu (P0 → P3),
bez żadnych zmian w kodzie.
```

### A2. Audyt zgodności AGENTS.md z rzeczywistością (po każdej większej zmianie stacku)
```
CEL: Wykryj rozjazd między instrukcjami dla agentów a stanem faktycznym.
KONTEKST: NIE zmieniasz plików. Porównaj AGENTS.md + .cursor/rules z faktycznym repo.
WERYFIKUJ: komendy (odpal każdą), ścieżki, nazwy katalogów, wersje narzędzi, konwencje gałęzi.
WYNIK: tabela [hejtun: co w AGENTS.md | co w rzeczywistości | propozycja poprawki].
Nie nanosisz poprawek — czekasz na moją akceptację.
```

### A3. Audyt kosztów (piątek — rytuał; część robisz ręcznie)
Ty: dashboard Cursor → usage/costs → notujesz: $/MR tygodnia, 3 najdroższe runy, model/kontekst.
Potem prompt do agenta:
```
CEL: Zaproponuj redukcję kosztów bez utraty jakości.
KONTEKST: moje 3 najdroższe runy tygodnia: [WYKLEJ: zadanie, model, tokeny/$].
ZADANIA: (1) które z nich powinny pójść na tańszym modelu/mniejszym kontekście;
(2) którym brakowało kontekstu w AGENTS.md (ile iteracji by zaoszczędzić);
(3) zaproponuj DOKŁADNIE 2 dopiski do AGENTS.md/rules, które obniżą koszt następnych runów.
Nie zmieniaj plików — czekam na zatwierdzenie.
```

### A4. Audyt bezpieczeństwa (raz w miesiącu)
```
CEL: Znajdź realne ryzyka bezpieczeństwa, zero teoretyzowania.
KONTEKST: Read-only. Sprawdź: (1) sekrety w kodzie i HISTORII gita (gitleaks-style);
(2) zależności bez uzasadnienia/z podatnościami; (3) endpointy bez autoryzacji vs wzorzec projektu;
(4) miejsca, gdzie treść z zewnątrz (input issue/komenty) mogłaby sterować agentem;
(5) uprawnienia nadpisywane "na szeroko".
WYNIK: lista [ryzyko | plik:miejsce | dotkliwość | fix], max 10 pozycji, od najgroźniejszych.
```

## B) PROMPTY BUDUJĄCE — Sztab projektuje, Cursor wykonuje

### B1. Wygeneruj ARCHITECTURE.md (jednorazowo, potem aktualizuj co iterację)
```
CEL: Stwórz ARCHITECTURE.md (max 1 strona + diagram ASCII) dla przyszłych agentów.
KONTEKST: przeanalizuj repo. Zasady z AGENTS.md stosuje się w pełni.
WYMAGANIA: warstwy systemu, mapowanie katalogów → odpowiedzialności, przepływ kluczowych danych,
3 ważne decyzje architektoniczne (dlaczego tak, nie inaczej — sprawdź DECISIONS.md i historię).
OGRANICZENIA: nie zmieniasz kodu; nie wymyślaj faktów — co niejasne oznacz [DO DECYZJI].
WERYFIKACJA: nowy agent, czytając TYLKO ten plik, potrafi wskazać, gdzie dodać [PRZYKŁADOWY FEATURE].
```

### B2. Nowy Skill (gdy trzeci raz robisz coś tak samo)
```
CEL: Utwórz skill [.cursor/skills/NAZWA/] opisujący procedurę: [np. "dodawanie-endpointu"].
KONTEKST: ostatnie 2-3 realizacje tego typu: [MR #:]. Wyciągnij wspólny mianownik.
WYMAGANIA: kroki, checklist kontroli jakości, typowe błędy, odwołania do wzorcowych plików w repo.
OGRANICZENIA: max 1 ekran tekstu; imperatyw; zero literatury.
WERYFIKACJA: opisz, jak agent użyje tego skillu przy hipotetycznym zadaniu [PRZYKŁAD].
```

### B3. Naprawa parity CI ↔ lokal ↔ AGENTS.md (gdy coś się rozjedzie)
```
CEL: Przywróć jedno źródło prawdy dla komend.
KONTEKST: rozjazd: [np. CI woła X, package.json nazywa to Y, AGENTS.md mówi Z].
WYMAGANIA: single-source (package.json/Makefile jako źródło), CI + AGENTS.md odwołują się do niego.
OGRANICZENIA: nie zmieniaj zachowania pipeline; nie dodawaj narzędzi.
WERYFIKACJA: odpal lokalnie każdą komendę; nowy MR pokazuje CI zielone z tymi samymi komendami.
```

## C) AUTOMATYZACJE GOTOWE (wklejasz w cursor.com/automations; trigger + prompt)

### C1. Daily digest — trigger: harmonogram, codziennie 7:30; bez repo lub z repo
```
Podsumuj ostatnie 24h w projekcie: (1) MR-e otwarte/zmergowane (tytuły + autor: człowiek/agent),
(2) status ostatniego pipeline na main, (3) nowe issue, (4) co czeka na MOJĄ decyzję.
Format: 6 linii max, emoji statusu. Wyślij na Slack #[kanał]. Nic nie zmieniaj w kodzie.
```

### C2. Weekly security sweep — trigger: poniedziałek 8:00; repo: [repo]
```
Przejrzyj zmiany z ostatnich 7 dni pod kątem podatności (sekrety, auth, walidacja wejścia,
zależności). Wynik: issue zatytułowane "Security sweep [data]" z listą wyników (lub "czysto").
Nie kodujesz poprawek — tylko raportujesz.
```

### C3. Issue → plan — trigger: event GitLab (nowe issue) lub Linear; repo: [repo]
```
Przeczytaj issue #[zdarzenie]. Nie zmieniaj kodu. Sprawdź zgodność z AGENTS.md i ARCHITECTURE.md.
W komentarzu do issue zostaw: (1) zrozumienie celu (2 zdania), (2) plan implementacji: kroki ≤1 dzień,
(3) pliki, których dotknie, (4) ryzyka/pytania do mnie, (5) oszacowany rozmiar S/M/L i sugerowany
model. Czekasz na moje "wykonaj".
```

### C4. Piątkowy raport (po Twoim wklejeniu usage) — patrz A3

## D) INCYDENTY — Sztab podejmuje, Cursor stabilizuje

### D1. Rollback złośliwego/zepsutego MR
```
CEL: Cofnij MR #[nr] z main minimalnym ryzykiem.
KONTEKST: powód: [co się zepsuło, objaw]. 
WYMAGANIA: gałąź revert/xxxx, `git revert` merge-commitu, pełny zestaw testów, MR „Revert: [tytuł]".
OGRANICZENIA: nie "poprawiaj po drodze"; DB: migracja wsteczna tylko jeśli bezpieczna — inaczej STOP.
WERYFIKACJA: CI ✅ na branchu revert + opis: co wraca, co świadomie zostaje.
```

### D2. Protokół hotfix produkcyjny
```
CEL: Hotfix [OBJAW] na produkcji.
KONTEKST: incydent: [opis + log/screenshot]. Branch: hotfix/[nazwa].
WYMAGANIA: minimalna zmiana izolująca przyczynę + test regresyjny (bez testu nie wchodzi).
OGRANICZENIA: zakaz refaktorów; zakaz nowych zależności; dokładnie ten jeden problem.
WERYFIKACJA: CI ✅ + kroki reprodukcji, które po fixie ZNIKAJĄ. Ja merdżuję i deployuję osobiście.
```

### D3. „Agent się zgubił” — protokół ratunkowy (ręczny, w 5 krokach)
1. Zatrzymaj run. Nie dopisuj „spróbuj jeszcze raz” w kółko (płacisz za błądzenie).
2. Oceń szkody na branchu (`git diff` — ilu plików? złych zmian?). Szkody duże → porzuć branch (`git reset`/nowy branch z main).
3. Zamień zadanie na DWA: „research/plan, bez zmian” → po akceptacji: implementacja z planu.
4. Dopisz do zadania brakujący kontekst (3 ostatnie pytania agenta → odpowiedzi W TREŚCI/issue).
5. Po naprawie: lekcja → nowa zasada w AGENTS.md/rules (zamyka pętlę: błąd nigdy nie wraca).

---
> Zasada żelazna: prompt poprawiasz W TYM PLIKU, potem używasz. Wersjonujesz go razem z repo (docs/).
> Prompt „w głowie” nie istnieje — system rośnie tylko przez zapisane procedury.
