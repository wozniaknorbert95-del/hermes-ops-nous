# Raport audytu — Hermes Ops (`/ops`)

**Data:** 2026-10-11  
**Plan:** audyt + plan naprawczy (Fale 1–3)  
**Gałąź:** `fix/ops-blocked-start-ux`  
**Kontrakt:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md) · [`CONTRACT-OPS-STATUS.md`](CONTRACT-OPS-STATUS.md)  
**Deploy tej sesji:** **nie** (Zasada 11 — brak GO)

---

## Executive summary

HUD truth (#93/#96) był już na `main`. Otwarte po splitcie: UX zablokowanego Startu (brak Linear CTA), Retry na non-retryable refuse, 401 `/ops` z marką Akademii, oraz **brak** `scripts/test_progress_vault.py` (DoD). Ta sesja domyka Fale 1–3 w kodzie; live VPS = po GO.

---

## Metody O1–O8

| Faza | Wynik | Dowód |
| --- | --- | --- |
| **O1** docs | **PASS** | README + DEPLOY-READY zsynchronizowane z cienką bramką; ten raport |
| **O2** vault API | **PASS** | `python scripts/test_progress_vault.py` — halt-wins, dispatch, I1, DoR 400, deploy 403, directory 409 |
| **O3** OPS UI | **PASS lokalnie** | Linear CTA, Wymagania przed startem, Zatrzymaj i przejmij, refuse-aware Retry, Jak zacząć |
| **O4** ops-cmd.json | **SKIP live** | Bez SSH/deploy |
| **O5** tick_alive | **SKIP live** | Bez `/ops/diag` na VPS |
| **O6** e2e Linear | **SKIP** | Conductor / Nous = WAITING-GO (parked) |
| **O7** smoke | **PARTIAL** | vault unit PASS; `deploy-ready` wymaga czystego `main` (feature branch = oczekiwany FAIL git) |
| **O8** mutacje | **SKIP** | Fala-* przeniesione do `akademia` przy splitcie |

---

## Findingi zamknięte w tej sesji

| Objaw | Naprawa |
| --- | --- |
| Start zablokowany bez drogi do Linear | `#run-linear` + title DoR; link w nagłówku kolejki |
| Copy „Zanim ruszysz” / Take over EN | „Wymagania przed startem” · „Zatrzymaj i przejmij” |
| Retry przy cap / directory / DoR refuse | `refuseRetryable()` |
| 401 `/ops` = Akademia | `host/auth-gate-ops.html` + nginx `location ^~ /ops` |
| Brak testów vault | `scripts/test_progress_vault.py` + wire AGENTS / deploy-ready |

## Świadomie poza zakresem

- Deploy VPS i smoke publiczny — GO Dowódcy.
- Nous + adapter ticka w `workflow-lab`.
- Rotacja kluczy, Projects landing.

---

## Werdykt

```
REPO: hermes-ops-nous
AUDYT: HUD | UX/UI | vault | docs
PLIK: OPS.html + host/ + scripts/test_progress_vault.py
GATE: PASS (lokalnie) · live VPS SKIP
STOP: brak GO deploy
NEXT: merge PR → GO Dowódcy → /ops-deploy → re-walk live C2/H1
```
