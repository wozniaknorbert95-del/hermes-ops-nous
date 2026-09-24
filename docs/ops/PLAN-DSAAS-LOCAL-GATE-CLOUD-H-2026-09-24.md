# Plan + DoD — 2026-09-24 (Akademia)

**Kontekst:** brak kasy na GitHub Actions; zgubiona zakładka DSAAS; otwarty Cloud PR #64 (dział H).

**Zasady:** 6 zakładek (nie 7.); Kokpit bez 7. działu; dział H = treść kursu (nie Kokpit); merge bez płatnego CI; deploy VPS tylko na GO.

---

## T1 — Bramka bez płatnego GitHuba

**Co:** Actions na `ubuntu-latest` w prywatnym repo **pali minuty**. `academy-gate` i tak pada (billing). Prawda = laptop: `bash scripts/deploy-ready-hermes-ops.sh`.

**Jak:**
1. `academy-gate.yml` → tylko `workflow_dispatch` (ręczny, gdy kiedyś będzie runner).
2. Zdjąć required check `academy-gate` z `main` (inaczej PR nigdy nie wejdzie).
3. Docs: `docs/ops/LOCAL-GATE.md` + linia w `AGENTS.md`.

**DoD T1**
- [ ] Push/PR **nie** startuje `ubuntu-latest` (zero minut).
- [ ] `main` **nie** wymaga `academy-gate`.
- [ ] Lokalnie: `deploy-ready-hermes-ops.sh` nadal jest bramką przed VPS.
- [ ] Fala J nadal widzi listę mutacji w pliku workflow (plik zostaje).

---

## T2 — Przywrócenie DSAAS (mermaidy + platforma)

**Fakt:** `renderDsaas()` jest w `DASHBOARD.html`, ale `renderMainPanel` woła tylko `renderKurs()`. `#dsaas` → `#guide`. Dane nie usunięte — odłączone.

**Jak (6 zakładek):**
- Tytuł zakładki `KURS` → **DSAAS** (`id` zostaje `kurs` — mniej rozjazdów guardów).
- `renderKurs()` zaczyna od pełnego `renderDsaas()`: produkt, galeria mermaid (przepływy), scoreboard, mistrzostwo, działy B–G.
- Potem INSTRUKCJA + Hermes + dział A (gym).
- `#dsaas` / stary `active_tab=dsaas` → panel DSAAS, kotwica `#dsaas` (nie guide).

**DoD T2**
- [ ] Nav pokazuje **DSAAS**. Nadal 6 zakładek (`ACADEMY_TAB_COUNT=6`).
- [ ] Widoczne: PRODUCT_MISSION, `DIAGRAMS.platform` + chain/hitl/agents/isolation/surfaces/budget, mastery, scoreboard.
- [ ] `#dsaas` scrolluje do bloku produktu, nie do INSTRUKCJI.
- [ ] `python scripts/validate-academy-export.py` + Fala 0/D/L/M PASS.
- [ ] Browser: klik DSAAS, mermaid rysuje się (lub ASCII fallback).

---

## T3 — Przejęcie Cloud PR #64 (dział H)

**Fakt:** draft [#64](https://github.com/wozniaknorbert95-del/akademia/pull/64) — H1–H3, SKU, outreach. Cloud mylił „8. dział Kokpitu” z **8. działem kursu**. AGENTS: 7. dział **Kokpitu** zakazany; H w kursie = GO Dowódcy (to przejęcie).

**Jak:** rebase na `main` po T1+T2; nie dublować mermaidów; `firstOpen` H1 tylko przy pustym postępie; guardy A–H z rozróżnieniem Kokpit vs kurs.

**DoD T3**
- [ ] Branch zrebasowany na aktualny `main` (heartbeat + SIGPIPE).
- [ ] H1–H3 + 3 pliki `docs/akademia/*`; TERAZ przy pustym stanie = H1.
- [ ] Nadal 6 zakładek; DSAAS mermaidy nie znikają.
- [ ] Pełna linia `testy:` z AGENTS.md PASS.
- [ ] PR #64 zaktualizowany albo zastąpiony jednym PR lokalnym (draft → ready po testach).

---

## T4 — Weryfikacja

**DoD T4**
- [ ] Pełna linia `testy:` PASS.
- [ ] Przeglądarka: DSAAS mermaid + (jeśli T3) H1 na TERAZ.
- [ ] Handoff w `docs/handoffs/`.
- [ ] Deploy VPS **nie** — czekamy na GO.
