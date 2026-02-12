# Meditation Guide Setup for Teammates

This guide will help you set up and run the Reachy Mini Zen Meditation Guide.

## What This Is

A conversational meditation guide for Reachy Mini that:
- Guides breathing meditation sessions (3, 5, or 10 minutes)
- Uses smooth, gentle movements (head tilt + Z-axis breathing)
- Plays realistic breath sounds (Reachy's sleep sound for exhale, reversed for inhale)
- Has a zen personality for calming conversations
- Fully voice-controlled via natural language

## Prerequisites

1. **Python 3.11+**
2. **Reachy Mini SDK** installed
3. **OpenAI API Key** (for conversational AI)

## Installation Steps

### 1. Clone This Repository

```bash
git clone <your-repo-url>
cd reachy_mini_meditation_tutor
```

### 2. Clone the Conversation App

```bash
git clone https://github.com/pollen-robotics/reachy_mini_conversation_app.git
cd reachy_mini_conversation_app
```

### 3. Install Dependencies

```bash
# Install Reachy Mini SDK with simulation support
pip install "reachy-mini[mujoco]"

# Install the conversation app
pip install -e .
```

### 4. Copy Meditation Profile

```bash
# Copy the meditation_guide profile into the conversation app
cp -r ../meditation_guide_profile src/reachy_mini_conversation_app/profiles/meditation_guide
```

### 5. Configure Environment

Create a `.env` file in the `reachy_mini_conversation_app` directory:

```bash
cd reachy_mini_conversation_app
cat > .env << 'EOF'
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME="gpt-realtime"
REACHY_MINI_CUSTOM_PROFILE=meditation_guide
LOCAL_VISION_MODEL=HuggingFaceTB/SmolVLM2-2.2B-Instruct
HF_HOME=./cache
HF_TOKEN=
EOF
```

**Important:** Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Running the Meditation Guide

### Option 1: In Simulation (Recommended for Testing)

**Terminal 1 - Start Simulation:**
```bash
mjpython -m reachy_mini.daemon.app.main --sim
```

Wait for "Daemon started successfully" message, then open http://localhost:8000 to verify.

**Terminal 2 - Start Meditation Guide:**
```bash
cd reachy_mini_conversation_app
python -m reachy_mini_conversation_app.main --gradio
```

**Browser:**
Open http://localhost:7860

### Option 2: On Real Robot

**Terminal 1 - Start Meditation Guide:**
```bash
cd reachy_mini_conversation_app
python -m reachy_mini_conversation_app.main --gradio
```

**Browser:**
Open http://localhost:7860

## Using the Meditation Guide

### Basic Commands

**Start a session:**
- "Start a 3 minute meditation"
- "Guide me through a 5 minute meditation"
- "Let's meditate for 10 minutes"

**Enable breath sounds:**
- "Enable breath sounds"
- "Turn on breathing sounds"

**Configure breathing:**
- "Make the exhale 10 seconds"
- "Set inhale to 6 seconds"
- "Disable the antennas"
- "Use ocean sounds"

**Stop early:**
- "Stop meditation"

**Chat:**
- "I'm feeling stressed"
- "Tell me about meditation"

### Default Settings

- **Inhale**: 5 seconds
- **Exhale**: 8 seconds
- **Antennas**: Enabled
- **Breath Sound**: Disabled (enable via voice)
- **Sound Type**: Ambient (uses sleep sound)

## Features

### Smooth Movements
- Gentle ±6-8° head pitch (not abrupt like before)
- Z-axis breathing depth (lifts 1cm on inhale, lowers 0.5cm on exhale)
- Sinusoidal easing for natural acceleration/deceleration
- Subtle yaw/roll variation (±1-2°) for natural feel

### Breath Sounds
- **Exhale**: Reachy's actual `go_sleep.wav` shutdown sound (calming)
- **Inhale**: Time-reversed exhale sound (gentle intake)
- Automatically timed with movements
- Graceful fallback if sounds unavailable

### Zen Personality
- Calm, mindful conversational style
- Short, peaceful responses
- Can provide meditation guidance
- Responds compassionately to stress

## Troubleshooting

### "Module not found" errors
```bash
cd reachy_mini_conversation_app
pip install -e .
```

### "Profile not found" errors
```bash
# Verify the profile exists
ls src/reachy_mini_conversation_app/profiles/meditation_guide/

# Should show:
# - instructions.txt
# - tools.txt
# - meditation_move.py
# - start_meditation.py
# - etc.
```

### scipy import errors
```bash
pip uninstall scipy reachy-mini
pip install "reachy-mini[mujoco]"
```

### Port already in use
```bash
# Kill processes on ports 8000 and 7860
lsof -ti :8000 | xargs kill -9
lsof -ti :7860 | xargs kill -9
```

### Breath sounds not playing
1. Make sure you said "Enable breath sounds"
2. Check that `breath_sound_enabled` is True in config
3. Verify audio system is working (try other Reachy sounds)

## File Structure

```
reachy_mini_meditation_tutor/
├── meditation_guide_profile/          # Your custom profile
│   ├── instructions.txt               # Zen personality
│   ├── tools.txt                      # Enabled tools
│   ├── voice.txt                      # Voice setting
│   ├── meditation_move.py             # Breathing movements
│   ├── start_meditation.py            # Start tool
│   ├── configure_meditation.py        # Config tool
│   ├── stop_meditation.py             # Stop tool
│   ├── meditation_config.py           # Settings management
│   ├── breath_sounds.py               # Audio generation
│   └── README.md                      # Profile docs
├── reachy_mini_conversation_app/      # Cloned conversation app
│   └── src/reachy_mini_conversation_app/
│       └── profiles/
│           └── meditation_guide/      # Copied from above
└── SETUP_FOR_TEAMMATES.md             # This file
```

## Development Notes

### Modifying the Meditation Profile

All meditation-specific code is in `meditation_guide_profile/`:

- **Movements**: Edit `meditation_move.py` (pitch angles, Z-axis, easing)
- **Personality**: Edit `instructions.txt` (zen prompts)
- **Tools**: Add new tools as Python files
- **Sounds**: Edit `breath_sounds.py` (audio generation)

After making changes, copy to conversation app:
```bash
cp -r meditation_guide_profile/* reachy_mini_conversation_app/src/reachy_mini_conversation_app/profiles/meditation_guide/
```

### Testing Changes

1. Stop the app (Ctrl+C)
2. Copy updated profile
3. Restart the app
4. Test in browser

## Support

For issues:
1. Check this guide's troubleshooting section
2. Review the profile README: `meditation_guide_profile/README.md`
3. Check conversation app docs: https://github.com/pollen-robotics/reachy_mini_conversation_app

## Quick Reference

**Start everything:**
```bash
# Terminal 1
mjpython -m reachy_mini.daemon.app.main --sim

# Terminal 2
cd reachy_mini_conversation_app
python -m reachy_mini_conversation_app.main --gradio

# Browser: http://localhost:7860
```

**Test meditation:**
```
1. Click "Connect"
2. Say: "Enable breath sounds"
3. Say: "Start a 3 minute meditation"
4. Watch Reachy breathe peacefully 🧘
```

Enjoy your zen meditation sessions!
