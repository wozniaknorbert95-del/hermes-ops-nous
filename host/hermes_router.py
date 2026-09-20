"""Hermes B2 router + pinned replies (vault + eval parity with DASHBOARD local engine)."""
from __future__ import annotations

import re
import unicodedata
from typing import Any

GLOSSARY_KEYS = [
    "odcs",
    "hitl",
    "human-stop",
    "ledger",
    "otel",
    "r7",
    "security",
    "owasp",
    "growth",
    "werdykt",
    "tenant",
    "objective",
    "guardrail",
    "mcp",
    "budżet",
    "budzet",
    "złożoności",
    "zlozonosci",
    "cedar",
    "rls",
    "izolacj",
]

STATE_RE = re.compile(
    r"instalac|co dalej|co mam|teraz zrob|gdzie jestem|lock|rytua|dzie[nń]|"
    r"jak u[zż]ywa|eksport|sync|mistrzostw|drill|podaj|poka[zż]|klucz|token|sekret",
    re.I,
)

PINNED_FACTS: dict[str, str] = {
    "odcs": (
        "ODCS 3.1.0 ingress\n"
        "Co to: Pierwszy etap łańcucha — walidacja wejścia i wyjścia kontraktu ODCS 3.1.0.\n"
        "Dlaczego: Brak kontraktu = brak wejścia do grafu.\n"
        "Źródło: runtime/odcs_validator.py (docs/SLOWNIK-HERMESA.md)"
    ),
    "r7": (
        "dsaas.governance.r7\n"
        "Co to: Weto R7 — zgodność, bezpieczeństwo, governance.\n"
        "Źródło: polityki/opa/r7_veto.rego"
    ),
}


def norm(s: str) -> str:
    t = unicodedata.normalize("NFD", str(s or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return t.replace("ł", "l")


def hermes_intent(question: str) -> str:
    q = str(question or "").lower()
    qn = norm(question)
    if re.search(r"(podaj|poka[zż]|daj).*(klucz|token|sekret|vault|has[lł])", q):
        return "state"
    if STATE_RE.search(q):
        return "state"
    if re.search(r"\b([a-h])(\d{1,2})\b", q):
        return "state"
    for key in GLOSSARY_KEYS:
        kn = norm(key)
        if key in q or kn in qn:
            return "fact"
    return "open"


def hermes_local_reply(question: str, state: dict[str, Any] | None, intent: str) -> str | None:
    q = str(question or "")
    ql = q.lower()
    st = state if isinstance(state, dict) else {}

    if re.search(r"(podaj|poka[zż]|daj).*(klucz|token|sekret|vault|has[lł])", ql):
        return (
            "Nie podam — zero sekretów w rozmowie. Klucze API żyją tylko w env vaulta na VPS, "
            "nie w repo ani w eksporcie postępu."
        )

    if intent == "fact":
        qn = norm(q)
        for key, text in PINNED_FACTS.items():
            if key in ql or norm(key) in qn:
                return text
        for key in GLOSSARY_KEYS:
            if key in ql or norm(key) in qn:
                return f"Nie mam rozszerzonego wpisu dla „{key}” w vault — zajrzyj do docs/SLOWNIK-HERMESA.md."

    if re.search(r"zmerguj|deploy", ql):
        return None

    lock = "LOCK" in str(st.get("day_lock") or "") or "LOCK" in str(st.get("priority") or "")
    if lock and re.search(r"co mam|co dalej|teraz|teraz zrob|nast[eę]pn", ql):
        lines = [
            "PRIORYTET: zakładka DZIEŃ — domknij rytuał, zanim pójdziesz w rozdział.",
        ]
        if st.get("next"):
            lines.append(str(st["next"]))
        if st.get("day_missing"):
            lines.append("Lista do odklikania: " + str(st["day_missing"]))
        return "\n".join(lines)

    if re.search(r"co dalej|nast[eę]pn|od czego|zacznij", ql):
        nxt = st.get("next")
        if nxt:
            return f"Jeden kawał: {nxt}"

    if re.search(r"jak u[zż]ywa|pomoc|help|instrukcj", ql):
        return (
            "Jak używać Akademii:\n"
            "1. TERAZ — jeden rozdział.\n"
            "2. DZIEŃ — rytuał; bez zielonego rytuału LOCK.\n"
            "3. WORKFLOW / NARZĘDZIA / DSAAS — świadomie.\n"
            "4. HERMES — read-only kierunek i pojęcia."
        )

    if intent == "state":
        return "Nie mam tego w źródłach vault — użyj zakładki TERAZ lub doprecyzuj pytanie."

    return None
