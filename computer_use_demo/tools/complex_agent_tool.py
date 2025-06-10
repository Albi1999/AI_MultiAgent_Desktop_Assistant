from .base import ToolResult, BaseAnthropicTool
from anthropic.types.beta import BetaToolParam

class ComplexAgentTool(BaseAnthropicTool):
    """
    Uno strumento per interagire con un agente complesso che risponde a domande in linguaggio naturale.
    Questo strumento invia una richiesta a un server locale che gestisce l'agente complesso.
    Utilizza il modello specificato per generare risposte a domande complesse.
    """

    name = "complex_agent"
    description = "Risponde a domande complesse in linguaggio naturale."

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
            }
        )

    async def __call__(self, *, message: str, model: str = "claude-3-sonnet-20250514", **kwargs) -> ToolResult:
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://localhost:8000/complex-agent",
                    json={"message": message, "model": model},
                    timeout=15,
                )
                resp.raise_for_status()
                reply = resp.json().get("response", "[Empty]")
        except Exception as e:
            return ToolResult(error=f"Errore durante la chiamata a Complex Agent: {e}")
        
        return ToolResult(output=reply)
