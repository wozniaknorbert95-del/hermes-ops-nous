# CONDUCTOR — procedura 6 kroków

Obowiązkowa. Pominięcie narzędzia D = nie wolno ogłosić PASS.

1. **Zczytaj** Linear: 6 pól, lista AC (checkbox / numerowane), etykiety, `repo`. DoR dziurawe → refuse, nie startuj Cursora. Handoff (lab): `url`, `ac[]`, `dor_excerpts`, `brief_kind`.
2. **Brief** dla Cloud API (implementacja: `workflow-lab` `hermes_conductor/loop.py`):
   - `brief_kind=real` (default): repo + AC/DoR excerpts + `.cursor/commands/autopilot.md` + `work_mode`. Nie szablon `conductor-lab-probe.md`.
   - `brief_kind=lab_probe` (smoke QUI-13x / `lab-smoke`): slice probe w `workflow-lab`.
3. **Sesja:** `POST /v1/agents` albo follow-up `POST /v1/agents/{id}/runs` na **tym samym** `agentId` (steer na FAIL AC). Zapisz `run_url`.
4. **Strumień:** SSE `tool_call` → `live.tests[]` (cmd, excerpt, PASS|FAIL|UNKNOWN). Puste w RUNNING = UNKNOWN testów.
5. **Narzędzie D** (mandatory): DoR, każdy punkt AC, required checks, dirty PR, R7/HITL. FAIL D → follow-up (limit `OPS_CONDUCTOR_MAX_FOLLOWUPS`) albo HITL. J (treść AC / UX) **tylko po** D.
6. **Raport** `live.conductor.report_pl`: zrobione · do laptopa · padło · następny pin. Tryb `ulepszaj` = jeden draft issue, zero kodu. Tryb `testuj` = nie merge.

Take over / Pause: cancel active run, archive agenta, zero nowego follow-up. Nie Start next przy stale lock (QUI-88).
