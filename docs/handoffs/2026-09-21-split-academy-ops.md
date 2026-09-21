# Handoff — Split Academy / Ops (Linear-first, auto-merge, deploy lokalny)

**Data:** 2026-09-21  
**Repo:** `akademia` (+ `workflow-lab/scripts/hermes_ops`, `dsaas-platform-main` kontrakt Linear)  
**Status kodu:** T01–T18 zaimplementowane. **Deploy VPS = NIE** (Zasada 11 — czekamy na GO Dowódcy).

## Co jest na `/` a co na `/ops`

| URL | Produkt |
| --- | --- |
| `/` i `DASHBOARD.html` | Darmowa Akademia: 4 zakładki TERAZ / KURS / NOTATKI / DZIEŃ. Działy A–G. Notatki w `_scratch.notes`. Zero DeepSeek. `POST /hermes/chat` → **410**. |
| `/ops` | Hermes Control Plane: Dashboard, Sterowanie, Kolejka (autopilot / manual / local), Live, Approval. Telefon czyta `GET /ops/status` (cache VPS). |
| PWA | Jeden origin. Shortcuts: **Ucz się** / **Praca**. Manifest bez Basic Auth (jak wcześniej). |

## Kontrakt ról (kanon)

`docs/ops/HERMES-ROLE-CONTRACT.md`:

- Decyzja jest w Linear, nie na GitHubie.
- Hermes Engineer + Cursor + CI dowożą aż do merge (lab **i** `dsaas-platform-main`).
- Wgranie na serwer = lokalnie, ręcznie (Zasada 11).
- HITL = etykieta **zanim** ruszy agent. Approval na `/ops` **nie** jest Merge.

`dsaas-platform-main/docs/ops/LINEAR-PLATFORM.md`: **Done** = zmergowane przez pętlę (CI green) + EV + `todo.json`. Human merge nie jest SoT Done.

## Orchestrator (workflow-lab)

Pakiet `scripts/hermes_ops/` + timer `scripts/hermes-ops-tick.py`.

- Router etykiet: `agent` → Autopilot/Manual; `hitl:approval-required` / brak `agent` / `blocked` → local (zero `@cursor`).
- Merge obu repo po zielonym CI. **Brak S-deploy.** `workflow_dispatch` production = deny w kodzie.
- Capy: `OPS_MAX_CONCURRENT=1`, `OPS_MAX_RUNS_PER_DAY=8`. Telemetry JSONL z redakcją sekretów.
- Tokeny (600, nie w git): `LINEAR_OPS_READ`, `GITHUB_OPS_WRITE` (oba repo, merge+comment), `GITHUB_ENGINEER_READ`.

## Testy

Akademia: linia `testy:` w `AGENTS.md` + Fala M.  
Lab: `python scripts/test_hermes_ops.py` w `phone-loop-guard`.  
Platforma: `tests/test_linear_agent_contract.py` (Done ≠ human merge).

## Deploy (gdy GO)

```
bash scripts/deploy-akademia-vps.sh
curl -fsS http://127.0.0.1:8097/health
curl -fsS -u academy:HASLO https://akademia.quietforge.flexgrafik.nl/
curl -fsS -u academy:HASLO https://akademia.quietforge.flexgrafik.nl/ops
```

Timer VPS (osobno, workflow-lab): `python scripts/hermes-ops-tick.py --status-out /ścieżka/ops-status.json`  
Vault Akademii: `HERMES_OPS_STATUS` wskazuje ten plik.

## Świadomie nie zrobione

- Autonomiczny deploy platformy / ENT-12 / restart usług.
- Natywna apka, drugi hostname, 8. dział kursu, iframe Kokpit, MCP w czacie Akademii, `Run all` default ON.
