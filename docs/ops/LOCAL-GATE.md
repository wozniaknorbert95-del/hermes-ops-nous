# Lokalna bramka Akademii (bez płatnego GitHub Actions)

Prywatne repo na `ubuntu-latest` **spala minuty** (limit darmowy). Ten projekt **nie wymaga** płatnego GitHuba, żeby trzymać jakość.

## Źródło prawdy

```bash
bash scripts/deploy-ready-hermes-ops.sh
```

To jest ta sama linia co `testy:` w `AGENTS.md` + `HEAD == origin/main` + czyste drzewo.

## GitHub Actions

Plik `.github/workflows/academy-gate.yml` zostaje (Fala J sprawdza listę mutacji), ale **nie odpala się na push/PR**. Uruchomienie ręczne: Actions → academy-gate → Run workflow — tylko gdy masz **darmowy self-hosted runner** albo wrócisz do płatnych minut.

`main` **nie** ma required check `academy-gate`. Merge = recenzja + lokalny `deploy-ready`.

## Self-hosted (opcjonalnie, 0 $)

Runner na istniejącym VPS (`runs-on: self-hosted`) nie liczy się do minut GitHuba. To osobny setup (systemd user, token repo) — nie w tej fali.

## Czego nie robić

- Nie włączaj znowu `on: pull_request` na `ubuntu-latest` bez budżetu.
- Nie fałszuj statusu checka.
- Nie deployuj bez `deploy-ready` (Zasada 11).
