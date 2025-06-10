from .base import BaseAnthropicTool, ToolResult
from anthropic.types.beta import BetaToolParam
from computer_use_demo.tools import ToolCollection
from .bash import BashTool20250124
from .computer import ComputerTool20250124
from .edit import EditTool20250429

class ComputerUseAgentTool(BaseAnthropicTool):
    """Esegue operazioni sul computer virtuale usando gli strumenti base come bash, computer e editor."""
    name = "computer_use_agent"
    description = "Esegue operazioni sul computer virtuale usando gli strumenti base come bash, computer e editor."

    def to_params(self) -> BetaToolParam:
        return BetaToolParam(
            type="custom",
            name=self.name,
            description=self.description,
            input_schema={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                },
                "required": ["message"],
            },
        )

    async def __call__(self, *, message: str, **kwargs) -> ToolResult:
        # Istanzia tool interni dell'agente
        tools = ToolCollection(
            BashTool20250124(),
            ComputerTool20250124(),
            EditTool20250429(),
        )
        # Per ora interpretiamo il messaggio come comando bash da eseguire
        result = await tools.run(name="bash", tool_input={"command": message})
        return result
