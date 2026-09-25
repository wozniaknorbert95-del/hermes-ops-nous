# Plan — prawdziwa zakładka DSAAS + ścieżka Monetyzacji

**Data:** 2026-09-25  
**Status:** w realizacji (GO Dowódcy)  
**Gałąź:** `feat/dsaas-tab-id`  
**Nie:** 7. zakładka · 7. dział Kokpitu · sekrety · deploy bez osobnego GO

## Werdykt

Zakładka musi mieć `id:'dsaas'` i `renderMainPanel → renderKurs() → renderDsaas()`. Etykieta „DSAAS” na `id:kurs` to fałszywe drzwi. `firstOpen` musi iść po `KURS_DZIAL_ORDER` (H→G→B…→A), inaczej po H1 TERAZ wraca na A1.

## P0 (ten PR)

- [x] `ACADEMY_TABS` `id:'dsaas'`
- [x] `TAB_BY_DZIAL` H→dsaas, A→workflow
- [x] `firstOpen` po mapie H (nie `ALL_ROZ`)
- [x] `load()` / `goAcademyTab` / `#roz-*` mapują `kurs` → `dsaas`
- [x] dział A tylko w WORKFLOW (nie doklejany pod DSAAS)
- [x] guardy walidator + mutacje A6–A8

## P1 (już na main / ten PR)

INSTRUKCJA: max 1 `guide-card` open (winda). H accordion jest w `renderDsaas()` **przed** `#guide`.

## P2 — Dowódca (nie agent)

Widełki EUR w SKU + H2 outreach ×10.

## DoD

- linia `testy:` AGENTS.md PASS
- TERAZ pusty start = H1; po `H1_pass` = H2
- nav DSAAS otwiera mermaidy + accordion H
- 6 zakładek, zero `id:kurs` w `ACADEMY_TABS`
