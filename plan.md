# Plan — Reachy Mini Meditation Tutor

## Understanding (what you want)
Build a local Reachy Mini app named `reachy_mini_meditation_tutor` that runs against the daemon (simulation or real) and guides the user through timed breathing sessions.

- Fixed script (no LLM).
- Breathing pattern:
  - Inhale: 5 seconds
  - Exhale: 8 seconds
- Session durations:
  - 3 minutes
  - 5 minutes
  - 10 minutes
- Expressive motion during guidance.
- Local-only for now (no Hugging Face publish).

## Technical approach

### Core loop
- Compute total session duration in seconds.
- One breathing cycle duration = 5 + 8 = 13 seconds.
- Run `N = floor(session_seconds / 13)` cycles.
- Use `stop_event.is_set()` checks frequently to allow clean stopping from the dashboard.

### Motion design (expressive but safe)
Use `ReachyMini.goto_target()` for smooth, slow moves:
- “Inhale” motion: gentle lift + open posture
  - Slight head pitch up
  - Slight head roll/yaw sway
  - Antennas rise outward a bit
- “Exhale” motion: gentle settle
  - Head pitch down slightly
  - Reduce roll/yaw sway
  - Antennas return closer to neutral

Add small variation per cycle to avoid robotic repetition, while keeping within safe ranges.

### App structure
- Implement main app in `reachy_mini_meditation_tutor/main.py`.
- Keep motion primitives as helper functions within `main.py` initially.
- Optionally add a small web UI later under `reachy_mini_meditation_tutor/static/` to select 3/5/10 min and start/stop.

### Testing
- Run with the simulation daemon already started (`--sim`).
- Verify:
  - Robot moves in the MuJoCo viewer.
  - App can be stopped cleanly.
  - Timing roughly matches the 5/8 breathing cadence.

## Questions (already answered)
- Fixed script vs dynamic: **fixed**
- Session durations: **3/5/10**
- Interaction: **UI (later) / ok**
- Motion style: **expressive**
