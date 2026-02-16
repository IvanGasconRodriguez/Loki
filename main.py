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
            return {"answer": "No hay leads pendientes por priorizar.", "data": []}

        summary = "Leads sin contactar:\n"
        for l in leads:
            summary += f"- {l['name']} | {l['pipeline']} | {l['stage']}\n"

        return {"answer": explain(summary), "data": leads}

    # --- INICIO DEL NUEVO COMANDO ---
    elif "contar" in message.lower():
        total = len(state)
        # Usamos explain() para que sea la IA quien nos dé la noticia
        texto_para_ia = f"Dile al usuario de forma amable que tiene un total de {total} leads en su cuenta."

        return {"answer": explain(texto_para_ia), "data": state}
    # --- FIN DEL NUEVO COMANDO ---
    # --- PARTE NUEVA: Gestión de saludos ---
    elif any(saludo in message.lower() for saludo in ["hola", "buenas", "saludos"]):
        # Llamamos a la IA para que el saludo sea natural
        prompt_saludo = "Saluda al usuario, preséntate como Loki y dile que puedes ayudarle a contar o priorizar sus leads de GHL."
        return {"answer": explain(prompt_saludo)}

    return {"answer": "No entendí la petición."}
