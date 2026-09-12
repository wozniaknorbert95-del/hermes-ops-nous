# OPERATING MODEL — ekosystem pracy (v1.0, 2026-09-12)

**Właściciel:** R1 · **Status:** obowiązuje · **Zakres:** `dsaas-platform-main`, `workflow-lab`, `akademia`, handbook L3, przyszłe repozytoria.

## 1. Role repozytoriów

| Repo | Lokalizacja | Remote | Rola | SSoT |
|---|---|---|---|---|
| `dsaas-platform-main` | `github/dsaas-platform-main` | `wozniaknorbert95-del/dsaas-platform-main` | Główny produkt: platforma DSaaS, Kokpit, Maszynownia, kanon | `kanon/`, `todo.json`, `tenancy/`, runtime |
| `workflow-lab` | `github/workflow-lab` | `wozniaknorbert95-del/workflow-lab` (public) | Trening procesu issue→MR→CI; Cloud Agents; Linear CO | `AGENTS.md` §2, `DECISIONS.md`, `docs/DOD-WORKFLOW.md` |
| `akademia` | `github/akademia` | `wozniaknorbert95-del/akademia` | Szkoła + dzienny Command Dashboard; lekcje, checkpointy, eksport postępu | `DASHBOARD.html`, `schema/academy-progress.v0.json`, `README.md`, ten dokument |
| Handbook L3 | `akademia/ops/workflow-marzen/` | wewnątrz `akademia` | Podręcznik operacyjny (GitLab CE, rytuały, prompty) | pliki `00–05` w tym katalogu |

Katalog `C:\Users\FlexGrafik\FlexGrafik\github\workflow-marzen\` (poza gitem) jest **kopią roboczą, nie SSoT**.
Kanoniczna wersja handbooka mieszka wyłącznie w `akademia/ops/workflow-marzen/`.

## 2. Dozwolone przepływy

- Dowódca → Academy Dashboard (`▶ TERAZ`) → działanie w `workflow-lab` → eksport JSON → opcjonalny podgląd w Kokpicie.
- `akademia` CZYTA (read-only) dowody z `workflow-lab` (linki do docs/PR).
- `dsaas-platform-main` CZYTA wyeksportowany `academy-progress.v0.json` wyłącznie jako `captured` overlay (jednokierunkowo, plik, bez API).
- Handbook L3 mieszka w `akademia`; inne repozytoria linkują, nie kopiują.

## 3. Twarde zakazy

1. Kod platformy NIGDY w `workflow-lab`; trening labu NIGDY w `dsaas-platform-main`.
2. `AGENTS.md` kursu NIGDY nie wklejamy do `dsaas-platform-main`.
3. Dashboardu Akademii NIGDY nie iframe'ujemy w Kokpicie; Akademia nie jest 7. działem (mapowanie F wyłącznie na istniejące 6 działów + Tacę).
4. `localStorage["aea-os"]` to scratchpad przeglądarki — Kokpit go nie czyta; czyta wyłącznie eksport po schemacie.
5. Zero sekretów i tokenów OIDC w `academy_url`, eksporcie i docs.
6. Jeden git SSoT na klasę artefaktu — zero orphan-folderów jako źródeł.

## 4. Stan stacku (2026-09-12, uczciwie)

| Element | Stan | Znaczenie |
|---|---|---|
| GitHub | **AKTYWNY** | działający host `workflow-lab` i platformy; origin do czasu udowodnienia CE |
| GitLab CE self-hosted | **FUTURE / human-stop VPS** | cutover wyłącznie po zielonej checkliście W0; zakaz dual-origin |
| Slack | **PARKED** | zbędny przy Linear mobile + GitHub mobile + Cursor |
| Grok BADACZ | **AKTYWNY** | research nie-kodowy |
| Grok PM | **PARKED (opcjonalny)** | digest + Linear wystarczają |
| Bugbot comment | **PARTIAL** | API `bugBotEnabled:true`, zero komentarzy na MR lab do 2026-09-12 |
| Daily digest / weekly sweep / comment→agent | **AKTYWNE** | F4 core PASS w labie |
| Academy→Kokpit widget | **ZAPROJEKTOWANY, nie wdrożony** | kontrakt JSON istnieje; konsument w platformie = osobny etap |

## 5. Checklist onboardingu nowego repo

Każde kolejne repo (osobny produkt/moduł) wdrażamy tym samym standardem:

- [ ] Granica produktu zapisana (1 akapit: co jest / czego nie ma w repo).
- [ ] `AGENTS.md` z prawdziwymi komendami (§2 = CI 1:1).
- [ ] Branch protection: `main` tylko przez PR + wymagany check CI.
- [ ] CI = `lint` + `test` + `build` (komendy z `AGENTS.md`, zero wymyślonych).
- [ ] Projekt/obszar w Linear + etykiety `agent`/`review`/`blocked` + owner.
- [ ] Szablon issue (Cel/Kontekst/Wymagania/Ograniczenia/Kryteria/Weryfikacja).
- [ ] `DECISIONS.md` (decyzje nieodwracalne, najnowsze na górze).
- [ ] Dowód pierwszego loop: issue → PR → zielone CI → merge.
- [ ] Automatyzacje tylko po zielonym loop; sekrety wyłącznie w provider secrets.
- [ ] Nowe repo nie dziedziczy statusu „gotowe" ani dostępu do danych platformy.

## 6. Zmiany tego dokumentu

Małe korekty redakcyjne — PR w `akademia`. Zmiana ról/SoT/zakazów — decyzja R1 + wpis w tym pliku (data, powód). Dokument nie nadpisuje kanonu platformy.
