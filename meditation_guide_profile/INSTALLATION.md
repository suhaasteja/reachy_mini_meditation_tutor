# Installing the Meditation Guide Profile

Quick guide to install this meditation_guide profile into the conversation app.

## Prerequisites

- Conversation app cloned: `git clone https://github.com/pollen-robotics/reachy_mini_conversation_app.git`
- Conversation app installed: `cd reachy_mini_conversation_app && pip install -e .`

## Installation

### Copy Profile to Conversation App

```bash
# From the reachy_mini_meditation_tutor directory
cp -r meditation_guide_profile reachy_mini_conversation_app/src/reachy_mini_conversation_app/profiles/meditation_guide
```

### Configure Environment

Create/edit `.env` in the conversation app directory:

```bash
cd reachy_mini_conversation_app
```

Add this line to `.env`:
```
REACHY_MINI_CUSTOM_PROFILE=meditation_guide
```

## Verify Installation

```bash
# Check profile exists
ls reachy_mini_conversation_app/src/reachy_mini_conversation_app/profiles/meditation_guide/

# Should show:
# - instructions.txt
# - tools.txt
# - meditation_move.py
# - start_meditation.py
# - configure_meditation.py
# - stop_meditation.py
# - meditation_config.py
# - breath_sounds.py
# - README.md
```

## Run

```bash
cd reachy_mini_conversation_app
python -m reachy_mini_conversation_app.main --gradio
```

Open http://localhost:7860 and start meditating! 🧘
