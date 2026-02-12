import threading
from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.utils import create_head_pose
import numpy as np
import time
from pydantic import BaseModel


class ReachyMiniMeditationTutor(ReachyMiniApp):
    # Optional: URL to a custom configuration page for the app
    # eg. "http://localhost:8042"
    custom_app_url: str | None = "http://0.0.0.0:8042"
    # Optional: specify a media backend ("gstreamer", "gstreamer_no_video", "default", etc.)
    #On the wireless, use gstreamer_no_video to optimise CPU usage if the app does not use video streaming
    request_media_backend: str | None = None

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event):
        inhale_s = 5.0
        exhale_s = 8.0

        antennas_enabled = True
        session_minutes = 3
        start_requested = False
        stop_session_requested = False
        breath_sound_enabled = False

        # You can ignore this part if you don't want to add settings to your app. If you set custom_app_url to None, you have to remove this part as well.
        #=== vvv ===
        class AntennaState(BaseModel):
            enabled: bool

        class SessionConfig(BaseModel):
            minutes: int

        class BreathSoundConfig(BaseModel):
            enabled: bool

        @self.settings_app.post("/antennas")
        def update_antennas_state(state: AntennaState):
            nonlocal antennas_enabled
            antennas_enabled = state.enabled
            return {"antennas_enabled": antennas_enabled}

        @self.settings_app.post("/session")
        def update_session_config(cfg: SessionConfig):
            nonlocal session_minutes
            if cfg.minutes not in (3, 5, 10):
                return {"ok": False, "error": "minutes must be one of: 3, 5, 10"}
            session_minutes = cfg.minutes
            return {"ok": True, "minutes": session_minutes}

        @self.settings_app.post("/start")
        def request_start():
            nonlocal start_requested, stop_session_requested
            start_requested = True
            stop_session_requested = False
            return {"ok": True}

        @self.settings_app.post("/breath_sound")
        def update_breath_sound(cfg: BreathSoundConfig):
            nonlocal breath_sound_enabled
            breath_sound_enabled = cfg.enabled
            return {"breath_sound_enabled": breath_sound_enabled}

        @self.settings_app.post("/stop")
        def request_stop():
            nonlocal stop_session_requested
            stop_session_requested = True
            return {"ok": True}

        # === ^^^ ===

        def _play_breath(duration_s: float, intensity: float) -> None:
            if not breath_sound_enabled:
                return
            if stop_event.is_set() or stop_session_requested:
                return
            try:
                sr = int(reachy_mini.media.get_output_audio_samplerate())
                n = max(1, int(duration_s * sr))
                t = np.linspace(0.0, duration_s, n, endpoint=False, dtype=np.float32)

                # White-ish noise + gentle low-frequency modulation for a "breath" feel.
                noise = np.random.normal(0.0, 1.0, size=n).astype(np.float32)
                mod = 0.6 + 0.4 * np.sin(2.0 * np.pi * 0.15 * t).astype(np.float32)
                raw = noise * mod

                # Smooth envelope (fade in/out) to avoid clicks.
                fade = int(0.25 * sr)
                fade = min(fade, n // 2)
                env = np.ones(n, dtype=np.float32)
                if fade > 0:
                    ramp = np.linspace(0.0, 1.0, fade, dtype=np.float32)
                    env[:fade] = ramp
                    env[-fade:] = ramp[::-1]

                y = intensity * raw * env

                # Stream audio: ensure player is started once.
                reachy_mini.media.start_playing()
                reachy_mini.media.push_audio_sample(y)
            except Exception:
                # Audio is best-effort; motion should keep working.
                return

        def _goto(head_kwargs: dict, antennas_deg: np.ndarray, duration: float) -> None:
            if stop_event.is_set() or stop_session_requested:
                return
            head_pose = create_head_pose(**head_kwargs, degrees=True)
            reachy_mini.goto_target(
                head=head_pose,
                antennas=np.deg2rad(antennas_deg),
                duration=duration,
            )

        def _settle() -> None:
            antennas_deg = np.array([0.0, 0.0])
            _goto({"yaw": 0.0, "pitch": 0.0, "roll": 0.0}, antennas_deg, 1.0)

        def _breathing_cycle(cycle_idx: int) -> None:
            base_yaw = 5.0 * np.sin(cycle_idx * 0.6)
            base_roll = 3.0 * np.sin(cycle_idx * 0.9)

            if antennas_enabled:
                inhale_ant = np.array([18.0, -18.0])
                exhale_ant = np.array([6.0, -6.0])
            else:
                inhale_ant = np.array([0.0, 0.0])
                exhale_ant = np.array([0.0, 0.0])

            # Inhale: head tilts UP (negative pitch)
            _goto(
                {"yaw": base_yaw, "pitch": -20.0, "roll": base_roll},
                inhale_ant,
                inhale_s,
            )
            _play_breath(inhale_s, intensity=0.08)
            # Exhale: head tilts DOWN (positive pitch)
            _goto(
                {"yaw": -base_yaw, "pitch": 15.0, "roll": -base_roll},
                exhale_ant,
                exhale_s,
            )
            _play_breath(exhale_s, intensity=0.06)

        # Main control loop
        while not stop_event.is_set():
            if not start_requested:
                time.sleep(0.05)
                continue

            stop_session_requested = False
            start_requested = False

            total_s = float(session_minutes) * 60.0
            cycle_s = inhale_s + exhale_s
            cycles = int(total_s // cycle_s)

            _settle()
            for i in range(cycles):
                if stop_event.is_set() or stop_session_requested:
                    break
                _breathing_cycle(i)
            _settle()


if __name__ == "__main__":
    app = ReachyMiniMeditationTutor()
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()