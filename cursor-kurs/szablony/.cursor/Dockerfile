# =====================================================================
# .cursor/Dockerfile — przykład dla stacku Node/pnpm (Debian/Ubuntu base
# = działa "computer use": agent może klikać w przeglądarce i nagrywać UI).
#
# ZASADY (ważne!):
#  - NIE kopiuj tutaj kodu projektu (żadne COPY . /app). Cursor sam
#    zarządza workspace i checkoutuje właściwy commit.
#  - Ten plik przygotowuje tylko SYSTEM: narzędzia, pakiety, wersje.
#  - Zależności projektu instaluje "install" w environment.json.
#  - Ścieżki w build są względne do katalogu .cursor (context: ".." = root repo).
#  - Dostosuj do swojego stacku albo (prościej) pozwól guided setup wygenerować
#    środowisko automatycznie i potem tylko przepnij config do repo.
# =====================================================================

FROM node:20-bookworm-slim

# Narzędzia systemowe przydatne agentowi (dostosuj listę)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    # postgres-client / sqlite3 / itp. — dokładasz co potrzebujesz:
    # postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# pnpm przez corepack (zmień na npm/yarn/bun jeśli używasz)
RUN corepack enable && corepack prepare pnpm@latest --activate

# Prywatne rejestry pakietów? Użyj build secrets, np.:
# RUN --mount=type=secret,id=npm_token \
#     npm config set //registry.npmjs.org/:_authToken=$(cat /run/secrets/npm_token)

# Gotowe. Kodu NIE kopiujemy. Zależności NIE instalujemy tutaj
# (to zadanie "install" z environment.json — dzięki temu ląduje w Buildzie).
