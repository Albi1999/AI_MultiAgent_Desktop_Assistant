from fastapi import FastAPI
from pydantic import BaseModel
import os
from anthropic import Anthropic
from anthropic.types.beta import BetaTextBlock
from fastapi.responses import JSONResponse

app = FastAPI()

DEFAULT_MODEL = "claude-opus-4-20250514"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=ANTHROPIC_API_KEY)

class CodeRequest(BaseModel):
    message: str
    model: str | None = None

@app.post("/code-agent")
async def code_agent(request: CodeRequest):
    try:
        system_prompt = (
            "Sei un agente esperto nella generazione di codice. L'utente ti chiederà di implementare funzioni, script o frammenti di codice. "
            "Il tuo compito è generare codice pulito e commentato. Quando necessario, comunica con il computer_use_agent "
            "per aprire un file, scrivere codice o compiere altre azioni sull'interfaccia utente tipo aprire un editor ed inserire il codice generato."
        )

        response = client.beta.messages.create(
            model=request.model or DEFAULT_MODEL,
            system=system_prompt,
            thinking={
            "type": "enabled",
            "budget_tokens": 1024
            },      
            messages=[
                {"role": "user", "content": request.message}
            ],
            max_tokens=1500
        )

        for block in response.content:
            if isinstance(block, BetaTextBlock):
                return {"response": block.text}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return {"response": "Nessuna risposta valida ricevuta dal code agent."}
