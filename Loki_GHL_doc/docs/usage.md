# Guía de uso

## ▶️ Ejecutar servidor

```bash
uvicorn main:app --reload


POST /loki/chat

{
  "message": "mueve la oportunidad Juan a negociación"
}
Respuestas posibles
{
  "intent": {...},
  "found_opportunity": {...},
  "resolved_stage_id": "..."
}
{
  "answer": "Resumen diario CRM..."
}