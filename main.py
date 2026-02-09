from fastapi import FastAPI
from pydantic import BaseModel

from services.ghl import get_opportunities
from logic.rules import normalize_opportunities, leads_sin_contacto
from services.llm import explain


app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.post("/loki/chat")
async def chat(req: ChatRequest):
    message = req.message

    opps = await get_opportunities()
    state = normalize_opportunities(opps)

    if "priorizar" in message.lower():
        leads = leads_sin_contacto(state)

        if not leads:
            return {
                "answer": "No hay leads pendientes por priorizar.",
                "data": []
            }

        summary = "Leads sin contactar:\n"
        for l in leads:
            summary += f"- {l['name']} | stage_id: {l['stage_id']}\n"


        return {
             "answer": summary,
             "count": len(leads)
            }


    return {"answer": "No entendí la petición."}

