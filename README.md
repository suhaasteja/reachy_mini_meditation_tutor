---
title: Reachy Mini Meditation Tutor
emoji: 👋
colorFrom: red
colorTo: blue
sdk: static
pinned: false
short_description: Write your description here
tags:
 - reachy_mini
 - reachy_mini_python_app
---

# Reachy Mini Meditation Tutor

Timed breathing sessions for Reachy Mini (works in simulation or on a real robot).

- Inhale: 5s
- Exhale: 8s
- Sessions: 3 / 5 / 10 minutes
- Optional breathing sound (synthesized, toggle in UI)

## Quickstart (simulation)

### 1) Create a venv and install Reachy Mini + MuJoCo

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install "reachy-mini[mujoco]"
```

### 2) Clone this repo

```bash
git clone https://github.com/suhaasteja/reachy_mini_meditation_tutor.git
cd reachy_mini_meditation_tutor
```

### 3) Install the app into the venv (so it shows up in the dashboard)

```bash
source .venv/bin/activate
pip install -e .
```

### 4) Run the simulation daemon (macOS)

```bash
source .venv/bin/activate
mjpython -m reachy_mini.daemon.app.main --sim
```

Open:
- http://localhost:8000

### 5) Start the app

In the dashboard:
- Go to **Apps**
- Toggle **reachy_mini_meditation_tutor** on
- Click the **⚙️** icon (opens the app UI)

App UI:
- http://localhost:8042

## Developer notes

See `DEVELOPMENT.md`.