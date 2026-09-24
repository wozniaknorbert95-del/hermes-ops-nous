# Plan aktualizacji dokumentacji — Akademia + Hermes Ops (2026-09-24)

**Repo:** `akademia`  
**Autor:** sztab R1 (Cursor, `/vibe-init`)  
**Status:** PLAN — bez zmian runtime poza docs / README (Fala 0)  
**Gate wejścia:** `validate-academy-export.py` + `test_progress_vault.py` → **PASS** (2026-09-24)

---

## 1. Cel

Repozytorium **hostuje dwa produkty na jednym originie**, ale pierwsze wrażenie (README, OPERATING-MODEL, kurs `cursor-kurs/`) wygląda jak „tylko szkoła”. Hermes Ops ma rozbudowany kanon w `docs/ops/` i handoffach, lecz **brak spójnej mapy wejścia** dla Dowódcy, agenta Cursor i nowego współpracownika.

**Sukces:** każdy czyta README → wie, że jest **Akademia (`/`)** i **Hermes Ops (`/ops`)**, gdzie jest kontrakt ról, jak smoke’ować, i który plik jest SSoT dla której warstwy.

**Poza zakresem tego planu:** orchestrator w `workflow-lab`, merge platformy, deploy VPS (Zasada 11), nowe funkcje UI.

---

## 2. Mapa produktów (kanon od split 2026-09-21)

| Warstwa | URL / artefakt | Rola | SSoT docs |
| --- | --- | --- | --- |
| **Akademia** | `/`, `DASHBOARD.html` | Kurs A–G, ▶ TERAZ, sync vault, eksport JSON | `DASHBOARD.html`, `schema/academy-progress.v0.json`, `docs/ACADEMY-UX-SPEC.md` |
| **Hermes Ops** | `/ops`, `OPS.html` | Control Plane: Linear → Cursor → CI → auto-merge; telefon = Pause/Start, nie merge | `docs/ops/HERMES-ROLE-CONTRACT.md`, `HERMES-OPS-HOWTO.md`, `RUNBOOK-OPS-WIRING.md` |
| **Vault** | `host/progress_vault.py` | `/progress`, `/ops/status`, `/ops/diag`, PWA, **410** na `POST /hermes/chat` | `docs/runbooks/AKADEMIA-VPS.md`, `docs/ops/CONTRACT-OPS-STATUS.md` |
| **Orchestrator** | `workflow-lab/scripts/hermes_ops/` | Tick timer, `ops-status.json`, merge obu repo | Lab runbooki + handoff `2026-09-21-split-academy-ops.md` |
| **Handbook L3** | `ops/workflow-marzen/` | GitLab CE, prompty sztabu (nie zastępuje `/ops`) | `00–05` w tym katalogu |

**Nie mylić:**

- **Hermes Akademii** (nauczyciel kursu, intent lokalny / morning API) ≠ **Hermes Engineer** (pętla `/ops`).
- **POST /hermes/chat** = emerytura (410). Stary runbook VPS §10 (DeepSeek czat) = **STALE** względem split — do korekty w Fali 2.

---

## 3. Audyt wejść (2026-09-24)

### 3.1 Pliki „pierwszego kontaktu”

| Plik | Hermes Ops widoczny? | Finding |
| --- | --- | --- |
| `README.md` | **NIE** (przed Falą 0) | Tylko „szkoła”, brak `/ops`, brak linku do `docs/ops/` |
| `AGENTS.md` | **Częściowo** | Link do `HERMES-ROLE-CONTRACT`; brak smoke `/ops`, brak `scripts/smoke-hermes-ops-vps.sh` |
| `docs/OPERATING-MODEL.md` v1.3 | **Słabo** | Wiersz `akademia` = „Command Dashboard”; brak OPS.html, vault routes, split PWA |
| `docs/CURSOR-WORKFLOW.md` vibeinit | **NIE** | Czyta tylko README + OPERATING-MODEL §1–3; nie wspomina `/ops` |
| `cursor-kurs/00-START-TUTAJ.md` | **NIE** | Biblioteka kursu OK; brak „praca = /ops” |
| `docs/ops/*` | **TAK** | 17 plików, brak **`README.md` indeksu** (nawigacja trudna) |
| `ops/workflow-marzen/README.md` | **Minimalnie** | L3 GitLab; Hermes Ops tylko obok |

### 3.2 UI (referencja — już spójne)

| Miejsce | Stan |
| --- | --- |
| `DASHBOARD.html` hero | Link **Hermes Ops →** `/ops` |
| `OPS.html` | Osobny tytuł PWA, manifest `manifest-ops.webmanifest` |
| Handoff `2026-09-21-split-academy-ops.md` | Tabela `/` vs `/ops` — **kanon historyczny** |

### 3.3 Testy / CI

| Obszar | Stan |
| --- | --- |
| `academy-gate.yml` | Walidator + mutacje Fala 0–N |
| `test_hermes_intent.py` | Intent Hermes **Akademii** (nie `/ops`) |
| Smoke Ops | `scripts/smoke-hermes-ops-vps.sh` — **nie** w linii `testy:` AGENTS.md |

---

## 4. Fale pracy (sztab)

Każda fala = **jeden PR**, pełna linia `testy:` z `AGENTS.md` zielona.

### Fala 0 — Mapa na drzwiach (ten PR / vibe-init)

| # | Plik | Akcja |
| --- | --- | --- |
| 0.1 | `README.md` | Sekcja **Dwa produkty**, tabela `/` vs `/ops`, linki do HOWTO + kontraktu |
| 0.2 | `docs/ops/README.md` | **Nowy** indeks: kolejność czytania, smoke, runbooki |
| 0.3 | `docs/ops/PLAN-AKTUALIZACJI-DOKUMENTACJI-HERMES-2026-09-24.md` | Ten dokument |
| 0.4 | `docs/handoffs/2026-09-24-vibe-init-hermes-ops-docs.md` | Handoff sesji |

**Właściciel:** Cursor Cloud Agent · **Review:** Dowódca R1

### Fala 1 — Model operacyjny i agent

| # | Plik | Akcja |
| --- | --- | --- |
| 1.1 | `docs/OPERATING-MODEL.md` | v1.4: podsekcja Hermes Ops w roli `akademia`; przepływ Linear-first; link split handoff |
| 1.2 | `AGENTS.md` | Rozszerzyć `smoke public` o `/ops` i `/ops/diag`; wskazać `smoke-hermes-ops-vps.sh` |
| 1.3 | `docs/CURSOR-WORKFLOW.md` | vibeinit: „przeczytaj `docs/ops/README.md` jeśli dotykasz `/ops`” |

### Fala 2 — Runbooki bez sprzeczności

| # | Plik | Akcja |
| --- | --- | --- |
| 2.1 | `docs/runbooks/AKADEMIA-VPS.md` §10 | Oznaczyć DeepSeek/czat jako legacy; wskazać 410 + `/hermes/morning` + split |
| 2.2 | `docs/ops/DEPLOY-READY-HERMES-OPS.md` | Cross-link do README repo root |
| 2.3 | Walidator (opcjonalnie) | Guard: README musi zawierać `/ops` i `HERMES-OPS-HOWTO` (Fala J pattern) — **tylko jeśli Dowódca chce twardy kontrakt** |

### Fala 3 — Kurs i onboarding

| # | Plik | Akcja |
| --- | --- | --- |
| 3.1 | `cursor-kurs/00-START-TUTAJ.md` | Akapit: nauka vs praca (`/ops`) |
| 3.2 | `cursor-kurs/05-Profesjonalny-workflow-autonomia.md` | Link do `HERMES-OPS-HOWTO` zamiast ogólników „telefon” |
| 3.3 | `docs/ops/AKADEMIA-INSTRUKCJA.md` | Spójność z zakładką INSTRUKCJA w UI (jeśli drift) |

### Fala 4 — Handbook L3 (opcjonalnie)

| # | Plik | Akcja |
| --- | --- | --- |
| 4.1 | `ops/workflow-marzen/00-PLAN-DZIALANIA.md` | Jedna strona: Akademia vs Hermes Ops vs platforma |
| 4.2 | `ops/workflow-marzen/README.md` | Link do `docs/ops/README.md` |

---

## 5. Role sztabu (RACI skrót)

| Rola | Fala 0–1 | Fala 2–3 | Fala 4 |
| --- | --- | --- | --- |
| **Dowódca (R1)** | Akceptacja mapy README | Akceptacja runbook VPS | Priorytet L3 vs ops |
| **Cursor Agent** | Edycja docs + guardy | Audyt STALE w DASHBOARD copy (osobny issue) | — |
| **Hermes Engineer (VPS)** | Smoke po deploy docs-only: N/A | Weryfikacja `/ops/diag` po deploy kodu | — |
| **Platforma** | Brak | Sync `LINEAR-PLATFORM.md` linki | — |

---

## 6. Kryteria DONE (program dokumentacji)

- [ ] README opisuje **oba** produkty i linkuje `docs/ops/README.md`.
- [ ] OPERATING-MODEL §1 wymienia `/ops` i wskazuje kontrakt ról.
- [ ] AGENTS.md ma copy-paste smoke dla `/ops` (bez haseł w repo).
- [ ] Brak sprzeczności: runbook VPS nie sugeruje aktywnego `POST /hermes/chat` jako ścieżki UI.
- [ ] Nowy dev: README → HOWTO → RUNBOOK w &lt; 15 min bez szukania w `docs/handoffs/`.

---

## 7. ▶ TERAZ (kurs — nie mylić z planem)

Dla **pustego** postępu w przeglądarce karta **▶ TERAZ** wskazuje pierwszy otwarty rozdział kursu (domyślnie **A1 — Fundament repozytorium** w `workflow-lab`). To zamierzone: TERAZ = nauka; praca agentowa = **`/ops`**.

---

## 8. Następny krok (jeden)

**Fala 1:** PR `docs/OPERATING-MODEL.md` v1.4 + rozszerzenie `AGENTS.md` (smoke Ops), po merge Falą 0.

---

## 9. Komendy weryfikacji

```bash
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
python -m http.server 8765
# → http://localhost:8765/DASHBOARD.html  oraz  http://localhost:8765/ops
bash scripts/smoke-hermes-ops-vps.sh   # na VPS / po deploy vault
```
