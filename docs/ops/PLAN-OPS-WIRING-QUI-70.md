# Hermes Ops: okablowanie i uczciwy stan runu (QUI-70)

> Plan do wykonania przez lokalnego agenta Cursora w repo `akademia`.
> Zasada: telefon ma przestać kłamać „running", gdy Cursor Cloud Agent nie wystartował.
>
> **Status 2026-09-22 (wieczór):** Część 1 (T1–T8) = **DONE** (akademia PR #49). Część 2 (E1–E5) = **DONE** na VPS.
> Lab: `workflow-lab@5378d85` (PR #69/#71/#76/#78/#79). Smoke E4: QUI-88 → RUNNING + `workflow-lab#80` z `@cursor` w body; `pr_url=null` aż do realnego PR; `agent.run_url` fail-closed do komentarza Cursor Cloud.
> Deploy Akademia: [`DEPLOY-READY-QUI-70.md`](DEPLOY-READY-QUI-70.md) — po merge #49, ręcznie (Zasada 11).
> **Token:** `GITHUB_OPS_WRITE` tworzy issue, ale **403 na comments** — `@cursor` jest w body; dla niezawodnego triggera dodaj scope *Issues: Write* (komentarze) na fine-grained PAT.

## Diagnoza (fakty, nie zgadywanie)

Autopilot świecił `running`, ale Cursor Cloud Agent nie wystartował (QUI-70 [F-N34]).
Powód: łańcuch narzędzi jest rozcięty na 2 repo + VPS + Cursor Cloud, a telefon pokazuje
`RUNNING` na podstawie **optymistycznego patcha vaulta**, nie faktu, że agent ruszył.

```mermaid
flowchart TD
  phone["OPS.html (telefon)"] -->|"POST /ops/run"| vault["vault akademia: write ops-cmd.json + patch RUNNING"]
  vault -. plik ops-cmd.json .-> tick["workflow-lab: hermes-ops.timer + hermes-ops-cmd.path (cron */15)"]
  tick -->|"@cursor + GITHUB_OPS_WRITE"| cloud["Cursor Cloud Agent (workflow-lab/.cursor/environment.json)"]
  cloud --> pr["PR -> CI -> merge"]
  pr --> status["tick pisze ops-status.json"]
  status --> vault
  vault -->|"GET /ops/status"| phone
```

Punkty pęknięcia (dowody w repo):
- Fałszywe RUNNING: `host/progress_vault.py` `_ops_run()` przy `start`/`run_next` robi
  `patch_ops_status({status:RUNNING})` niezależnie od ticka. To bezpośrednia przyczyna „widzę running".
- Konsument komendy jest poza repo: `ops-cmd.json` czyta tick w `/opt/workflow-lab`
  (handoff `docs/handoffs/2026-09-21-hermes-ops-f0-deployed.md`: `hermes-ops.timer: active`, lab @ `63bd003`).
- Tokeny na VPS: „Run next / merge wymaga `GITHUB_OPS_WRITE`", a `LINEAR_OPS_READ` był „nadal pusty".
- `QUI-70`/`F-N34`/`refuse-` nie istnieją w tym repo — cron */15 i „refuse-" to logika workflow-lab.
- Duchy z poprzedniej sesji (PR #46): pola `pr_url/ci_url/agent/diff/recent` mają 0 wystąpień poza
  plikami zmienionymi w tym PR; realny tick daje `pr_number` (nie `pr_url`), więc dowód/proweniencja
  się nie wypełnią, a `done` jest nieosiągalne (realny sukces pokaże błędne „unverified").

## Zasada projektowa

Telefon nigdy nie pokazuje `RUNNING`, dopóki tick nie potwierdzi. Kontrakt dyspozycji:
`queued → picked_up → running → refused | stalled`. Vault sam wyliczy `stalled`/`no_ack`
przez porównanie `ops-cmd.json` vs świeżości `ops-status.json` (tick żywy = pisze co ~15 min).
`picked_up`/`refused` wymagają, by tick echo-wał `cmd_id` i pisał `refuse-*` — to zadanie
zewnętrzne (E3), ale slot kontraktu robimy tu.

## Reguły repo (twarde — z AGENTS.md)

- Jedno ▶ TERAZ. Brak 7. działu. Bez sekretów. Kontrakt eksportu bez zmian.
- NIE edytować `workflow-lab` z tego repo. E1–E5 to zadania zewnętrzne (tylko dokument tutaj).
- Testy (cała linia z AGENTS.md) muszą być zielone; każdy nowy `scripts/mutation-test-*.py`
  wpięty do CI (`.github/workflows/academy-gate.yml`) i do linii `testy:` w tym samym PR (guard Fala J).
- Commit per logiczna zmiana; PR draft; CI `academy-gate` zielony.

---

## CZĘŚĆ 1 — W tym repo (budujemy + testujemy)

| ID | Zadanie | Pliki | DoD |
| --- | --- | --- | --- |
| T1 | Runbook diagnostyczny QUI-70 (najpierw — nie mamy logów) | `docs/ops/RUNBOOK-OPS-WIRING.md` (nowy) | Komendy VPS (`systemctl status hermes-ops.timer hermes-ops-cmd.path`, `journalctl -u hermes-ops.service --since -1h`, podgląd `ops-cmd.json`/`ops-status.json` mtime+treść, env `GITHUB_OPS_WRITE`/`LINEAR_OPS_READ`, ostatni run `@cursor`) pozwalają przypisać awarię do JEDNEGO ogniwa: (a) tick martwy, (b) brak tokenu, (c) komenda nieodczytana, (d) agent niewyzwolony, (e) agent ruszył, status nie wrócił. Zero komend „na oko". |
| T2 | Koniec fałszywego RUNNING | `host/progress_vault.py` `_ops_run()`, `OPS.html` `send()` | `start`/`run_next` ustawia `queued` (nie `RUNNING`), zachowuje `run_started_at`+`pending_issue`; pigułka „QUEUED". Bez działającego ticka telefon NIGDY nie pokazuje „running". Test w `scripts/test_progress_vault.py` to wymusza. |
| T3 | Koperta komendy + `derive_dispatch` | `host/progress_vault.py` (`write_ops_cmd`, `ops_status_view`/`derive_run`) | `write_ops_cmd` dokłada `id`; `run.dispatch={state,cmd_id,cmd_at,ack_at,refuse_reason}`. Reguły: tick żywy = `age(status.updated_at) < TICK_STALE (~18 min)`; `cmd_at > status.updated_at` świeże → `queued`, przeterminowane → `no_ack`; tick martwy → `stalled` (sygnatura QUI-70); `ack`/`refuse` dla `cmd_id` → `picked_up`/`refused`. Testy pokrywają 6 stanów; `stalled` nie udaje `running`. |
| T4 | Endpoint `/ops/diag` | `host/progress_vault.py` (GET handler) | Read-only, za tą samą autoryzacją. Zwraca: żywotność ticka (wiek `ops-status.json`), ostatnią komendę + wiek, stan dyspozycji, podpowiedź tekstową („tick nie pisał od X min — sprawdź `hermes-ops.timer`"). `curl /ops/diag` jednoznacznie mówi czy tick żyje i czy komenda podjęta. |
| T5 | UI dyspozycji | `OPS.html` (`mapServerVerdict`/`renderVerdict`) | Render `run.dispatch`: `QUEUED / NO-ACK / REFUSED / STALLED` + `refuse_reason` + akcja naprawcza. 4 stany czytelne „jak dla dziecka"; `STALLED`/`NO-ACK` proponują Retry/Take over; guardy Fala L/M i walidator zielone. |
| T6 | Wycięcie duchów (uczciwość na realnych danych) | `OPS.html`, `host/progress_vault.py` (`derive_run`) | Proweniencja/przyciski dowodu renderują się TYLKO gdy realne linki istnieją (koniec „🤖 Cursor" bez linku). `done` opierać o realny `pr_number` + 6/6 kroków PASS (tick merguje po zielonym CI), nie o wymyślone `pr_url`/`pr_state`; brak pełnego dowodu nie krzyczy „unverified" na realnym sukcesie. Przy realnym kształcie `live` (issue/step/steps/checks/pr_number) UI nie pokazuje pustych/mylących elementów; zmergowany run = `done`, nie `unverified`. |
| T7 | Testy + guardy | `scripts/test_progress_vault.py` | Pokrycie: dispatch (queued/no_ack/stalled/picked_up/refused/running), `/ops/diag`, de-ghost. Cała linia `testy:` z AGENTS.md = exit 0, każda fala mutacyjna 100%, CI `academy-gate` zielony. |
| T8 | Kontrakt dla ticka (dokument) | `docs/ops/CONTRACT-OPS-STATUS.md` (nowy) | Dokładny JSON, który tick MUSI pisać: `ack{cmd_id,at}`, `refuse-<id>.json`/`refuse{reason}`, realne pola dowodu (`live.agent{run_url,model}`, `pr_url`, `ci_url`, `diff`, `recent`) spójne z UX z PR #46. Każde pole ma typ, przykład i regułę fail-closed; workflow-lab wdraża bez pytań. |

## CZĘŚĆ 2 — Zewnętrzne (DoD; wykonać poza tym repo)

Przyczyna „agent nie wystartował". NIE edytować z repo akademia — tylko dokument/zlecenie.

| ID | Zadanie | Gdzie | DoD |
| --- | --- | --- | --- |
| E1 | Tokeny VPS | `/etc/workflow-lab/hermes-engineer.env` (chmod 600) | `GITHUB_OPS_WRITE` + `LINEAR_OPS_READ` ustawione; `Run next` realnie wyzwala `@cursor`; koniec `reason=queue_file`/UNKNOWN z braku tokenu. |
| E2 | Żywotność ticka + cron */15 | VPS (systemd) | `hermes-ops.timer` i `hermes-ops-cmd.path` active; ostatni run < 15 min; komenda podjęta ≤ 1 tick; brak zawieszeń między cyklami (sedno QUI-70). |
| E3 | Ack + refuse w ticku | workflow-lab (`hermes_ops`) | Tick echo-uje `cmd_id` (`ack`) i przy odmowie pisze `refuse-<id>.json`/`refuse{reason}` (brak tokenu / cap `OPS_MAX_RUNS_PER_DAY` / LOCK / błąd). `queued`→`picked_up` ≤ 1 tick; odmowa → `refused` z powodem na telefonie. |
| E4 | Trigger @cursor + środowisko Cursor Cloud | workflow-lab + Cursor Cloud | `@cursor` i `workflow-lab/.cursor/environment.json` dowożą realny run + PR. Realny Start na issue testowym otwiera realny run agenta i PR; URL runu wraca do `ops-status.json.live.agent`. |
| E5 | Realne pola dowodu | workflow-lab (tick) | Tick wypełnia `live.agent/pr_url/ci_url/diff` + `recent` wg T8. UI dowodu z PR #46 pokazuje REALNE dane; `done` zielone tylko z kompletem dowodu. |

## Kolejność i weryfikacja

`T1 → (T2, T3, T4, T5, T6) → T7 → T8`, potem `E1, E2` (odblokowują agenta) → `E3, E4, E5`
(domknięcie dowodu). Każdy krok w repo: pełny zestaw testów + krótkie demo na telefonie.
Dowód końcowy dopiero na JEDNYM realnym runie (E4), nie na symulacji.
