# Meditation Guide Profile

A zen meditation guide profile for Reachy Mini that combines conversational AI with guided breathing meditation sessions.

## Features

- **Guided Meditation Sessions**: 3, 5, or 10 minute breathing sessions
- **Configurable Breathing**: Adjust inhale/exhale duration via voice or UI
- **Breath Sounds**: Ambient tones, ocean sounds, or white noise (optional)
- **Antenna Movements**: Synchronized antenna movements during breathing (optional)
- **Zen Personality**: Calm, mindful conversational style
- **Voice Control**: Natural language commands for all features

## Default Settings

- **Inhale**: 5 seconds
- **Exhale**: 8 seconds
- **Antennas**: Enabled
- **Breath Sound**: Disabled (can be enabled)
- **Sound Type**: Ambient tones

## Voice Commands

### Start Meditation
- "Guide me through a 5 minute meditation"
- "Start a 10 minute breathing session"
- "Let's meditate for 3 minutes with breathing sounds"
- "Begin meditation with 6 second inhales"

### Configure Settings
- "Make the exhale 10 seconds"
- "Set inhale to 4 seconds"
- "Disable the antennas"
- "Enable breath sounds"
- "Use ocean sounds"

### Stop Meditation
- "Stop meditation"
- "End the session"

## Tools Available

### start_meditation
Begin a guided meditation session.

**Parameters:**
- `duration_minutes` (required): 3, 5, or 10
- `breath_sound` (optional): true/false
- `custom_inhale_s` (optional): custom inhale duration
- `custom_exhale_s` (optional): custom exhale duration

### configure_meditation
Adjust meditation parameters.

**Parameters:**
- `inhale_seconds` (optional): 2-15 seconds
- `exhale_seconds` (optional): 3-20 seconds
- `enable_antennas` (optional): true/false
- `enable_breath_sound` (optional): true/false
- `sound_type` (optional): 'ambient', 'ocean', 'white_noise'

### stop_meditation
Stop the current meditation session early.

## Breathing Patterns

### Inhale Phase (default 5s)
- Head tilts up (pitch -20°)
- Antennas spread outward (±18°)
- Gentle variation in yaw/roll for natural feel

### Exhale Phase (default 8s)
- Head tilts down (pitch +15°)
- Antennas narrow inward (±6°)
- Opposite yaw/roll variation

## Breath Sound Types

### Ambient (default)
Soft harmonic tones like a singing bowl. Gentle and meditation-friendly.

### Ocean
Filtered noise resembling ocean waves. Calming and natural.

### White Noise
Original synthesized breath sound. Fallback option.

## Running the Profile

### Option 1: Set as default profile
```bash
# In .env file
REACHY_MINI_CUSTOM_PROFILE=meditation_guide
```

### Option 2: Run with command line
```bash
REACHY_MINI_CUSTOM_PROFILE=meditation_guide python -m reachy_mini_conversation_app.main --gradio
```

### Option 3: Switch in UI
If running with `--gradio`, use the Personality panel to select "meditation_guide"

## Architecture

### MeditationMove
Implements the `Move` interface for smooth breathing cycles. Evaluated at 100Hz by the MovementManager for fluid motion.

### Configuration Management
Runtime configuration stored in `meditation_config.py`. Persists across meditation sessions until changed.

### Breath Sounds
Generated on-demand using numpy. Three types available with smooth fade in/out envelopes.

## Benefits Over Standalone App

1. **Smoother Motion**: 100Hz control loop vs blocking goto calls
2. **Conversational**: Can chat about meditation, answer questions
3. **Voice Control**: Natural language for all settings
4. **Better Integration**: Works with conversation app features
5. **Extensible**: Easy to add new meditation styles

## Example Conversation

```
User: "I'm feeling stressed"
Reachy: "Let's find some calm together. Would you like to try a short breathing meditation?"

User: "Yes, 5 minutes please"
Reachy: "Of course. Find a comfortable position. I'll guide your breath. Beginning now..."
[Meditation session starts]

User: "Make the exhale longer"
Reachy: "I'll extend the exhale to help you release tension. How does 10 seconds feel?"

User: "Perfect, and add ocean sounds"
Reachy: "Ocean sounds enabled. Let the waves guide your breath."
```

## Files

- `meditation_move.py` - MeditationMove class (breathing cycles)
- `start_meditation.py` - Start meditation tool
- `configure_meditation.py` - Configuration tool
- `stop_meditation.py` - Stop meditation tool
- `meditation_config.py` - Configuration management
- `breath_sounds.py` - Audio generation utilities
- `instructions.txt` - Zen personality prompt
- `tools.txt` - Enabled tools list
- `voice.txt` - Voice setting (shimmer)

## Future Enhancements

- Guided visualization options
- Progressive muscle relaxation
- Body scan meditation
- Loving-kindness meditation
- Custom meditation scripts
- Session history tracking
