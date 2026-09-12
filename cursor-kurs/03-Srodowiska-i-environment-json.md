# 🛠️ LEKCJA 03 — Środowiska i `environment.json` (SERCE SYSTEMU)

> Cursor mówi wprost: **„Nie skonfigurować środowiska dla cloud agenta to jak nie dać
> inżynierowi komputera.”** Agent, który umie pisać kod, ale nie umie go uruchomić,
> nie może zweryfikować własnej pracy. Stąd: **80% jakości Cloud Agents = jakość środowiska.**

---

## 1. Co dokładnie zawiera „środowisko”

Środowisko = przepis na w pełni wyposażone biurko agenta:

| Element | Przykład |
|---|---|
| repozytorium (lub grupa repo) | `twoja-firma/dsaas` |
| system + narzędzia | Ubuntu + Node 20 + pnpm + git |
| zależności projektu | `pnpm install` |
| sekrety / zmienne | `DATABASE_URL`, `STRIPE_KEY` (z sejfu Cursora) |
| komendy startowe | odpal dev-server, bazę w Dockerze |
| sieć | do jakich domen agent może się łączyć |
| **Build** | „zamrożony” stan dysku po wszystkich instalacjach = szybki start |

**Kolejność, w jakiej Cursor szuka konfiguracji** (pierwszy traf wygrywa):
1. `.cursor/environment.json` **w repo** ← najlepsze: działa dla całego zespołu, wersjonowane gitem
2. osobiste zapisane środowisko (przydatne do testowania nowej konfiguracji)
3. zespołowe zapisane środowisko (domyślne dla firmy)

---

## 2. Dwie ścieżki ustawienia

### Ścieżka A — Agent-driven setup ✅ (ZALECANA, zacznij od niej)

Z dashboardu Cloud Agents (zakładka Environments) lub z Agents Window w desktopie wybierasz
guided setup. Co się dzieje:

```
1. Podłączasz GitHub / GitLab / Azure DevOps / Bitbucket
2. Wybierasz repo (lub KILKA repo → środowisko multi-repo)
3. Podajesz zmienne/sekrety potrzebne do instalacji i uruchomienia
4. Agent-setup pracuje ~10 min: patrzysz na WSPÓLNY terminal, jak instaluje zależności
   i sam weryfikuje, że projekt się buduje/odpala
5. Cursor zapisuje środowisko po udanej weryfikacji → powstaje Build
6. Twoje przyszłe runy startują z tego Buildu → szybko i z wszystkim gotowym
7. Commitujesz konfigurację do `.cursor/environment.json` → zyskują na tym wszyscy w zespole
```

Dlaczego zalecana: agent sam wykrywa Twój stack i ogarnia detale; Ty tylko patrzysz i zatwierdzasz.

### Ścieżka B — Dockerfile + `environment.json` (zaawansowana)

Gdy potrzebujesz konkretnych pakietów systemowych, wersji kompilatorów, innego obrazu bazowego:

- Tworzysz `.cursor/Dockerfile` (wzór: `szablony/.cursor/Dockerfile`),
- wskazujesz go w `.cursor/environment.json`,
- zasady ważne:
  - ❌ **Nie rób `COPY` całego projektu** — Cursor sam zarządza workspace i checkoutuje właściwy commit. Dockerfile tylko przygotowuje SYSTEM.
  - Używaj *build secrets* do prywatnych rejestrów pakietów (nie wpadają do warstw obrazu).
  - Docker pozwala na cache warstw — po zmianie Dockerfile Cursor przebudowuje tylko zmienione warstwy.
  - **Computer use** (klikanie w UI przez agenta + nagrania) działa dla obrazów bazowych Debian/Ubuntu.

---

## 3. `environment.json` pole po polu

Plik leży w repo: `.cursor/environment.json`. Ścieżki w sekcji `build` są **względne do katalogu
`.cursor`**, a `install` uruchamia się **z katalogu głównego projektu**.

```json
{
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "install": "pnpm install && ./custom_script.sh",
  "start": "sudo service docker start",
  "terminals": [
    { "name": "dev", "command": "pnpm dev" }
  ]
}
```

| Pole | Kiedy się wykonuje | Do czego |
|---|---|---|
| `build.dockerfile` / `build.context` | przy tworzeniu Buildu | budowa obrazu systemowego (opcjonalne; bez tego jest obraz domyślny) |
| `install` | przy tworzeniu **Buildu**, w tle | wszystko, co da się przygotować Z GÓRY: instalacja zależności, codegen, kompilacja artefaktów, rozgrzanie cache |
| `start` | po starcie agenta z Buildu | usługi, które mają żyć w trakcie runu (np. `sudo service docker start`) — w wielu repo można pominąć |
| `terminals[]` | po `start` | procesy aplikacyjne (dev-server, baza, worker). Lecą we **współdzielonym tmux-ie** — Ty i agent widzicie te same terminale |

### Zasada złota: co gdzie wkładać

```
install  →  ciężka, powtarzalna PRZYGOTOWKA (zapisa się na dysku Buildu)
start/terminals →  PROCESY, które maju żyć podczas runu (serwery, bazy, tunele)
```

⚠️ **Build zachowuje TYLKO STAN DYSKU.** Działające procesy, eksportowane zmienne shella i cache
w pamięci **nie** przechodzą do runu. Dlatego serwery startujesz przez `start`/`terminals`,
a nie w `install`.

⚠️ **`install` musi być idempotentny** = uruchomiony drugi raz na gotowym dysku nie psuje niczego
(`pnpm install` to dobry wzór: na przygotowanym stanie tylko doinstaluje różnice).

---

## 4. Buildy — „zamrożony gotowy komputer”

- Build = wynik: obraz bazowy + sklonowane repo + `install` do końca → **zapisany stan dysku**.
  Nowi agenci startują z aktywnego Buildu (sekundy).
- **Przygotowanie z góry:** wszystko ciężkie dajesz do `install` — wtedy NIE wydłuża startu agenta
  (build robi się w tle, nie przy starcie).
- **Bezpieczna porażka:** nieudany Build NIE podmienia aktywnego — agenci dalej startują z ostatniego
  dobrego, a Ty oglądasz logi w zakładce **Builds** i możesz odpalić agenta z tego zepsutego Buildu
  w celach debugowych.
- **Test build:** przycisk w zakładce Builds — sprawdzasz konfigurację bez włączania jej dla wszystkich.
- Istniejąca środowiska można domknąć do Builds: zakładka Builds → **Run setup agent**
  (agent zaproponuje poprawki; dla konfiguracji w repo umie otworzyć PR) albo **Enable Builds**.
- Full setup-agent może też otworzyć PR z poprawkami do `.cursor/environment.json` w repo.

---

## 5. Sekrety — sejf, nie kod

- Wpisujesz raz: `cursor.com/dashboard/cloud-agents` (Secrets) albo w ustawieniach środowiska.
- Agent dostaje je jako **zmienne środowiskowe** przy starcie runu.
- **Multi-repo:** używaj **environment-scoped secrets** — obowiązują we wszystkich repo danej
  grupy, ale nie wyciekają do innych środowisk.
- Po dodaniu nowego sekretu — **odpal nowego agenta** (trwający go nie dostanie).
- `.env.local` w snapshotach technicznie działa (zapisuje się w Buildzie), ale **niezalecane** —
  sekrety trzymaj w zakładce Secrets.
- Dla AWS istnieje opcja IAM Roles (Cursor ustawia profil `cursor-cloud-agent`).

---

## 6. Sieć

- Możesz ustawić **allowlistę domen wychodzących** (restricted egress).
- Do prywatnych zasobów (baza w Twojej sieci, wewnętrzne API): **Tailscale** albo
  **Cloudflare Tunnel** na VM-ce agenta (opisane sekcjami w docs Setup) lub PrivateLink (Enterprise).

---

## 7. Środowiska multi-repo

Jedno środowisko może obejmować **kilka repozytoriów** (frontend + backend + infra + wspólna libka):

- Wybierasz repo przy **tworzeniu** środowiska → to definiuje „repo group”. **Zaplanuj grupę z góry**
  (dokumentacja nie opisuje dokładania repo do istniejącego środowiska).
- Cursor klonuje każde repo obok siebie; agent robi koordynowane zmiany i **otwiera PR/MR w każdym
  zmienionym repo**.
- Sekrety: environment-scoped (patrz wyżej).
- Ograniczenie: long-running nie jest dla multi-repo jeszcze dostępny.

---

## 8. Sekcja chmurowa w AGENTS.md

Cloud Agents czytają `AGENTS.md`. Cursor oficjalnie zaleca dodać rozdział w stylu
`## Cursor Cloud specific instructions` z rzeczami typu:

```markdown
## Cursor Cloud specific instructions
- Po starcie: `pnpm dev` jest już w terminalu "dev" (terminals w environment.json).
- Testy: `pnpm test`; pojedynczy test: `pnpm test <nazwa>`.
- Baza dev: SQLite w pliku ./dev.db — nie wymaga Docker-a; migracje: `pnpm db:migrate`.
- Aby zweryfikować UI: otwórz http://localhost:3000 i zrób screenshot zmienionego widoku.
- NIGDY nie commituj plików .env* — sekrety są w zmiennych środowiskowych.
```

To jest „mapa osiedla” dla agenta — z niej korzysta od pierwszej minuty. (Pełny szkielet AGENTS.md:
`szablony/AGENTS.md`.)

---

## 9. Checklista zdrowego środowiska

- [ ] Setup A (guided) przeszedł, Build jest zielony
- [ ] `install` jest idempotentny i robi całą ciężką robotę
- [ ] serwery żyją w `start`/`terminals`, nie w `install`
- [ ] sekrety w zakładce Secrets (nie w kodzie, nie w Dockerfile)
- [ ] AGENTS.md ma sekcję „Cursor Cloud specific instructions”
- [ ] testowałem: agent potrafi odpalić `testy + dev server` bez pytania
- [ ] konfiguracja jest commitnięta jako `.cursor/environment.json`
- [ ] dla multi-repo: grupa repo zaplanowana z góry, sekrety environment-scoped

### Najczęstsze błędy (nie popełniaj)
1. ❌ `COPY . /app` w Dockerfile (Cursor sam zarządza kodem!)
2. ❌ odpalanie dev-serwera w `install` (Build zachowa tylko dysk — proces zniknie)
3. ❌ sekrety w repo / Dockerfile
4. ❌ doklejanie sekretów i oczekiwanie, że działający agent je zobaczy
5. ❌ zakładanie, że agent „sobie poradzi” bez opisu jak odpalić projekt

---

**Następna lekcja:** `04-Pierwszy-Cloud-Agent-krok-po-kroku.md` — warsztat praktyczny.
Po niej będziesz mieć pierwszy własny MR zrobiony przez agenta w chmurze.
