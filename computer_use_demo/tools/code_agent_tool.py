from .base import ToolResult, BaseAnthropicTool
from anthropic.types.beta import BetaToolParam

class CodeAgentTool(BaseAnthropicTool):
    """
    Uno strumento per interagire con un agente specializzato nella scrittura di codice.
    Questo strumento invia una richiesta a un server locale che gestisce l'agente di codice.
    Utilizza il modello specificato per generare risposte a richieste di codice.
    """
    name = "code_agent"
    description = "Invia un messaggio all'agente specializzato nella scrittura di codice."

    def to_params(self) -> BetaToolParam:
        return BetaToolParam(
            type="custom",
            name=self.name,
            description=self.description,
            input_schema={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "model": {"type": "string"},
                },
                "required": ["message"],
            },
        )

    async def __call__(self, *, message: str, model: str = "claude-3-sonnet-20250514", **kwargs) -> ToolResult:
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://localhost:8000/code-agent",
                    json={"message": message, "model": model},
                    timeout=15,
                )
                resp.raise_for_status()
                reply = resp.json().get("response", "[Empty]")
        except Exception as e:
            return ToolResult(error=f"Errore durante la chiamata a Code Agent: {e}")
        
        return ToolResult(output=reply)
