# Plan — self-hosted runner na VPS dla `dsaas-platform-main` (szczegółowy, DoD per zadanie)

**Status:** ✅ **WYKONANY w 100% (2026-09-27)** — runner działa, wszystkie workflowy na self-hosted, byte za $0.
**Data:** 2026-09-27 · **Trigger wykonawczy:** Hermes Ops (autonomicznie, wg workflow S0→S6) + Dowódca na sudo VPS.
**Cel:** bramka `gates` (required check) chodzi na VPS za **$0** i odpala się **autonomicznie** na każdym PR, bez żadnego ręcznego wyzwalacza.

---

## 1. Decyzja (przyjęta)

Self-hosted runner na wspólnym VPS (`root@185.243.54.115`). Ten sam `policy-gates.yml` (G1–G34) będzie odpalał się na VPS po zmianie `runs-on: ubuntu-latest → self-hosted`.

**Odrzucone alternatywy (za poprzednią analizą):**
- repo publiczne (wyciek kodu klienta), GitHub Pro (płatne), branch/SHA hack (nie skaluje się), `prod-gate.py --quick` + admin-merge (bypass + niepełna bramka).

---

## 2. Stan faktyczny — co dokładnie wiemy (z czytania źródeł)

### 2.1 Workflowy platformy (6 plików, 12 x `runs-on: ubuntu-latest`)

| Workflow | Trigger | Job/y | Wymaga Dockera? | Rola |
|---|---|---|---|---|
| `policy-gates.yml` | push + PR | `gates` (G1–G34) | **NIE** | **REQUIRED CHECK** (merge) |
| `db-rls.yml` | path-filtered push+PR | `postgres-rls` | **TAK** (service `pgvector:pg16`) | dodatkowy |
| `security.yml` | path-filtered (requirements*) | `dependency-audit` | nie | dodatkowy |
| `policy-gates-ui.yml` | path-filtered (SPA) | `spa-ui-e2e` | nie (Playwright+Chromium) | dodatkowy |
| `nightly-heavy.yml` | schedule 03:30 UTC + dispatch | 7 jobów | **TAK** (container-scan) | nocny |
| `gitleaks.yml` | dispatch-only | stub (deprecated) | nie | historyczny |

### 2.2 Zależności `gates` (kluczowe, z `policy-gates.yml`)
- **Python 3.12** (`actions/setup-python@v5` — sama go ściągnie), **Node 22** (`setup-node@v4`).
- **OPA 1.19.0** (inline `curl` openpolicyagent.org), **gitleaks 8.30.1** (inline `curl` github releases), **trivy** (akcja JS `trivy-action@v0.36.0` → binarka, **bez Dockera** dla `scan-type: fs`).
- **pip**: `requirements-platform-api.txt -db.txt -telemetry.txt pytest pytest-cov pyyaml rdflib pyshacl httpx2 ruff`.
- **npm**: `npm install` (cedar-eval). **Docker: NIE.**

→ **Host runnera dla Fazy A potrzebuje tylko**: curl, tar, git, unzip + sam binary runnera. Resztę workflow ściąga sam inline.

### 2.3 Mechanika triggera (kluczowe dla autonomii)
- `gates` odpala się **automatycznie na zdarzeniu `push`/`pull_request`** — żaden `workflow_dispatch` nie jest potrzebny.
- `workflow_dispatch` w policy Hermes Ops jest **celowo wyłączony** (`allow_deploy` blokuje; deploy-guard).
- Retry realizuje **Cursor agent** (bootstrap: „gate FAIL → 1 retry" przez re-push), nie Hermes Ops.
- Merge realizuje **D-AUTOMERGE** (squash po zielonym) → Hermes Ops `_observe_merge_if_done` odnotowuje DONE.

**Wniosek:** nie dodajemy ŻADNEGO nowego mechanizmu triggerowania testów. Brakującym elementem jest **tylko zawsze-dostępny runner**. Autonomia jest już zaprojektowana — była stubowana przez runner na github-hosted (billing).

---

## 3. Architektura docelowa

```
VPS 185.243.54.115
├── /opt/akademia ........ vault Hermes Ops (host/progress_vault.py) + hermes-engineer.env
├── /opt/workflow-lab .... tick S0→S6 (GITHUB_OPS_WRITE/COMMENT tokeny)
└── /home/actions/ ..... NOWY: self-hosted runner (dedykowany user, NIE root)
        └── ~/actions-runner/_work/dsaas-platform-main/...  ← roboczy checkout z PR

GitHub (dsaas-platform-main)
  └── policy-gates.yml:  runs-on: [self-hosted, dsaas]  → podpina jednego runnera z VPS
```

**Izolacja:** `actions` nie czyta `/opt/akademia`, `/opt/workflow-lab`, `hermes-engineer.env`, żadnych `GITHUB_*` env. Zero sudo. (szczegóły §6).

---

## 4. Faza A — odblokowanie merge'a (T1–T5, bez Dockera)

### T1 — Utworzenie dedykowanego usera `actions` + izolacja
**Kroki (root na VPS):**
```bash
useradd --create-home --shell /bin/bash actions          # NIE root, NIE ma w /etc/sudoers
chmod 750 /home/actions
# Weryfikacja izolacji (musi zwrócić permission denied):
su - actions -c 'ls /opt/akademia /opt/workflow-lab' 2>&1 | grep -i "denied"
```
**DoD:** user `actions` istnieje, bez hasła-login z zewnątrz, nie jest w grupie `sudo`, nie czyta katalogów tenanta.
**Weryfikacja:** `su - actions -c 'sudo -n true'` → exit ≠ 0; `ls /opt/akademia` jako `actions` → denied.

### T2 — Instalacja + rejestracja runnera (jako usługa systemd, auto-start)
**Kroki:**
```bash
# 1) Na GitHub: repo → Settings → Actions → Runners → New self-hosted runner
#    → Linux x64 → skopiuj URL + one-time REG_TOKEN (wygaśnie).
# 2) Na VPS jako user `actions`:
mkdir -p ~/actions-runner && cd ~/actions-runner
curl -o actions-runner.tar.gz -L https://github.com/actions/runner/releases/download/v2.322.0/actions-runner-linux-x64-2.322.0.tar.gz
tar xzf actions-runner.tar.gz
./config.sh --url https://github.com/wozniaknorbert95-del/dsaas-platform-main \
            --token <REG_TOKEN> --unattended --name dsaas-vps-runner --labels dsaas
sudo ./svc.sh install        # instaluje systemd unit actions.runner.*.service (Restart=on-failure)
sudo ./svc.sh start
```
**DoD:** runner widoczny w GitHub jako **`Idle`** (zielony) w Settings → Actions → Runners; systemd unit `enabled` (start przy bootcie) + `Restart=on-failure`.
**Weryfikacja:** `systemctl is-enabled actions.runner.*` → `enabled`; `sudo ./svc.sh status` → running; GitHub panel → `Idle`.

### T3 — Zależności bazowe + weryfikacja toolchainu
**Kroki (root):**
```bash
apt-get update -y && apt-get install -y curl tar git unzip jq ca-certificates
# ew. build-essential libpq-dev libffi-dev libssl-dev — dodaj TYLKO gdy pierwszy
# zielony bieg ujawni wheel bez prekompilowanego binaria (np. psycopg/cryptography).
```
**DoD:** `gates` odpala krok `Setup Python` (3.12) i `Setup Node` (22) bez błędu; pierwszy **pełny** bieg `gates` jest zielony (albo czerwony wyłącznie z powodu realnego testu, nie środowiska).
**Weryfikacja:** `gh run watch` / `gh pr checks 125` → kroki setup-python/setup-node/OPA/gitleaks/trivy OK.

### T4 — Przepnij `gates` na self-hosted
**Zmiana** (1 linia w `.github/workflows/policy-gates.yml`, job `gates`, linia 19):
```yaml
    runs-on: ubuntu-latest        # → zmień na:
    runs-on: [self-hosted, dsaas]
```
**DoD:** `gates` job wchodzi na runnera z VPS (nie github-hosted); nazwa checka bez zmian (= `gates`, wymóg branch protection).
**Weryfikacja:** nowy commit na PR #125 → job `gates` w UI pokazuje runnera `dsaas-vps-runner`; brak błędu „payments failed".

### T5 — Re-run `gates` na PR #125 → zielony → merge Atom 0
**Kroki:**
```bash
# push T4 na branch, który re-triggeruje `gates` na PR #125 (chore/cursor-env-hygiene)
gh pr checks 125 --repo wozniaknorbert95-del/dsaas-platform-main --watch
# po PASS:
gh pr merge 125 --repo wozniaknorbert95-del/dsaas-platform-main --squash --delete-branch
```
**DoD:** PR #125 (`chore/cursor-env-hygiene`, atom 0) zmergowany **bez** `--admin`; bilans minut Actions dla repo = **0** za ten bieg.
**Weryfikacja:** `gh pr view 125 --json state` → `MERGED`; `gh api /repos/.../actions/billing` → used_minutes nie rośnie.

**Wyjście Fazy A:** pełna autonomiczna bramka merge dla platformy działa na VPS, $0, bez Dockera.

---

## 5. Faza B — zero minut na zawsze (T6–T8)

### T6 — Docker + Playwright/Chromium (dla pozostałych workflowów)
**Kroki (root):**
```bash
# Docker (do db-rls service postgres + nightly container-scan):
curl -fsSL https://get.docker.com | sh
usermod -aG docker actions          # runner buduje obrazy bez sudo
# Playwright/Chromium (do spa-ui-e2e) instalują się inline w workflow
# (`python -m playwright install --with-deps chromium`) — runner musi mieć
# uprawnienia apt-get lub deps zainstalowane: libnss3 libatk-* (instaluje --with-deps).
```
**DoD:** `docker run hello-world` jako user `actions` → OK; `nightly-heavy` job `container-scan` + `db-rls` service `postgres` startują.
**Weryfikacja:** `su - actions -c 'docker run --rm hello-world'` → „Hello from Docker".

### T7 — Przepnij pozostałe 11 x `runs-on` → self-hosted
**Zmiany** (ta sama 1-linijka w 5 plikach):
- `db-rls.yml:35`, `security.yml:31`, `policy-gates-ui.yml:29`, `gitleaks.yml:15`
- `nightly-heavy.yml:20,42,83,105,123,138,165` (7 jobów)
- wszystkie `runs-on: ubuntu-latest` → `runs-on: [self-hosted, dsaas]`

**DoD:** zero `ubuntu-latest` w `.github/workflows/`; wszystkie checki + nightly chodzą na VPS.
**Weryfikacja:** `grep -rn "ubuntu-latest" .github/workflows/` → pusto; uruchom `nightly-heavy` przez `workflow_dispatch` → zielony na VPS.

### T8 — Monitoring dostępności + dokumentacja + rollback
**Kroki:**
- Heartbeat (opcjonalnie, np. cron co ~6h): `gh api repos/<owner>/dsaas-platform-main/actions/runners --jq '.runners[].status'` → alert gdy `offline`.
- Zaktualizuj `docs/ops/CI-GATES-MAP.md`: dopisz sekcję „Self-hosted runner (VPS)" z label `dsaas`, ścieżką `~/actions-runner`, userem `actions`.
**DoD:** dokumentacja mapuje runnera → repo; istnieje sposób wykrycia runnera offline.
**Weryfikacja:** `gh api .../runners` → `online`; CI-GATES-MAP.md opisuje nową topologię.

---

## 6. Bezpieczeństwo — bo VPS współdzielony (krytyczne)

**Zagrożenie:** runner **wykonuje kod z PR** na serwerze, gdzie siedzi vault akademii + tick workflow-lab. Kompromitacja PR = wektor na tenantów.

**Twarde granice (wymagane przed pierwszym zielonym biegiem):**
1. `actions` ≠ root, brak `sudo`, `chmod 750 /home/actions` — nie czyta `/opt/*`, `hermes-engineer.env`, `GITHUB_*` env.
2. **Brak sekretów na runnerze:** `gates` używa tylko `permissions: contents: read`, nie referuje żadnego secretu → na jego filesystem nie lądują żadne tokeny.
3. **Repo prywatne + zero forków** → powierzchnia ataku = tylko PR-y otwarte przez własnego Cursora (nie nieufny kod z forków). To drastycznie obniża ryzyko self-hosted (GitHub sam ostrzega o nieufnych forkach — tu ich nie ma).
4. **Deploy NIE na runnerze:** workflowy deplojujące (jeśli powstaną) nie używają `self-hosted` — deploy zostaje HITL/`/deployready` (Zasada 11). Runner tylko testuje.
5. Opcjonalnie (wyższy rygor): runner `--ephemeral` (czysty workspace co job) + rotacja checkoutu. Dla „min złożoności" zaczynamy persistent.

---

## 7. Autonomia Hermes Ops — jak dokładnie działa (bez nowego kodu)

```
tick (S0) → Linear issue
  └─ run_next (S2) → ensure_cursor_trigger → @cursor comment (2xx = wake)
      └─ Cursor otwiera PR (ready-for-review, NIE draft)  [github.py: NEVER_DRAFT_LINE]
          └─ push → GitHub zdarzenie → `gates` AUTO-startuje na runnerze VPS  ← tu żadna rola Hermes Ops
              ├─ FAIL → Cursor naprawia + re-push (1 retry) → `gates` znowu auto
              └─ PASS → D-AUTOMERGE squash (checks_green) → merged
      └─ refresh_live → _observe_merge_if_done → ledger "merged" + engine PAUSED
```

- **Hermes Ops nie triggeruje testów** — testy triggeruje GitHub na `push`/`pull_request`. Hermes Ops **obserwuje** wynik przez already-existing `enrich_live`/`_observe_merge_if_done`.
- **Jedyny warunek autonomii:** runner `online` w 100% czasu → dlatego systemd `enabled` + `Restart=on-failure` (T2) + heartbeat (T8).
- **Policy bez zmian:** `workflow_dispatch` zostaje wyłączony (deploy-guard nienaruszony).

---

## 8. Rollback

| Sytuacja | Akcja |
|---|---|
| Runner pada / nie startuje | `systemctl restart actions.runner.*`; status w panelu → `Idle` |
| Self-hosted niestabilny (decyzja) | revert `runs-on` → `ubuntu-latest` (1 linia/plik) + podnieś cap po 2026-10-01 (CI-GATES-MAP) |
| Awaryjny merge bez CI | precedens #124: squash `--admin` (komandor, świadomie) |
| Usunięcie runnera | Settings → Runners → Remove + `sudo ./svc.sh stop && sudo ./svc.sh uninstall` |

---

## 9. DoD całości (meta)

Całość jest DONE, gdy **wszystkie** poniższe są prawdą:
1. `gh pr checks 125` → `gates` **green** na runnerze VPS, merge bez `--admin`.
2. `grep -rn ubuntu-latest .github/workflows/` → **pusto**.
3. `nightly-heavy` (dispatch) → green na VPS, bilans minut = **0**.
4. Runner `online` (heartbeat), systemd `enabled`, user `actions` bez sudo.
5. `CI-GATES-MAP.md` opisuje topologię self-hosted.

---

## 10. Szacunek wysiłku

| Faza | Zadania | Wysiłek | Bloker |
|---|---|---|---|
| A | T1–T5 | ~1 h (głównie pierwszy bieg `gates` = iteracja brakujących libów) | sudo VPS (Dowódca) |
| B | T6–T8 | ~1 h | Docker + Playwright na VPS |

Razem ~2 h pracy na VPS + czas pierwszego pełnego biegu `gates` (G1–G34, ~25 kroków, realnie kilka minut na runnerze).