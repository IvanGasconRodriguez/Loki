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
                "source": o.get("source")
            }
        )

    return state



LEAD_ENTRANTE_STAGE_ID = "82ae1545-2029-4c0c-8c00-a60c21ab4f10"
TAG_CONTACTO_REALIZADO = "accion - contacto manual"


def parse_iso_date(value):
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    return None


def leads_sin_contacto(state, minutes=60):
    now = datetime.now(timezone.utc)
    result = []

    for o in state:
        # Solo Lead Entrante
        if o["stage"] != LEAD_ENTRANTE_STAGE_ID:
            continue

        # Excluir si ya fue contactado
        if TAG_CONTACTO_REALIZADO in o.get("tags", []):
            continue

        # SLA tiempo
        created = parse_iso_date(o["created_at"])
        if not created:
            continue

        if now - created > timedelta(minutes=minutes):
            result.append(o)

    return result
