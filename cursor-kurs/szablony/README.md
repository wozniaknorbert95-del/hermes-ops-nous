# Jak użyć szablonów (mapowanie → gdzie co wkleić w repo)

Skopiuj zachowując strukturę katalogów — układ jest celowo IDENTYCZNY jak w docelowym repo:

```
Twoje repo/
├── AGENTS.md                          ←  szablony/AGENTS.md
├── .gitlab-ci.yml                     ←  szablony/.gitlab-ci.yml
│                                         (GitHub zamiast GitLaba? przerób na
│                                          .github/workflows/ci.yml — logika ta sama)
├── .cursor/
│   ├── environment.json               ←  szablony/.cursor/environment.json
│   ├── Dockerfile                     ←  szablony/.cursor/Dockerfile
│   └── rules/
│       ├── 00-fundament.mdc           ←  szablony/.cursor/rules/00-fundament.mdc
│       ├── 10-git-flow.mdc            ←  szablony/.cursor/rules/10-git-flow.mdc
│       └── 20-kod-zrodlowy.mdc        ←  szablony/.cursor/rules/20-kod-zrodlowy.mdc
└── .gitlab/
    ├── issue_templates/
    │   └── zadanie-dla-agenta.md      ←  szablony/.gitlab/issue_templates/zadanie-dla-agenta.md
    └── merge_request_templates/
        └── domyslny.md                ←  szablony/.gitlab/merge_request_templates/domyslny.md
```

`PROMPTY-DLA-AGENTOW.md` — to Twoja ściąga, nie idzie do repo.

⚠️ Szablony zakładają stack **Node + pnpm**. Inny stack (Python/Go/Rails)? 
① podmień komendy w AGENTS.md i .gitlab-ci.yml, 
② daj Dockerfile/environment.json wygenerować guided-setupowi (lekcja 03, ścieżka A)
— sam wykryje stack, a Ty tylko zacommitujesz wynik do repo.

Kolejność wdrażania: patrz lekcja 06 → „Plan 30 dni”, Tydzień 1.
