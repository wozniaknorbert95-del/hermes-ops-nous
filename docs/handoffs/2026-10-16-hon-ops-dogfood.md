# Handoff — HON-OPS-DOGFOOD PASS (2026-10-16)

**Atom:** `HON-OPS-DOGFOOD` · tor `NOUS-PRODUCT-LOOP`  
**Granica:** jedna sesja pętli 5 kroków + max 3 bóle UX. Zero polish w PR.

## A0 Preflight

| Check | Wynik |
| --- | --- |
| `main` / validate | PASS · open PR = 0 |
| `/ops/diag` | tick_alive · dispatch idle |
| Baseline `created` 5 min | **0** |
| Issue | **QUI-43** Ready · DoR kompletne · `dsaas-platform-main` |

## A1 Sesja (API = ta sama ścieżka co telefon `/ops`)

| Pole | Wartość |
| --- | --- |
| `select_next` `{}` | 200 · selected=QUI-43 |
| Zapytaj „co robić” | Start/Run next · STOPPED · QUI-43 |
| Zapytaj „deploy” | **ZASADA_11** odmowa |
| Start | `work_mode=testuj` · cmd_id `8db38e8f72324fcb` · HTTP 200 |
| Conductor | **1×** `created` create_ms=**3343** url=True · agent `bc-b56cadd7-6471-4d21-968a-ca5037d45cf2` |
| HUD `run_url` 0–180 s | **pusty** przy status=RUNNING (poll ×36) |
| Zapytaj „url” w trakcie | „Brak https run_url… Teraz: Czekaj” |
| Pause → Stop | 200 · FINAL STOPPED |
| Idle create po stop (90 s) | **0** |
| URL po stop/tick | https://cursor.com/agents/bc-b56cadd7-6471-4d21-968a-ca5037d45cf2 |

**Werdykt pętli:** PASS (create + URL w końcu + Zapytaj + Stop bez spam).  
**KPI create:** journal. **Doświadczenie operatora URL:** FAIL do ~3 min.

Public `/ops` w browserze: ekran logowania Basic Auth (oczekiwane; nie liczony jako ból pętli).

## A2 Max 3 bóle UX (blokują pętlę na telefonie)

1. **RUNNING bez `run_url` przez minuty** — conductor już `created url=True` (~8 s), HUD/status pusty URL aż do stop/tick. Operator nie otworzy sesji. Podejrzenie: tick/adapter live w `workflow-lab` (OUT_OF_SCOPE tu) + lag statusu.
2. **`#hud-truth` przy RUNNING bez sesji** — `paintHudDecision` nie ma gałęzi `RUNNING && !sessUrl` → spada na „Możesz Start / Run next” mimo żywej pętli. Plik: [`OPS.html`](../../OPS.html) `paintHudDecision` (~1027–1036). (Wyjątek „jedna linia prawdy” możliwy bez pełnego F5 polish — osobne GO / mały atom.)
3. **Zapytaj nie ratuje sesji podczas lagu** — czyta ten sam pusty `run_url` ze statusu; nie pokazuje journal/`create` URL. Plik: `ops_chat_reply` w vault — świadomy limit facts-only.

## NEXT

- F5 polish **BLOCKED**.
- Jeśli Dowódca chce naprawić ból 2 bez unfreeze: `GO` na atom truth `RUNNING&&!url → Teraz: Czekaj`.
- Ból 1 = eskalacja lab / tick early-live parity (nie ten PR).
- Produkt: Cloud agent QUI-43 może dalej żyć — monitor PR platformy poza tym repo.
