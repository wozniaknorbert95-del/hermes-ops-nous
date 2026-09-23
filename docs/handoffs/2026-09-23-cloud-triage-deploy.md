# Handoff — Cloud triage + deploy Hermes Ops (2026-09-23)

**Repo:** akademia · **GO Dowódcy:** merge + deploy  
**Main:** `c13c346` (PR #54) · **VPS:** deployed 2026-09-23T18:21Z

## Co zrobione (fakty)

### GitHub (Cloud leftover)

| PR | Akcja | Powód |
| --- | --- | --- |
| [#55](https://github.com/wozniaknorbert95-del/akademia/pull/55) Autopilot-only | **closed** | Łamie kontrakt MANUAL \| AUTOPILOT \| SUPERVISED |
| [#46](https://github.com/wozniaknorbert95-del/akademia/pull/46) dowód runu | **closed** | Superseded: QUI-70 T6 + Wake (#49/#52). Rebase cofnąłby `done=pr_number+6/6` do `unverified` bez URL |
| [#47](https://github.com/wozniaknorbert95-del/akademia/pull/47) plan dowodu | **closed** | Plan, nie SSoT |
| [#48](https://github.com/wozniaknorbert95-del/akademia/pull/48) plan QUI-70 | **closed** | Wiring DONE (#49–#53) |
| [#54](https://github.com/wozniaknorbert95-del/akademia/pull/54) deploy-ready docs | **merged** | Historyczny status SSH u Cloud Agenta |
| [#53](https://github.com/wozniaknorbert95-del/akademia/pull/53) preflight + smoke | już na `main` | Deploy w tej sesji |

Otwarte PR-y akademia po sesji: **0**.

### Deploy VPS (`bash scripts/deploy-akademia-vps.sh`)

GO Zasada 11 z laptopa Dowódcy (Cloud Agent nie miał klucza SSH).

| Check | Wynik |
| --- | --- |
| HEAD == origin/main | `c13c346` |
| deploy-ready (pełny zestaw AGENTS.md) | PASS |
| vault `/health` | `{"ok": true, "service": "academy-vault"}` |
| `/ops/diag` tick_alive | **true** (age ~5 s) |
| `ops-cmd.json` | **plik** (nie katalog), pusty aż do Start |
| `hermes-ops-cmd.path` MakeDirectory | **false** (było true → patched w setup) |
| systemd | timer=**active** path=**active** |
| public GET `/ops` | HTTP **200** |
| HTTPS progress envelope | `schema_version` 0.1.0, `source` academy-os |
| smoke-hermes-ops-vps.sh | **SMOKE PASS** |

## Co live

- Akademia: `https://akademia.quietforge.flexgrafik.nl/` (Basic Auth — hasło tylko `CREDENTIALS.local.txt` na VPS)
- Ops: `https://akademia.quietforge.flexgrafik.nl/ops`
- Dispatch bez Start: `idle` + tick żywy (uczciwe, nie fałszywy RUNNING)

## Co zablokowane

- Hermes LLM na VPS: `llm: false` — czat lokalnym silnikiem faktów. Model: `ACADEMY_HERMES_*` w `/opt/akademia/.env` (nie ta sesja).
- Merge z telefonu: nadal zabroniony.
- Autopilot-only: **odrzucone** — trzy tryby zostają, dopóki R1 nie zmieni kontraktu.

## Następny krok (jeden TERAZ)

Telefon: otwórz `/ops` → **Start** → oczekuj **QUEUED**, potem ack ticka (RUNNING albo REFUSED z powodem). Nie RUNNING bez ack.

Kurs TERAZ: A1 jeśli rozdział niezaliczony.

## Komendy weryfikacji

```bash
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
ssh root@185.243.54.115 'curl -fsS http://127.0.0.1:8097/ops/diag; echo; ls -ld /opt/akademia/data/ops-cmd.json; systemctl is-active hermes-ops.timer hermes-ops-cmd.path'
```

## Pliki dotknięte (ta sesja docs)

- `docs/handoffs/2026-09-23-cloud-triage-deploy.md` — ten plik
- `docs/handoffs/2026-09-22-start-to-cloud.md` — handoff poprzedniej sesji (dopisany do git)
- `docs/ops/DEPLOY-READY-HERMES-OPS.md` — SSH blocker zdjęty
- `docs/handoffs/2026-09-23-hermes-ops-awaria-plan.md` — deploy DONE
