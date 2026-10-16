# Handoff — HON-OPS-SELECT-NEXT PASS (2026-10-16)

**Atom:** `HON-OPS-SELECT-NEXT` · F3 residual · tor `NOUS-PRODUCT-LOOP`

## Problem (ORPHAN)

`POST /ops/run` `select_next` bez `issue_id` → `400 qui_not_in_queue` mimo niepustej kolejki Autopilot / `next` w statusie. UI też nie wysyłał `issue_id` gdy `recommended_issue` = null a `next` żyje.

## Fix

| Warstwa | Zmiana |
| --- | --- |
| vault | puste `issue_id` → `_recommended_issue` → else `next.id` → `_find_lane_issue` |
| OPS.html | `select_next`: `rec.id` else `next.id` |
| test | `select_next {}` → 200 + selected QUI-70 |

## DoD

- [x] `select_next` {} → 200 gdy Autopilot niepusty
- [x] UI fallback `next.id`
- [x] F5 polish nietknięty
- [x] `validate_todo_nous` + `test_progress_vault` PASS

## NEXT

Deploy vault (zmiana `progress_vault.py` + drobny OPS.html) → IDLE. F5 BLOCKED.
