# Meditation Guide - Quick Start

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies
```bash
cd /Users/mac/Desktop/reachy_mini_meditation_tutor/reachy_mini_conversation_app
pip install -e .
```

### Step 2: Set Your OpenAI API Key
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your API key:
# OPENAI_API_KEY=sk-your-key-here
# REACHY_MINI_CUSTOM_PROFILE=meditation_guide
```

### Step 3: Start Simulation (Terminal 1)
```bash
mjpython -m reachy_mini.daemon.app.main --sim
```

Wait for "Server started" message, then open http://localhost:8000 to verify.

### Step 4: Run Meditation Guide (Terminal 2)
```bash
cd /Users/mac/Desktop/reachy_mini_meditation_tutor/reachy_mini_conversation_app
REACHY_MINI_CUSTOM_PROFILE=meditation_guide python -m reachy_mini_conversation_app.main --gradio
```

### Step 5: Open Browser
Go to http://localhost:7860

### Step 6: Test It!
1. Click "Connect"
2. Say or type: **"Start a 3 minute meditation"**
3. Watch Reachy breathe! 🧘

## 🎯 Quick Commands to Try

```
"Guide me through a 5 minute meditation"
"Make the exhale 10 seconds"
"Enable breath sounds"
"Use ocean sounds"
"Stop meditation"
```

## 📁 What Was Created

```
reachy_mini_conversation_app/
└── src/reachy_mini_conversation_app/
    └── profiles/
        └── meditation_guide/
            ├── meditation_move.py         # Breathing cycles
            ├── start_meditation.py        # Start tool
            ├── configure_meditation.py    # Config tool
            ├── stop_meditation.py         # Stop tool
            ├── breath_sounds.py           # Audio (ambient/ocean/white noise)
            ├── meditation_config.py       # Settings management
            ├── instructions.txt           # Zen personality
            ├── tools.txt                  # Enabled tools
            ├── voice.txt                  # Voice setting
            └── README.md                  # Full documentation
```

## 🎨 Features

- **Voice Control**: Natural language for everything
- **Configurable**: Adjust inhale/exhale, antennas, sounds
- **3 Sound Types**: Ambient tones, ocean waves, white noise
- **Zen Personality**: Calm, mindful conversation
- **Smooth Motion**: 100Hz control loop (way smoother than standalone app)

## 📚 Documentation

- **Full Setup**: See `MEDITATION_GUIDE_SETUP.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **Profile README**: See `reachy_mini_conversation_app/src/reachy_mini_conversation_app/profiles/meditation_guide/README.md`

## 🐛 Troubleshooting

**"Module not found"**
```bash
cd reachy_mini_conversation_app
pip install -e .
```

**"Profile not found"**
```bash
# Check it exists:
ls src/reachy_mini_conversation_app/profiles/meditation_guide/
```

**scipy import error**
```bash
pip uninstall scipy reachy-mini
pip install "reachy-mini[mujoco]"
```

## ✨ Migration Complete!

Your standalone meditation app is now a conversational zen guide. Enjoy! 🧘‍♂️
