from fastapi import FastAPI
from pydantic import BaseModel
import os
import dotenv
import anthropic
from anthropic.types.beta import BetaTextBlock

dotenv.load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

app = FastAPI()

class MessageRequest(BaseModel):
    message: str
    model: str = "claude-opus-4-20250514"
    has_thinking: bool = True

@app.post("/complex-agent")
async def complex_agent(request: MessageRequest):
    message = client.messages.create(
        model=request.model,
        max_tokens=1024,
        thinking={
            "type": "enabled",
            "budget_tokens": 1024
        },  
        messages=[
            {"role": "user", "content": request.message}
        ]
    )

    for block in message.content:
        if isinstance(block, BetaTextBlock):
            return {"response": block.text}

    return {"response": "No valid response received."}
