# Deploy plan — Akademia UX v5 + dział H (2026-09-24)

**Status:** gotowy do wykonania po merge PR i **GO Dowódcy (Zasada 11)**  
**Host:** `https://akademia.quietforge.flexgrafik.nl`  
**Runbook:** [`runbooks/AKADEMIA-VPS.md`](runbooks/AKADEMIA-VPS.md) · bramka: [`ops/DEPLOY-READY-HERMES-OPS.md`](ops/DEPLOY-READY-HERMES-OPS.md)

---

## 1. Zakres tego wdrożenia

| Warstwa | Zmiana | Ryzyko |
| --- | --- | --- |
| UI `DASHBOARD.html` | Quiet landing, kolory v5, KURS density, Calm mode | Niskie — statyczny HTML, rollback = poprzedni tar |
| Kurs | Dział **H** (H1–H3), start pustego postępu → H1 | Średnie — walidator wymaga H; istniejący postęp bez zmian ścieżki |
| Ops `/ops` | Brak wymaganego redeploy dla samego UX (HUD już na VPS) | — |
| Vault | Bez zmian kontraktu `/progress` | — |

**Poza scope:** merge PR #64 osobno — ten plan zakłada **jeden** deploy z gałęzi zawierającej H + UX v5.

---

## 2. Preconditions (must PASS przed GO)

| # | Check | Komenda / dowód |
| --- | --- | --- |
| P1 | CI lokalnie = CI GitHub | Pełna linia `testy:` z `AGENTS.md` |
| P2 | Deploy-ready git | `bash scripts/deploy-ready-hermes-ops.sh` → PASS (`HEAD == origin/main`) |
| P3 | Brak sekretów w diff | Brak tokenów w `academy_url`, brak `.env` w commit |
| P4 | PR zmergowany do `main` | Cloud/laptop: `git fetch origin main && git log -1 origin/main` |
| P5 | Decyzja Dowódcy | Jawne **GO deploy VPS** (Zasada 11) — wpis w handoff / Linear |

```bash
cd /path/to/akademia
python scripts/validate-academy-export.py && \
python scripts/test_progress_vault.py && \
python scripts/test_hermes_intent.py && \
python scripts/mutation-test-fala-0.py && \
python scripts/mutation-test-fala-d.py && \
python scripts/mutation-test-fala-e.py && \
python scripts/mutation-test-fala-i.py && \
python scripts/mutation-test-fala-j.py && \
python scripts/mutation-test-fala-k.py && \
python scripts/mutation-test-fala-l.py && \
python scripts/mutation-test-fala-m.py && \
python scripts/mutation-test-fala-n.py
bash scripts/deploy-ready-hermes-ops.sh
```

---

## 3. Deploy execution (laptop Dowódcy)

**Wymagania:** SSH do VPS, `AKADEMIA_REMOTE`, czyste `main` zsynchronizowane z origin.

| Krok | Akcja | Oczekiwany wynik |
| --- | --- | --- |
| D1 | `export AKADEMIA_REMOTE=root@185.243.54.115` | — |
| D2 | `bash scripts/deploy-akademia-vps.sh` | Tar/scp OK, `setup-akademia-vps.sh` bez błędu |
| D3 | Setup: `ensure_hermes_ops_cmd_file`, `fix_hermes_ops_systemd` | Plik `ops-cmd.json`, `MakeDirectory=false` |
| D4 | Smoke na VPS | `bash scripts/smoke-hermes-ops-vps.sh` → **SMOKE PASS** |

Skrypt deploy **odmawia** gdy lokalne `HEAD != origin/main` (chyba że `--force` — tylko świadomie).

---

## 4. Smoke matrix (po deploy)

### 4.1 VPS loopback

```bash
curl -fsS http://127.0.0.1:8097/health
curl -fsS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8097/DASHBOARD.html
```

Oczekiwane: `200` health, `200`/`401` dashboard (zależnie od auth na loopback).

### 4.2 Public HTTPS (Basic Auth)

```bash
curl -fsS -u academy:HASLO -o /dev/null -w '%{http_code}\n' \
  https://akademia.quietforge.flexgrafik.nl/DASHBOARD.html
curl -fsS -u academy:HASLO https://akademia.quietforge.flexgrafik.nl/progress | python3 -m json.tool | head
curl -fsS -u academy:HASLO https://akademia.quietforge.flexgrafik.nl/ops/diag | python3 -m json.tool
```

Oczekiwane:

- Dashboard 200, hero bez chipów, legenda pod tabami
- `/progress` envelope: `schema_version` `0.1.0`, `source` `academy-os`
- `/ops/diag`: `tick_alive`, dispatch sensowny

### 4.3 UX v5 (manual 360px — Dowódca lub agent)

| Scenariusz | PASS |
| --- | --- |
| Pierwsza wizyta / 0% | Pasek postępu zwinięty; welcome ≤3 kroki; jeden primary CTA |
| TERAZ pusty postęp | Rozdział **H1** |
| KURS | INSTRUKCJA: tylko „Winda” open; dział **H** open |
| NOTATKI | Calm mode zapisuje się po odświeżeniu (vault) |
| Telefon | Sync checkbox między urządzeniami |

---

## 5. Rollback

| Sytuacja | Akcja |
| --- | --- |
| UI regresja, vault OK | Redeploy poprzedniego commita z `main` (lub tag) tym samym skryptem |
| Vault uszkodzony | Przywróć `/opt/akademia/data/progress.json.bak` na VPS przed restartem |
| Pełny stop | `ssh … 'cd /opt/akademia/host && docker-compose -p akademia down'` (DSaaS/jadzia nietknięte) |

**Czas do rollbacku:** jeden redeploy (~5–10 min) + smoke.

---

## 6. Post-deploy checklist

- [ ] Zaktualizuj [`ops/DEPLOY-READY-HERMES-OPS.md`](ops/DEPLOY-READY-HERMES-OPS.md) — data, commit SHA, wynik smoke
- [ ] Handoff: `docs/handoffs/YYYY-MM-DD-deploy-ux-v5.md` (co poszło, znane WARN)
- [ ] Telefon: PWA odświeżone (hard refresh / reinstall jeśli cache SW)
- [ ] Kokpit: brak zmian — nadal tylko eksport JSON, bez iframe

---

## 7. Role

| Rola | Odpowiedzialność |
| --- | --- |
| **Dowódca** | GO Zasada 11, smoke telefon, akceptacja UX |
| **Cloud Agent / laptop** | testy, merge PR, deploy script po GO |
| **Hermes Engineer** | `/ops` tick — nie deploy platformy DSaaS |

**▶ TERAZ po merge:** P1–P2 lokalnie → czekaj na GO → D2–D4 → sekcja 4 + 6.
