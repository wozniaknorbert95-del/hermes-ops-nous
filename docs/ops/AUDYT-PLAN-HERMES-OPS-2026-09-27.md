# Plan audytu — Hermes Ops (`/ops`) — round 3 (po gate DoR + run-truth HUD)

**Status:** **PROJEKT — czeka na GO Dowódcy** (decyzja w §8)
**Data draftu:** 2026-09-27

**Zakres:** Control Plane UI (`OPS.html`), vault Akademii (`host/progress_vault.py`),
gate DoR (`scripts/ops_linear_dor.py`), kontrakt JSON (`CONTRACT-OPS-STATUS.md`),
smoke/deploy-ready, mutacje Fala 0–R. Orchestrator tick w **`workflow-lab`** pozostaje
**read-only** (timer żywy → nie audytujemy kodu ticka, tylko zachowanie przez `/ops/diag`).

**Kontekst (co się zmieniło od audytów 1 i 2):**

| Poprzedni audyt | Werdykt | Co wniosło |
| --- | --- | --- |
| [`AUDYT-WYNIK-...09-24`](AUDYT-WYNIK-HERMES-OPS-2026-09-24.md) (O1–O8) | FAIL-CLOSED HUD trzyma się kontraktu | baseline; 2× P2 |
| [`AUDYT-HERMES-OPS-ENGINEER-...09-26`](AUDYT-HERMES-OPS-ENGINEER-2026-09-26.md) (Cloud 3290) | „Budzik + sekretarz, nie strażnik” | **P0: vault Linear READ + 400**, HUD 3 strefy, markery platformy |

P0#1 i P0#2 **weszły na `main`** (commit `c7a7a4a` „DoR gate and run-truth HUD”, `fa7922f` „zero VPS
nie jest LANE=LOCAL”, `301bb9b` rejestr deploy). Ten audyt jest **bramką weryfikującą, że P0 fixy
są poprawne, fail-closed i nie regresują kontraktu I1–I7** — plus zaległy O6 (e2e) z audytu 1.

---

## 1. Cel audytu

Udowodnić **trzy rzeczy**:

1. **Gate DoR jest fail-closed i poprawny** — telefon nigdy nie obudzi `@cursor` na dziurawym
   / HITL / LOCAL / brudnym issue; token `LINEAR_OPS_READ` = obowiązkowy (brak → 400).
2. **Run-truth HUD nie kłamie** — 3 strefy, chipy, pulse; UNKNOWN ≠ zielone; RUNNING tylko po
   ack + `live.issue`; Approval ≠ Merge; deploy nie istnieje w orchestratorze.
3. **Zaległy O6** — pełny przebieg S0–S6 na issue testowym (jeśli Dowódca da issue test).

**Deliverable:** `docs/ops/AUDYT-WYNIK-HERMES-OPS-2026-09-27.md` + ewentualny wpis
`engineer-loop-e2e.json` (tylko jeśli O6 realnie przejdzie S0–S6 na świeżym issue).

---

## 2. Wejścia (przed startem)

- GO na audyt (§8).
- Repo `akademia` na świeżym `main`; `HEAD == origin/main` (bramka `deploy-ready-hermes-ops.sh`).
- Dostęp VPS: loopback **lub** public HTTPS z Basic Auth (hasło poza repo).
- Fixtures DoR: `LINEAR_OPS_READ=test-linear-fixture` + `data/ops-linear-fixture.json` /
  `ops-pulse-fixture.json` / `ops-todo-fixture.json` — **bez sieci**.
- Dla O6: issue testowy w Linear (nie QUI-92 ani żadna realna praca In Progress).
- Zdefiniowany SHA bazowy (przed startem: `` `git rev-parse HEAD` ``).

---

## 3. Fazy audytu

### Faza A — Kontrakt & SSoT drift (read-only)

| # | Sprawdzenie | Metoda | PASS |
| --- | --- | --- | --- |
| A1 | `HERMES-ROLE-CONTRACT` ↔ `ops_linear_dor.py` (kody refuse: `qui_dor_not_ready`, `qui_hitl`, `qui_blocked`, `qui_lane_local`, `qui_todo_mismatch`, `qui_dirty_pr`, `missing_LINEAR_OPS_READ`) | diff semantyczny | 1:1, bez kodu nieudokumentowanego |
| A2 | `CONTRACT-OPS-STATUS.md` I1–I7 ↔ `host/progress_vault.py` (`derive_dispatch`, `derive_run`, `patch_ops_status`) | review + testy | invarianty spełnione |
| A3 | HOWTO / RUNBOOK / README spójne z aktualnym UI (Autopilot-only, 3 strefy) | review | brak martwych opisów (Manual/Supervised) |
| A4 | „zero VPS / bez SSH nie jest LOCAL” → zakotwiczone w ROLE + test (fa7922f) | review | kotwica obecna, test na `_NEG_ENV` |

### Faza B — Gate DoR (`scripts/ops_linear_dor.py`) — rdzeń P0

| # | Sprawdzenie | Metoda | PASS |
| --- | --- | --- | --- |
| B1 | Brak `LINEAR_OPS_READ` → `gate_start` zwraca `missing_LINEAR_OPS_READ`, `lane=UNKNOWN`, fail-closed | unit (fixture off) | 400 na `/ops/run` |
| B2 | 6 pól lab / platform-DoR (severity, NC, fala, owner/RACI, zakres środowiska, rollback) → wykrywanie braków | unit + fixture issues | każdy brak = `missing` + `qui_dor_not_ready` |
| B3 | Lane: LOCAL (prawdziwy VPS/SSH: `_REQUIRE_LOCAL`) vs HERMES vs STOP; **zero VPS / bez SSH NIE spycha na LOCAL** | unit (`_NEG_ENV`) | QUI-93 regresją nie wraca |
| B4 | HITL: `hitl:approval-required` → `qui_hitl`; `blocked`/`blocked:external` → `qui_blocked` (bez HITL label) | unit | routing zgodny |
| B5 | `todo` mismatch + `dirty` PR → `qui_todo_mismatch` / `qui_dirty_pr` | unit (fixtures) | 400 przed `@cursor` |
| B6 | Cache: `ops-dor-cache.json` TTL 60 s; invalidation przy zmianie `next_id`; **nie** serwuje starych pulse po zmianie | unit + inspekcja | stale cache nie kłamie |
| B7 | Fixture-mode gating: `test-linear-fixture` w produkcji **nie** dzwoni do Linear API | code review | brak sieci w teście; żadnego hard-switcha na prod |
| B8 | **Bezpieczeństwo + sekrety:** token nie trafia do cache/logów/diag; `_gql` timeout + fail-closed na błąd sieci/JSON; `issue_id` walidowany (`IDENT_RE`) przed zapytaniem GQL | review + grep | zero tokenów w artifactach; brak SSRF (URL sztywny) |

### Faza C — Run-truth HUD (`OPS.html` + vault dispatch)

| # | Sprawdzenie | Metoda | PASS |
| --- | --- | --- | --- |
| C1 | UNKNOWN nigdy nie jest zielone (pill + banner „nie tapnij Run next w ciemno”) | unit + manual 360px | brak zielonego przy UNKNOWN |
| C2 | `derive_dispatch`: `idle` / `queued` / `no_ack` / `stalled` / `picked_up` / `running` / `refused` — **`running` tylko po ack + `status=RUNNING` + `live.issue`** | unit (stany graniczne) | I2 |
| C3 | `stalled` tylko gdy tick martwy (`updated_at` ≥ ~18 min) + świeża komenda worker | unit | I6 |
| C4 | Pulse + chipy (DoR · lane · testy · CI · todo zgodny?) renderowane z `status_overlay` | manual 360px | chipy obecne, spójne z kolejką |
| C5 | 3 strefy/sekcie (Dashboard·pulse, Kolejka, Live, Approval, Sterowanie) — Kolejka nie udaje RUN | manual | zgodne z HOWTO §sekcje |
| C6 | Approval ≠ Merge; 0 przycisków Merge; deploy/merge z telefonu → 403 | unit + manual | I7 |

### Faza D — Regresja invariantów vault (audyt 1)

| # | Sprawdzenie | PASS |
| --- | --- | --- |
| D1 | I1 `updated_at` tick-only; Pause/Stop nie bumpują | `test_progress_vault.py` |
| D2 | I3 `ops-cmd.json` plik/absent, nigdy katalog (`ops_cmd_path_state`, `ensure_ops_cmd_file`) | unit + VPS |
| D3 | I4 `id`+`at` na side-effect; I5 brak `cmd.id` → `idle` (nie `stalled`) | unit |
| D4 | `safe_static_path` — `/ops` → `OPS.html`, brak traversal, `/hermes/chat` 410 | unit + VPS |

### Faza E — O6 (e2e S0–S6) — **zaległy z audytu 1**

| Warunek | Akcja |
| --- | --- |
| Dowódca daje issue testowy lab (nie realna praca) | przebieg S0–S6: etykieta → 6 pól → `@cursor` twin → PR `cursor/*` → required checks → squash/merge lab |
| Brak issue testowego | **SKIP** (jak 24.09) — nie Start na realnym QUI In Progress |

Kryterium PASS: pełny S0–S6 bez deploy prod (S-deploy nie istnieje).

### Faza F — Smoke + deploy-ready (read-only, bez deploy)

| # | Komenda | PASS |
| --- | --- | --- |
| F1 | `bash scripts/deploy-ready-hermes-ops.sh` | `HEAD == origin/main`, wszystkie bramki |
| F2 | `bash scripts/smoke-hermes-ops-vps.sh` (VPS) | SMOKE PASS; brak `ops-cmd.json` = idle (nie awaria); katalog = FAIL |
| F3 | `curl /ops/diag`, `/ops/status`, public `/ops` (Basic Auth) | `tick_alive`, `MakeDirectory=false`, `dispatch=idle` |

### Faza G — Regresja mutacyjna (Fala 0–R)

| # | Komenda | PASS |
| --- | --- | --- |
| G1 | `python scripts/mutation-test-fala-{0,d,e,i,j,k,l,m,n,o,p,q,r}.py` | 0 PRZEPUSZCZONE (guardy łapią każdą mutację) |
| G2 | `python scripts/test_progress_vault.py` + `test_hermes_intent.py` + `validate-academy-export.py` | PASS |
| G3 | **Nowe mutacje** dla gate DoR (jeśli audyt wykryje lukę) | wpięte do linii `testy:` i `.github/workflows/academy-gate.yml` **w tym samym PR** |

---

## 4. Wstępne obserwacje ze scopingów (hipotezy do zweryfikowania)

Zapisane **przed** GO — kandydaci na findingi, do potwierdzenia/obalenia w audycie:

1. **Stale cache pulse (B6):** `status_overlay` keyuje cache po `id` + `pulse is not None`; przy
   częstych zmianach kolejki 60 s TTL może pokazać starą kolejkę. Czy degraduje do kłamstwa HUD?
2. **Residuum w cache (B8):** `write_cache` zapisuje pełny `gate_start` payload (tytuł + opis +
   labels) do `ops-dor-cache.json` na dysku. Czy opis issue może nieść wrażliwe dane? Czy cache
   jest wykluczony z git / logów?
3. **`load_todo_active` bez tokenu:** jedna ścieżka czyta `ops-status.json` z dysku niezależnie od
   `LINEAR_OPS_READ` — czy to zgodne z „fail-closed, brak tokenu = pusta kolejka”?
4. **`_NEG_ENV` bypass (B3):** regex `\b(zero|bez|nie|no)\s+(vps|ssh|deploy)\b` — czy frazy typu
   „bezpośrednio VPS”, „nie dotykać SSH” (z inną interpunkcją) omijają negację i fałszywie spychają
   na LOCAL?
5. **Academy-gate wpięcie (G3):** czy każdy z 14 `mutation-test-fala-*` jest wpięty do linii
   `testy:` w AGENTS.md **i** do `academy-gate.yml` (Fala J guard „każdy nowy plik w tym samym PR”)?

---

## 5. Poza zakresem

- Orchestrator tick + worker Cursor w `workflow-lab` — read-only (timer żywy → tylko przez `/ops/diag`).
- Markery preflight platformy / session-entry `/gate`+`/verify` (P0#3 z 26.09) — **workflow-lab /
  dsaas-platform-main**, nie to repo.
- Deploy VPS oraz redeploy Akademii — Zasada 11, GO Dowódcy (osobna sesja).
- Kurs A–G, TERAZ, DSAAS 18 DoD, eksport Kokpitu — [`AUDYT-PLAN-AKADEMIA`](../AUDYT-PLAN-AKADEMIA-2026-09-24.md).

---

## 6. Ryzyka

| Ryzyko | Mitigacja |
| --- | --- |
| Tick martwy na VPS → false `stalled` | Runbook A przed werdyktem (fazy C3/D) |
| O6 na realnym issue → zmiana produkcji | Tylko issue testowy; Pause domyślnie; zero deploy |
| Token Linear w logach/artifactach | B8: grep tokenów; redakcja telemetry; cache poza git |
| Błędny werdykt „PASS” na fake HUD | Każdy werdykt z adresem dowodu (plik:linia / curl / fixture) |

---

## 7. Forma raportu

Każdy finding w formacie:

```
### P{n} — <objaw> — CLOSED | OPEN
| Objaw | ... |
| Przyczyna | ... |
| Naprawa / decyzja | ... (kotwica: plik:linia lub curl) |
| Lekcja | ... |
```

Plus tabela checklist kontraktu (jak w audycie 24.09) i sekcja „następne kroki”.
**Zero sekretów w raporcie.**

---

## 8. Decyzja Dowódcy (do wypełnienia)

- [ ] **GO** — start audytu Hermes Ops round 3 (data: _____)
- [ ] **GO + O6** — start audytu **z** przebiegiem e2e (dostarczam issue testowy lab)
- [ ] **STOP / zmiana zakresu** — komentarz: _____