# Handoff — zakładka INSTRUKCJA + UX Hermes/loop

**Data:** 2026-09-20  
**Repo:** akademia

## Co

- 7. zakładka **INSTRUKCJA** (`guide`) — 2. na pasku po TERAZ: mapa ról, dwa poranki, start kodu (Linear/GitHub @cursor), W-06 S1–S6, anty-pułapki.
- Odchudzenie: welcome, HERMES, WORKFLOW banner, skrócony callout Engineer → link do INSTRUKCJA.
- SoT: [`docs/ops/AKADEMIA-INSTRUKCJA.md`](../ops/AKADEMIA-INSTRUKCJA.md), wzmianka w [`HERMES-ROLE-CONTRACT.md`](../ops/HERMES-ROLE-CONTRACT.md).
- Guardy CI: `ACADEMY_TABS == 7`, `renderGuide`, link do AKADEMIA-INSTRUKCJA.

## Test

```text
python scripts/validate-academy-export.py  # PASS
# pełna linia AGENTS.md — PASS (sesja 2026-09-20)
```

## Deploy (Dowódca, Zasada 11)

```bash
bash scripts/deploy-akademia-vps.sh
```

Telefon: twarde odświeżenie PWA → **7 zakładek**, INSTRUKCJA na 2. pozycji.

## Następny krok (poza tym PR)

Epik „Start zadania jednym tapnięciem” + VPS timer z `--pr` — osobny issue.
