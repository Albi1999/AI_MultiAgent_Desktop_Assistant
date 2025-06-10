from fastapi import FastAPI
from pydantic import BaseModel
from anthropic import Anthropic
from fastapi.responses import JSONResponse
import os
from anthropic.types.beta import BetaTextBlock, BetaMCPToolUseBlock

app = FastAPI()

DEFAULT_MODEL = "claude-sonnet-4-20250514"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=ANTHROPIC_API_KEY)

class DocParseInput(BaseModel):
    message: str
    model: str | None = None
    doc_url: str | None = None

@app.post("/doc-parser-agent")
async def doc_parser_agent(input: DocParseInput):
    try:
        system_prompt = (
            "Sei un agente che legge documentazione tecnica da sorgenti MCP o link forniti. "
            "Analizza la documentazione e fornisci una spiegazione o istruzioni per aggiornare codice, "
            "scrivere funzioni o chiarire l'utilizzo di API. "
            "Collabora con altri agenti come il code_agent per generare codice aggiornato."
        )

        response = client.beta.messages.create(
            model=input.model or DEFAULT_MODEL,
            system=system_prompt,
            messages=[
                {"role": "user", "content": input.message + (f"\nDocumentazione: {input.doc_url}" if input.doc_url else "")}
            ],
            max_tokens=1500
        )

        for block in response.content:
            if isinstance(block, BetaTextBlock):
                return {"response": block.text}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return {"response": "Nessuna risposta valida ricevuta dal model MCP."}
