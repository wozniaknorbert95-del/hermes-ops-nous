# Handoff — pre-flight gate fix + roadmap UX/UI nawigacji — 2026-09-28

**Status:** Zielono. 6/6 faz wykonanych. Fix na produkcji. Git czysty. Gotowy do następnej sesji.

---

## 1. Co zrobione w tej sesji

### PR #82 — fix(ops): pre-flight gate blokuje Start przy czerwonym warunku

**Bug:** `computePreflight()` renderował 6 binarnych warunków w pre-flight gate (DoR, Tor, Tick, CI, Slot, Limit), ale `canAct` w `paint()` sprawdzało tylko:
- `unk` (UNKNOWN status)
- `hasAuto || live.issue` (czy jest kolejka)
- `dor.ok === false`

Żaden z pozostałych 5 warunków nie był podpięty pod `btnRun.disabled`. Przycisk "Start pętli" był **enabled** mimo ✗ na "Wolny slot (max 1 agent)".

**Fix (OPS.html:724-735):**
```javascript
// Enterprise pre-flight gate: każdy ✗ blokuje Start.
var pf=computePreflight(s), blockedBy=[];
for(var i=0;i<pf.length;i++){
  var ch=pf[i];
  if(!ch.ok){
    if(ch.id==='slot' && live && live.issue) continue;
    canAct=false; blockedBy.push(ch.label);
  }
}
btnRun.disabled=!canAct;
if(blockedBy.length) btnRun.title='Zablokowane: '+blockedBy.join('; ');
```

**Wyjątek:** slot (max 1 agent) gdy `live.issue` istnieje — ten sam agent nie koliduje sam ze sobą.

**Weryfikacja:**
- 3 scenariusze przetestowane w konsoli (live+agent ✓, agent bez live ✗ blokuje, tick stalled ✗ blokuje)
- 151/151 mutacji ZŁAPANE (0 PRZEPUSZCZONE)
- validate-academy-export: PASS · test_progress_vault: PASS · test_hermes_intent: PASS
- Smoke na VPS: wszystkie zielone
- Produkcja: 6/6 ✓✓✓✓✓✓ → Start enabled; title pusty (poprawnie)

### Deploy

`bash scripts/deploy-akademia-vps.sh --force` → VPS live, vault OK, tick_alive=true, public /ops HTTP 200.

### Porządki git

- Branch: tylko `main` (lokalnie i zdalnie)
- Wszystkie stare branche usunięte (`git fetch --prune` potwierdza)
- Working tree czysty, HEAD == origin/main
- Ostatnie PR-y: #78 (enterprise), #79 (housekeeping), #80 (N5), #81 (handoff), #82 (pre-flight fix)

---

## 2. Co live

| Endpoint | Status |
|---|---|
| `https://akademia.quietforge.flexgrafik.nl/ops` | HTTP 200 |
| `/ops/status` | run_result + deploy_readiness obecne |
| `/ops/diag` | ok:true, tick_alive:true |
| vault `:8097/health` | ok:true |
| systemd timers | hermes-ops + push + report — wszystkie active |

---

## 3. Co zostało do decyzji Dowódcy

| Bloker | Stan |
|---|---|
| Atom 0 (billing GitHub Actions) | ⛔ QUI-98 |
| workflow-lab push bezpośredni | ⛔ decyzja Dowódcy |
| Hermes LLM na VPS | ⚠️ brak modelu |

---

## 4. Następna sesja — optymalizacja UX/UI nawigacji Hermes Ops (P1)

**Cel:** przeprojektować sterowanie i nawigację w `/ops` z "amatorskiego" na profesjonalny kokpit decyzyjny, w którym Dowódca w 2 minuty podejmuje decyzję i wykonuje akcję.

### 4.1 Zidentyfikowane braki (audyt z produkcji)

#### A. Brak odnośników do Lineara w kolejce
- `renderLane()` (linia 437) tworzy `<button class="issue">` bez `href`. Elementy kolejki (Autopilot i Lokalna) pokazują ID issue, ale **nie linkują do Linear**.
- Dla porównania: sekcja Approval (linia 694) używa `it.url` do tworzenia `<a href>`. Ta sama logika powinna być w lane'ach.
- **Fix:** dodać `it.url` jako link w każdym elemencie kolejki (zarówno autopilot, jak i local).

#### B. Zasłonięte / sfałdowane sekcje
- Na mobile (360px-720px) desktopowy 2-panel layout (grid 430px+724px) może zasłaniać krytyczne informacje.
- Brak wyraźnego folding/unfolding z保留 kontekstu.
- **Fix:** przemyśleć IA — co jest widoczne na pierwszym ekranie (STERUJE), co pod fałdą (KONTEKST, DZIENNIK). Sekcja "Deploy" powinna być zawsze na wierzchu gdy `deploy_readiness.ready === true`.

#### C. Brak rekomendacji przed startem
- Sekcja "Next" pokazuje priorytetowy issue z kolejki, ale nie podpowiada **dlaczego** ten issue ani **co sprawdzić** przed startem.
- Brak "suggested next" — system powinien podświetlić najlepszego kandydata z kolejki (np. najwyższy priorytet z zielonym DoR).
- Brak przycisku "Użyj tego issue" obok rekomendacji.
- **Fix:** dodać `recommended_issue` w payload `/ops/status` (backend: `progress_vault.py`) lub obliczać kliencko z kolejki.

#### D. Nawigacja — ogólne problemy
- Brak scroll-spy / sticky nagłówków — na desktop przewijanie gubi kontekst (która sekcja jest aktywna).
- Przyciski sterowania (Start/Pause/Stop/Retry/Take over) nie mają wyraźnej hierarchii wizualnej (wszystkie taki sam rozmiar).
- Brak skrótów klawiszowych dla power-userów.
- "Take over" nie pokazuje wyraźnie co się stanie (brak tooltipa/confirm).
- Kolejka "Pokaż jeszcze N" expanduje listę w miejscu, zamiast otwierać dedykowany widok.

#### E. Brak pierwszeństwa sekcji wg ważności
- Obecna kolejność H2: Sterowanie → Dashboard → Kolejka → Live → Approval → Wynik → Deploy → Dziennik.
- Deploy handoff powinien być wyżej (zaraz po Sterowaniu), gdy jest aktywny.
- DZIENNIK powinien być zawsze dostępny, ale nie dominować widoku.

### 4.2 Proponowany plan naprawczy (do akceptacji Dowódcy)

| # | Zadanie | Priorytet | Plik(i) |
|---|---|---|---|
| 1 | Dodać linki do Lineara w elementach kolejki (`it.url` → `<a href>`) | P0 | OPS.html `renderLane()` |
| 2 | Dodać `recommended_issue` w `/ops/status` + UI rekomendacji przed startem | P0 | `progress_vault.py` + OPS.html |
| 3 | Poprawić IA: Deploy handoff nad DZIENNIKIEM, sticky nagłówki na desktop | P1 | OPS.html CSS + HTML |
| 4 | Hierarchia wizualna przycisków: Start primary, Pause/Stop secondary, Retry/Take over tertiary | P1 | OPS.html CSS |
| 5 | Confirm dialog na Take over + tooltip wyjaśniający konsekwencje | P2 | OPS.html JS |
| 6 | Collapse/expand sekcji z zachowaniem stanu (localStorage) | P2 | OPS.html JS |
| 7 | Skróty klawiszowe: Enter=Start, Escape=Pause, R=Retry | P3 | OPS.html JS |

### 4.3 DoD sesji UX/UI

1. Każdy element kolejki (autopilot + local) ma klikalny link do `linear.app/quietforge/issue/QUI-XX`.
2. Sekcja "Next" pokazuje rekomendowany issue z powodem (np. "najwyższy priorytet z zielonym DoR") i przyciskiem "Użyj tego".
3. Deploy handoff (gdy `deploy_readiness.ready`) jest zawsze widoczny bez przewijania.
4. Przyciski sterowania mają wyraźną hierarchię wizualną (rozmiar/kolor).
5. Nagłówki H2 są sticky na desktop.
6. Zero regresji: 151/151 mutacji ZŁAPANE, wszystkie testy PASS.
7. Zero sekretów w kodzie, zero URL-i z tokenami.

---

## 5. Komendy weryfikacji (copy-paste)

```bash
# Lokalny gate
python scripts/validate-academy-export.py && python scripts/test_progress_vault.py && python scripts/test_hermes_intent.py
bash scripts/deploy-ready-hermes-ops.sh

# VPS smoke
ssh root@185.243.54.115 'bash /opt/akademia/scripts/smoke-hermes-ops-vps.sh'

# Public
curl -fsS -u academy:$(ssh root@185.243.54.115 'grep "^password=" /opt/akademia/CREDENTIALS.local.txt | cut -d= -f2') https://akademia.quietforge.flexgrafik.nl/ops/diag

# Dev lokalny
python -m http.server 8765
# → http://localhost:8765/OPS.html
```

## Pliki dotknięte w tej sesji

- `OPS.html` — PR #82 (pre-flight gate fix, +12 linii)
- `scripts/mutation-test-fala-n.py` — PR #80 (N5 double-anchor fix, już wcześniej)
- `docs/handoffs/2026-09-28-vibe-init-sprzatanie.md` — PR #81 (poprzedni handoff)
- `.gitignore` — PR #79 (`.hermes/` entry)
- `docs/ops/PLAN-HERMES-OPS-UX-ENTERPRISE-2026-09-27.md` — PR #79 (archiwum planu)

Zero sekretów.