"""Stop meditation tool for early termination of sessions."""

import logging
from typing import Any, Dict

from reachy_mini_conversation_app.tools.core_tools import Tool, ToolDependencies


logger = logging.getLogger(__name__)


class StopMeditation(Tool):
    """Stop the current meditation session early."""

    name = "stop_meditation"
    description = "Stop the current meditation session before it completes"
    parameters_schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }

    async def __call__(self, deps: ToolDependencies, **kwargs: Any) -> Dict[str, Any]:
        """Stop the current meditation session.
        
        Args:
            deps: Tool dependencies
            **kwargs: No parameters required
            
        Returns:
            Status dictionary
        """
        logger.info("Tool call: stop_meditation")

        try:
            # Clear the move queue to stop meditation
            movement_manager = deps.movement_manager
            movement_manager.clear_move_queue()

            return {
                "status": "meditation stopped",
                "message": "Meditation session ended peacefully",
            }

        except Exception as e:
            logger.exception("Failed to stop meditation")
            return {"error": f"Failed to stop meditation: {e!s}"}
