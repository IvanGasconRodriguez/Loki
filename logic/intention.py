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


async def interpretar_intencion(message: str):
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