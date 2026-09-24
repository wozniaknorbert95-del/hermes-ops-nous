# AI Engineering Academy OS

To repo hostuje **dwa produkty** na jednym originie (VPS + PWA). **Nie** jest Kokpitem QuietForge ani repozytorium `workflow-lab`.

| Produkt | URL | Po co |
| --- | --- | --- |
| **Akademia** | `/` · `DASHBOARD.html` | Darmowy kurs A–G, jedna karta **▶ TERAZ**, sync postępu, eksport JSON |
| **Hermes Ops** | `/ops` · `OPS.html` | Control Plane pracy: Linear → Cursor Cloud → CI → auto-merge (telefon: Start/Pause, **nie** merge) |

**Hermes Ops — start docs:** [`docs/ops/README.md`](docs/ops/README.md) → [`HERMES-OPS-HOWTO`](docs/ops/HERMES-OPS-HOWTO.md) → [`HERMES-ROLE-CONTRACT`](docs/ops/HERMES-ROLE-CONTRACT.md).  
Plan doprecyzowania całej dokumentacji: [`docs/ops/PLAN-AKTUALIZACJI-DOKUMENTACJI-HERMES-2026-09-24.md`](docs/ops/PLAN-AKTUALIZACJI-DOKUMENTACJI-HERMES-2026-09-24.md).

## Zasada nr 1

Codziennie: otwórz `DASHBOARD.html` → zrób to, co pisze na karcie **▶ TERAZ** → zamknij.

Jedno ▶ TERAZ w całym systemie. Kokpit może **pokazać ten sam tekst** po eksporcie JSON — nie uczy.

## Trzy systemy

| System | Gdzie | Co |
| --- | --- | --- |
| Platforma | `dsaas-platform-main` | firma / Kokpit |
| Lab | `workflow-lab` | pętla issue→MR→CI→auto-merge + Jupyter Notebooki (warstwa analityczna, Python, opt-in, gate `execute`) |
| Akademia (tu) | to repo `/` | lekcje + checkpointy |
| Hermes Ops (tu) | to repo `/ops` | pętla inżynierska; orchestrator w `workflow-lab` |

## Tory

- **W (workflow)** — gesty w `workflow-lab` (Git, CI, MR, Linear).
- **F (firma)** — jak gest mapuje się na **istniejące** 6 działów Kokpitu + Taca. Zero siódmego działu.

## Postęp (SSoT)

`localStorage["aea-os"]` = scratchpad przeglądarki, da się podrobić. Kokpit go **nie czyta**.

Eksport (przycisk na dole DASHBOARD) emituje `schema/academy-progress.v0.json`.
Właściciel wkleja plik jako overlay tenanta (`captured`). Projekcja Kokpitu pokazuje % i ▶ TERAZ.

## Cztery poziomy materiału

1. `DASHBOARD.html` — co teraz w **kursie** (codziennie).
2. `OPS.html` (`/ops`) — co teraz w **pracy** (Linear, Autopilot, bez merge z telefonu).
3. `cursor-kurs/` — podręcznik, gdy checkpoint = NIE.
4. `ops/workflow-marzen/` — L3 operacyjne (GitLab CE, incydent). Kopia handbooka; kanon platformy nie mieszka tutaj.

## Dev lokalny

```bash
python -m http.server 8765
# Akademia: http://localhost:8765/DASHBOARD.html
# Hermes Ops: http://localhost:8765/ops
```

Vault (sync, `/ops/status`): osobno `host/progress_vault.py` — patrz `docs/runbooks/AKADEMIA-VPS.md`.

## Absolutne nie

- Nie wklejaj `AGENTS.md` kursu na `dsaas-platform-main`.
- Nie iframe'uj tego dashboardu w Kokpicie.
- Nie ćwicz labu w repo platformy.
