---
title: Reachy Mini Meditation Tutor
emoji: 🧘
colorFrom: red
colorTo: blue
sdk: static
pinned: false
short_description: Guided breathing meditation for Reachy Mini
tags:
 - reachy_mini
 - reachy_mini_python_app
---

# Reachy Mini Meditation Tutor

A conversational zen meditation guide for [Reachy Mini](https://github.com/pollen-robotics/reachy_mini/) that combines OpenAI's realtime voice API with guided breathing sessions and synchronized robot movements.

## Features

- **Voice-guided breathing** — OpenAI TTS says "Breathe in… / Breathe out…" with configurable timing (default 6 s inhale, 8 s exhale)
- **Calming intro & outro** — session starts with a soothing introduction and ends with a congratulatory message
- **Synchronized head movements** — head tilts up on inhale, down on exhale, with subtle variation for a natural feel
- **Antenna animations** — antennas spread on inhale, narrow on exhale (optional)
- **Freshen-up animation** — gentle wake-up sequence after the session (look left/right/up, antenna wiggle)
- **Voice interrupt** — say "stop" mid-session to end early; mic is only muted during TTS playback
- **Session durations** — 3, 5, or 10 minutes
- **Zen personality** — calm, mindful conversational AI for before/after the session

---

## Setup for Teammates

### Prerequisites

| Requirement | Notes |
|-------------|-------|
| **Python 3.11+** | macOS / Linux |
| **Reachy Mini SDK** | `pip install "reachy-mini[mujoco]"` for simulation |
| **OpenAI API key** | Needs access to `gpt-realtime` and `tts-1` models |

### 1. Clone the repo

```bash
git clone https://github.com/suhaasteja/reachy_mini_meditation_tutor.git
cd reachy_mini_meditation_tutor
```

### 2. Create a virtual environment & install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip

# Install Reachy Mini SDK (with MuJoCo for simulation)
pip install "reachy-mini[mujoco]"

# Install the conversation app
cd reachy_mini_conversation_app
pip install -e .
cd ..
```

### 3. Configure environment variables

```bash
cd reachy_mini_conversation_app
cp .env.example .env
```

Edit `.env` and set:

```dotenv
OPENAI_API_KEY=sk-your-key-here
REACHY_MINI_CUSTOM_PROFILE=meditation_guide
```

### 4. Run (simulation)

**Terminal 1 — Start the Reachy Mini simulator:**

```bash
source .venv/bin/activate
mjpython -m reachy_mini.daemon.app.main --sim
```

Wait for the daemon to start, then verify at http://localhost:8000.

**Terminal 2 — Start the meditation guide:**

```bash
source .venv/bin/activate
cd reachy_mini_conversation_app
REACHY_MINI_CUSTOM_PROFILE=meditation_guide python -m reachy_mini_conversation_app.main --gradio
```

### 5. Open the UI

Go to **http://localhost:7860** in your browser.

1. Click **Connect**
2. Say or type: **"Start a 3 minute meditation"**
3. Watch Reachy guide you through breathing 🧘

### Running on a real robot

Skip Terminal 1 (no simulator needed). Make sure the robot is powered on and reachable, then run Terminal 2 as above.

---

## Voice Commands

| Action | Example |
|--------|---------|
| Start session | "Guide me through a 5 minute meditation" |
| Stop early | "Stop meditation" |
| Configure | "Set inhale to 4 seconds" / "Make the exhale 10 seconds" |
| Enable sounds | "Enable breath sounds" / "Use ocean sounds" |
| Disable antennas | "Disable the antennas" |

---

## Session Flow

```
1. Calming intro TTS  →  "Let's get started… We will breathe in for 6 seconds…"
2. Breathing loop      →  "Breathe in…" (6 s) → "Breathe out…" (8 s) × N cycles
3. Calming outro TTS   →  "Well done… You did beautifully… Namaste."
4. Freshen-up animation →  Gentle head look-around + antenna wiggle (5 s)
```

Head movements stay at neutral during the intro, then sync precisely with each breathing phase via a shared `intro_done` event.

---

## Architecture

All meditation-specific code lives in the conversation app profile:

```
reachy_mini_conversation_app/src/reachy_mini_conversation_app/profiles/meditation_guide/
├── instructions.txt            # Zen personality prompt for the LLM
├── tools.txt                   # Enabled tools list
├── voice.txt                   # Voice setting (shimmer)
├── __init__.py
├── meditation_orchestrator.py  # TTS orchestrator (intro → breathing loop → outro)
├── meditation_move.py          # MeditationMove — 100 Hz head/antenna breathing
├── freshen_up_move.py          # Post-session wake-up animation (5 s)
├── start_meditation.py         # start_meditation tool
├── stop_meditation.py          # stop_meditation tool (voice-interruptible)
├── configure_meditation.py     # configure_meditation tool
├── meditation_config.py        # Runtime config (inhale/exhale/antennas/sounds)
└── breath_sounds.py            # Audio generation (ambient/ocean/white noise)
```

### Key threading events (in `meditation_orchestrator.py`)

| Event | Purpose |
|-------|---------|
| `mic_muted` | Set during each TTS playback + 0.5 s tail to prevent audio feedback |
| `meditation_active` | Set for the entire session; suppresses LLM audio output to prevent echoing |
| `stop_session` | Set by `stop_meditation` tool; checked every 0.25 s for clean interruption |
| `intro_done` | Set after intro TTS finishes; `MeditationMove` waits for this before starting breathing |

---

## Default Settings

| Parameter | Default |
|-----------|---------|
| Inhale | 6 seconds |
| Exhale | 8 seconds |
| Antennas | Enabled |
| Breath sound | Disabled |
| Sound type | Ambient |

All configurable at runtime via voice commands or the `configure_meditation` tool.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | `cd reachy_mini_conversation_app && pip install -e .` |
| Profile not found | Verify `ls src/reachy_mini_conversation_app/profiles/meditation_guide/` |
| OpenAI API errors | Check `OPENAI_API_KEY` in `.env` and account credits |
| Port already in use | `lsof -ti :7860 \| xargs kill -9` |
| scipy import error | `pip uninstall scipy reachy-mini && pip install "reachy-mini[mujoco]"` |
| Robot timeout | Ensure the daemon is running (`mjpython -m reachy_mini.daemon.app.main --sim`) |

---

## License

Apache 2.0