from datetime import datetime, timedelta, timezone


def normalize_opportunities(opps):
    state = []

    for o in opps:
        state.append({
            "id": o["id"],
            "name": o["name"],
            "pipeline_id": o.get("pipelineId"),
            "stage_id": o.get("pipelineStageId"),
            "created_at": o["createdAt"],
            "updated_at": o["updatedAt"],
            "assigned_to": o.get("assignedTo"),
            "tags": o.get("contact", {}).get("tags", []),
            "source": o.get("source"),
        })

    return state





def parse_iso_date(value):
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    return None


def leads_sin_contacto(state, minutes=60):
    now = datetime.now(timezone.utc)
    result = []

    for o in state:
        created = parse_iso_date(o["created_at"])
        if not created:
            continue

        if now - created > timedelta(minutes=minutes):
            result.append(o)

    return result