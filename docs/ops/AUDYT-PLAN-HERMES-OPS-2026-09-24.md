# Plan audytu — produkt **Hermes Ops** (`/ops`)

**Status:** **PROPOZYCJA — czeka na GO Dowódcy (R1)**  
**Nie uruchamiać** przed zatwierdzeniem. Ten plik to tylko harmonogram i kryteria.

**Zakres:** Control Plane UI (`OPS.html`), vault (`/ops/status`, `/ops/diag`, `/ops/run`), kontrakt JSON, smoke VPS, orchestrator w **`workflow-lab`** (read-only z perspektywy audytu akademia). **Bez** zmiany kanonu platformy.

---

## 1. Cel audytu

Udowodnić fail-closed HUD: telefon nie kłamie RUNNING/DONE; UNKNOWN nie jest zielone; Approval ≠ Merge; deploy nie istnieje w orchestratorze.

**Deliverable:** raport `docs/ops/AUDYT-WYNIK-HERMES-OPS-YYYY-MM-DD.md` + opcjonalnie wpis w `engineer-loop-e2e.json` jeśli dotyczy.

---

## 2. Wejścia (przed startem)

- GO na audyt (ten dokument §6).
- Dostęp: VPS loopback **lub** public HTTPS z Basic Auth (hasło poza repo).
- Lab: `workflow-lab` na znanym SHA; `systemctl` timer/path (runbook A).
- Lokalnie: vault + `bash scripts/smoke-hermes-ops-vps.sh` (na hoście).

---

## 3. Fazy audytu

| Faza | Obszar | Metoda | Kryterium PASS |
| --- | --- | --- | --- |
| **O1** | Kontrakt docs | Review | `HERMES-ROLE-CONTRACT`, HOWTO, `CONTRACT-OPS-STATUS` spójne |
| **O2** | Vault API | `test_progress_vault.py` + curl | `/ops/diag` ok; dispatch fail-closed; 410 `/hermes/chat` |
| **O3** | OPS UI | Manual 360px | Autopilot-only; Start → QUEUED; STALLED copy; Take over |
| **O4** | ops-cmd.json | VPS ls + test | Plik, nie katalog; `MakeDirectory=false` |
| **O5** | Tick alive | `/ops/diag` + systemd | `tick_alive` zgodny z timerem; hint runbook |
| **O6** | E2E (opcjonalnie) | Issue testowe Linear | S0–S6 na issue lab; **bez** deploy prod |
| **O7** | Smoke | `smoke-hermes-ops-vps.sh` | PASS na VPS po deploy |
| **O8** | Regresja repo akademia | Mutacje Fala M/N | 0 PRZEPUSZCZONE |

---

## 4. Poza zakresem (Akademia)

Kurs A–G, TERAZ, eksport Kokpitu — patrz [`docs/AUDYT-PLAN-AKADEMIA-2026-09-24.md`](../AUDYT-PLAN-AKADEMIA-2026-09-24.md).

---

## 5. Ryzyka

| Ryzyko | Mitigacja |
| --- | --- |
| Tick martwy na VPS | Runbook A przed werdyktem UI |
| Issue produkcyjne w Autopilot | Tylko issue test / lab; Pause domyślnie |
| Sekrety w logach | Redakcja w telemetry; brak tokenów w diag public |

---

## 6. Decyzja Dowódcy (do wypełnienia)

- [ ] **GO** — start audytu Hermes Ops (data: _____)
- [ ] **STOP / zmiana zakresu** — komentarz: _____
