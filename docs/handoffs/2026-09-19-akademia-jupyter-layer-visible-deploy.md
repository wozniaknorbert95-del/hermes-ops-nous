# Handoff — Akademia: warstwa Jupyter widoczna na dashboardzie + deploy

**Data:** 2026-09-19
**Repo:** `akademia`
**Sesja:** domknięcie luki „Jupyter nigdzie nie widać" → kafel, loopy, diagram warstw, A7; PR #10; deploy VPS
**Gałąź close:** `chore/handoff-jupyter-layer`

---

## Problem, który zamknęliśmy

PR #8 opisał warstwę notebooków (`D-W7-JUPYTER`), ale **nie nazwał jej wprost**:

1. brak kafla w `NARZĘDZIA` — blokada twarda: walidator wymagał `proofHref == 14`,
2. brak w loopach (laptop/telefon pokazywały samo `CI green`),
3. rozdział `A7` był schowany (kontrakt `firstOpen()` otwiera A1, nie A7),
4. w całym `DASHBOARD.html` nie było słowa „Jupyter".

## Co zrobione

| Warstwa | Zmiana |
|---|---|
| Kontrakt | `proofHref` 14 → **15** + twarde checki: `Jupyter`, `D-W7-JUPYTER`, `execute`, `notebook execute`, `DIAGRAMS.layers` |
| `NARZĘDZIA` | kafel **Jupyter Notebook (lab)** (opt-in, dowód `DECISIONS.md`); kafel `CI` przestał kłamać („dsaas 4 workflows" → `validate + execute`) |
| Loopy | `CI green: validate + execute` + **kropkowana** krawędź `notebook execute (opt-in)` w loopie telefonu i laptopa |
| Nowy diagram | `DIAGRAMS.layers` — Node core (validate → auto-merge) vs warstwa analizy (execute, opt-in) |
| `A7` | tytuł z „Jupyter", `pliki` 7 → **14**, +1 krok labu (Cloud Agents z telefonu), rozszerzony DoD |
| Deep-link | `openHashTarget`: `#roz-*` otwiera zwinięty `<details>` i przełącza zakładkę (A → WORKFLOW, B–G → DSAAS); re-scroll po Mermaid z guardem |
| Źródła | `docs.jupyter.org`, `nbstripout` |
| Docs | `OPERATING-MODEL.md` v1.3, `README.md`, `cursor-kurs/szablony/README.md`, `ACADEMY-UX-SPEC.md`, `AUDYT-UX-UI-2026-09-19.md` §7 |

## Weryfikacja wobec SSoT

`workflow-lab@d554af5` (`ci: make execute a required check (always-report) #59`, `feat: Jupyter Notebook analysis layer (D-W7-JUPYTER) #56`).

- Wszystkie **14 plików** z `A7.pliki` istnieje w `workflow-lab/main`.
- Poprawiona precyzja: path-filter joba `execute` to `notebooks/`, `requirements.txt`, `scripts/run-notebooks.sh`, `.github/workflows/notebooks.yml` — **nie** tylko `notebooks/**`.
- `.cursor/Dockerfile` dodaje tylko `python3/pip/venv` (kernel `ci-kernel` rejestruje CI) — opis kafla poprawiony.

## Co live

| Element | Wartość |
|---|---|
| URL | https://akademia.quietforge.flexgrafik.nl/DASHBOARD.html |
| Treść | `main` `5fcf8f9` (#10) |
| Hash `DASHBOARD.html` na VPS | `279a4f7487b363f32c9c7ff04fd7c031` = **1:1 z lokalnym** |
| Vault | `127.0.0.1:8097` healthy, envelope `0.1.0` / `academy-os` |
| Served HTML | `Jupyter` ×4, `proofHref:` ×15, `layers:` ×2 |
| Auth | `/` → **401**, `/progress` bez auth → **401** |
| Walidator na VPS | `PASS: academy export contract + dashboard v3.1` |

## Testy tej sesji

- `python scripts/validate-academy-export.py` → PASS
- `python scripts/test_progress_vault.py` → PASS
- `node --check` na inline JS → PASS
- 15 kafli `NARZĘDZIA`, 3/3 SVG Mermaid w WORKFLOW, zero błędów Mermaid
- 375 px: brak poziomego scrolla, taby 2 rzędy, `--scroll-offset` 128
- `#roz-A7` i `#roz-B2`: details otwarte, właściwa zakładka, lądowanie `top == --scroll-offset` (76 px)

## Co zablokowane / świadomie odłożone

- **Vault: pierwszy realny PUT** — brak dowodu, że sync telefon↔laptop kiedykolwiek zapisał dane. Sprawdzić z telefonu na HTTPS.
- Service worker / offline cache — deploy to tar bez hashowanych nazw → ryzyko serwowania starego HTML.
- Playwright killer-flows — repo nie ma CI/runnera.

## Następny krok (jeden TERAZ)

Wejść na live z telefonu, zalogować vault (`academy` + hasło z `/opt/akademia/CREDENTIALS.local.txt`), kliknąć banner **„Warstwa analityczna" → A7** i potwierdzić, że rozdział otwiera się rozwinięty. To jednocześnie test pierwszego PUT.

## Komendy weryfikacji

```
python scripts/validate-academy-export.py
python scripts/test_progress_vault.py
ssh root@185.243.54.115 "curl -fsS http://127.0.0.1:8097/health"
ssh root@185.243.54.115 "md5sum /opt/akademia/DASHBOARD.html"
```

## Pliki tej sesji

- `DASHBOARD.html`, `scripts/validate-academy-export.py`
- `README.md`, `docs/OPERATING-MODEL.md`, `docs/ACADEMY-UX-SPEC.md`
- `cursor-kurs/szablony/README.md`, `docs/ops/AUDYT-UX-UI-2026-09-19.md`
- ten handoff
