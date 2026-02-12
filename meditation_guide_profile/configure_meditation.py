"""Configure meditation tool for adjusting breathing parameters."""

import logging
from typing import Any, Dict

from reachy_mini_conversation_app.tools.core_tools import Tool, ToolDependencies
from reachy_mini_conversation_app.profiles.meditation_guide import meditation_config


logger = logging.getLogger(__name__)


class ConfigureMeditation(Tool):
    """Adjust meditation breathing parameters."""

    name = "configure_meditation"
    description = "Adjust meditation breathing parameters (inhale/exhale duration, antennas, breath sound)"
    parameters_schema = {
        "type": "object",
        "properties": {
            "inhale_seconds": {
                "type": "number",
                "description": "Inhale duration in seconds (3-10 seconds recommended)",
            },
            "exhale_seconds": {
                "type": "number",
                "description": "Exhale duration in seconds (5-15 seconds recommended)",
            },
            "enable_antennas": {
                "type": "boolean",
                "description": "Enable or disable antenna movements during breathing",
            },
            "enable_breath_sound": {
                "type": "boolean",
                "description": "Enable or disable breath sounds",
            },
            "sound_type": {
                "type": "string",
                "enum": ["ambient", "ocean", "white_noise"],
                "description": "Type of breath sound to use",
            },
        },
        "required": [],
    }

    async def __call__(self, deps: ToolDependencies, **kwargs: Any) -> Dict[str, Any]:
        """Configure meditation parameters.
        
        Args:
            deps: Tool dependencies
            **kwargs: Configuration parameters
            
        Returns:
            Updated configuration dictionary
        """
        config = meditation_config.get_current_config()
        updates = {}

        # Update inhale duration
        if "inhale_seconds" in kwargs:
            inhale_s = float(kwargs["inhale_seconds"])
            if 2.0 <= inhale_s <= 15.0:
                config['inhale_s'] = inhale_s
                updates['inhale_s'] = inhale_s
            else:
                return {"error": "inhale_seconds must be between 2 and 15"}

        # Update exhale duration
        if "exhale_seconds" in kwargs:
            exhale_s = float(kwargs["exhale_seconds"])
            if 3.0 <= exhale_s <= 20.0:
                config['exhale_s'] = exhale_s
                updates['exhale_s'] = exhale_s
            else:
                return {"error": "exhale_seconds must be between 3 and 20"}

        # Update antenna setting
        if "enable_antennas" in kwargs:
            antennas = bool(kwargs["enable_antennas"])
            config['antennas_enabled'] = antennas
            updates['antennas_enabled'] = antennas

        # Update breath sound setting
        if "enable_breath_sound" in kwargs:
            sound = bool(kwargs["enable_breath_sound"])
            config['breath_sound_enabled'] = sound
            updates['breath_sound_enabled'] = sound

        # Update sound type
        if "sound_type" in kwargs:
            sound_type = kwargs["sound_type"]
            if sound_type in ["ambient", "ocean", "white_noise"]:
                config['sound_type'] = sound_type
                updates['sound_type'] = sound_type
            else:
                return {"error": "sound_type must be 'ambient', 'ocean', or 'white_noise'"}

        # Save updated config
        meditation_config.update_config(config)

        logger.info(f"Tool call: configure_meditation updates={updates}")

        return {
            "status": "meditation configured",
            "updates": updates,
            "current_config": config,
        }
