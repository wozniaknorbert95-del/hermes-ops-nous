# Plan — nauczyć Hermes Ops palety komend platformy (EV-454)

**Status:** **WYKONANY** — atomy 1/2/3 done; Atom 0 (merge platformy) zablokowany billingiem `gates`. Patrz [`2026-09-27-hermes-ops-palette.md`](handoffs/2026-09-27-hermes-ops-palette.md).  
**Data:** 2026-09-27  
**Źródło platformy:** worktree `dsaas-cursor-env-hygiene` · `chore/cursor-env-hygiene` · `960b99b` (EV-454)  
**Nie robić na branchu** `fix/dor-neg-env-p2` (PR #74) — osobny atom, nie mieszać.

**Deploy VPS:** dopiero po GO (Zasada 11). Ten plan **nie** zawiera `/deploy`.

---

## 0. Werdykt weryfikacji (platforma — już zmierzone)

| Check | Wynik |
| --- | --- |
| Worktree hygiene | czysty; `ahead 2` vs `origin/main` (`1ce2555` EV-453 + `960b99b` EV-454) |
| Paleta | **38** `.cursor/commands/*.md` = **38** `.opencode/command/*.md` |
| `/vibe-init` | **brak pliku** (H-05) |
| Anty-lista | brak `deploy.md` / `publish.md` / `skip-gate.md` / `force-merge.md` |
| Kontrakt testów | `42 passed` (`test_command_palette_contract` + parity + vibeinit + session + cursor_pack + linear + cloud_env_hooks) |
| Dowód | EV-454 + `todo.json` meta.log + `docs/audit/evidence/2026-09-27/S27_EV454-COMMAND-PALETTE.md` |
| **Cloud dziś** | **NIE widzi palety** — `origin/main` platformy nadal pętla 9. Merge hygiene = warunek wstępny. |

Hermes Ops **nie wykonuje** slash-komend (to robi Cursor Cloud w klonie repo). Hermes **budzi** Cloud komentarzem `@cursor` i **pokazuje** pętlę na `/ops`. Dziś budzik uczy tylko preflight; HUD kłamie „cała pętla = `/gate`”.

---

## 1. As-is (kotwice `plik:linia`)

| Warstwa | Co jest | Luka vs EV-454 |
| --- | --- | --- |
| Wake Cloud | `workflow-lab/scripts/hermes_ops/github.py` `cursor_wake_bodies` ~L29–38: README + `session-preflight.py` + zakazy | Brak `/autopilot`, `/scope-lock`, cap 3, `/park`, `/resume` |
| Decyzja labu | `workflow-lab/DECISIONS.md` D-NO-DSAAS-FALLBACK: wake = README + preflight | Trzeba rewizji *tekstu wake*, nie fallbacku repo |
| HUD `/ops` | `OPS.html` L173 + L472: hardcoded `Cloud: /gate` | Jedna komenda z 9; paleta 38 nie istnieje na telefonie |
| Guard CI Akademii | `scripts/validate-academy-export.py` ~L1311: **wymaga** stringu `Cloud: /gate` | Zmiana HUD = ten sam PR co walidator |
| HOWTO | `docs/ops/HERMES-OPS-HOWTO.md` L31, L44: `/gate` + preflight | Brak unattended `/autopilot` |
| Kontrakt ról | `HERMES-ROLE-CONTRACT.md` S2 = `@cursor` na twin | S2 nie mówi, *jaką procedurę* Cloud ma odpalić |
| Karta narzędzi | `TOOL-MASTERY.md` Cursor Cloud + Hermes Engineer | 9-krokowa pętla z 26.09, nie cap 3 / park / look |
| Audyt 26.09 | `AUDYT-HERMES-OPS-ENGINEER-2026-09-26.md` L27: `/vibeinit→/plan→/gate→/verify→/evidence→/handoff` | Poprawna pętla **kodu**, ale bez warstwy trwania (lock/look/env/park) |
| Rytuały Akademii | `docs/CURSOR-WORKFLOW.md` | To **akademia**, nie paleta platformy — nie duplikować 38 komend tutaj |

S0–S6 na pasku `/ops` = **orchestrator** (Linear→PR→CI→merge).  
`/autopilot` = **procedura w VM Cloud**. Nie spłaszczać do jednego paska — HUD ma pokazać *obie* osie.

---

## 2. Zasada nauczania (żeby „zaawansowanie” nie = więcej przycisków)

Hermes **nie** dostaje 38 przycisków na 360px. Dostaje:

1. **Jeden czasownik unattended:** w wake: `/autopilot <QUI>` (wewnątrz: lock → plan → kod → gate → verify → evidence → handoff).
2. **TrzyRecovery:** `/park` (2× BLOCKED), `/resume` (Take over / freeze), `/context-reset` (rot kontekstu) — w HOWTO + wake, nie jako tap.
3. **Anty-lista w wake (twarde):** nigdy nie instruować `/deploy` `/publish` `/skip-gate` `/force-merge`.
4. **Lab vs platforma:** issue `workflow-lab` **bez** preflightu i **bez** `/autopilot` platformy (test `test_hermes_ops.py` już strzeże preflight-only-on-platform).

---

## 3. Kolejność wykonania (Dowódca)

### Atom 0 — platforma (inne repo, bramka)

1. Review + merge PR `chore/cursor-env-hygiene` → `dsaas-platform-main` `main` (albo jawny Cloud branch = ten SHA).  
2. Bez tego każdy `@cursor` na `main` **nie ma** plików `/autopilot.md`.  
3. Nie zamykaj Linear Done platformy z telefonu. CI `gates`. Billing czerwony = QUI-98.

### Atom 1 — `workflow-lab` (producent tekstu `@cursor`) — **obowiązkowy, nie akademia**

Plik: `scripts/hermes_ops/github.py` `cursor_wake_bodies` (gałąź `PLATFORM_REPO`).

Dopisać po kroku preflight (numeracja 8+), bez usuwania 1–7:

```text
8. Unattended procedure: `/autopilot <id>` (max 3 atoms; gate FAIL → 1 retry; 2× BLOCKED → `/park`).
9. Before code: `/scope-lock` then `/scope-look`. Host change → `/env`. Pause/Take over → `/resume` (read `.cursor/context-state.md`).
10. Do not invent `/deploy`, `/publish`, `/skip-gate`, `/force-merge`. Laptop HITL: `/deployready` then wait for Commander GO.
```

- Testy: `scripts/test_hermes_ops.py` — platform comment **musi** zawierać `/autopilot` + `session-preflight`; lab comment **nie** zawiera `/autopilot` ani `session-preflight`.
- Rewizja `DECISIONS.md` D-NO-DSAAS-FALLBACK: jeden akapit „Wake text (2026-09-27)” — fallback repo **bez zmian**.

### Atom 2 — `akademia` docs (ten repo)

Nowy branch od `origin/main` (nie od `fix/dor-neg-env-p2`):

`docs/feat/hermes-ops-palette-ev454`

| Plik | Zmiana |
| --- | --- |
| `docs/ops/HERMES-OPS-HOWTO.md` | Po starcie: `Cloud: /autopilot` (S0–S6 osobno). Ticket platformy: bootstrap = README + preflight + `/autopilot`. Take over = `/resume` na laptopie. |
| `docs/ops/HERMES-ROLE-CONTRACT.md` | S2: „`@cursor` + procedura `/autopilot` (paleta `.cursor/commands/` na platformie, EV-454)”. Anty-lista w Anty-slop. |
| `docs/ops/TOOL-MASTERY.md` | Karta Cursor Cloud: praktyka = `/autopilot` po preflight. Karta Hermes Engineer: HUD pokazuje procedurę Cloud ≠ pasek S0–S6. |
| `docs/ops/AUDYT-HERMES-OPS-ENGINEER-2026-09-26.md` | Nie przepisywać historii; 1 linia SUPERSEDED → HOWTO 2026-09-27. |
| `docs/CURSOR-WORKFLOW.md` | **Nie** wklejać 38 komend. Jedna linia: paleta platformy = repo `dsaas-platform-main` `.cursor/commands/`; akademia = te 4 rytuały lokalne. |

### Atom 3 — `akademia` HUD + CI lock (ten sam PR co Atom 2)

| Plik | Zmiana |
| --- | --- |
| `OPS.html` | Domyślny + `paintChips`: `Cloud: /autopilot` zamiast `/gate`. Opcjonalnie (min. złożoności): jeśli `live.action` już jest, dopisać ` · ` + action; **nie** zgadywać komendy z S-step. |
| `scripts/validate-academy-export.py` | Zamienić asercję `Cloud: /gate` → `Cloud: /autopilot` (ten sam PR, inaczej CI czerwone). |
| `scripts/test_progress_vault.py` | Jeśli snapshot HTML/string — zaktualizować. |
| `docs/ops/CONTRACT-OPS-STATUS.md` | 1 zdanie: linia prawdy Cloud = procedura palety, nie alias `/gate`. |

**Nie** dodawać 38 chipów. **Nie** nowych przycisków Run dla `/park`. Pause/Stop/Take over zostają.

### Atom 4 — bramki + handoff (akademia)

```bash
python scripts/validate-academy-export.py
python scripts/test_progress_vault.py
python scripts/test_hermes_intent.py
bash scripts/deploy-ready-hermes-ops.sh
```

Handoff: `docs/handoffs/2026-09-27-hermes-ops-palette.md` (fakty, nie plan).  
Deploy: **STOP** na GO Dowódcy (`deploy-akademia-vps.sh` + `smoke-hermes-ops-vps.sh`).

---

## 4. Anty-zakres (świadomie)

| Nie | Dlaczego |
| --- | --- |
| Przycisk `/deploy` na `/ops` | Zasada 11 + anty-lista palety |
| Uczenie DeepSeek 38 komend | Akademii = 0 tokenów; Ops brief = szablon |
| Duplikat ciał komend w `akademia/.cursor/commands` | SoT = platforma; Cloud klonuje **to** repo issue |
| Mieszanie z PR #74 `_NEG_ENV` | Inny atom, inny rollback |
| O6 e2e na prawdziwym QUI produktu | Tylko issue **lab testowe** (jak audyt 27.09) |
| Zmiana S0–S6 na 38 kroków | Orchestrator ≠ paleta |

---

## 5. Definition of Done (Hermes „umie” paletę)

- [ ] `main` platformy ma 38 komend (albo Cloud target SHA = `960b99b`+)
- [ ] Komentarz `@cursor` na issue **platformy** zawiera `/autopilot` + preflight; lab — nie
- [ ] `/ops` 360px: linia `Cloud: /autopilot · CI … · AC n/m`
- [ ] `validate-academy-export.py` PASS
- [ ] HOWTO + ROLE + TOOL-MASTERY cytują EV-454 / `.cursor/commands/`
- [ ] Zero instrukcji `/deploy` w wake
- [ ] VPS: tylko po **GO** + smoke

---

## 6. Rekomendacja R1 (jedna)

Najpierw **merge hygiene na platformę**, potem **jeden PR labu (wake)** i **jeden PR Akademii (HOWTO+HUD+walidator)**. Bez merge platformy nauczanie Hermesa jest teatrem: telefon pokaże `/autopilot`, Cloud na `main` nie znajdzie komendy.

**Właściciel wykonań:** Dowódca (merge/deploy GO). Agent Akademii: Atomy 2–4 po GO na czystym `main`. Tick labu: Atom 1 w `workflow-lab`.
