from .base import ToolResult, BaseAnthropicTool
from anthropic.types.beta import BetaToolParam

class DocParserAgentTool(BaseAnthropicTool):
    """
    Uno strumento per interagire con un agente che analizza documentazione tecnica.
    Questo strumento invia una richiesta a un server locale che gestisce l'agente di parsing dei documenti.
    Utilizza il modello specificato per generare risposte a domande su codice e API basate su documentazione tecnica.
    """
    name = "doc_parser_agent"
    description = "Inoltra una richiesta all'agente che analizza documentazione tecnica per fornire indicazioni su codice e API."

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
                    "doc_url": {"type": "string"},
                },
                "required": ["message"],
            },
        )

    async def __call__(self, *, message: str, model: str = "claude-3-sonnet-20250514", doc_url: str = "", **kwargs) -> ToolResult:
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                payload = {"message": message, "model": model}
                if doc_url:
                    payload["doc_url"] = doc_url

                resp = await client.post(
                    "http://localhost:8000/doc-parser-agent",
                    json=payload,
                    timeout=15,
                )
                resp.raise_for_status()
                reply = resp.json().get("response", "[Empty]")
        except Exception as e:
            return ToolResult(error=f"Errore durante la chiamata a Doc Parser Agent: {e}")
        
        return ToolResult(output=reply)
