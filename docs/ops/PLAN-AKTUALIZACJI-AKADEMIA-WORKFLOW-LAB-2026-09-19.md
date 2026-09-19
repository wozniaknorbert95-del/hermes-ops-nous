# Plan aktualizacji Akademii — workflow-lab: notebooki + auto-merge (2026-09-19)

**Repo:** `akademia`
**Autor planu:** sesja `workflow-lab` (Cursor)
**Status:** PLAN — do wykonania na gałęzi `docs/workflow-lab-automerge-notebooks`
**Zakres:** tylko repo `akademia`. Poza zakresem: `workflow-lab`, `dsaas-platform-main`, `akademia-wfp9`.

---

## 1. Cel

Dopasować dział **A (Workflow Lab)** w `DASHBOARD.html` oraz dokumentację Akademii do dwóch zmian, które weszły na `main` w `workflow-lab` w dniu 2026-09-19:

1. **D-AUTOMERGE** — pełny automatyczny merge (koniec bramki „human merge").
2. **D-W7-JUPYTER** — opt-in warstwa notebooków (Python, analiza / dowody).

**Efekt:** Akademia opisuje **stan realny** `workflow-lab/main` — nie uczy nieaktualnego gestu (ręczny merge) i nie pomija nowej warstwy (notebooki).

**Zasada nadrzędna:** nie dokumentujemy w Akademii niczego, czego nie ma na `workflow-lab/main`.

---

## 2. Stan wyjściowy — `workflow-lab/main` (SoT, read-only)

| Fakt | Dowód |
|------|-------|
| Pełny auto-merge (non-draft PR + zielone wymagane checki → squash) | `workflow-lab/DECISIONS.md` → `D-AUTOMERGE`; `.github/workflows/automerge.yml` |
| Wymagane checki `main`: `validate` + `execute` (`strict`) | GitHub branch protection |
| `ci.yml` zawsze raportuje `validate` (path-filter w kroku, nie w triggerze) | `.github/workflows/ci.yml` |
| `notebooks.yml` zawsze raportuje `execute` | `.github/workflows/notebooks.yml` |
| Escape hatch: etykieta `no-automerge` (albo `blocked`) wstrzymuje auto-merge; draft nigdy nie merge | `.github/workflows/automerge.yml` |
| PR #58 (auto-merge), #57 (handoff), #56 (notebooki), #59 (execute required) — zmergowane autonomicznie | `workflow-lab` git log |
| Warstwa notebooków (Python, opt-in, oddzielona od Node core) | `notebooks/**`, `requirements.txt`, `scripts/run-notebooks.sh`, `.gitattributes`, `.cursor/skills/dodaj-notebook/SKILL.md` |

**Uwaga o Akademii:** akademia **nie ma** CI ani ochrony gałęzi — merge do `main` pozostaje **ręczny** (proces Akademii bez zmian; to osobna decyzja Dowódcy). Auto-merge dotyczy **wyłącznie** `workflow-lab`.

---

## 3. Co jest nieaktualne w Akademii (audyt 2026-09-19)

| Miejsce | Dziś | Problem |
|---------|------|---------|
| `DASHBOARD.html` → `PLAYBOOK_LAPTOP` krok 6 | `Human merge` | Nieaktualne — merge jest automatyczny |
| `DASHBOARD.html` → `PLAYBOOK_PHONE` krok 6 | `Human merge (Zasada 11)` | Nieaktualne + mylące (Zasada 11 = deploy, nie merge) |
| `DASHBOARD.html` → `TOOL_DATA` „Cursor local" | `… test/lint/build, human merge.` | Nieaktualne |
| `DASHBOARD.html` → 2 diagramy mermaid (`renderWorkflow`) | węzeł `Merge["human merge"]` | Nieaktualne |
| `DASHBOARD.html` → dział A (rozdziały) | A1–A6, brak notebooków | Brak warstwy `D-W7-JUPYTER` |
| `README.md` → „Trzy systemy" | `pętla issue→MR→CI` | Brak auto-merge i notebooków |
| `docs/OPERATING-MODEL.md` → rola `workflow-lab` | brak auto-merge / notebooków | Niepełne |
| `cursor-kurs/szablony/README.md` | brak wzmianki o warstwie Python | Ryzyko pomylenia z Node core |

---

## 4. Backlog — co zmienić

### 4.1 `DASHBOARD.html`

#### A. Playbook laptop — krok 6

`PLAYBOOK_LAPTOP`, element `{n:6,...}`:

- Było: `label:'Human merge'`, `path:'workflow-lab/AGENTS.md'`
- Ma być: `label:'Auto-merge (CI zielone)'`, `path:'workflow-lab/DECISIONS.md'` (dowód `D-AUTOMERGE`)

#### B. Playbook telefon — krok 6

`PLAYBOOK_PHONE`, element `{n:6,...}`:

- Było: `label:'Human merge (Zasada 11)'`, `path:'dsaas-platform-main/AGENTS.md'`
- Ma być: `label:'Auto-merge (CI zielone)'`, `path:'workflow-lab/DECISIONS.md'`

Usunąć `(Zasada 11)` — Zasada 11 dotyczy deployu, nie merge. Krok 6 nie wskazuje już pliku platformy (nie mylić torów).

#### C. `TOOL_DATA` — karta „Cursor local"

- Było (fragment `text`): `Laptop loop: issue/PR, lokalna edycja, test/lint/build, human merge.`
- Ma być: `Laptop loop: issue/PR, lokalna edycja, test/lint/build, auto-merge po zielonym CI (D-AUTOMERGE).`

**Nie dodawać** nowej karty do `TOOL_DATA` — walidator wymaga dokładnie 14 wystąpień `proofHref:`. Warstwę notebooków pokazuje rozdział A7 (patrz niżej), nie karta narzędzia.

#### D. Diagramy mermaid (`renderWorkflow`)

Oba wykresy `flowchart LR` zawierają węzeł `Merge["human merge"]`. Zmienić na `Merge["auto-merge"]` (oba wystąpienia).

#### E. Nowy rozdział A7 — „Notebooki — warstwa analityczna"

Dodać do `DZIAL_DATA` działu A (id `"A"`), **po** rozdziale A6:

```js
{ id:"A7", title:"Notebooki — warstwa analityczna",
  pliki:[
    { path:"notebooks/README.md", rola:"Warstwa analityczna: po co jest, jak uruchomić lokalnie, kontrakt CI." },
    { path:"notebooks/hello-analysis.ipynb", rola:"Przykład (happy path + edge): analiza bez commitowania outputs." },
    { path:"requirements.txt", rola:"Pinned zależności Pythona (opt-in) — osobno od zero-dep Node core." },
    { path:".github/workflows/notebooks.yml", rola:"Job execute: always-report, path-filter na notebooks/. Wymagany check na main." },
    { path:"scripts/run-notebooks.sh", rola:"Headless run wszystkich *.ipynb (kernel ci-kernel)." },
    { path:".gitattributes", rola:"nbstripout: zero outputs / sekretów w .ipynb w git." },
    { path:".cursor/skills/dodaj-notebook/SKILL.md", rola:"Procedura agenta: jak dodać notebook zgodnie z kontraktem." }
  ],
  lab:[
    "Wyjaśnij różnicę: Node core (npm test/lint/build) vs warstwa notebooków (Python, opt-in) — czemu się nie mieszają",
    "Otwórz .gitattributes i notebooks/README.md — po co nbstripout i dlaczego outputs nie idą do gita",
    "W notebooks.yml wskaż, że job execute jest wymaganym checkiem na main (obok validate)"
  ],
  dod:"Tłumaczysz, że notebooki to osobna warstwa analityczna (nie core), a gate execute jest wymagany na main. Wiesz, czemu outputs nie są commitowane." },
```

`ALL_ROZ` jest wyprowadzane automatycznie z `DZIAL_DATA`, więc A7 wchodzi do sekwencji bez dodatkowej rejestracji. A7 dziedziczy blokadę sekwencyjną (`isLocked`) po A6 — zgodne z UX działu A.

### 4.2 `README.md`

Tabela „Trzy systemy", wiersz Lab:

- Było: `| Lab | workflow-lab | pętla issue→MR→CI |`
- Ma być: `| Lab | workflow-lab | pętla issue→MR→CI→auto-merge + notebooki (warstwa analityczna) |`

### 4.3 `docs/OPERATING-MODEL.md`

- §1 tabela, wiersz `workflow-lab`, kolumna „Rola": dopisać ` auto-merge (D-AUTOMERGE); warstwa notebooków (Python, opt-in)`.
- Bump wersji w nagłówku: `v1.1` → `v1.2` + data `2026-09-19`.

### 4.4 `cursor-kurs/szablony/README.md` (opcjonalnie)

Dopisać jedno zdanie: notebooki to **osobna warstwa Python** (opt-in), nie część Node core — nie mieszaj komend.

---

## 5. Walidacja / kryteria akceptacji

- [ ] `python scripts/validate-academy-export.py` → **PASS** (bez zmian: `proofHref:` = 14, klucze `DIAGRAMS` bez zmian, `WF-P6` / `ENT-12` / `WAIT` dalej obecne).
- [ ] `python scripts/test_progress_vault.py` → **PASS**.
- [ ] (Opcjonalnie) nowe gate'y w walidatorze: A7 + auto-merge — w tym samym PR.
- [ ] `python -m http.server 8765` → `DASHBOARD.html`: playbook #6 mówi „Auto-merge", diagramy pokazują „auto-merge", rozdział A7 widoczny, DZIEŃ renderuje się bez regresji.
- [ ] Zero sekretów.
- [ ] Diff wyłącznie w `akademia`.

---

## 6. Granice (żelazne — „nie mieszać")

1. Zmiany **tylko** w repo `akademia`.
2. **Nie** dotykać `workflow-lab` (SSoT — tylko czytamy), `dsaas-platform-main`, `akademia-wfp9`.
3. **Nie** zmieniać procesu merge samej Akademii (osobna decyzja Dowódcy).
4. Nie dodawać drugiej karty „TERAZ" (`akademia/AGENTS.md` §1).
5. Zero sekretów / OIDC w eksporcie i docs (`akademia/AGENTS.md` §6).

---

## 7. Ryzyka

| Ryzyko | Mitigacja |
|--------|-----------|
| Walidator liczy `proofHref:` == 14 | Nie dodawać kart do `TOOL_DATA` |
| Regresja `_scratch` (utrata historii checkboxów) | Nie zmieniać kluczy `day_*`; A7 używa nowych kluczy `A7l1..3`, bez migracji |
| Mylenie warstw Node / Python | Sekcja 4.4 + rola A7 „osobna warstwa" |
| WIP na `main` (`schema/academy-progress.v0.json`) | Nowa gałąź od `origin/main`; commituj tylko własne pliki |

---

## 8. Kolejność / właściciel

1. Ten plan → gałąź `docs/workflow-lab-automerge-notebooks` w `akademia` (PR).
2. Agent w Akademii: implementacja §4 na tej samej gałęzi → walidacja §5 → PR gotowy do review.
3. Dowódca: review + merge (proces Akademii bez zmian — merge ręczny).

**WŁAŚCICIEL:** agent w `akademia` · **SSoT:** `workflow-lab/DECISIONS.md` (`D-AUTOMERGE`, `D-W7-JUPYTER`)
