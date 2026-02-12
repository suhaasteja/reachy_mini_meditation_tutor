"""Breath sound generation for meditation sessions.

This module provides various breath sound types:
- ambient: Soft harmonic tones (like singing bowl)
- ocean: Filtered noise (ocean wave sound)
- white_noise: Original synthesized breath sound (fallback)
"""

import logging
import numpy as np
from typing import Optional
from pathlib import Path
import wave


logger = logging.getLogger(__name__)


# Cache for loaded sleep sound
_SLEEP_SOUND_CACHE = None


def generate_ambient_tone(duration_s: float, intensity: float = 0.08) -> np.ndarray:
    """Generate soft ambient harmonic tones.
    
    Creates a gentle, meditation-friendly sound using sine wave harmonics
    similar to a singing bowl or bell tone.
    
    Args:
        duration_s: Duration in seconds
        intensity: Volume intensity (0.0 to 1.0)
        
    Returns:
        Audio samples as float32 array
    """
    # Sample rate (will be adjusted to match robot's audio system)
    sr = 44100
    n = max(1, int(duration_s * sr))
    t = np.linspace(0.0, duration_s, n, endpoint=False, dtype=np.float32)
    
    # Fundamental frequency (A3 = 220Hz) with harmonics
    f0 = 220.0
    
    # Create harmonic series with decreasing amplitudes
    harmonics = [
        (f0, 0.5),        # Fundamental
        (f0 * 2, 0.3),    # Octave
        (f0 * 3, 0.15),   # Fifth
        (f0 * 4, 0.08),   # Second octave
    ]
    
    # Sum harmonics
    signal = np.zeros(n, dtype=np.float32)
    for freq, amp in harmonics:
        signal += amp * np.sin(2.0 * np.pi * freq * t)
    
    # Normalize
    signal = signal / np.max(np.abs(signal))
    
    # Apply smooth envelope (fade in/out)
    fade_samples = int(0.3 * sr)
    fade_samples = min(fade_samples, n // 2)
    
    env = np.ones(n, dtype=np.float32)
    if fade_samples > 0:
        ramp = np.linspace(0.0, 1.0, fade_samples, dtype=np.float32)
        env[:fade_samples] = ramp
        env[-fade_samples:] = ramp[::-1]
    
    # Apply envelope and intensity
    y = intensity * signal * env
    
    return y


def generate_ocean_sound(duration_s: float, intensity: float = 0.06) -> np.ndarray:
    """Generate ocean wave-like sound.
    
    Creates a filtered noise pattern that resembles ocean waves.
    
    Args:
        duration_s: Duration in seconds
        intensity: Volume intensity (0.0 to 1.0)
        
    Returns:
        Audio samples as float32 array
    """
    sr = 44100
    n = max(1, int(duration_s * sr))
    t = np.linspace(0.0, duration_s, n, endpoint=False, dtype=np.float32)
    
    # Generate pink-ish noise (filtered white noise)
    noise = np.random.normal(0.0, 1.0, size=n).astype(np.float32)
    
    # Low-frequency modulation for wave-like pattern
    wave_freq = 0.2  # Hz (slow wave)
    modulation = 0.5 + 0.5 * np.sin(2.0 * np.pi * wave_freq * t)
    
    # Apply modulation
    signal = noise * modulation
    
    # Normalize
    signal = signal / np.max(np.abs(signal))
    
    # Apply smooth envelope
    fade_samples = int(0.25 * sr)
    fade_samples = min(fade_samples, n // 2)
    
    env = np.ones(n, dtype=np.float32)
    if fade_samples > 0:
        ramp = np.linspace(0.0, 1.0, fade_samples, dtype=np.float32)
        env[:fade_samples] = ramp
        env[-fade_samples:] = ramp[::-1]
    
    y = intensity * signal * env
    
    return y


def generate_white_noise_breath(duration_s: float, intensity: float = 0.08) -> np.ndarray:
    """Generate white noise breath sound (original fallback).
    
    This is the original breath sound from the meditation app.
    
    Args:
        duration_s: Duration in seconds
        intensity: Volume intensity (0.0 to 1.0)
        
    Returns:
        Audio samples as float32 array
    """
    sr = 44100
    n = max(1, int(duration_s * sr))
    t = np.linspace(0.0, duration_s, n, endpoint=False, dtype=np.float32)
    
    # White-ish noise + gentle low-frequency modulation for a "breath" feel
    noise = np.random.normal(0.0, 1.0, size=n).astype(np.float32)
    mod = 0.6 + 0.4 * np.sin(2.0 * np.pi * 0.15 * t).astype(np.float32)
    raw = noise * mod
    
    # Smooth envelope (fade in/out) to avoid clicks
    fade = int(0.25 * sr)
    fade = min(fade, n // 2)
    env = np.ones(n, dtype=np.float32)
    if fade > 0:
        ramp = np.linspace(0.0, 1.0, fade, dtype=np.float32)
        env[:fade] = ramp
        env[-fade:] = ramp[::-1]
    
    y = intensity * raw * env
    
    return y


def load_sleep_sound() -> np.ndarray:
    """Load Reachy's sleep/shutdown sound.
    
    Returns:
        Audio samples as float32 array
    """
    global _SLEEP_SOUND_CACHE
    
    if _SLEEP_SOUND_CACHE is not None:
        return _SLEEP_SOUND_CACHE
    
    try:
        # Path to Reachy's go_sleep.wav sound
        import reachy_mini
        reachy_path = Path(reachy_mini.__file__).parent
        sleep_sound_path = reachy_path / 'assets' / 'go_sleep.wav'
        
        if not sleep_sound_path.exists():
            logger.warning(f"Sleep sound not found at {sleep_sound_path}")
            return None
        
        # Load WAV file
        with wave.open(str(sleep_sound_path), 'rb') as wav_file:
            n_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            framerate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            
            # Read audio data
            audio_data = wav_file.readframes(n_frames)
            
            # Convert to numpy array
            if sample_width == 2:  # 16-bit
                samples = np.frombuffer(audio_data, dtype=np.int16)
            elif sample_width == 4:  # 32-bit
                samples = np.frombuffer(audio_data, dtype=np.int32)
            else:
                samples = np.frombuffer(audio_data, dtype=np.uint8)
            
            # Convert to float32 and normalize
            samples = samples.astype(np.float32) / np.iinfo(samples.dtype).max
            
            # If stereo, convert to mono
            if n_channels == 2:
                samples = samples.reshape(-1, 2).mean(axis=1)
            
            _SLEEP_SOUND_CACHE = samples
            logger.info(f"Loaded sleep sound: {len(samples)} samples at {framerate}Hz")
            return samples
            
    except Exception as e:
        logger.error(f"Failed to load sleep sound: {e}")
        return None


def generate_exhale_sound(duration_s: float, intensity: float = 0.08) -> np.ndarray:
    """Generate exhale sound using Reachy's sleep sound.
    
    Args:
        duration_s: Duration in seconds
        intensity: Volume intensity (0.0 to 1.0)
        
    Returns:
        Audio samples as float32 array
    """
    sleep_sound = load_sleep_sound()
    
    if sleep_sound is None:
        # Fallback to ocean sound if sleep sound not available
        return generate_ocean_sound(duration_s, intensity)
    
    # Resample to match desired duration
    original_duration = len(sleep_sound) / 44100  # Assume 44.1kHz
    target_samples = int(duration_s * 44100)
    
    if target_samples != len(sleep_sound):
        # Simple resampling
        indices = np.linspace(0, len(sleep_sound) - 1, target_samples)
        resampled = np.interp(indices, np.arange(len(sleep_sound)), sleep_sound)
    else:
        resampled = sleep_sound.copy()
    
    # Apply gentle fade-out for calming effect
    fade_samples = int(0.3 * 44100)
    if fade_samples > 0 and fade_samples < len(resampled):
        fade_out = np.linspace(1.0, 0.3, fade_samples, dtype=np.float32)
        resampled[-fade_samples:] *= fade_out
    
    # Apply intensity
    result = (intensity * resampled).astype(np.float32)
    
    return result


def generate_inhale_sound(duration_s: float, intensity: float = 0.06) -> np.ndarray:
    """Generate inhale sound (gentle intake/reverse of exhale).
    
    Args:
        duration_s: Duration in seconds
        intensity: Volume intensity (0.0 to 1.0)
        
    Returns:
        Audio samples as float32 array
    """
    # Option 1: Time-reverse the exhale sound for inhale
    exhale = generate_exhale_sound(duration_s, intensity)
    
    # Reverse the audio
    inhale = np.flip(exhale).copy()
    
    # Apply gentle fade-in at the start
    fade_samples = int(0.2 * 44100)
    if fade_samples > 0 and fade_samples < len(inhale):
        fade_in = np.linspace(0.3, 1.0, fade_samples, dtype=np.float32)
        inhale[:fade_samples] *= fade_in
    
    return inhale


def generate_breath_sound(
    duration_s: float,
    intensity: float,
    sound_type: str = 'ambient',
    sample_rate: Optional[int] = None,
    phase: str = 'exhale'
) -> np.ndarray:
    """Generate breath sound of specified type.
    
    Args:
        duration_s: Duration in seconds
        intensity: Volume intensity (0.0 to 1.0)
        sound_type: Type of sound ('ambient', 'ocean', 'white_noise')
        sample_rate: Target sample rate (if None, uses 44100)
        
    Returns:
        Audio samples as float32 array
    """
    try:
        # Use sleep sound for exhale, reversed for inhale (realistic breathing)
        if phase == 'exhale':
            samples = generate_exhale_sound(duration_s, intensity)
        elif phase == 'inhale':
            samples = generate_inhale_sound(duration_s, intensity)
        # Fallback to original sound types if phase not specified
        elif sound_type == 'ambient':
            samples = generate_ambient_tone(duration_s, intensity)
        elif sound_type == 'ocean':
            samples = generate_ocean_sound(duration_s, intensity)
        else:  # 'white_noise' or fallback
            samples = generate_white_noise_breath(duration_s, intensity)
        
        # Resample if needed
        if sample_rate is not None and sample_rate != 44100:
            # Simple resampling (could use scipy.signal.resample for better quality)
            current_length = len(samples)
            target_length = int(duration_s * sample_rate)
            indices = np.linspace(0, current_length - 1, target_length)
            samples = np.interp(indices, np.arange(current_length), samples).astype(np.float32)
        
        return samples
        
    except Exception as e:
        logger.error(f"Failed to generate {sound_type} breath sound: {e}")
        # Fallback to white noise
        return generate_white_noise_breath(duration_s, intensity)


def play_breath_sound(
    reachy_mini,
    duration_s: float,
    intensity: float,
    sound_type: str = 'ambient',
    phase: str = 'exhale'
) -> None:
    """Play breath sound through robot's audio system.
    
    Args:
        reachy_mini: ReachyMini instance
        duration_s: Duration in seconds
        intensity: Volume intensity
        sound_type: Type of sound to play
    """
    try:
        # Get robot's audio sample rate
        sr = int(reachy_mini.media.get_output_audio_samplerate())
        
        # Generate sound with phase information
        samples = generate_breath_sound(duration_s, intensity, sound_type, sr, phase)
        
        # Play audio
        reachy_mini.media.start_playing()
        reachy_mini.media.push_audio_sample(samples)
        
    except Exception as e:
        # Audio is best-effort; motion should keep working
        logger.debug(f"Breath sound playback failed (non-critical): {e}")
