import os
import json
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
Eres un parser de instrucciones para un CRM.

Devuelve SIEMPRE JSON válido.
Nunca expliques nada.
Nunca añadas texto extra.

Acciones posibles:
- move_opportunity
- add_tag
- create_task
- none

Formato obligatorio:

{
  "action": "...",
  "opportunity_name": "...",
  "target_stage": "...",
  "tag": "...",
  "task_description": "..."
}

Si no detectas acción clara:
{
  "action": "none"
}
"""


async def interpretar_intencion(message: str) -> dict:
    """
    Interpreta la intención del usuario a partir de un mensaje en lenguaje natural
    utilizando un modelo de OpenAI.

    El modelo devuelve una respuesta en formato JSON con una acción específica
    relacionada con operaciones en el CRM.

    Args:
        message (str): Texto enviado por el usuario.

    Returns:
        dict: Diccionario con la intención detectada. Ejemplo:
            {
                "action": "move_opportunity",
                "opportunity_name": "Juan",
                "target_stage": "Negociación",
                "tag": "...",
                "task_description": "..."
            }

        En caso de error o si no se detecta intención clara:
            {"action": "none"}
    """
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {"action": "none"}