# OPERATING MODEL — Hermes Ops Nous (v1.0, 2026-10-04)

**Właściciel:** R1 · **Status:** obowiązuje · **Zakres:** `hermes-ops-nous` (Control Plane), `workflow-lab` (orchestrator), `dsaas-platform-main` (platforma).

## 1. Rola repo

| Repo | Rola | SSoT |
|---|---|---|
| `hermes-ops-nous` | Control Plane: Linear → Cursor Cloud → CI → auto-merge; vault postępu; PWA | `OPS.html`, `docs/ops/`, `host/` |
| `workflow-lab` | Orchestrator tick (heartbeat, merge); warstwa analityczna | `AGENTS.md` §2, `scripts/hermes_ops/` |
| `dsaas-platform-main` | Platforma DSaaS, Kokpit, kanon | `kanon/`, `tenancy/`, runtime |
| `akademia` | Kurs A–G, ▶ TERAZ, eksport JSON | `DASHBOARD.html`, `schema/` |

## 2. Dozwolone przepływy

- **Praca (Linear-first):** Dowódca → issue w Linear (etykieta `agent`, 6 pól) → **`/ops`** (Start / Run next) → orchestrator w `workflow-lab` → PR → CI → auto-merge → **nie** deploy z telefonu.
- **Vault:** `host/progress_vault.py` — sync postępu, heartbeat tick.
- **Dokumentacja:** `docs/ops/` — kontrakty, runbooki, plany.

## 3. Twarde zakazy

1. Kod platformy NIGDY w `workflow-lab`; trening labu NIGDY w `dsaas-platform-main`.
2. `AGENTS.md` kursu NIGDY nie wklejamy do `dsaas-platform-main`.
3. Dashboardu Akademii NIGDY nie iframe'ujemy w Kokpicie.
4. Zero sekretów i tokenów OIDC w `academy_url`, eksporcie i docs.
5. **Telefon nie merguje** i **nie deployuje produkcji** — Approval na `/ops` ≠ Merge na GitHubie (Zasada 11).
6. Deploy = lokalnie, ręcznie (Zasada 11). Zero `workflow_dispatch` w orchestratorze.
7. Tick nie woła `POST /v1/agents` (zakaz drugiego S2).

## 4. Stan stacku (2026-10-04)

| Element | Stan | Znaczenie |
|---|---|---|
| Linear platform (`dsaas-platform-main`) | **PARTIAL → PASS** | Projekt QUI + widoki |
| GitHub | **AKTYWNY** | host `workflow-lab` i platformy |
| **Hermes Ops** (`/ops` + tick VPS) | **WDROŻONE** | Autopilot-only; kontrakt w `docs/ops/` |
| GitLab CE self-hosted | **FUTURE / human-stop VPS** | cutover po W0 |
| Slack | **PARKED** | Linear mobile + GitHub mobile + Cursor |

## 5. Zmiany tego dokumentu

Małe korekty redakcyjne — PR w `hermes-ops-nous`. Zmiana ról/SoT/zakazów — decyzja R1 + wpis w tym pliku (data, powód).

**v1.0 (2026-10-04):** split `akademia` → `akademia` + `hermes-ops-nous`. Control Plane = osobne repo, prawa ręka R1 do prowadzenia workflow i budowania platformy autonomicznie zdalnie w chmurze.
