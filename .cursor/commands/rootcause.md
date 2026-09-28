---
description: RCA Akademii — DNS, vault :8097, nginx, TLS, sync 0.1.0 (bez deployu)
---

Komenda **`/rootcause`**. Symptom: `$ARGUMENTS` (np. DNS_PROBE, 401, sync conflict, vault 500). Jeśli puste — poproś o wklejenie błędu, nie zgaduj.

Repo: **akademia**. Runbook: `docs/runbooks/AKADEMIA-VPS.md`. To nie jest RCA platformy (OPA, tenant, `prod-gate`).

## Kolejność (twarda)

1. **DNS:** `nslookup akademia.quietforge.flexgrafik.nl ns1.cyberfolks.pl` oraz `dig +short akademia.quietforge.flexgrafik.nl A @8.8.8.8`
2. **VPS vault:** `ssh root@185.243.54.115 'curl -fsS http://127.0.0.1:8097/health'`
3. **nginx:** `curl -fsSI -H Host:akademia.quietforge.flexgrafik.nl -u academy:*** http://127.0.0.1/DASHBOARD.html` (hasło tylko z `CREDENTIALS.local.txt` na VPS — **nie** wklejaj do czatu ani handoffu).
4. **TLS:** `ls /etc/letsencrypt/live/akademia.quietforge.flexgrafik.nl/`
5. **Sync:** GET/PUT `/progress` — envelope `schema_version` 0.1.0, `source` academy-os, `academy_url` bez tokenów.

Zatrzymaj się na pierwszym FAIL. Nie skacz do „napraw wszystko”.

## Zakres

- TAK: diagnoza + **jeden** proponowany fix.
- NIE: `bash scripts/deploy-akademia-vps.sh`, `workflow_dispatch`, zmiana DNS bez GO, wypisanie hasła.

## Zakazy

- `/deploy` `/publish` `/skip-gate` `/force-merge`. Nie dodawaj rytuału z palety platformy.
- Zasada 11: nie deployuj bez jawnego GO Dowódcy.
- Nie wsadzaj sekretów do `docs/handoffs/` ani `academy_url`.

## Format wyniku

```
SYMPTOM: <cytat>
LAYER: DNS | vault | nginx | TLS | sync | other
ROOT CAUSE: <jedno zdanie, zmierzone>
FIX: <jeden krok>
GO: czeka na Dowódcę | nie wymaga deployu
```

## PASS / FAIL

- PASS: warstwa + root cause ze sprawdzenia, jeden fix, zero zgadywania.
- FAIL: „pewnie DNS” bez nslookup; deploy w tej samej odpowiedzi; hasło w logu.
