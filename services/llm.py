from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def explain(context: str) -> str:
    """
    Genera una explicación en lenguaje natural basada en un contexto dado
    utilizando un modelo de OpenAI.

    Args:
        context (str): Texto base para generar la explicación.

    Returns:
        str: Respuesta generada por el modelo.

    En caso de error:
        str: Mensaje de error.
    """
    try:
        r = client.responses.create(
            model="gpt-4.1-mini",
            temperature=0.2,
            max_output_tokens=300,
            input=[
                {"role": "system", "content": "Eres Loki, asistente CRM."},
                {"role": "user", "content": context}
            ]
        )

        return r.output_text
    except Exception as e:
        return f"Error generando respuesta: {e}"   

