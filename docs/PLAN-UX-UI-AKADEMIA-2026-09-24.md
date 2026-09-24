# Plan UX/UI — Akademia (profesjonalnie + ADHD-first)

**Status:** **WDROŻONE w PR (U1–U5)** — deploy VPS czeka na GO Dowódcy ([`DEPLOY-PLAN-AKADEMIA-2026-09-24.md`](DEPLOY-PLAN-AKADEMIA-2026-09-24.md))  
**Powiązane:** [`ACADEMY-UX-SPEC.md`](ACADEMY-UX-SPEC.md) · [`docs/ops/AUDYT-UX-UI-2026-09-19.md`](ops/AUDYT-UX-UI-2026-09-19.md)  
**Persona (zablokowana):** Dowódca R1, ADHD-first — *„co robię w tej minucie?”*, nie czyta ściany tekstu.

---

## 1. Werdykt sztabu (UX + „biznes lis”)

| Co masz dobrze | Co psuje profesjonalizm / focus |
| --- | --- |
| Jedno TERAZ, sticky taby, 44px touch, skip link | **Ekran startowy = 7 warstw** zanim treść (hero, sync, welcome, postęp, nowcard, taby, zone, banery) |
| Semantyka zakładek (pytanie → akcja) | **15+ kolorów akcentu** bez jednej legendy — użytkownik nie wie, *co* oznacza kolor |
| Terminal chrome = tożsamość | **Tęcza banerów** (żółty welcome, cyan phone-first, fiolet Hermes, ciemne sync/zone) na ciepłym tle `#f4efe4` |
| Guardy CI na kontrakt | **KURS** po dodaniu H = ściana accordionów; INSTRUKCJA 4× `<details open>` naraz |
| Audyt 2026-09-19 (część naprawiona) | Kolizje znaczenia: `--workflow` = `--llm`, `--dsaas` = `--arch` = `--hermes` |

**Zasada pro (Hick + progressive disclosure):** Na starcie użytkownik widzi **1 nagłówek, 1 CTA, 1 krok**. Reszta schowana lub wtórna. Kolory = **3 role**, nie dekoracja.

---

## 2. Narzędzia i standardy (świat pro + ADHD)

| Narzędzie / standard | Do czego w projekcie |
| --- | --- |
| **[WCAG 2.2](https://www.w3.org/TR/WCAG22/)** AA | Kontrast tekstu ≥ 4.5:1, focus visible, brak pułapki fokusu (audyt już częściowo) |
| **W3C *Making Content Usable*** (cognitive) | Krótkie zdania, chunking, jeden cel na ekran, redundant entry off |
| **Neurodiversity design** (np. [kuakua NDS](https://kuakua.app/docs/product-psychology/neurodiversity-design-system/neurodiversity-types)) | Mniej clutter, progress, spójna nawigacja, kontrola tempa, opcjonalny dark/calm |
| **axe DevTools** (Chrome) | Regresja contrast / aria po każdej fazie UI |
| **Polypane / Responsively** | 360px + 768px — persona telefon |
| **Laws of UX** | Hick (mniej wyborów na start), Jakob (spójność tab = kolor tylko aktywnej) |
| **Design tokens** (Figma lub CSS `:root` v5) | Jedna tabela: `--role-*`, nie `--dzial-*` na całym UI |

**Inspiracja produktowa (nie kopiuj UI):** Tiimo (timeline jednego dnia), Goblin Tools (chunking zadań), Focus Bear (calm palette, user-controlled motion) — u nas odpowiednik: **TERAZ + DZIEŃ + jeden kolor fokusu**.

---

## 3. System kolorów — propozycja v5 (znaczenie > ozdoba)

### 3.1 Trzy warstwy (użytkownik uczy się raz)

```text
WARSTWA A — Nawigacja (cały dashboard)
  --nav-active     → aktywna zakładka (jeden kolor: np. --now teal)
  --nav-idle       → nieaktywne taby (neutral, bez tęczy per tab)
  --surface        → tło kart (#fffdf8)
  --text / --muted → treść

WARSTWA B — Semantyka (statusy, zawsze to samo)
  --sem-ok         → zaliczone / sync online / approve
  --sem-warn       → partial / uwaga / LOCK DZIEŃ
  --sem-bad        → błąd / blocked
  --sem-info       → neutralny hint (jeden niebieski, nie 3 odcienie)

WARSTWA C — Kurs (tylko wewnątrz KURS / accordion działu)
  --dept-H … --dept-A → pasek lewy accordionu, NIE kolor całej zakładki TERAZ
```

**Zmiana zachowania:** Taby **TERAZ / WORKFLOW / …** tracą `--tab-accent` per zakładka na ekranach poza KURS. Aktywna zakładka = `--nav-active`; reszta = szaro-beż. Dział B vs D nie muszą różnić się kolorem tabu — różnią się **w drzewie KURS**.

### 3.2 Co usunąć / scalić

| Dziś | Propozycja |
| --- | --- |
| `--focus` żółty + żółta obwódka active tab | Jeden `--focus-ring` (np. teal 3px), bez drugiego żółtego glow |
| `--tools` = `--warn` = `--money` (bursztyn) | OK jako **sem-warn**; nie trzecia „osobna” barwa na banerach |
| Ciemne `rgba(2,6,23,.55)` na dod-box, sync, zone | **Jasne** dod-box (krem + lewa kreska `--sem-info`) — mniej „dwóch theme’ów” |
| Migający blok `▮` w `.nowcard .tag` | Domyślnie off; tylko `prefers-reduced-motion: no-preference` + opcja „calm mode” w NOTATKI/_scratch |
| 4 chipy w hero | **0–1 chip** albo jedna linia `sub` |

### 3.3 Legenda (1 linia pod tabami, opcjonalna, dismiss)

`🟢 gotowe · 🟡 uwaga · 🔴 blokada · ▶ teraz` — tylko semantyka, bez nazw działów.

---

## 4. Ekran startowy — „quiet landing”

**Cel:** Pierwsze 5 sekund = *„Otwórz TERAZ, krok H1”*, nie manifest akademii.

| Element | Teraz | Propozycja |
| --- | --- | --- |
| Hero H1 + 4 chipy + ops + sub | ~120px + cognitive load | **Compact hero:** tytuł 1 linia + link `/ops` mały (ghost). Sub: *„Jeden rozdział naraz.”* |
| `#welcome` | 4 kroki + 3 przyciski + install | **3 kroki max**, install w `<details>`; primary **jeden** przycisk → TERAZ |
| `#barwrap` postęp | Zawsze widoczny | **Zwinięty** przy 0% lub pierwszej wizycie; rozwija się po 1 zaliczonym rozdziale |
| `#nowcard` na innych tabach | Duplikat TERAZ | Zostaje, ale **krótszy** (tytuł + 1 btn), bez filepath na mobile |
| `#zone-strip` | Osobny pasek | **Scal z `#sync-bar`** — jeden pasek statusu (sync + strefa) |
| `#hermes-banner` | Fioletowy, dodatkowy | Pokazuj **tylko raz** / po dismiss nigdy; nie na pierwszym paint |

**Kolejność DOM (above the fold):** sync → taby → **panel TERAZ** (welcome tylko first visit, pod tabami lub modal light).

---

## 5. Porządki per zakładka

| Zakładka | Problem | Propozycja |
| --- | --- | --- |
| **TERAZ** | Lab + ops-howto + duży panel-head | Panel-head 1 zdanie; ops-howto w `<details>`; **jedna** lista checkboxów |
| **KURS** | INSTRUKCJA wszystko `open`, 8 działów | INSTRUKCJA: **1** sekcja open (winda); reszta closed. Działy: tylko **H** open na starcie; mapa H→G→… jako **pasek**, nie 4 banery |
| **WORKFLOW** | 3 phone-first-bannery z rzędu | Jeden banner + linki |
| **NARZĘDZIA** | Grid 3 kolumn + scoreboard | Mobile 1 kolumna; scoreboard w `<details>` |
| **DZIEŃ** | Już OK (Fala I) | Zachować 2-tap approve; nie dokładać kolorów |
| **NOTATKI** | — | Opcjonalnie: **Calm mode** toggle (zapis `_scratch.ui_calm`) — wyłącza animacje + redukuje cienie |

---

## 6. Fazy wdrożenia (techniczne, bez 7. działu Kokpitu)

| Faza | Zakres | Pliki | PASS |
| --- | --- | --- | --- |
| **U0** | Baseline | Screenshot 360/768 + axe report zapisany w `docs/handoffs/` | 0 Serious axe |
| **U1** | Quiet landing | `DASHBOARD.html` hero, welcome, bar collapse, sync+zone merge | 1 CTA above fold; welcome ≤3 steps |
| **U2** | Tokeny kolorów v5 | CSS `:root`, `renderTabs` bez per-tab rainbow | Legenda semantyki; dept colors tylko `.dzial-acc` |
| **U3** | KURS density | `renderGuide`, `renderKursMap`, default `details` closed | INSTRUKCJA max 1 open; H open only |
| **U4** | Motion & focus | `.nowcard` blink, `prefers-reduced-motion`, roving tabindex audit | Focus never BODY; reduced-motion = static |
| **U5** | Spec + guard | `ACADEMY-UX-SPEC.md` v5, opcjonalny guard walidatora (np. brak 4 chipów w hero) | `validate-academy-export.py` PASS |

**Zasady PR:** jedna faza = jeden PR; pełna linia `testy:`; walkthrough 360px video.

---

## 7. Czego nie robimy (scope creep)

- Pełny redesign / nowy font / ilustracje stock.
- Dark mode w pierwszej iteracji (można **U6** — `_scratch.theme=dark`).
- 7. zakładka lub iframe Kokpitu.
- Animowane gradienty, glassmorphism, neon.

---

## 8. Decyzja Dowódcy

- [x] **U1–U5** — quiet landing, tokeny v5, KURS density, motion/calm, spec + guardy
- [ ] **GO deploy VPS** — Zasada 11 + smoke z deploy planu

**▶ TERAZ po merge:** `bash scripts/deploy-ready-hermes-ops.sh` → GO Dowódcy → `deploy-akademia-vps.sh`.
