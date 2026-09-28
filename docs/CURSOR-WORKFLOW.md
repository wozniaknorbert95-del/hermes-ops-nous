# Cursor workflow — akademia

Slash-komendy w **tym** repo: `.cursor/commands/`. Wpisz `/nazwa` w chacie Cursora.

> Paleta 38 komend = `dsaas-platform-main/.cursor/commands/` (nie duplikować tu). Akademia trzyma tylko te 4 rytuały lokalne.

| Komenda | Plik | Kiedy |
|---|---|---|
| `/vibeinit` | [`.cursor/commands/vibeinit.md`](../.cursor/commands/vibeinit.md) | Start sesji — TERAZ, jeden plik, gate export+vault |
| `/rootcause` | [`.cursor/commands/rootcause.md`](../.cursor/commands/rootcause.md) | DNS / vault `:8097` / nginx / TLS / sync 0.1.0 |
| `/auditread` | [`.cursor/commands/auditread.md`](../.cursor/commands/auditread.md) | Przed merge albo po większej zmianie UI |
| `/handoff` | [`.cursor/commands/handoff.md`](../.cursor/commands/handoff.md) | Koniec sesji — `docs/handoffs/`, zero sekretów |

Ciała procedur są **tylko** w tych czterech plikach (żeby się nie rozjechały z docs).

Glob-rules (nie always-on): `.cursor/rules/ui-dashboard.mdc`, `python-scripts.mdc`, `ops-surface.mdc`. Cloud: `.cursor/environment.json` (terminal `dev` = `:8765`).

Anty-lista (wszystkie 4): nie instrukować `/deploy` `/publish` `/skip-gate` `/force-merge`; nie dodawać 5. rytuału z palety platformy.
