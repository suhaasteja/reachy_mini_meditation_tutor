"""Meditation configuration management.

This module manages the runtime configuration for meditation sessions,
including breathing parameters, antenna settings, and sound preferences.
"""

import logging
from typing import Dict, Any


logger = logging.getLogger(__name__)


# Default meditation configuration
DEFAULT_INHALE_S = 5.0
DEFAULT_EXHALE_S = 8.0
DEFAULT_ANTENNAS_ENABLED = True
DEFAULT_BREATH_SOUND = False
DEFAULT_SOUND_TYPE = 'ambient'  # 'ambient', 'ocean', 'white_noise'


# Runtime configuration (mutable)
_current_config: Dict[str, Any] = {
    'inhale_s': DEFAULT_INHALE_S,
    'exhale_s': DEFAULT_EXHALE_S,
    'antennas_enabled': DEFAULT_ANTENNAS_ENABLED,
    'breath_sound_enabled': DEFAULT_BREATH_SOUND,
    'sound_type': DEFAULT_SOUND_TYPE,
}


def get_current_config() -> Dict[str, Any]:
    """Get the current meditation configuration.
    
    Returns:
        Dictionary containing current meditation settings
    """
    return _current_config.copy()


def update_config(new_config: Dict[str, Any]) -> None:
    """Update the meditation configuration.
    
    Args:
        new_config: Dictionary with updated configuration values
    """
    global _current_config
    _current_config.update(new_config)
    logger.info(f"Meditation config updated: {_current_config}")


def reset_to_defaults() -> None:
    """Reset configuration to default values."""
    global _current_config
    _current_config = {
        'inhale_s': DEFAULT_INHALE_S,
        'exhale_s': DEFAULT_EXHALE_S,
        'antennas_enabled': DEFAULT_ANTENNAS_ENABLED,
        'breath_sound_enabled': DEFAULT_BREATH_SOUND,
        'sound_type': DEFAULT_SOUND_TYPE,
    }
    logger.info("Meditation config reset to defaults")
