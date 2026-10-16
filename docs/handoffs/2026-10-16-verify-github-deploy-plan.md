# Handoff — weryfikacja poprawek + porządek GitHub + plan deploy (2026-10-16)

**Repo:** `hermes-ops-nous` @ `main` `bad926c`  
**Zasada 11:** ten plik = plan. Deploy dopiero po jawnym GO Dowódcy.

## 1. Weryfikacja poprawek (profesjonalna)

| Warstwa | Stan | Dowód |
| --- | --- | --- |
| SoT `todo.json` 1.1.0 | PASS | `validate_todo_nous.py` · tor `NOUS-PRODUCT-LOOP` · aktywne `HON-OPS-ORPHAN` |
| Vault unit | PASS | `test_progress_vault.py` OK |
| Product-loop docs | PASS | HOWTO 5 kroków · Direction Lock · AGENTS · F9 reject |
| HUD decyzja `#hud-truth` | na `main` | `paintHudDecision` w `OPS.html` (SHA lokalny MD5 `e7628adb…`) |
| HON-OPS-PROD-01 | PASS | QUI-41 → create_ms=4578 → https://cursor.com/agents/bc-fdc99f29-ccaf-457e-ae6c-2c54ddeac95e |
| PR #6 / #7 | MERGED | SoT + handoff PROD |

### Drift VPS (blocker deploy)

| Artefakt | `main` (laptop) | VPS `/opt/akademia` |
| --- | --- | --- |
| `OPS.html` mtime | 2026-10-16 (PR #6) | **2026-10-11** (stary) |
| MD5 | `e7628adbf5d584c1f3c64692d979afd9` | `45414c94145ed76b9f350e907650e445` |
| Linia **Teraz:** / baner Nous | w kodzie | **brak na prod** |

Wniosek: mózg (conductor) i vault API działają; **HTML Control Plane na VPS jest za `main`**. Smoke produktowy Start nie wymaga nowego HTML — ale UX decyzji tak.

### VPS runtime (read-only 2026-10-16 ~21:30 CEST)

| Check | Wynik |
| --- | --- |
| `akademia-vault` docker | Up healthy |
| `hermes-conductor` | Up |
| `hermes-ops.timer` + `path` | active |
| `/ops/diag` tick_alive | true (age ~294s — pod progiem stale) |
| dispatch | idle · `ops_cmd_state=missing` (legal po ACK) |
| status | STOPPED po stop QUI-41 · URL sesji w `live.agent` (historyczny) |

## 2. Porządek GitHub

| Akcja | Stan |
| --- | --- |
| Open PR | **0** |
| Zmergowane #1–#7 | OK |
| Usunięte remote po merge (wcześniej) | `chore/*`, `feat/*`, `fix/*`, `docs/hon-ops-prod-01-pass` |
| Usunięte w tej sesji | `docs/conductor-t1c-pass`, `docs/verify-merge-deploy` |
| Docelowy remote | tylko `main` (+ ochrona branch) |

## 3. Plan deploy (GO wymagane)

**Cel:** wyrównać `/opt/akademia` z `origin/main` `bad926c` (albo nowszy HEAD), bez ruszania conductor image (już OK po #108).

### Preflight (przed GO)

```bash
cd hermes-ops-nous
git checkout main && git pull --ff-only origin main
git status   # czysto
python scripts/validate_todo_nous.py
python scripts/test_progress_vault.py
bash scripts/deploy-ready-hermes-ops.sh   # jeśli obecny
```

### Execute (po GO)

```bash
# Git Bash / laptop z SSH do VPS
bash scripts/deploy-akademia-vps.sh
```

Skrypt pakuje working copy — **musi** być czysty `main` == `origin/main`.

### Post-deploy smoke

```bash
bash scripts/smoke-hermes-ops-vps.sh
# na VPS:
curl -fsS http://127.0.0.1:8097/health
curl -fsS http://127.0.0.1:8097/ops/diag
# MD5 OPS.html == lokalny main
md5sum /opt/akademia/OPS.html
# Public (Basic Auth):
# https://akademia.quietforge.flexgrafik.nl/ops
# Oczekiwane: baner „Nous na VPS · brak aktywnej sesji…” + linia Teraz: przy idle
```

### DoD deploy

- [ ] `HEAD` deploy = `origin/main`
- [ ] MD5 `OPS.html` VPS = laptop main
- [ ] smoke PASS · diag `tick_alive=true` · idle
- [ ] HUD: `paintHudDecision` widoczna (Teraz:)
- [ ] Handoff deploy z SHA + smoke (osobny plik)

### Poza zakresem tego deploy

- Rebuild `hermes-conductor` image (niepotrzebny)
- Unfreeze polish / chat (F4/F5 BLOCKED)
- `HON-OPS-ORPHAN` — obserwacja po kolejnym Start, nie blokuje deploy HTML

### Rollback

```bash
# poprzedni tar nie zawsze trzymany — redeploy starszego main SHA
git checkout <sha-przed-031f153>
bash scripts/deploy-akademia-vps.sh --force   # tylko świadomie
git checkout main
```

## 4. NEXT

1. **GO Dowódcy** → `bash scripts/deploy-akademia-vps.sh` + smoke + handoff.
2. `HON-OPS-ORPHAN` — po kolejnym Start sprawdzić brak create-spam.
3. QUI-41 Cloud sesja — monitor PR platformy (poza tym repo).
