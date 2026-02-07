# Reachy Mini Meditation Tutor (local app)

## What this is
A Reachy Mini app that runs against the Reachy Mini daemon (simulation or real robot) and guides a timed breathing session.

- Fixed cadence:
  - Inhale: 5s
  - Exhale: 8s
- Session durations:
  - 3 / 5 / 10 minutes
- Expressive motion (head + antennas)
- Optional synthesized breathing sound (toggle in the app UI)

## Where the code lives
- App logic: `reachy_mini_meditation_tutor/main.py`
- App UI (served by the app): `reachy_mini_meditation_tutor/static/`
- Plan / notes: `plan.md`

## Run the simulation (macOS)
Use the venv under `~/reachy_mini_resources/.venv` (MuJoCo GUI works best via `mjpython` on macOS):

```bash
source /Users/mac/reachy_mini_resources/.venv/bin/activate
mjpython -m reachy_mini.daemon.app.main --sim
```

Dashboard:
- http://localhost:8000

## Install the app into the daemon environment (recommended)
So it shows up in the Dashboard "Apps" list:

```bash
source /Users/mac/reachy_mini_resources/.venv/bin/activate
pip install -e /Users/mac/reachy_mini_resources/reachy_mini_meditation_tutor
```

Then restart the daemon.

## Start / test the meditation app
### Option A: From the Dashboard (recommended)
1. Open http://localhost:8000
2. Go to Apps
3. Toggle `reachy_mini_meditation_tutor` on
4. Click the ⚙️ icon to open the app settings UI

### Option B: Run directly (dev)
```bash
source /Users/mac/reachy_mini_resources/.venv/bin/activate
python /Users/mac/reachy_mini_resources/reachy_mini_meditation_tutor/reachy_mini_meditation_tutor/main.py
```

App UI:
- http://localhost:8042

## App UI features
- Antennas toggle
- Breathing sound toggle
- Session duration buttons: 3 / 5 / 10 min
- Start / Stop buttons

## App endpoints (served by the app on :8042)
- `POST /antennas` body `{ "enabled": true|false }`
- `POST /breath_sound` body `{ "enabled": true|false }`
- `POST /session` body `{ "minutes": 3|5|10 }`
- `POST /start`
- `POST /stop`

## Breathing sound implementation
The breathing sound is synthesized in Python (no external audio file required):
- Generate noise
- Apply slow modulation + fade-in/out envelope
- Stream via `reachy_mini.media.start_playing()` and `reachy_mini.media.push_audio_sample(...)`

If audio output is not satisfactory, a future alternative is to use a `.wav` breath sound via `reachy_mini.media.play_sound(...)`.
