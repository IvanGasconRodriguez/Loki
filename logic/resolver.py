def find_opportunity_by_name(state: list, name: str) -> dict | None:
    """
    Busca una oportunidad dentro del estado del CRM por coincidencia de nombre.

    Args:
        state (list): Lista de oportunidades normalizadas.
        name (str): Nombre (o parte del nombre) de la oportunidad.

    Returns:
        dict | None: La oportunidad encontrada o None si no existe coincidencia.
    """
    if not name:
        return None

    name = name.lower()

    for o in state:
        if name in o["name"].lower():
            return o

    return None

STAGE_MAP = {

    "Lead Entrante": "82ae1545-2029-4c0c-8c00-a60c21ab4f10",
    "Contacto Calificado":"accion - contacto manual",
    "Discovery Agendada":"ef2da212-7581-47dc-92ec-8fb3beb6986f",
    "Propuesta Enviada":"65233f1b-ca89-41a9-ac94-bac28d7146ec",
    "Reunion Realizada": "0b2eaf29-8192-4b44-9499-5a18e2f12e55",
    "Propuesta Enviada": "d4321144-9f4c-43c4-bf33-269ed1a3b13d",
    "Negociacion":"0015c928-687a-4829-832f-47141a3070c7"
}


def resolve_stage_id(stage_name: str) -> str | None:
    """
    Convierte un nombre de etapa a su ID correspondiente dentro del pipeline.

    La búsqueda se realiza de forma flexible (case-insensitive y parcial).

    Args:
        stage_name (str): Nombre de la etapa (ej. "Negociación").

    Returns:
        str | None: ID de la etapa o None si no se encuentra.
    """
    if not stage_name:
        return None

    for key in STAGE_MAP:
        if stage_name.lower() in key.lower():
            return STAGE_MAP[key]

    return None