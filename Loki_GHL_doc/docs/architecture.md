# Arquitectura

El sistema sigue un flujo basado en agentes:

Usuario → API → LLM → Lógica → CRM

## Componentes

### 1. API (main.py)
Expone endpoint `/loki/chat`

### 2. LLM (services/llm.py)
Genera respuestas explicativas

### 3. Intención (logic/intention.py)
Convierte texto en JSON estructurado

### 4. Reglas (logic/rules.py)
Analiza estado del CRM

### 5. Integración CRM (services/ghl.py)
Comunicación con API externa

---

## Flujo completo

1. Usuario envía mensaje
2. Se obtienen oportunidades del CRM
3. Se normalizan datos
4. LLM interpreta intención
5. Se ejecuta lógica según acción
6. Se devuelve respuesta estructurada