"""Start meditation tool for guided breathing sessions."""

import logging
from typing import Any, Dict

from reachy_mini_conversation_app.tools.core_tools import Tool, ToolDependencies
from reachy_mini_conversation_app.profiles.meditation_guide.meditation_move import MeditationMove
from reachy_mini_conversation_app.profiles.meditation_guide import meditation_config


logger = logging.getLogger(__name__)


class StartMeditation(Tool):
    """Begin a guided meditation breathing session."""

    name = "start_meditation"
    description = "Begin a guided meditation breathing session with configurable duration and settings"
    parameters_schema = {
        "type": "object",
        "properties": {
            "duration_minutes": {
                "type": "integer",
                "enum": [3, 5, 10],
                "description": "Duration of meditation session in minutes (3, 5, or 10)",
            },
            "breath_sound": {
                "type": "boolean",
                "description": "Enable breath sounds during meditation (optional, uses current setting if not specified)",
            },
            "custom_inhale_s": {
                "type": "number",
                "description": "Custom inhale duration in seconds (optional, uses current setting if not specified)",
            },
            "custom_exhale_s": {
                "type": "number",
                "description": "Custom exhale duration in seconds (optional, uses current setting if not specified)",
            },
        },
        "required": ["duration_minutes"],
    }

    async def __call__(self, deps: ToolDependencies, **kwargs: Any) -> Dict[str, Any]:
        """Start a meditation session.
        
        Args:
            deps: Tool dependencies (robot, movement manager, etc.)
            **kwargs: Parameters from LLM (duration_minutes, breath_sound, etc.)
            
        Returns:
            Status dictionary with session details
        """
        duration_minutes = kwargs.get("duration_minutes")
        if not duration_minutes or duration_minutes not in [3, 5, 10]:
            return {"error": "duration_minutes must be 3, 5, or 10"}

        # Get current config or use provided values
        config = meditation_config.get_current_config()
        
        inhale_s = kwargs.get("custom_inhale_s", config['inhale_s'])
        exhale_s = kwargs.get("custom_exhale_s", config['exhale_s'])
        breath_sound = kwargs.get("breath_sound", config['breath_sound_enabled'])
        antennas_enabled = config['antennas_enabled']
        sound_type = config['sound_type']

        logger.info(
            f"Tool call: start_meditation duration={duration_minutes}min, "
            f"inhale={inhale_s}s, exhale={exhale_s}s, "
            f"sound={breath_sound}, antennas={antennas_enabled}"
        )

        try:
            # Create meditation move with reachy_mini instance for audio
            meditation_move = MeditationMove(
                duration_minutes=duration_minutes,
                inhale_s=inhale_s,
                exhale_s=exhale_s,
                antennas_enabled=antennas_enabled,
                breath_sound_enabled=breath_sound,
                sound_type=sound_type,
                reachy_mini=deps.reachy_mini,
            )

            # Queue the move
            movement_manager = deps.movement_manager
            movement_manager.queue_move(meditation_move)
            
            # Calculate total duration for status
            total_duration = duration_minutes * 60.0
            movement_manager.set_moving_state(total_duration)

            return {
                "status": "meditation started",
                "duration_minutes": duration_minutes,
                "inhale_s": inhale_s,
                "exhale_s": exhale_s,
                "breath_sound": breath_sound,
                "total_duration_s": total_duration,
            }

        except Exception as e:
            logger.exception("Failed to start meditation")
            return {"error": f"Failed to start meditation: {e!s}"}
