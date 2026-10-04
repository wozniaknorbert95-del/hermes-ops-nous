---
description: Deploy Hermes Ops — VPS, vault, tick
---

Jesteś agentem w repo **hermes-ops-nous** (Control Plane). Komenda **`/ops-deploy`**.

Deploy = lokalnie, ręcznie (Zasada 11). Zero OIDC / tokenów w `academia_url`.

## Komendy

```
deploy VPS:     bash scripts/deploy-akademia-vps.sh
TLS po DNS:     bash scripts/finish-akademia-tls.sh
smoke VPS:      curl -fsS http://127.0.0.1:8097/health
smoke ops VPS:  bash scripts/smoke-hermes-ops-vps.sh
```

## Zakazy

- Push na `main` bez GO.
- Deploy bez potwierdzenia R1.
- Sekrety w `academy_url` lub `ops-status.json`.
