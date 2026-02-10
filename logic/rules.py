from datetime import datetime, timedelta, timezone


def normalize_opportunities(opps):
    state = []

    for o in opps:
        # Usamos .get() para evitar que el programa se detenga si falta algún campo
        # GHL en la búsqueda básica envía 'pipelineStageId' y 'pipelineId'
        state.append(
            {
                "id": o.get("id"),
                "name": o.get("name", "Sin nombre"),
                # Si no viene el nombre de la etapa, ponemos el ID para que no de error
                "stage": o.get("pipelineStageId", "N/A"),
                "pipeline": o.get("pipelineId", "N/A"),
                "owner": o.get("assignedTo"),
                "created_at": o.get("createdAt"),
            }
        )

    return state


def leads_sin_contacto(state, minutes=1440):
    now = datetime.now(timezone.utc)
    result = []

    for o in state:
        if not o["created_at"]:
            continue

        # Convertimos la fecha de GHL a formato Python
        try:
            # GHL usa milisegundos, por eso dividimos por 1000
            created = datetime.fromisoformat(o["created_at"].replace("Z", "+00:00"))

            # Aquí la regla: si lleva más de 'X' minutos en una etapa específica
            if now - created > timedelta(minutes=minutes):
                result.append(o)
        except Exception as e:
            print(f"Error procesando fecha: {e}")
            continue

    return result
