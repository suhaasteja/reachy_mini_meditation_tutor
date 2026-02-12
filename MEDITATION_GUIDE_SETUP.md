# Meditation Guide Setup Instructions

This guide will help you set up and run the Zen Meditation Guide profile for Reachy Mini.

## Prerequisites

1. **Reachy Mini SDK installed**
   ```bash
   pip install "reachy-mini[mujoco]"  # For simulation
   # OR
   pip install reachy-mini  # For real robot
   ```

2. **OpenAI API Key**
   - Get your API key from https://platform.openai.com/api-keys
   - Set it in your environment or .env file

## Installation

### 1. Navigate to the conversation app directory
```bash
cd /Users/mac/Desktop/reachy_mini_meditation_tutor/reachy_mini_conversation_app
```

### 2. Install the conversation app
```bash
pip install -e .
```

### 3. Create .env file (if not exists)
```bash
cp .env.example .env
```

### 4. Configure .env file
Edit `.env` and add:
```bash
OPENAI_API_KEY=your_api_key_here
REACHY_MINI_CUSTOM_PROFILE=meditation_guide
```

## Running in Simulation

### 1. Start the Reachy Mini simulation daemon
In one terminal:
```bash
mjpython -m reachy_mini.daemon.app.main --sim
```

Wait for it to start, then open http://localhost:8000 to verify the simulation is running.

### 2. Run the meditation guide app
In another terminal:
```bash
cd /Users/mac/Desktop/reachy_mini_meditation_tutor/reachy_mini_conversation_app
REACHY_MINI_CUSTOM_PROFILE=meditation_guide python -m reachy_mini_conversation_app.main --gradio
```

### 3. Open the Gradio interface
Open http://localhost:7860 in your browser.

## Running on Real Robot

### 1. Ensure robot is powered on and connected

### 2. Run the meditation guide app
```bash
cd /Users/mac/Desktop/reachy_mini_meditation_tutor/reachy_mini_conversation_app
REACHY_MINI_CUSTOM_PROFILE=meditation_guide python -m reachy_mini_conversation_app.main --gradio
```

## Quick Test

Once the app is running:

1. **Click "Connect"** in the Gradio interface
2. **Say or type**: "Hello"
   - Expected: Zen greeting from Reachy
3. **Say or type**: "Start a 3 minute meditation"
   - Expected: Meditation session begins with breathing movements
4. **Observe**: Head tilts up/down, antennas move (if enabled)
5. **Say or type**: "Stop meditation"
   - Expected: Session stops gracefully

## Voice Commands to Try

### Starting Sessions
- "Guide me through a 5 minute meditation"
- "Let's meditate for 10 minutes"
- "Start a quick 3 minute session with breathing sounds"

### Configuring
- "Make the exhale 10 seconds"
- "Set inhale to 6 seconds"
- "Enable breath sounds"
- "Use ocean sounds"
- "Disable the antennas"

### Stopping
- "Stop meditation"
- "End the session"

## Troubleshooting

### "Module not found" errors
```bash
# Reinstall the conversation app
cd /Users/mac/Desktop/reachy_mini_meditation_tutor/reachy_mini_conversation_app
pip install -e .
```

### "Profile not found" errors
```bash
# Verify the profile exists
ls src/reachy_mini_conversation_app/profiles/meditation_guide/

# Should show:
# - instructions.txt
# - tools.txt
# - voice.txt
# - meditation_move.py
# - start_meditation.py
# - configure_meditation.py
# - stop_meditation.py
# - meditation_config.py
# - breath_sounds.py
```

### OpenAI API errors
- Verify your API key is set correctly in .env
- Check you have credits in your OpenAI account
- Ensure you're using a valid model (gpt-realtime)

### Robot connection issues
- For simulation: Ensure daemon is running on port 8000
- For real robot: Check network connection and robot IP
- Try: `curl http://localhost:8000/status` (should return JSON)

### Audio not working
- Breath sounds are optional - meditation works without them
- Check robot's audio system is initialized
- Try enabling sounds: "Enable breath sounds"

## Configuration Options

### Breathing Parameters
- **Inhale**: 2-15 seconds (default: 5s)
- **Exhale**: 3-20 seconds (default: 8s)
- **Antennas**: On/Off (default: On)
- **Breath Sound**: On/Off (default: Off)
- **Sound Type**: ambient/ocean/white_noise (default: ambient)

### Session Durations
- 3 minutes
- 5 minutes
- 10 minutes

## File Structure

```
reachy_mini_conversation_app/
└── src/reachy_mini_conversation_app/
    └── profiles/
        └── meditation_guide/
            ├── README.md                  # Profile documentation
            ├── instructions.txt           # Zen personality prompt
            ├── tools.txt                  # Enabled tools
            ├── voice.txt                  # Voice setting
            ├── __init__.py                # Package init
            ├── meditation_move.py         # Breathing move implementation
            ├── meditation_config.py       # Configuration management
            ├── start_meditation.py        # Start tool
            ├── configure_meditation.py    # Config tool
            ├── stop_meditation.py         # Stop tool
            └── breath_sounds.py           # Audio generation
```

## Next Steps

1. **Test in simulation** to verify everything works
2. **Try different voice commands** to explore features
3. **Experiment with configurations** (inhale/exhale timing, sounds)
4. **Test on real robot** when ready
5. **Customize personality** by editing `instructions.txt`

## Comparison: Standalone vs Conversation App

| Feature | Standalone App | Conversation App |
|---------|---------------|------------------|
| Control | HTTP API | Voice + UI |
| Motion | Blocking goto | 100Hz control loop |
| Conversation | None | Full AI chat |
| Configuration | Manual API calls | Voice commands |
| Integration | Isolated | Part of ecosystem |
| Extensibility | Limited | Highly extensible |

## Support

For issues or questions:
1. Check the profile README: `profiles/meditation_guide/README.md`
2. Review conversation app docs: https://github.com/pollen-robotics/reachy_mini_conversation_app
3. Check Reachy Mini SDK docs: https://github.com/pollen-robotics/reachy_mini

## Migration Complete! 🎉

Your meditation tutor has been successfully migrated to the conversation app architecture. Enjoy your zen meditation sessions with Reachy Mini!
