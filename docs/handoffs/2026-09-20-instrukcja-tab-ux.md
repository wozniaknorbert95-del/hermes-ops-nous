# Handoff — zakładka INSTRUKCJA + UX Hermes/loop

**Data:** 2026-09-20  
**Repo:** akademia  
**Status:** ZAMKNIĘTE (merge + deploy VPS)

## Co

- 7. zakładka **INSTRUKCJA** (`guide`) — 2. na pasku po TERAZ: mapa ról, dwa poranki, start kodu (Linear/GitHub @cursor), W-06 S1–S6, anty-pułapki.
- Odchudzenie: welcome, HERMES, WORKFLOW banner, skrócony callout Engineer → link do INSTRUKCJA.
- SoT: [`docs/ops/AKADEMIA-INSTRUKCJA.md`](../ops/AKADEMIA-INSTRUKCJA.md), wzmianka w [`HERMES-ROLE-CONTRACT.md`](../ops/HERMES-ROLE-CONTRACT.md).
- Guardy CI: `ACADEMY_TABS == 7`, `renderGuide`, link do AKADEMIA-INSTRUKCJA.
- Fix mutacji **D7b** (Fala D): marker refs po `INSTRUKCJA` w `hermesLocal`.

## Merge

- **PR:** [#33](https://github.com/wozniaknorbert95-del/akademia/pull/33) (squash)
- **main:** `d735a1a60877cb34080bdddca537dedf5401ff53`
- **CI:** academy-gate PASS

## Deploy VPS (2026-09-20 ~21:16 CEST)

```text
bash scripts/deploy-akademia-vps.sh
integralnosc OK: HEAD == origin/main (d735a1a…)
vault health: {"ok": true, "service": "academy-vault"}
hermes: llm true, deepseek-flash
HTTPS smoke: progress schema 0.1.0 OK
PWA: manifest=200 ikona512=200
```

**Prod:** `https://akademia.quietforge.flexgrafik.nl/` — po hard refresh PWA: **7 zakładek**, **INSTRUKCJA** na pozycji 2.

## Test (lokalnie przed merge)

```text
python scripts/validate-academy-export.py  # PASS
python scripts/mutation-test-fala-d.py     # 19/19 (po fix D7b)
# pełna linia AGENTS.md — PASS
```

## Następny krok (poza tym zamknięciem)

Epik „Start zadania jednym tapnięciem” + VPS timer `phone-loop-status` z `--pr` — osobny issue.
