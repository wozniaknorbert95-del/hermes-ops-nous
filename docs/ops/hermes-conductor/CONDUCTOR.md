# CONDUCTOR — procedura 6 kroków

Obowiązkowa. Pominięcie narzędzia D = nie wolno ogłosić PASS.

1. **Zczytaj** Linear: 6 pól, lista AC (checkbox / numerowane), etykiety, `repo`. DoR dziurawe → refuse, nie startuj Cursora.
2. **Brief** dla Cloud API: AC, DoD ids z kanonu których plików issue dotyczy, zakazy (zero deploy/SSH/sekretów), `work_mode` (`buduj` | `testuj` | `ulepszaj`).
3. **Sesja:** `POST /v1/agents` albo follow-up `POST /v1/agents/{id}/runs` na **tym samym** `agentId`. Zapisz `run_url`.
4. **Strumień:** SSE `tool_call` → `live.tests[]` (cmd, excerpt, PASS|FAIL|UNKNOWN). Puste w RUNNING = UNKNOWN testów.
5. **Narzędzie D** (mandatory): DoR, każdy punkt AC, required checks, dirty PR, R7/HITL. FAIL D → follow-up (limit `OPS_CONDUCTOR_MAX_FOLLOWUPS`) albo HITL. J (treść AC / UX) **tylko po** D.
6. **Raport** `live.conductor.report_pl`: zrobione · do laptopa · padło · następny pin. Tryb `ulepszaj` = jeden draft issue, zero kodu. Tryb `testuj` = nie merge.

Take over / Pause: cancel active run, archive agenta, zero nowego follow-up. Nie Start next przy stale lock (QUI-88).
