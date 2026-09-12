# PROMPTY-DLA-AGENTOW.md — gotowe wzory zadań
### Kopiuj-wklej → zamień [NAWIASY]. Formuła: Cel → Kontekst → Wymagania → Ograniczenia → Kryteria → Weryfikacja.

---

## ❌ vs ✅ — najpierw zobacz różnicę

**ŹLE:**
> „popraw formularz rejestracji”
(agent zgadnie źle: który formularz? co poprawić? po co?)

**DOBRZE:**
> „W `src/components/SignupForm.tsx` walidacja e-mail akceptuje adresy bez domeny.
> Napraw walidację (standard RFC, bez regexów-skrzynia-narzędziowa), dodaj czytelny komunikat
> błędu pod polem (i18n: klucz `auth.invalidEmail`). Dodaj testy: poprawny adres, brak @,
> brak domeny, pusty string. Nie ruszaj pozostałych pól formularza ani API. Kryterium:
> testy ✅ + screenshot formularza z widocznym komunikatem błędu.”

---

## 1️⃣ Zadanie: nowa funkcja (feature)

```
CEL: [co użytkownik zyska — 1 zdanie]
ISSUE: [link / numer]
KONTEKST: funkcja dotyczy [moduł/plik]. Powiązane: [pliki, docs].
WYMAGANIA:
- [punkt 1 — konkretny, wykonywalny]
- [punkt 2]
OGRANICZENIA:
- nie zmieniaj: [pliki/API/kontrakty]
- zachowaj konwencje z AGENTS.md; bez nowych zależności
KRYTERIA AKCEPTACJI:
- [ ] gdy [warunek] → [rezultat]
- [ ] testy: [które]
WERYFIKACJA: [komenda testu / ścieżka UI + prośba o screenshot]
ZAKOŃCZENIE: nowa gałąź → MR z szablonem; linkuj issue (Closes #[nr]).
```

## 2️⃣ Zadanie: naprawa buga

```
OBJAW: [co się dzieje, np. "500 przy pustym polu X"]
KROKI REPRODUKCJI: 1) ... 2) ... 3) ...
OCZEKIWANE: [co ma się dziać]
HIPOTEZA (opcjonalnie): podejrzewam [plik/obszar] — zweryfikuj, nie zakładaj.
WYMAGANE: poprawka + TEST REGRESYJNY, który bez poprawki pada.
OGRANICZENIA: nie zmieniaj [obszary]; nie maskuj błędu pustym catchem.
WERYFIKACJA: [komenda testu]; dołącz log dowodzący naprawy.
```

## 3️⃣ Zadanie: research / plan (BEZ zmian w kodzie) — do zadań L

```
ZADANIE: przeanalizuj, NIC nie zmieniaj w kodzie.
PYTANIE: [np. "jak najlepiej dodać multi-tenancy do warstwy X?"]
PRZEJRZYJ: [pliki/moduły]; uwzględnij ARCHITECTURE.md i DECISIONS.md.
WYNIK (jako podsumowanie runu):
1) 2–3 opcje rozwiązania: +/−, ryzyka, koszt pracy,
2) rekomendacja + uzasadnienie,
3) rozbicie na kroki ≤1 dzień każdy (kandydaci na osobne issue),
4) pytania otwarte do mnie.
NIE otwieraj MR — to tylko analiza.
```

## 4️⃣ Zadanie: refaktor

```
CEL: [np. "ułatwić testowanie modułu Y"].
ZAKRES: tylko [pliki/katalog].
TWARDA ZASADA: zachowanie ZEWNĘTRZNE bez zmian — wszystkie istniejące
testy muszą przechodzić bez ich modyfikacji.
POMYSŁ (opcjonalnie): [co masz na myśli] — jeśli odkryjesz lepiej: zaproponuj, nie rób.
KRYTERIUM: testy ✅, zero zmian w plikach spoza zakresu, diff czytelny w review.
```

## 5️⃣ Zadanie: testy do istniejącego kodu

```
OBSZAR: [pliki/funkcje].
Napisz testy pokrywające: ścieżka szczęśliwa, przypadki brzegowe: [lista], błędy: [lista].
NIE ZMIENIAJ implementacji — jeśli znajdziesz bug, opisz go w podsumowaniu runu.
Mocki: zgodnie ze wzorcem z [plik-wzór]; nie mockuj [czego].
KRYTERIUM: `pnpm test` ✅; nowe testy faktycznie wykonują się (nie skippowane).
```

## 6️⃣ Zadanie: review istniejącego MR (druga para oczu)

```
Przejrzyj gałąź [nazwa] / MR [nr] pod kątem: bezpieczeństwo, [np. multi-tenancy],
zgodność z AGENTS.md, przypadki brzegowe, jakość testów.
WYNIK: lista uwag (blokujące / nieblokujące) z wskazaniem plik:linia + propozycje poprawek.
Nic nie zmieniaj w kodzie.
```

---

## 📌 Zasady promptowania pro

1. Jedno zadanie = jeden run = jeden MR. Rozmiar S/M; L → research/plan najpierw.
2. Zawsze podawaj „jak zweryfikować” (komenda / ścieżka UI / screenshot) — agent bez weryfikacji
   kończy „na 80%”.
3. „Nie ruszaj X” jest równie ważne jak „zrób Y”.
4. Linkuj issue zamiast powielać wiedzę (pamięć organizacji!).
5. Po każdym runie: jeśli agent coś źle zrozumiał → dopisz zasadę do AGENTS.md/rules,
   a nie tylko popraw prompt następnym razem.
6. Follow-up w TYM SAMYM runie kontynuuje gałąź — nie odpalaj nowego agenta do poprawek.
