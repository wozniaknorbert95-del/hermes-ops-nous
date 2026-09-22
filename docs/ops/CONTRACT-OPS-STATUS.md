# Kontrakt `ops-status.json` / `ops-cmd.json` (QUI-70)

> Dla ticka w **workflow-lab** (`hermes-ops`). Vault Akademii **czyta** ten JSON
> i wylicza `run.dispatch` / `run.verdict`. Tick **pisze** — bez zgadywania pól.
>
> Powiązane: [`PLAN-OPS-WIRING-QUI-70.md`](PLAN-OPS-WIRING-QUI-70.md) ·
> [`RUNBOOK-OPS-WIRING.md`](RUNBOOK-OPS-WIRING.md) · `GET /ops/diag`.

**Fail-closed:** brak pola / zły typ / pusty URL = telefon **nie** pokazuje dowodu
ani `running`/`done`. Lepiej `stalled`/`queued` niż kłamstwo HUD.

---

## 1. `ops-cmd.json` (pisze vault, czyta tick)

| Pole | Typ | Przykład | Reguła |
| --- | --- | --- | --- |
| `id` | string (hex ≤16) | `"a1b2c3d4e5f60718"` | **Wymagane.** Vault zawsze dokłada. Tick MUSI echo-wać w `ack.cmd_id` / `refuse`. |
| `action` | string | `"start"` | Jedno z: `start`, `run_next`, `retry`, `run_all`, `pause`, `stop`, `take_over`, `set_mode`, … |
| `issue_id` | string | `"QUI-70"` | Może być puste przy `pause`/`set_mode`. |
| `mode` | string | `"AUTOPILOT"` | Przy `set_mode`. |
| `at` | ISO-8601 UTC | `"2026-09-22T18:00:00Z"` | Czas zapisu komendy. Porównywany z `status.updated_at`. |

Przykład:

```json
{
  "id": "a1b2c3d4e5f60718",
  "action": "start",
  "issue_id": "QUI-70",
  "mode": "",
  "at": "2026-09-22T18:00:00Z"
}
```

---

## 2. `ops-status.json` — rdzeń (pisze tick co cykl)

| Pole | Typ | Przykład | Reguła fail-closed |
| --- | --- | --- | --- |
| `ok` | bool | `true` | Zawsze `true` gdy plik kompletny. |
| `updated_at` | ISO-8601 UTC | `"2026-09-22T18:05:00Z"` | **Żywotność ticka.** Vault: `age < ~18 min` ⇒ tick żywy. Brak / stary ⇒ `stalled` (NIGDY `running`). |
| `mode` | string | `"AUTOPILOT"` | `MANUAL` \| `AUTOPILOT` \| `SUPERVISED`. |
| `engine` / `status` | string | `"RUNNING"` | `PAUSED` \| `QUEUED` \| `RUNNING` \| `STOPPED`. **`RUNNING` tylko gdy tick naprawdę prowadzi run** (ma `live.issue` + ack). |
| `reason` | string | `"tick_ok"` | Krótki kod, nie sekret. |
| `lanes` | object | `{ "autopilot": [], "manual": [], "local": [] }` | Kolejki Linear. Puste ≠ błąd. |
| `today` | object | `{ "runs": 1, "merged": 0, "failed": 0 }` | Liczniki dnia. |
| `live` | object \| `{}` | patrz §4 | Bez `live.issue` telefon nie pokazuje postępu kroków. |

---

## 3. Ack i refuse (E3 — obowiązkowe dla `picked_up` / `refused`)

### 3a. `ack` w `ops-status.json`

| Pole | Typ | Przykład | Reguła |
| --- | --- | --- | --- |
| `ack.cmd_id` | string | `"a1b2c3d4e5f60718"` | **Musi = `ops-cmd.json.id`.** Inaczej vault zostaje w `queued`/`no_ack`. |
| `ack.at` | ISO-8601 UTC | `"2026-09-22T18:00:05Z"` | Czas podjęcia komendy. |

```json
"ack": { "cmd_id": "a1b2c3d4e5f60718", "at": "2026-09-22T18:00:05Z" }
```

### 3b. Odmowa — plik **lub** blob

**Preferowane:** plik obok statusu:

`refuse-<cmd_id>.json`:

```json
{ "cmd_id": "a1b2c3d4e5f60718", "reason": "missing_GITHUB_OPS_WRITE", "at": "2026-09-22T18:00:06Z" }
```

**Alternatywa:** w statusie:

```json
"refuse": { "cmd_id": "a1b2c3d4e5f60718", "reason": "missing_GITHUB_OPS_WRITE" }
```

| `reason` (przykłady) | Znaczenie |
| --- | --- |
| `missing_GITHUB_OPS_WRITE` | Brak tokenu (E1) |
| `missing_LINEAR_OPS_READ` | Brak Linear |
| `cap_OPS_MAX_RUNS_PER_DAY` | Limit dnia |
| `lock` | Inny run trzyma LOCK |
| `unknown_action` | Komenda nieobsługiwana |

Fail-closed: odmowa **bez** `cmd_id` zgodnego z komendą → telefon może nie pokazać `REFUSED`
(zostanie `queued`/`no_ack`). Zawsze echo `cmd_id`.

---

## 4. `live` — przebieg + dowód (E4/E5)

| Pole | Typ | Przykład | Reguła fail-closed |
| --- | --- | --- | --- |
| `live.issue` | string | `"QUI-70"` | Wymagane przy realnym runie. Brak + `status=RUNNING` ⇒ vault: `starting` (handoff), nie zielony postęp. |
| `live.step` | int | `3` | Aktualny krok 1–6. |
| `live.action` | string | `"@cursor"` | Co tick właśnie robi. |
| `live.steps` | array | `[{ "step": 1, "status": "PASS" }, …]` | Status: `PASS` \| `FAIL` \| `RED` \| `PENDING`. **`done` wymaga ≥6 `PASS`.** |
| `live.pr_number` | int \| string | `48` | **Kanoniczny dowód sukcesu.** `done` = `pr_number` + 6/6 PASS. Bez numeru PR → nie `done`. |
| `live.pr_url` | string URL https | `"https://github.com/org/repo/pull/48"` | Opcjonalne. Puste ⇒ brak przycisku PR (OK). **Nie** wymyślać. |
| `live.ci_url` | string URL https | `"https://github.com/org/repo/actions/runs/1"` | Opcjonalne. Tylko realny link. |
| `live.pr_state` | string | `"open"` | Opcjonalne. UI nie opiera `done` o to pole. |
| `live.agent` | object | patrz niżej | Proweniencja. Bez `run_url` ⇒ **zero** badge „Cursor". |
| `live.diff` | object \| string | `{ "files": 3, "summary": "…" }` | Opcjonalne podsumowanie. |
| `live.recent` | array | `[{ "at": "…", "text": "…" }]` | Opcjonalny log. Brak ⇒ sekcja ukryta. |
| `live.checks` | object | `{ "ci": "PASS" }` | Opcjonalne. |

### `live.agent`

| Pole | Typ | Przykład | Reguła |
| --- | --- | --- | --- |
| `provider` | string | `"cursor-cloud"` | Puste OK jeśli jest `run_url` z cursor.com (vault doda label). |
| `run_url` | string URL https | `"https://cursor.com/agents/…"` | **Jedyny** warunek pokazu proweniencji. Fail-closed: brak URL = brak UI agenta. |
| `model` | string | `"claude-…"` | Opcjonalne. |
| `run_id` | string | `"bc-…"` | Opcjonalne. |

```json
"live": {
  "issue": "QUI-70",
  "step": 6,
  "action": "@cursor",
  "steps": [
    { "step": 1, "status": "PASS" },
    { "step": 2, "status": "PASS" },
    { "step": 3, "status": "PASS" },
    { "step": 4, "status": "PASS" },
    { "step": 5, "status": "PASS" },
    { "step": 6, "status": "PASS" }
  ],
  "pr_number": 48,
  "pr_url": "https://github.com/example/workflow-lab/pull/48",
  "ci_url": "https://github.com/example/workflow-lab/actions/runs/123",
  "agent": {
    "provider": "cursor-cloud",
    "run_url": "https://cursor.com/agents/abc",
    "model": "composer",
    "run_id": "abc"
  },
  "diff": { "files": 4, "summary": "ops wiring" },
  "recent": [{ "at": "2026-09-22T18:10:00Z", "text": "PR opened" }]
}
```

---

## 5. Stany `run.dispatch` (wylicza vault — tick ich nie pisze)

| Stan | Warunek (skrót) | Telefon |
| --- | --- | --- |
| `idle` | Brak worker-action / brak `cmd.id` | cisza |
| `queued` | Tick żywy, `cmd.at` > `updated_at`, wiek cmd < ~20 min, brak ack | QUEUED |
| `no_ack` | Tick żywy, komenda stara / status po cmd bez ack | NO-ACK |
| `stalled` | Tick martwy (`updated_at` ≥ ~18 min) + świeża komenda worker | STALLED — **nigdy `running`** |
| `picked_up` | `ack.cmd_id` = cmd.id, jeszcze nie RUNNING+live | podjęte |
| `running` | ack + `status=RUNNING` + `live.issue` | RUNNING (tylko wtedy) |
| `refused` | `refuse` / `refuse-<id>.json` dla cmd.id | REFUSED + reason |

**Werdykt `done`:** `live.pr_number` obecny **oraz** 6/6 `PASS` (lub `live.done=true`).
Brak `pr_url` / `agent.run_url` **nie** degraduje do `unverified`.

---

## 6. Minimalny happy-path ticka (checklista implementera)

1. Odczytaj `ops-cmd.json` → zapisz `ack{cmd_id,at}`.
2. Odśwież `updated_at` (nawet przy idle — utrzymuje tick_alive).
3. Przy starcie: `status=RUNNING`, wypełnij `live.issue` + kroki.
4. Po `@cursor`: wpisz `live.agent.run_url` **dopiero gdy URL istnieje**.
5. Po PR: `live.pr_number` (+ opcjonalnie `pr_url`/`ci_url`).
6. Przy odmowie: `refuse-<id>.json` z `reason`, **nie** udawaj RUNNING.
7. Nigdy nie ustawiaj `status=RUNNING` bez `live.issue`.

---

## 7. Poza tym repo (E1–E5)

Tokeny, systemd timer/path, ack/refuse w kodzie ticka, trigger `@cursor`,
wypełnianie pól dowodu — **workflow-lab + VPS**. Ten dokument jest SoT kształtu JSON.
