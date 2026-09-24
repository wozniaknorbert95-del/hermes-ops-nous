# Raport audytu — Hermes Ops (`/ops`)

**Data:** 2026-09-24  
**Plan:** [`AUDYT-PLAN-HERMES-OPS-2026-09-24.md`](AUDYT-PLAN-HERMES-OPS-2026-09-24.md) (GO Dowódcy, sesja HERMES OPS ONLY)  
**Repo SHA:** `5c955f7` (`main`, merge PR #63 — docs + IA Akademii; `OPS.html` nietknięty w tym PR)  
**Kontrakt:** [`HERMES-ROLE-CONTRACT.md`](HERMES-ROLE-CONTRACT.md) · [`CONTRACT-OPS-STATUS.md`](CONTRACT-OPS-STATUS.md)  
**Deploy tej sesji:** **nie** (brak GO Zasada 11)

---

## Executive summary

Fail-closed HUD na `/ops` **trzyma się kontraktu**: Autopilot-only, Start → QUEUED (nigdy RUNNING bez ticka), UNKNOWN nie jest zielone, Approval ≠ Merge, brak S-deploy w orchestratorze, `POST /hermes/chat` = **410**. Vault + mutacje Fala M/N lokalnie **PASS**. VPS (read-only): `tick_alive: true`, timer/path **active**, `MakeDirectory=false`, public `/ops` 200, **SMOKE PASS**.

Jedyna luka Ops na hoście: **brak pliku** `/opt/akademia/data/ops-cmd.json` (to **nie** jest katalog — stary trap Docker/path nie wrócił). Smoke traktuje to jako WARN; vault utworzy plik przy pierwszym Start. Redeploy `/ops` **nie jest wymagany** — HUD #59–#61 już na VPS. Redeploy Akademii (6 zakładek) to osobna sesja Cloud/Dowódcy.

O6 (e2e Linear S0–S6) **pominięte** — brak issue testowego labu; QUI-92 jest prawdziwą pracą In Progress.

---

## Metody

| Faza | Wynik | Dowód |
| --- | --- | --- |
| **O1** docs | **PASS** | ROLE / HOWTO / CONTRACT / RUNBOOK / `docs/ops/README` spójne (Autopilot, 410, brak S-deploy, telefon nie merguje) |
| **O2** vault API | **PASS** | `test_progress_vault.py` PASS; VPS `POST /hermes/chat` → 410 `academy_llm_retired`; `/ops/diag` `ok:true` |
| **O3** OPS UI 360px | **PASS** | `innerWidth=360`; Autopilot pill; Take over; Run next → QUEUED (nie RUNNING); STALLED copy w JS; Approval „nie Merge”; 0 przycisków Merge |
| **O4** ops-cmd.json | **PASS z P2** | Nie katalog; `MakeDirectory=false`; plik **nie istnieje** (smoke WARN) |
| **O5** tick_alive | **PASS** | `/ops/diag` `tick_alive: true` (age ~54 s); `hermes-ops.timer` + `hermes-ops-cmd.path` = active; hint runbook |
| **O6** e2e Linear | **SKIP** | Brak issue test/lab; nie Start na QUI-92 / Done QUI-70 |
| **O7** smoke | **PASS** | `bash scripts/deploy-ready-hermes-ops.sh` lokalnie PASS; `smoke-hermes-ops-vps.sh` na VPS **SMOKE PASS** (bez nowego deploy) |
| **O8** Fala M/N | **PASS** | 9/9 + 9/9, **0 PRZEPUSZCZONE** |

`engineer_loop_e2e`: nadal `true` ([`engineer-loop-e2e.json`](engineer-loop-e2e.json), verified 2026-09-20) — tej sesji **nie** odtwarzano S0–S6.

---

## Findingi

### P2 — `ops-cmd.json` znika między deployami — **CLOSED w kodzie (2026-09-24 igła vault)**

| | |
| --- | --- |
| **Objaw** | Na VPS `ls` nie widzi `/opt/akademia/data/ops-cmd.json`. `is_dir=false`. Dispatch = `idle`. |
| **Przyczyna** | Tick unlink po ACK; `main()` vaulta nie tworzył pliku. Smoke WARN mylił idle z awarią. |
| **Naprawa** | `ensure_ops_cmd_file()` przy starcie procesu (`{}` JSON); `/health.ops_cmd_state`; smoke: missing = idle PASS, katalog = FAIL. **Live VPS** zamknie się po GO deploy / restarcie vaulta. |
| **Lekcja** | Smoke WARN ≠ trap katalogu. Trap = `d` w `ls -ld`. |

### P2 — kanoniczne zdanie ROLE vs 410

`HERMES-ROLE-CONTRACT` strzeże CI zdaniem **„POST /hermes/chat nie ma narzędzi MCP.”** Runbook VPS i vault mówią **410 Gone**. To się nie gryzie (emerytura ⊆ brak MCP). Handoffy z 2026-09-20/21 (czat 200, 4 zakładki, MANUAL/SUPERVISED) są **archiwum** — nie SSoT.

### Świadomie poza zakresem

- `DASHBOARD.html`, welcome, plan audytu Akademii — sesja Cloud.
- Orchestrator tick w `workflow-lab` — read-only (timer żywy).
- Deploy VPS — czeka na GO Dowódcy.

---

## O3 — notatki 360px (lokalny `http.server`, bez vault)

- Pill: **AUTOPILOT** (brak Manual/Supervised).
- Banner UNKNOWN: „nie tapnij Run next w ciemno”.
- Run next (włączony w teście) → pill **QUEUED**, dispatch: „Bez świeżego ticka nie ma running.”
- Take over obecny; Sterowanie: Pause / Stop / Retry.
- Approval: „Status i laptop — nie Merge z telefonu.”
- SyntaxError `DOCTYPE` na `/ops/status` — **tylko localhost bez vault**; na VPS `/ops/status` HTTP 200.

---

## VPS (read-only, 2026-09-24)

```text
/ops/diag: ok=true tick_alive=true tick_age_sec≈54 dispatch=idle
engine=PAUSED status=PAUSED mode=AUTOPILOT reason=vps_timer
systemd: timer=active path=active service=inactive (timer kick — OK)
MakeDirectory=false
POST /hermes/chat: 410 {"ok":false,"reason":"academy_llm_retired"}
public GET /ops: 200
OPS.html na hoście: Take over, STALLED, AUTOPILOT, target_repo_create_forbidden (HUD #61)
smoke-hermes-ops-vps.sh: SMOKE PASS (WARN: brak ops-cmd.json)
mtime OPS.html / progress_vault.py: 2026-09-23 23:00
```

Zero sekretów w tym raporcie.

---

## Checklist kontraktu

| Reguła | Status |
| --- | --- |
| Telefon nie merguje | OK (HOWTO + UI Approval) |
| Brak S-deploy w orchestratorze | OK (ROLE § maszyna stanów) |
| RUNNING tylko po ack + live.issue | OK (CONTRACT + test_progress_vault + UI QUEUED) |
| UNKNOWN nigdy nie zielone | OK (pill unk + banner) |
| Autopilot-only | OK (OPS.html + VPS mode) |
| 410 `/hermes/chat` | OK (vault + VPS) |
| Zero sekretów w diag | OK (diag bez tokenów) |

---

## Następne kroki

1. **Nie deploy** aż GO Dowódcy (Akademia 6 zakładek na `/` to osobna sesja).
2. Przy następnym GO: `bash scripts/deploy-akademia-vps.sh` → ponownie `ensure_hermes_ops_cmd_file` + `smoke-hermes-ops-vps.sh`.
3. O6 kiedy Dowódca da **issue testowe labu** (nie QUI-92).

**Podpis:** Hermes Ops audit (lokalny agent, 2026-09-24).
