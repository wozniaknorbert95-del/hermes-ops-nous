# Cursor workflow — akademia

Krótkie rytuały sesji. Wklej blok do Cursora na start / debug / przed MR / na koniec.

---

## vibeinit — start sesji (2 min)

```
Repo: akademia (szkoła + Hermes Ops /ops, NIE workflow-lab, NIE dsaas-platform-main).
Przeczytaj: AGENTS.md, README.md, docs/OPERATING-MODEL.md (§1–3, §1.1 split).
Jeśli dotykasz /ops, vault lub tick: docs/ops/README.md → HERMES-ROLE-CONTRACT → RUNBOOK-OPS-WIRING.
Otwórz DASHBOARD.html — zakładka TERAZ = jedyny „co teraz” kursu; praca agentowa = /ops (osobna PWA).
Uruchom: python -m http.server 8765 → localhost:8765/DASHBOARD.html i localhost:8765/ops
Gate: python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
Zasady: jedno #nowcard, eksport schema 0.1.0, zero sekretów w academy_url, brak iframe Kokpitu, telefon nie merguje.
Powiedz: co jest w ▶ TERAZ, czy sesja dotyka /ops, i jaki jeden plik dotykamy.
```

---

## rootcause — gdy coś nie działa (DNS / VPS / sync)

```
Symptom: [wklej błąd — np. DNS_PROBE, 401, sync conflict, vault 500]
Sprawdź w kolejności:
1. DNS: nslookup akademia.quietforge.flexgrafik.nl ns1.cyberfolks.pl
        dig +short akademia.quietforge.flexgrafik.nl A @8.8.8.8
2. VPS vault: ssh root@185.243.54.115 'curl -fsS http://127.0.0.1:8097/health'
3. nginx: ssh … 'curl -fsSI -H Host:akademia.quietforge.flexgrafik.nl -u academy:*** http://127.0.0.1/DASHBOARD.html | head -5'
4. TLS: ls /etc/letsencrypt/live/akademia.quietforge.flexgrafik.nl/
5. Sync: GET/PUT /progress — envelope schema_version 0.1.0, source academy-os
Runbook: docs/runbooks/AKADEMIA-VPS.md
Nie zgaduj — podaj root cause + jeden fix. Nie deployuj bez GO Dowódcy (Zasada 11).
```

---

## auditread — przed merge / po większej zmianie UI

```
Przeczytaj: docs/ACADEMY-UX-SPEC.md, schema/academy-progress.v0.json, AGENTS.md.
Uruchom: python scripts/validate-academy-export.py && python scripts/test_progress_vault.py
Sprawdź ręcznie (360px + 768px): jedno TERAZ, sticky taby, scroll-margin kotwic, sync-bar stany.
Mermaid: kontrast edgeLabel ≥ 4.5:1; offline = fallback tekstowy jeśli CDN padnie.
Eksport JSON: schema_version 0.1.0, source academy-os, academy_url bez tokenów, _scratch OK.
Wynik: PASS / lista findingów z repro + plik podejrzany.
Skill opcjonalny: ux-audit na localhost:8765 dla pełnego sweepu.
```

---

## team handoff — koniec sesji

```
Zapisz docs/handoffs/YYYY-MM-DD-krotki-tytul.md z sekcjami:
- Co zrobione (fakty, nie plany)
- Co live (URL, smoke)
- Co zablokowane (blocker + właściciel)
- Następny krok (jeden TERAZ)
- Komendy weryfikacji (copy-paste)
- Pliki dotknięte (lista)
Zero sekretów w handoffie — hasła tylko „VPS CREDENTIALS.local.txt”.
Nie commituj bez prośby Dowódcy.
```

Szablon pliku: skopiuj ostatni handoff z `docs/handoffs/` i podmień sekcje.
