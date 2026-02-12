"""Meditation breathing move for guided meditation sessions.

This module implements a meditation breathing move that can be queued and executed
by the MovementManager. It provides smooth, intentional breathing patterns with
configurable timing and antenna movements.
"""

from __future__ import annotations
import logging
from typing import Tuple

import numpy as np
from numpy.typing import NDArray

from reachy_mini.motion.move import Move
from reachy_mini.utils import create_head_pose
from reachy_mini.utils.interpolation import linear_pose_interpolation


logger = logging.getLogger(__name__)


class MeditationMove(Move):  # type: ignore
    """Guided meditation breathing move with configurable parameters.
    
    This move implements a series of breathing cycles with:
    - Inhale: head tilts up (negative pitch), antennas spread
    - Exhale: head tilts down (positive pitch), antennas narrow
    - Subtle variation in yaw/roll across cycles for natural feel
    """

    def __init__(
        self,
        duration_minutes: int,
        inhale_s: float = 5.0,
        exhale_s: float = 8.0,
        antennas_enabled: bool = True,
        breath_sound_enabled: bool = False,
        sound_type: str = 'ambient',
        reachy_mini = None,
    ):
        """Initialize meditation move.

        Args:
            duration_minutes: Total session duration in minutes (3, 5, or 10)
            inhale_s: Duration of inhale phase in seconds
            exhale_s: Duration of exhale phase in seconds
            antennas_enabled: Whether to move antennas during breathing
            breath_sound_enabled: Whether to play breath sounds
            sound_type: Type of breath sound ('ambient', 'ocean', 'white_noise')
        """
        self.duration_minutes = duration_minutes
        self.inhale_s = inhale_s
        self.exhale_s = exhale_s
        self.antennas_enabled = antennas_enabled
        self.breath_sound_enabled = breath_sound_enabled
        self.sound_type = sound_type
        self.reachy_mini = reachy_mini

        # Calculate total cycles
        self.cycle_s = inhale_s + exhale_s
        self.total_s = float(duration_minutes) * 60.0
        self.total_cycles = int(self.total_s // self.cycle_s)
        self._duration = self.total_s

        # Breathing parameters - smoother, more subtle movements
        self.inhale_pitch = -6.0   # Subtle tilt up (was -20.0)
        self.exhale_pitch = 8.0    # Subtle tilt down (was 15.0)
        self.inhale_z = 0.01       # Lift slightly (breathing depth)
        self.exhale_z = -0.005     # Lower slightly
        
        if antennas_enabled:
            self.inhale_antennas = np.array([18.0, -18.0])  # Spread
            self.exhale_antennas = np.array([6.0, -6.0])    # Narrow
        else:
            self.inhale_antennas = np.array([0.0, 0.0])
            self.exhale_antennas = np.array([0.0, 0.0])

        # Track last phase for sound triggering
        self._last_phase = None
        self._last_cycle_idx = -1

        logger.info(
            f"MeditationMove initialized: {duration_minutes}min, "
            f"inhale={inhale_s}s, exhale={exhale_s}s, "
            f"cycles={self.total_cycles}, antennas={antennas_enabled}"
        )

    @property
    def duration(self) -> float:
        """Duration property required by official Move interface."""
        return self._duration

    def evaluate(self, t: float) -> tuple[NDArray[np.float64] | None, NDArray[np.float64] | None, float | None]:
        """Evaluate meditation breathing at time t.
        
        Args:
            t: Time in seconds from start of move
            
        Returns:
            Tuple of (head_pose_4x4, antennas_array, body_yaw)
        """
        # Determine which cycle we're in
        cycle_idx = int(t // self.cycle_s)
        cycle_idx = min(cycle_idx, self.total_cycles - 1)  # Clamp to valid range
        
        # Time within current cycle
        t_in_cycle = t - (cycle_idx * self.cycle_s)
        
        # Determine phase: inhale or exhale
        if t_in_cycle < self.inhale_s:
            phase = 'inhale'
            phase_t = t_in_cycle / self.inhale_s  # 0 to 1
        else:
            phase = 'exhale'
            phase_t = (t_in_cycle - self.inhale_s) / self.exhale_s  # 0 to 1
        
        # Trigger breath sound on phase transitions (if enabled)
        if self.breath_sound_enabled:
            if phase != self._last_phase or cycle_idx != self._last_cycle_idx:
                self._trigger_breath_sound(phase)
                self._last_phase = phase
                self._last_cycle_idx = cycle_idx
        
        # Calculate variation for natural movement - more subtle
        base_yaw = 2.0 * np.sin(cycle_idx * 0.6)   # Reduced from 5.0
        base_roll = 1.0 * np.sin(cycle_idx * 0.9)  # Reduced from 3.0
        
        # Smooth interpolation with sinusoidal easing (ease-in-ease-out)
        ease_t = np.sin(phase_t * np.pi / 2)  # 0→1 with smooth acceleration
        
        if phase == 'inhale':
            # Inhale: smooth transition from neutral to inhale pose
            current_pitch = 0 + (self.inhale_pitch * ease_t)
            current_z = 0 + (self.inhale_z * ease_t)
            current_yaw = base_yaw * ease_t
            current_roll = base_roll * ease_t
            target_antennas = self.inhale_antennas
        else:
            # Exhale: smooth transition from inhale to exhale pose
            start_pitch = self.inhale_pitch
            start_z = self.inhale_z
            current_pitch = start_pitch + ((self.exhale_pitch - start_pitch) * ease_t)
            current_z = start_z + ((self.exhale_z - start_z) * ease_t)
            current_yaw = base_yaw + ((-base_yaw - base_yaw) * ease_t)
            current_roll = base_roll + ((-base_roll - base_roll) * ease_t)
            target_antennas = self.exhale_antennas
        
        # Create head pose with smooth Z-axis breathing
        head_pose = create_head_pose(
            x=0, y=0, z=current_z,
            roll=current_roll,
            pitch=current_pitch,
            yaw=current_yaw,
            degrees=True
        )
        
        # Convert antennas to radians and create array
        antennas = np.deg2rad(target_antennas).astype(np.float64)
        
        # Body yaw stays at 0 for meditation
        body_yaw = 0.0
        
        return (head_pose, antennas, body_yaw)

    def _trigger_breath_sound(self, phase: str) -> None:
        """Trigger breath sound for the given phase.
        
        Args:
            phase: 'inhale' or 'exhale'
        """
        if not self.reachy_mini:
            logger.debug(f"Breath sound trigger: {phase} (no reachy_mini instance)")
            return
            
        try:
            from reachy_mini_conversation_app.profiles.meditation_guide.breath_sounds import play_breath_sound
            
            # Determine duration and sound type based on phase
            if phase == 'inhale':
                duration = self.inhale_s
                intensity = 0.06
            else:  # exhale
                duration = self.exhale_s
                intensity = 0.08
            
            # Play the breath sound
            play_breath_sound(
                self.reachy_mini,
                duration_s=duration,
                intensity=intensity,
                sound_type=self.sound_type,
                phase=phase
            )
            logger.debug(f"Breath sound playing: {phase}")
        except Exception as e:
            # Audio is best-effort; don't crash meditation
            logger.debug(f"Breath sound error (non-critical): {e}")
