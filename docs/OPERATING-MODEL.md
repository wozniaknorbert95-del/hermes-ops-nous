# OPERATING MODEL — ekosystem pracy (v1.4, 2026-09-24)

**Właściciel:** R1 · **Status:** obowiązuje · **Zakres:** `dsaas-platform-main`, `workflow-lab`, `akademia`, handbook L3, przyszłe repozytoria.

## 1. Role repozytoriów

| Repo | Lokalizacja | Remote | Rola | SSoT |
|---|---|---|---|---|
| `dsaas-platform-main` | `github/dsaas-platform-main` | `wozniaknorbert95-del/dsaas-platform-main` | Główny produkt: platforma DSaaS, Kokpit, Maszynownia, kanon | `kanon/`, `todo.json`, `tenancy/`, runtime |
| `workflow-lab` | `github/workflow-lab` | `wozniaknorbert95-del/workflow-lab` (public) | Trening procesu issue→MR→CI; Cloud Agents; Linear CO; auto-merge (D-AUTOMERGE); **orchestrator Hermes Ops** (`scripts/hermes_ops/`); warstwa Jupyter Notebooków (Python, opt-in, D-W7-JUPYTER, gate `execute`) | `AGENTS.md` §2, `DECISIONS.md`, `notebooks/README.md`, `docs/DOD-WORKFLOW.md` |
| `akademia` | `github/akademia` | `wozniaknorbert95-del/akademia` | **Dwa produkty UI** na jednym originie: szkoła + Control Plane; vault postępu; PWA | patrz §1.1 |
| Handbook L3 | `akademia/ops/workflow-marzen/` | wewnątrz `akademia` | Podręcznik operacyjny (GitLab CE, rytuały, prompty) — **nie** zastępuje `/ops` | pliki `00–05` w tym katalogu |

Katalog `C:\Users\FlexGrafik\FlexGrafik\github\workflow-marzen\` (poza gitem) jest **kopią roboczą, nie SSoT**.
Kanoniczna wersja handbooka mieszka wyłącznie w `akademia/ops/workflow-marzen/`.

### 1.1 Repo `akademia` — dwa produkty (split 2026-09-21)

| Produkt | Ścieżka | SSoT | Nie robi |
|---|---|---|---|
| **Akademia** | `/`, `DASHBOARD.html` | `DASHBOARD.html`, `schema/academy-progress.v0.json`, `docs/ACADEMY-UX-SPEC.md` | merge PR, deploy, start agenta bez `/ops` |
| **Hermes Ops** | `/ops`, `OPS.html` | `docs/ops/HERMES-ROLE-CONTRACT.md`, `HERMES-OPS-HOWTO.md`, `CONTRACT-OPS-STATUS.md` | nauka kursu, edycja postępu kursu |
| **Vault** | `host/progress_vault.py` | `docs/runbooks/AKADEMIA-VPS.md`, kontrakt JSON ops | orchestrator tick (to `workflow-lab`) |

Indeks dokumentacji Ops: [`docs/ops/README.md`](ops/README.md).  
Historyczny opis split: [`docs/handoffs/2026-09-21-split-academy-ops.md`](handoffs/2026-09-21-split-academy-ops.md).

**Role Hermes (skrót):**

- **Hermes Akademii** — kierunek kursu, rytuał DZIEŃ, intent lokalny w UI; `POST /hermes/chat` = **410** (emerytura).
- **Hermes Engineer** — pętla na `/ops`: Linear (etykiety) → `@cursor` → CI → auto-merge **labu i platformy**; deploy = lokalnie (Zasada 11).
- **Cursor Cloud Agent** — jedyny executor kodu w telefon loopie.

## 2. Dozwolone przepływy

- **Nauka:** Dowódca → Academy Dashboard (`▶ TERAZ`) → działanie w `workflow-lab` → eksport JSON → opcjonalny podgląd w Kokpicie.
- **Praca (Linear-first):** Dowódca → issue w Linear (etykieta `agent`, 6 pól) → **`/ops`** (Start / Run next) → orchestrator w `workflow-lab` → PR → CI → auto-merge → **nie** deploy z telefonu.
- Poranek platformy: `DASHBOARD.html` zakładka **DZIEŃ** + widok [CEO/Today](https://linear.app/quietforge/team/QUI/view/ceotoday-1ef420fc07c0) → issue platformy → **nie** ENT-12 przed M0 PASS.
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
7. **Telefon nie merguje** i **nie deployuje produkcji** — Approval na `/ops` ≠ Merge na GitHubie (Zasada 11).

## 4. Stan stacku (2026-09-24, uczciwie)

| Element | Stan | Znaczenie |
|---|---|---|
| Linear platform (`dsaas-platform-main`) | **PARTIAL → PASS** | Projekt QUI + widoki; QUI-18 HITL w toku |
| GitHub | **AKTYWNY** | host `workflow-lab` i platformy |
| **Hermes Ops** (`/ops` + tick VPS) | **WDROŻONE** | Autopilot-only; kontrakt w `docs/ops/`; smoke `scripts/smoke-hermes-ops-vps.sh` |
| GitLab CE self-hosted | **FUTURE / human-stop VPS** | cutover po W0; zakaz dual-origin |
| Slack | **PARKED** | Linear mobile + GitHub mobile + Cursor |
| Daily digest / weekly sweep / comment→agent | **AKTYWNE** | F4 core PASS w labie |
| Academy→Kokpit widget | **ZAPROJEKTOWANY, nie wdrożony** | kontrakt JSON istnieje |

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

**v1.4 (2026-09-24):** split Akademia / Hermes Ops w §1.1, przepływ Linear-first, zakaz merge z telefonu, stan `/ops`.
