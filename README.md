# Hermes Ops Nous — Control Plane

To repo hostuje **Hermes Ops** — Control Plane pracy: Linear → Cursor Cloud → CI → auto-merge.

| Produkt | URL | Po co |
| --- | --- | --- |
| **Hermes Ops** | `/ops` · `OPS.html` | Control Plane pracy: Linear → Cursor Cloud → CI → auto-merge (telefon: Start/Pause, **nie** merge) |

**Hermes Ops — start docs:** [`docs/ops/README.md`](docs/ops/README.md) → [`HERMES-OPS-HOWTO`](docs/ops/HERMES-OPS-HOWTO.md) → [`HERMES-ROLE-CONTRACT`](docs/ops/HERMES-ROLE-CONTRACT.md).

**Ekosystem:** [`docs/OPERATING-MODEL-HERMES-OPS.md`](docs/OPERATING-MODEL-HERMES-OPS.md) — role, przepływy, zakazy.

## Zasada nr 1

Hermes Ops = prawa ręka R1 do prowadzenia workflow i budowania platformy autonomicznie zdalnie w chmurze.

- Linear-first: issue w Linear (etykieta `agent`, 6 pól) → `/ops` (Start / Run next) → orchestrator → PR → CI → auto-merge.
- **Telefon nie merguje.** Approval na `/ops` = Pause / Stop / laptop / link CI — nie przycisk Merge.
- Deploy = lokalnie, ręcznie (Zasada 11).

## Ekosystem repozytoriów

| System | Gdzie | Co |
| --- | --- | --- |
| Platforma | `dsaas-platform-main` | firma / Kokpit |
| Lab | `workflow-lab` | pętla issue→MR→CI→auto-merge + Jupyter Notebooki |
| Akademia | `akademia` | lekcje + checkpointy |
| **Hermes Ops (tu)** | `hermes-ops-nous` | pętla inżynierska; orchestrator w `workflow-lab` |

## Dev lokalny

```bash
python -m http.server 8765
# Hermes Ops: http://localhost:8765/ops
```

Vault (sync, `/ops/status`): osobno `host/progress_vault.py` — patrz `docs/ops/DEPLOY-READY-HERMES-OPS.md`.

## Absolutne nie

- Nie wklejaj `AGENTS.md` Hermes Ops do `akademia` ani `dsaas-platform-main`.
- Nie iframe'uj `OPS.html` w Kokpicie.
- Nie deployuj bez GO Dowódca.
