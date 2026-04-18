from datetime import datetime, timedelta, timezone


def normalize_opportunities(opps: list) -> list:
    """
    Normaliza la estructura de oportunidades obtenidas del CRM.

    Convierte los datos en un formato uniforme para facilitar su procesamiento
    en el agente.

    Args:
        opps (list): Lista de oportunidades crudas desde la API.

    Returns:
        list: Lista de oportunidades normalizadas con campos estándar.
    """
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
CALIFICADO_STAGE_ID = "ef2da212-7581-47dc-92ec-8fb3beb6986f"
DISCOVERY_AGENDADA_STAGE_ID = "65233f1b-ca89-41a9-ac94-bac28d7146ec"
REUNION_REALIZADA_STAGE_ID= "0b2eaf29-8192-4b44-9499-5a18e2f12e55"
PROPUESTA_ENVIADA_STAGE_ID= "d4321144-9f4c-43c4-bf33-269ed1a3b13d"
NEGOCIACION_STAGE_ID= "0015c928-687a-4829-832f-47141a3070c7"




def parse_iso_date(value: str):
    """
    Convierte una cadena de fecha en formato ISO a un objeto datetime.

    Args:
        value (str): Fecha en formato ISO (ej. "2024-01-01T10:00:00Z").

    Returns:
        datetime | None: Objeto datetime o None si el formato es inválido.
    """
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    return None


def leads_sin_contacto(state: list, minutes: int = 60) -> list:
    """
    Detecta leads en etapa inicial que no han recibido contacto reciente.

    Args:
        state (list): Lista de oportunidades normalizadas.
        minutes (int): Tiempo límite en minutos para considerar inactividad.

    Returns:
        list: Lista de leads que requieren contacto inmediato.
    """
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

def discovery_bloqueada(state: list, hours: int = 24) -> list:
    """
    Identifica oportunidades en etapa de discovery que no han sido actualizadas.

    Args:
        state (list): Lista de oportunidades.
        hours (int): Número de horas sin actualización.

    Returns:
        list: Oportunidades bloqueadas.
    """
    now = datetime.now(timezone.utc)
    result = []

    for o in state:
        if o["stage_id"] != DISCOVERY_AGENDADA_STAGE_ID:
            continue

        updated = parse_iso_date(o["updated_at"])
        if not updated:
            continue

        if now - updated > timedelta(hours=hours):
            result.append(o)

    return result

def propuestas_sin_respuesta(state: list, days: int = 3) -> list:
    """
    Detecta oportunidades en etapa de propuesta que no han tenido seguimiento.

    Args:
        state (list): Lista de oportunidades.
        days (int): Días sin respuesta.

    Returns:
        list: Oportunidades sin seguimiento.
    """
    now = datetime.now(timezone.utc)
    result = []

    for o in state:
        if o["stage_id"] != PROPUESTA_ENVIADA_STAGE_ID:
            continue

        updated = parse_iso_date(o["updated_at"])
        if not updated:
            continue

        if now - updated > timedelta(days=days):
            result.append(o)

    return result

def generar_resumen_diario(state: list):
    """
    Genera un resumen del estado del CRM incluyendo métricas clave.

    El resumen incluye:
    - Leads sin contacto
    - Discoveries bloqueadas
    - Propuestas sin respuesta

    Args:
        state (list): Lista de oportunidades normalizadas.

    Returns:
        tuple:
            - str: Texto del resumen
            - list: Leads sin contacto
            - list: Discoveries bloqueadas
            - list: Propuestas sin respuesta
    """
    leads = leads_sin_contacto(state)
    discoveries = discovery_bloqueada(state)
    propuestas = propuestas_sin_respuesta(state)

    resumen = "📊 Resumen diario CRM:\n\n"

    resumen += f"• Leads sin primer contacto: {len(leads)}\n"
    resumen += f"• Discoveries pendientes de mover: {len(discoveries)}\n"
    resumen += f"• Propuestas sin seguimiento: {len(propuestas)}\n"

    return resumen, leads, discoveries, propuestas

