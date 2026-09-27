# Plan naprawczy — P2 (`_NEG_ENV` za wąski → fałszywy LOCAL)

**Status:** **GO — WYKONANE 2026-09-27** (implementacja + testy; deploy = osobna decyzja Zasada 11)
**Data:** 2026-09-27
**Źródło:** [`AUDYT-WYNIK-HERMES-OPS-2026-09-27.md`](AUDYT-WYNIK-HERMES-OPS-2026-09-27.md) (round 3)
**Zakres naprawy:** `scripts/ops_linear_dor.py` + testy (unit + mutacja). Bez zmian UI, bez deploy.

---

## 1. Znalezisko

`_requires_local()` w `scripts/ops_linear_dor.py` fałszywie klasyfikuje jako `qui_lane_local`
(LOCAL → tor laptop, 400 przed `@cursor`) zadania, które **wprost wykluczają** VPS/SSH/deploy,
gdy czasownik-zaprzeczenie jest oddzielony od rzeczownika środowiska.

**Zmierzone (live + lokalnie):**

| Fraza w `Zakres środowiska` | `requires_local` | Powinno być |
| --- | --- | --- |
| `zero VPS` | 0 | 0 (OK — fix fa7922f) |
| `bez SSH` | 0 | 0 (OK) |
| `nie deploy` | 0 | 0 (OK) |
| `nie wymaga SSH` | **1** | **0 ← BŁĄD** |
| `nie dotyczy VPS` | **1** | **0 ← BŁĄD** |
| `bez dostępu do VPS` | **1** | **0 ← BŁĄD** |
| `vps ssh` | 1 | 1 (OK — naprawdę LOCAL) |
| `certbot` | 1 | 1 (OK — naprawdę LOCAL) |

**Kierunek:** fail-safe. Fałszywy LOCAL = za dużo ostrożności (blokuje autopilota), nigdy nie
auto-aprobuje zadania naprawdę lokalnego. **Nie** luka bezpieczeństwa, ale psuje routing.

---

## 2. Root cause

```python
# scripts/ops_linear_dor.py:41
_NEG_ENV = re.compile(r"\b(zero|bez|nie|no)\s+(vps|ssh|deploy)\b")
```

Regex kasuje negację **tylko** gdy zaprzeczenie styka się **bezpośrednio** z rzeczownikiem.
`fa7922f` naprawił wyłącznie przypadek „zero VPS”. Frazy z czasownikiem pośrodku
(„nie **wymaga** SSH”, „bez **dostępu do** VPS”) nie są łapane, więc „ ssh”/„vps ” z
`REQUIRE_LOCAL` wciąż trafia → fałszywy LOCAL.

---

## 3. Design naprawy

**Zasada:** zachować chirurgiczne usuwanie tokenów (per-token, nie globalne „wykluczenie wygrywa”)
— dzięki temu „bez SSH, ale deploy lab na laptopie” nadal trafi na LOCAL przez „deploy lab”.
Rozszerzamy jedynie zbiór fraz-negacji o czasownik-pośredni (bounded, whitelist — nie `.*`).

**Proponowana zmiana (Option A — rekomendowana):**

```python
# przed
_NEG_ENV = re.compile(r"\b(zero|bez|nie|no)\s+(vps|ssh|deploy)\b")

# po — dodany opcjonalny „czasownik-pośredni” (whitelist, NIECH ten sam token zostaje usunięty)
_NEG_ENV = re.compile(
    r"\b(zero|bez|nie|no)\s+"
    r"(?:(?:wymaga|wymagają|dotyczy|używa|używany|potrzebuje|zawiera|"
    r"ma\s+dostę[pu]\s+do|dostępu\s+do|wymogu)\s+)?"
    r"(?:jakiegokolwiek\s+|żadnego\s+)?"
    r"(vps|ssh|deploy|deployment)\b",
    re.I,
)
```

Weryfikacja fraz (target): patrz tabela w §1 — wszystkie 3 „BŁĄD” schodzą na 0, 3 „OK” zostają bez zmian.

**Option B (alternatywa, czystszy refaktor — nie wymagany):** rozbić na dwie jawnie nazwane
funkcje `_excludes_local()` + `_requires_local()` i unit-testować korpus fraz. Więcej ruchu,
ta sama semantyka. Rekomenduję A (mniejsza delta, mniejsze ryzyko regresji).

---

## 4. Test — nowa mutacja (guard anty-regresja)

Reguły Fala J: każdy nowy mutation-test `*.py` musi być wpięty do linii `testy:` w AGENTS.md
**i** do `.github/workflows/academy-gate.yml` **w tym samym PR**.

Rekomendacja: **rozszerzyć istniejącą Falę R** (plik `scripts/mutation-test-fala-r.py`, już
wpięty) o mutacje R4–R6 — unikamy nowego pliku i związanej z nim dopinki:

| Mutacja | Co psuje | Guard musi złapać |
| --- | --- | --- |
| R4 | `_NEG_ENV` zwężone z powrotem do bezpośredniego `(zero\|bez\|nie\|no)\s+(vps\|ssh\|deploy)` | test „nie wymaga SSH → NIE local” pada |
| R5 | usunięcie frazy `wymaga\|dotyczy\|dostępu do` z whitelisty | „nie dotyczy VPS” + „bez dostępu do VPS” padają |
| R6 | `deployment` przepuszczony do `REQUIRE_LOCAL` bez negacji | „nie deploy/deployment” pada |

Plus: rozszerzyć `dor_gate_unit()` w `scripts/test_progress_vault.py` o 3 asercje pozytywne
(„nie wymaga SSH”, „nie dotyczy VPS”, „bez dostępu do VPS” → `ok=True`, `lane=HERMES`)
i 2 asercje negatywne („vps ssh”, „certbot” → nadal `qui_lane_local`).

---

## 5. Weryfikacja (po implementacji, przed deploy)

```bash
python scripts/test_progress_vault.py          # unit + integracja gate DoR
python scripts/mutation-test-fala-r.py         # 0 PRZEPUSZCZONE (R1–R6)
python scripts/mutation-test-fala-0.py         # sanity reszty fal
bash scripts/deploy-ready-hermes-ops.sh        # HEAD==origin/main + wszystkie bramki
```

Sonda (powtórka z audytu, musi dać 0 dla 3 fraz):

```python
# re-import ops_linear_dor; _requires_local dla:
# "nie wymaga SSH", "nie dotyczy VPS", "bez dostępu do VPS"  → False
# "vps ssh", "certbot"                                       → True
```

---

## 6. Rollback

`git revert <sha>` przywraca `_NEG_ENV` do stanu fa7922f. Brak migracji danych — czysta zmiana
funkcji w pamięci (bez plików cache/status, które wymagałyby sprzątania).

---

## 7. Ryzyka

| Ryzyko | Ocena | Mitigacja |
| --- | --- | --- |
| Fałszywy-negatyw: realne lokalne zadanie ukryte frazą | niskie | whitelist czasowników, NIE `.*`; per-token removal; korpus w teste |
| Regresja „zero VPS” (fa7922f) | brak | R4 łapie; dor_gate_unit QUI-93 zostaje |
| Niedokładność regex dla nowych fraz | akceptowalne | to heurystyka wspomagająca routing — fałszywy LOCAL pozostaje fail-safe |

---

## 8. Poza zakresem

Orchestrator `workflow-lab`, markery platformy (P0#3), deploy VPS (Zasada 11), kurs Akademii.
O6 e2e i deploy to osobne decyzje (nie defekty).

---

## 9. Checklist wykonawczy (po GO)

- [ ] `_NEG_ENV` rozszerzony (Option A)
- [ ] `dor_gate_unit` + 5 asercji
- [ ] mutation R4–R6 w fala-r
- [ ] AGENTS.md `testy:` **i** academy-gate.yml — bez zmian (fala-r już wpięta)
- [ ] pełna bateria + sonda → PASS
- [ ] commit + PR (nie deploy) → GO Zasada 11 osobno

**Decyzja Dowódcy:** GO na implementację? (deploy pozostaje poza tym GO)
- [ ] GO — implementuj fix + testy (osobny PR, bez deploy)
- [ ] STOP / zmiana designu