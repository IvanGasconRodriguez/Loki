from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def explain(context: str) -> str:
    try:
        # CAMBIO: 'chat.completions' en lugar de 'responses'
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            max_tokens=300,  # CAMBIO: 'max_tokens' en lugar de 'max_output_tokens'
            messages=[  # CAMBIO: 'messages' en lugar de 'input'
                {"role": "system", "content": "Eres Loki, un asistente CRM."},
                {"role": "user", "content": context},
            ],
        )

        # CAMBIO: La respuesta se accede así:
        return r.choices[0].message.content

    except Exception as e:
        return f"Error generando respuesta: {e}"
