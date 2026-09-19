# AI Engineering Academy OS

Szkoła. **Nie** jest działem Kokpitu QuietForge. **Nie** jest repozytorium `workflow-lab`.

## Zasada nr 1

Codziennie: otwórz `DASHBOARD.html` → zrób to, co pisze na karcie **▶ TERAZ** → zamknij.

Jedno ▶ TERAZ w całym systemie. Kokpit może **pokazać ten sam tekst** po eksporcie JSON — nie uczy.

## Trzy systemy

| System | Gdzie | Co |
| --- | --- | --- |
| Platforma | `dsaas-platform-main` | firma / Kokpit |
| Lab | `workflow-lab` | pętla issue→MR→CI→auto-merge + Jupyter Notebooki (warstwa analityczna, Python, opt-in, gate `execute`) |
| Akademia (tu) | to repo | lekcje + checkpointy |

## Tory

- **W (workflow)** — gesty w `workflow-lab` (Git, CI, MR, Linear).
- **F (firma)** — jak gest mapuje się na **istniejące** 6 działów Kokpitu + Taca. Zero siódmego działu.

## Postęp (SSoT)

`localStorage["aea-os"]` = scratchpad przeglądarki, da się podrobić. Kokpit go **nie czyta**.

Eksport (przycisk na dole DASHBOARD) emituje `schema/academy-progress.v0.json`.
Właściciel wkleja plik jako overlay tenanta (`captured`). Projekcja Kokpitu pokazuje % i ▶ TERAZ.

## Trzy poziomy materiału

1. `DASHBOARD.html` — co teraz (codziennie).
2. `cursor-kurs/` — podręcznik, gdy checkpoint = NIE.
3. `ops/workflow-marzen/` — L3 operacyjne (GitLab CE, incydent). Kopia handbooka; kanon platformy nie mieszka tutaj.

## Absolutne nie

- Nie wklejaj `AGENTS.md` kursu na `dsaas-platform-main`.
- Nie iframe'uj tego dashboardu w Kokpicie.
- Nie ćwicz labu w repo platformy.
