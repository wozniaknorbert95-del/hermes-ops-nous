# Runbook — diagnostyka okablowania Hermes Ops (QUI-70)

> Cel: jednym przebiegiem na VPS przypisać awarię „telefon świeci running / agent nie ruszył”
> do **jednego** ogniwa. Zero komend „na oko”.

**Powiązane:** [`PLAN-OPS-WIRING-QUI-70.md`](PLAN-OPS-WIRING-QUI-70.md) · [`CONTRACT-OPS-STATUS.md`](CONTRACT-OPS-STATUS.md) · `GET /ops/diag` (vault Akademii).

## Ogólna procedura (5 minut)

```bash
ssh vcms-vps   # albo root@VPS
```

Uruchom bloki poniżej **po kolei**. Zatrzymaj się przy pierwszym FAIL — to Twoje ogniwo.

---

## A) Tick martwy?

```bash
systemctl is-active hermes-ops.timer hermes-ops-cmd.path hermes-ops.service
systemctl status hermes-ops.timer hermes-ops-cmd.path --no-pager -l | head -40
journalctl -u hermes-ops.service --since '1 hour ago' --no-pager | tail -80
```

| Objaw | Werdykt |
| --- | --- |
| `timer` / `path` ≠ `active` | **(a) tick martwy** — `systemctl enable --now hermes-ops.timer hermes-ops-cmd.path` |
| Brak wpisów w journalu >15 min | **(a) tick martwy** — sprawdź unit + Python path w service |
| Journal: traceback / exit ≠ 0 | **(a) tick martwy** — napraw skrypt w `/opt/workflow-lab` |

---

## B) Brak tokenu?

```bash
# NIE wypisuj wartości sekretów — tylko obecność / długość.
sudo grep -E '^(LINEAR_OPS_READ|GITHUB_OPS_WRITE)=' /etc/workflow-lab/hermes-engineer.env \
  | sed -E 's/=.+/=<set len='\''$(echo -n "$(cut -d= -f2- <<<"$REPLY")" | wc -c)'\''>/'
# prostszy wariant (zero wartości):
sudo awk -F= '/^(LINEAR_OPS_READ|GITHUB_OPS_WRITE|GITHUB_OPS_COMMENT)=/{print $1"="(length($2)>0?"SET":"EMPTY")}' \
  /etc/workflow-lab/hermes-engineer.env
```

| Objaw | Werdykt |
| --- | --- |
| `GITHUB_OPS_WRITE=EMPTY` | **(b) brak tokenu** — bez tego create issue / merge nie ruszy |
| `GITHUB_OPS_COMMENT=EMPTY` | **(b) brak tokenu komentarza** — Start nie obudzi Cloud (`cursor_wake_*`) |
| `LINEAR_OPS_READ=EMPTY` i `reason=queue_file` / UNKNOWN | **(b) brak tokenu** Linear — kolejka z pliku albo fail-closed |
| Oba SET, ale tick pisze `refuse` / `missing_*` / `cursor_wake_*` | **(b)** token odrzucony / scope — COMMENT musi mieć Issues write |

---

## C) Komenda nieodczytana?

```bash
ls -la --time-style=long-iso /opt/akademia/data/ops-cmd.json /opt/akademia/data/ops-status.json
python3 - <<'PY'
import json, time
from pathlib import Path
from datetime import datetime, timezone

def age(p):
    if not p.is_file():
        return None
    return time.time() - p.stat().st_mtime

cmd_p = Path('/opt/akademia/data/ops-cmd.json')
st_p = Path('/opt/akademia/data/ops-status.json')
cmd = json.loads(cmd_p.read_text()) if cmd_p.is_file() else {}
st = json.loads(st_p.read_text()) if st_p.is_file() else {}
print('cmd_id=', cmd.get('id'), 'action=', cmd.get('action'), 'at=', cmd.get('at'))
print('status.updated_at=', st.get('updated_at'), 'engine=', st.get('engine'), 'status=', st.get('status'))
print('ack=', st.get('ack'))
print('mtime_age_cmd_s=', round(age(cmd_p) or -1), 'mtime_age_status_s=', round(age(st_p) or -1))
PY
# Po tapnięciu Start na telefonie — path unit powinien od razu kicknąć tick:
journalctl -u hermes-ops.service --since '5 min ago' --no-pager | tail -30
```

| Objaw | Werdykt |
| --- | --- |
| `ops-cmd.json` świeży, `ops-status.json` stary (>18 min), path inactive | **(c) komenda nieodczytana** — path unit / bind-mount |
| Cmd nowszy niż status, journal bez nowego startu po `PathChanged` | **(c)** — path nie widzi pliku (Docker volume / rights) |
| `ops-cmd.json` jest **katalogiem** (`ls -ld` → `d`) | **(c)+filesystem** — `409 ops_cmd_path_is_directory`; napraw: `rm -rf` + `touch` pliku, albo `bash scripts/setup-akademia-vps.sh` / `install-hermes-ops-vps.sh`. Przyczyna: stary `MakeDirectory=true` w `hermes-ops-cmd.path` (lab: `MakeDirectory=false`). |
| Status ma `ack.cmd_id` = cmd.id | Komenda **odczytana** — idź do D |

Szybko z Akademii (bez SSH treści):

```bash
curl -fsS -u academy:HASLO https://akademia…/ops/diag | python3 -m json.tool
```

---

## D) Agent niewyzwolony?

```bash
# Ostatni tick powinien logować próbę @cursor / GITHUB_OPS_WRITE.
journalctl -u hermes-ops.service --since '1 hour ago' --no-pager | grep -iE 'cursor|refuse|ops_write|run_next|trigger' | tail -40
ls -la /opt/akademia/data/refuse-*.json 2>/dev/null | tail -5
```

| Objaw | Werdykt |
| --- | --- |
| `refuse-*.json` / `refuse.reason` = brak tokenu / cap / LOCK | **(d) agent niewyzwolony** — odmowa ticka (patrz powód) |
| Tick ACK, zero triggera `@cursor`, zero run URL | **(d)** — trigger / `environment.json` (zadanie E4 poza Akademią) |
| Cap `OPS_MAX_RUNS_PER_DAY` | **(d)** — limit dnia |

---

## E) Agent ruszył, status nie wrócił?

```bash
python3 - <<'PY'
import json
from pathlib import Path
st = json.loads(Path('/opt/akademia/data/ops-status.json').read_text())
live = st.get('live') or {}
print('live.issue=', live.get('issue'), 'step=', live.get('step'), 'pr_number=', live.get('pr_number'))
print('live.agent=', live.get('agent'))
print('status=', st.get('status'), 'engine=', st.get('engine'), 'reason=', st.get('reason'))
PY
# Porównaj z Cursor Cloud / GitHub: czy jest run / PR dla tego issue?
```

| Objaw | Werdykt |
| --- | --- |
| Jest PR / run w Cursor Cloud, `live` puste lub stare | **(e) status nie wrócił** — tick nie zapisuje dowodu (E5) |
| Jest `live.issue` + `pr_number`, telefon nadal QUEUED | Cache / SW — twarde odświeżenie `/ops` |

---

## Mapa ogniw → naprawa

| Ogniwo | Gdzie naprawiać |
| --- | --- |
| (a) tick martwy | VPS systemd (`install-hermes-ops-vps.sh`) — **E2** |
| (b) brak tokenu | `/etc/workflow-lab/hermes-engineer.env` — **E1** |
| (c) komenda nieodczytana | path unit + mount `/opt/akademia/data` — **E2** |
| (d) agent niewyzwolony | workflow-lab tick + `@cursor` — **E3/E4** |
| (e) status nie wrócił | tick pola dowodu — **E5** |

Akademia (to repo) odpowiada tylko za uczciwy HUD: `queued` / `no_ack` / `stalled` / `refused` — nigdy fałszywego `RUNNING` bez potwierdzenia ticka.
