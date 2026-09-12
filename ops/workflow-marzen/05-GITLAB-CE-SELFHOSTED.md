# 🦊 05 — GitLab CE self-hosted na Twoim VPS (decyzja D1, 07.09.2026)
### Cel: w pełni darmowy, własny „source of truth” z CI i (po teście) integracją Cursor Cloud Agents.

**Status prawny/licencyjny:** GitLab Community Edition = darmowy, bez limitu użytkowników.
Źródło cennika: about.gitlab.com/pricing (Self-Managed → Free $0, „bring your own storage and runners”).
Kluczowa korzyść dla nas: docs.gitlab.com — *„On GitLab Self-Managed … project access tokens are
available with any license”* → to one są wymagane przez integrację Cursor.

---

## 1. Wymagania

| Zasób | Minimum | Zalecane |
|---|---|---|
| RAM | 4 GB | 8 GB |
| vCPU | 2 | 4 |
| Dysk | 40 GB SSD | 80+ GB (repo + buildy + backupy) |
| System | Ubuntu 22.04/24.04 LTS | — |
| Inne | Docker + docker compose; domena (np. `gitlab.twojadomena.pl`) ze rekordem A → IP VPS |

⚠️ Poniżej 4 GB RAM GitLab będzie się dławił. Jeśli Twój VPS jest słabszy → D1 zmieniasz na GitHub Free
(albo podnosisz VPS), nie rób GitLaba „na siłę”.

---

## 2. Instalacja (Docker, oficjalny obraz) — ~20 minut

1. **DNS:** rekord A `gitlab.twojadomena.pl` → IP VPS. Poczekaj na propagację.
2. **Firewall (ufw):** `allow 80`, `allow 443`, `allow 2222` (git-ssh), Twój SSH admin zostaje jak jest.
3. Plik `docker-compose.yml` na VPS (np. w `/srv/gitlab`):

```yaml
services:
  gitlab:
    image: gitlab/gitlab-ce:18.3.1-ce.0   # ⚠️ przypnij wersję; NIGDY :latest
    container_name: gitlab
    hostname: gitlab.twojadomena.pl
    restart: always
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://gitlab.twojadomena.pl'
        letsencrypt['enable'] = true
        letsencrypt['contact_emails'] = ['ty@twojadomena.pl']
        gitlab_rails['gitlab_shell_ssh_port'] = 2222
    ports:
      - "80:80"
      - "443:443"
      - "2222:22"
    volumes:
      - /srv/gitlab/config:/etc/gitlab
      - /srv/gitlab/logs:/var/log/gitlab
      - /srv/gitlab/data:/var/opt/gitlab
```

4. `docker compose up -d` → pierwszy start trwa **5–10 min** (nie panikuj przy 502).
5. Hasło root: `docker exec gitlab grep 'Password:' /etc/gitlab/initial_root_password` → zaloguj się
   jako `root` → **natychmiast zmień hasło** (plik znika po 24h).
6. Sprawdź: `https://gitlab.twojadomena.pl` otwiera się z poprawnym certem (kłódka).

---

## 3. Hardening (15 minut, wszystkie punkty obowiązkowe)

- [ ] Zmienione hasło root + **2FA włączone**
- [ ] **Admin Area → Settings → Sign-up restrictions: rejestracja WYŁĄCZONA** (publiczny internet!)
- [ ] Wymagaj 2FA dla wszystkich userów (Admin Area)
- [ ] Utwórz sobie konto osobiste (adminem) i **nie pracuj jako root**
- [ ] VPS: logowanie SSH tylko kluczami (hasło off), `unattended-upgrades` dla poprawek systemu
- [ ] Backup skonfigurowany (sekcja 6) i **przetestowany restore** (raz na start!)
- [ ] SMTP opcjonalnie (powiadomienia mail); bez SMTP wyłącz funkcje wymagające potwierdzeń mailowych

---

## 4. Runner CI (własne minuty = brak limitu 400)

```bash
docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:latest
```

Rejestracja: Admin Area → CI/CD → Runners → *New instance runner* → bierzesz token, potem:

```bash
docker run --rm -it -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  gitlab/gitlab-runner register \
  --url https://gitlab.twojadomena.pl --token <TOKEN> \
  --executor docker --docker-image node:20
```

Test: pipeline z `cursor-kurs/szablony/.gitlab-ci.yml` musi przejść na Twoim runnerze.
Od teraz CI masz **bez limitów minut** (Twój hardware).

---

## 5. 🔌 Test integracji z Cursor — 15 minut, rozstrzyga sprawę

1. W GitLab: **Twój projekt → Settings → Access Tokens → Add new token**:
   nazwa `cursor-integration`, rola `Maintainer`, zakresy `api` + `read_repository` + `write_repository`.
2. Cursor: `cursor.com/dashboard/integrations` → **Connect GitLab** → wybierz **Self-Hosted** →
   podaj `https://gitlab.twojadomena.pl` + token.
3. **Manage → Sync Repos** → repo widoczne.
4. Cloud Agents → Environments → guided setup na testowym repo → obserwuj, czy VM klonuje.

| Wynik | Konsekwencja |
|---|---|
| ✅ Integracja działa | Fundament potwierdzony: **$0 za GitLab + pełni Cloud Agents**. Wpisz sukces do DECISIONS.md. |
| ❌ Cursor odrzuca | Zachowujesz GitLab CE jako source of truth (lokalny Cursor działa 100%) i dla Cloud Agents robisz **plan B**: gitlab.com Premium dla JEDNEGO projektu albo GitHub Free obok (mirror cho>_picked repo). Decyzję wdrażasz w DECISIONS.md, nie w panice. |

➡️ Ten test wykonujesz **najpóźniej w Fazie 3, najlepiej już w Fazie 0** — od niego zależy ekonomia
całej autonomii.

---

## 6. Backup (bez tego nie ma spokoju)

```bash
# dane (repo, baza, konfiguracja aplikacyjna)
docker exec gitlab gitlab-backup create     # ląduje w /srv/gitlab/data/backups
# konfiguracja + SEKRETY (osobno, zaszyfrowane!)
tar czf gitlab-config-$(date +%F).tar.gz /srv/gitlab/config   # zawiera gitlab-secrets.json — pilnuj!
```

- Cron co noc → kopia **POZA VPS** (S3/Backblaze/inny serwer/rsync na domowy PC przez Tailscale).
- Retencja: 7 dziennie + 4 tygodniowe. Co miesiąc: **test restore** na chwilę (nie czytaj backupu — przywróć).

## 7. Aktualizacje (raz w miesiącu, ~30 min)

1. Backup (sekcja 6) + notujesz obecną wersję.
2. Sprawdzasz upgrade path (docs.gitlab.com — przy przeskoku przez wersje MAJOR idziesz etapami).
3. `docker compose pull` (z nowym, przypiętym TAGIEM) → `docker compose up -d`.
4. Poczekaj 5–10 min, sprawdź: UI działa, pipeline przechodzi, projekty na miejscu.
5. Coś nie działa → wracasz do poprzedniego tagu + restore backupu.

## 8. Miesięczny rytuał opieki (30–60 min; wpisz do piątkowego kalendarza raz w miesiącu)

- [ ] update GitLaba (sek. 7)
- [ ] test restore backupu
- [ ] miejsce na dysku < 75%
- [ ] przegląd userów/tokenów (nic niepotrzebnego nie żyje)
- [ ] runner żywy (`docker ps`), logi bez powtarzających się błędów

## 9. Szybkie rozwiazywanie problemów

| Objaw | Najczęstsza przyczyna / lek |
|---|---|
| 502 po starcie/reboocie | GitLab wstaje 5–10 min — poczekaj; jak trwa >15: `docker logs gitlab` |
| Dławienie, swap 100% | za mało RAM → wyłącz zbędne usługi omnibusa albo podnieś VPS |
| `git clone` po SSH nie działa | używasz portu 2222: `git@gitlab.twojadomena.pl:2222/…` albo klonuj po HTTPS |
| Runner offline | `docker restart gitlab-runner`; token wygasł → zarejestruj ponownie |
| Zapomniałeś hasła root | `docker exec -it gitlab gitlab-rake "gitlab:password:reset[root]"` |
| Pełny dysk | czyszczenie starych backupów/artefaktów CI; `docker system prune` |

> Plus, o którym zapomina cennik: **Twoje dane zostają na Twoim VPS** (RODO/klienci to docenią),
> a koszt to istniejący VPS + ~1h/mc opieki. To jest wymiana, którą przyjąłeś decyzją D1 — uczciwie.
