# SLOWNIK-HERMESA — pinned facts (Hermes Akademii)

Każdy wpis: definicja kursu, po co, cytat ścieżki. Bez trafienia → „nie mam w źródłach”, nie Wikipedia.

## ODCS 3.1.0 ingress

**Co:** Pierwszy etap łańcucha: walidacja wejścia i wyjścia kontraktu ODCS 3.1.0.  
**Po co:** Brak kontraktu = brak wejścia do grafu. Kontrakt jest bramką, nie dokumentacją.  
**Źródło:** `runtime/odcs_validator.py` (kurs DSAAS / `HERMES_GLOSSARY` w `DASHBOARD.html`).

## HITL (human-stop)

**Co:** Agent proponuje intencję; zapisuje się wyłącznie intencja (append-only), nie wykonanie.  
**Po co:** Nieodwracalne decyzje wracają do Ciebie: reject z komentarzem, approve → execute_tool + receipt.  
**Źródło:** zakładka DSAAS — drill „Bramki człowieka”.

## Decision i Evidence Ledger

**Co:** Append-only dziennik decyzji i dowodów plus spany OTel GenAI.  
**Po co:** „Deprecated”, nie „delete” — historia decyzji jest dowodem.  
**Źródło:** `ledgery/README.md`.

## dsaas.governance.r7

**Co:** Weto R7: zgodność, bezpieczeństwo, governance. Sign-off W1–W7 rejestru zgodności.  
**Po co:** Growth nie przeskakuje zgodności.  
**Źródło:** `polityki/opa/r7_veto.rego`.

## dsaas.security

**Co:** Security-first: OWASP LLM01/05/06 oraz Art.50 disclosure.  
**Po co:** Deny = 403/STOP przed wzrostem.  
**Źródło:** `polityki/opa/security_runtime.rego`.

## dsaas.growth_decision

**Co:** Werdykt AUTO / REVIEW / BLOCK.  
**Po co:** Twarde naruszenie kończy sprawę na tym etapie.  
**Źródło:** `polityki/opa/growth_decision.rego`.

## dsaas.tenant_objective

**Co:** Tenant bez ratyfikowanej Objective Function = NO-GO (QF-TOR-1b).  
**Po co:** Brak growthu bez zdefiniowanego sukcesu najemcy.  
**Źródło:** `polityki/opa/quietforge_objective.rego`.

## dsaas.objective

**Co:** Wagi Objective Function i guardrails: approve ≥ 0.60, max_cpa_ratio ≤ 0.40, SLA lead ≤ 15 min.  
**Po co:** Werdykt policzalny, nie z odczucia.  
**Źródło:** `polityki/opa/objective_function.rego`.

## MCP execute_tool

**Co:** Bezstanowy MCP z header routing; execute_tool nie omija OPA.  
**Po co:** Narzędzie nie jest furtką — polityka przed wykonaniem.  
**Źródło:** `mcp/mcp_server.py`.

## Budżet złożoności (30 / 6 / 3 / 1)

**Co:** ≤30 bytów · ≤6 płaszczyzn · ≤3 agenty · ≤1 store.  
**Po co:** Przekroczenie = STOP + EV + Bramka zmian (arbitraż R1).  
**Źródło:** Konstytucja §3.3 — zakładka DSAAS / drill budżetu.

## Prowadzący vs builder

**Co:** Hermes Engineer (Nous) prowadzi sesję Cursor Cloud API; Cursor jest jedynym koderem. Tick tylko zapisuje status.  
**Po co:** Lead nie gumuje własnego kodu. Komentarz `@cursor` nie jest sesją.  
**Źródło:** `docs/ops/HERMES-ROLE-CONTRACT.md` · `docs/ops/PLAN-HERMES-CONDUCTOR-2026-10-01.md`.

## Izolacja najemcy (Cedar + RLS)

**Co:** Cedar default-deny → brak allow → 403; Postgres RLS → cross-tenant → 403.  
**Po co:** Dwie niezależne bramki przed wyciekiem.  
**Źródło:** diagram izolacji — zakładka DSAAS.
