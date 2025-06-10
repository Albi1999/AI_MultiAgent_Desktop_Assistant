from . import BaseAnthropicTool, ToolResult
from anthropic.types.beta import BetaToolParam, BetaTextBlock

class RouterAgentTool(BaseAnthropicTool):
    name = "router_agent"
    description = "Decide quale agente delegato usare in base al messaggio utente."

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
        from anthropic import Anthropic
        client = Anthropic()
        response = client.beta.messages.create(
            model="claude-sonnet-4-20250514",
            system="Sei un router intelligente. Il tuo compito è quello di scegliere il tool corretto in base al messaggio dell'utente: " \
            "'code_agent', 'doc_parser_agent', 'complex_agent', 'computer_use_agent'. Rispondi solo col nome. Le funzionalità dei tool sono le seguenti: " \
            "'code_agent' per scrivere codice, 'doc_parser_agent' per analizzare documenti, 'complex_agent' per rispondere a domande complesse, " \
            "e 'computer_use_agent' per eseguire operazioni sul computer virtuale.",
            messages=[
                {"role": "user", "content": message}
            ],
            max_tokens=20
        )
        for block in response.content:
            if isinstance(block, BetaTextBlock):
                selected_tool = block.text.strip().lower()
                if selected_tool in {"code_agent", "doc_parser_agent", "complex_agent", "computer_use_agent"}:
                    return ToolResult(output=f"Delegated to {selected_tool}", system=selected_tool)
        
        # Fallback if no BetaTextBlock is found
        return ToolResult(output="Delegated to computer_use_agent", system="computer_use_agent")
