# Handoff — Akademia: sync z vaultem, dwa defekty z weryfikacji (2026-09-20)

**Cel sesji:** deploy napraw z audytu UX/UI + weryfikacja, czy Hermes i backup realnie działają.

**Gałęzie/PR-y:** [#18](https://github.com/wozniaknorbert95-del/akademia/pull/18) `fix/tab-state-heal` ·
[#19](https://github.com/wozniaknorbert95-del/akademia/pull/19) `fix/sync-za-basic-auth`

**STATUS: WDROŻONE NA PRODUKCJĘ.** `origin/main` = `9d0e2b9`, VPS ma dokładnie ten kod.

---

## 1. Najważniejsze: postęp NIGDY nie dotarł do vaulta

Zmierzone w logach nginx, **cała historia** (łącznie z archiwami `.gz`):

```
PUT /progress            ->  0 wystąpień
/progress, User-Agent    ->  curl 35x, PowerShell 1x, PRZEGLĄDARKA 0x
```

Telefon **ani razu** nie wysłał postępu. Kurs żył wyłącznie w `localStorage`.

**Przyczyna:** `pullProgress()` robiło `if(!syncCreds())return;`, a `syncCreds()` czyta
`sessionStorage` — bez **ręcznego** wpisania hasła synchronizacja wyłączała się **cicho**,
zanim cokolwiek wysłała. `pushProgress()` miało tę samą blokadę.

**A etykieta obiecywała coś innego:** „hasło Basic Auth **(raz na urządzenie)**" vs
`sessionStorage` = **raz na sesję**. Ustawiasz raz, wierzysz, że działa — a od następnego
otwarcia PWA backup nie działa. Jedyny sygnał: etykietka w stopce.

### Dlaczego blokada była zbędna (dowód, nie założenie)

Vault **nie robi** Basic Auth — `authorized()` przy pustym `BEARER` zwraca `True`.
`/progress` chroni **wyłącznie nginx**, ten sam, który wpuszcza dashboard.
Kto widzi dashboard, ten ma już prawo do vaulta.

Stub z Basic Auth, `fetch('/progress',{credentials:'same-origin'})` **bez** nagłówka w JS:

```
GET /         | Authorization=<BRAK>            | BRAK/ZLE POSWIADECTWA   <- kontrola: 401
GET /progress | Authorization=Basic dGVzdDp0ZXN0 | OK                     <- przeglądarka dołożyła sama
```

### Dowód end-to-end (prawdziwy `DASHBOARD.html`, mini-nginx + mini-vault, HTTPS)

Zero wpisanego hasła:

```
GET /DASHBOARD.html | auth=OK
GET /progress       | auth=OK              <- sync startuje sam przy wejściu
PUT /progress       | auth=ZAPISANO 412 B  <- postęp wgrany do vaulta
klik zakładki       -> PUT /progress | ZAPISANO 417 B
stan: active_tab=workflow, updated_at zaktualizowany
```

**Naprawa:** usunięte obie blokady; 401 → jawny komunikat; `syncWarn()` pokazuje brak
autoryzacji **toastem** (raz na sesję — to jedyny stan, w którym praca NIE jest zabezpieczona);
etykieta mówi prawdę; panel ręczny zostaje jako **fallback**, nie warunek.

---

## 2. Śmieciowy hash trwale psuł panel (PR #18)

Na `main` żyła wersja `if(!el&&tabDef(id))`, a `tabDef` ma **fallback** na `ACADEMY_TABS[0]` —
jest więc prawdziwy dla każdego śmiecia. Zmierzone w przeglądarce:

| Wejście | Było | Jest |
|---|---|---|
| `#smieciowy-hash` | **pusty panel**, zero zakładek | zakładka domyślna |
| stan już zatruty | **pusty na zawsze** | samonaprawa przy starcie |
| `#day` (push 07:00) | DZIEŃ | DZIEŃ ✓ |

Najgorsze nie było wyświetlanie: `active_tab='cokolwiek'` szedł przez `save()` do
`localStorage`, więc użytkownik, który raz trafił w link z ogonem, **tracił dashboard bez
wyjścia z UI**. Naprawa: walidacja przy odczycie (`load()`) **i** przy renderze (`currentTab()`).

**Uspokajające:** `start_url` manifestu jest bez hasha, więc start PWA z ekranu tego nie odpalał.

---

## 3. Wzorzec, który warto zapamiętać (trzeci raz ten sam)

**Guard asertujący na SŁOWIE, nie na KODZIE, przepuszcza regresję.**

| Guard | Pisał | Dlaczego nie działał |
|---|---|---|
| A2 (hash) | `"tabDef(" in hash_fn` | komentarz obok w tej samej funkcji wspomina `tabDef(id)` |
| A4b (deploy) | `"--force" in deploy_txt` | `--force` występowało w innym miejscu skryptu |
| G3 (sync) | `"syncWarn('Vault " in html` | są **dwa** miejsca (odczyt i zapis); mutacja cofała jedno, guard widział drugie |

Dwa pierwsze mutacje raportowały **„nienauzyte"** — nie miały czego złapać, więc nikt nie
zauważył, że guard jest dekoracją. G3 złapał sam mutation test (22/22 → 21/22) i dopiero
wtedy guard zaostrzono, rozbijając na G3a/G3b.

**Wniosek:** każdy nowy guard musi mieć mutację, która go **naprawdę** obala. Zielony
walidator bez tego sprawdzenia nic nie znaczy.

---

## 4. Bramki

| Bramka | Wynik |
|---|---|
| `validate-academy-export.py` | PASS |
| `test_progress_vault.py` | PASS |
| mutation Fala 0 | **10/10** |
| mutation Fala D | **19/19** |
| mutation Fala E+F+G | **22/22** |
| CI `academy-gate` (PR + main) | pass |
| parytet produkcji | VPS md5 == blob `origin/main` (po LF→CRLF) ✓ |

---

## 5. Stan produkcji

- integralność deployu: bramka `HEAD == origin/main` + fail-closed poza repo git ✓
- vault: `{"ok": true}` · Hermes: `{"llm": true, "model": "deepseek-flash", "daily_cap": 200}`
- PWA z zewnątrz: manifest **200** · ikona512 **200** · HTML bez hasła **401** ✓
- push: timer `Mon 2026-09-21 07:03:59 CEST` ✓
- `/opt/akademia/data/`: `progress.json` **nadal nie istnieje** — pierwszy zapis zrobi telefon
- przy deployu: `data/progress.json` i `.bak` są wykluczone z tara, więc deploy nie kasuje postępu

---

## 6. Co zrobić na telefonie (jedyny brakujący dowód)

Nginx i vault są po stronie serwera — **nie da się ich przetestować z laptopa**, bo tam nie ma
cache'u poświadczeń przeglądarki telefonu.

1. Otwórz Akademię (HTTPS) i zaloguj się **raz**.
2. Odczekaj chwilę — pasek w stopce powinien przejść na **„Online — zsynchronizowano"**.
3. Odhacz jeden krok, odczekaj ~2 s, odśwież stronę — krok ma zostać.
4. Sprawdź, że `PUT /progress` pojawił się w logach:

```bash
ssh root@185.243.54.115 "grep -c 'PUT /progress' /var/log/nginx/access.log"
```

Wynik `> 0` = backup realnie działa. `0` = nadal nie działa, wracamy do tematu.

Uwaga: hasło wpisane w URL (`https://user:haslo@host/...`) **psuje** relatywny `fetch` —
Chrome rzuca `Request cannot be constructed from a URL that includes credentials`.
Loguj się przez natywne okno przeglądarki, nie wklejając poświadczeń w adres.

---

## 7. Następne kroki

Z planu `docs/ops/PLAN-HERMES-NADZORCA-NAUCZYCIEL-2026-09-20.md`:

- **Fala 1 — „Mój dzień" robi Hermes** (deterministyczny, działa bez LLM i internetu)
- Fala 2 — nadzorca workflow (GitHub-first, bez Linear)
- Fala 3 — nauczyciel (router + przypięty fakt, nie pełny RAG)

Otwarte drobne: `syncEnabled()` wymaga `https:` — na `localhost` sync jest wyłączony
(świadome, ale warto wiedzieć przy testach); nginx ostrzega o konflikcie
`api.zzpackage.flexgrafik.nl` — **cudza konfiguracja**, nie Akademia.
