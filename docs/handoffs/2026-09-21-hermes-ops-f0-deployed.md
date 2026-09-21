# Handoff — Hermes Ops F0 complete DEPLOYED 2026-09-21

**GO Dowódcy:** merge + deploy + testy (sesja Cursor).

## Merges
| Repo | PR | SHA |
|------|----|-----|
| workflow-lab | [#66](https://github.com/wozniaknorbert95-del/workflow-lab/pull/66) | `63bd003` |
| akademia | [#39](https://github.com/wozniaknorbert95-del/akademia/pull/39) | `f554c04` |

## Deploy VPS
- Akademia: `bash scripts/deploy-akademia-vps.sh` → HEAD `f554c04`
- Lab: `install-hermes-ops-vps.sh` → `/opt/workflow-lab` @ `63bd003`
- Kolejka: `/opt/workflow-lab/data/linear-queue.json` (bootstrap; `LINEAR_OPS_READ` nadal pusty)

## Kanarek produkcja
- `/ops/status`: `PAUSED` · `reason=queue_file` · next **QUI-61** · auto 8 · local 5 · waiting 5
- `OPS.html`: Active agents ✅ · `push-send --ops` ✅
- `hermes-ops.timer`: active

## Testy lokalne (PASS)
- akademia: walidator + vault + Fala M 8/8
- lab: `test_hermes_ops.py`

## Next (opcjonalnie u Dowódcy)
```powershell
cd workflow-lab
$lin = Read-Host -AsSecureString "LINEAR_OPS_READ"
$gh  = Read-Host -AsSecureString "GITHUB_OPS_WRITE"
.\scripts\push-ops-tokens-to-vps.ps1 -SecureLinear $lin -SecureGithub $gh
```
Potem API Linear wygrywa nad plikiem; Run next / merge wymaga `GITHUB_OPS_WRITE`.
