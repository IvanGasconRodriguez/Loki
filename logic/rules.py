from datetime import datetime, timedelta, timezone

def normalize_opportunities(opps):
    state = []

    for o in opps:
        state.append({
            "id": o["id"],
            "name": o["name"],
            "stage": o["pipelineStage"]["name"],
            "pipeline": o["pipeline"]["name"],
            "owner": o.get("assignedTo"),
            "created_at": o["createdAt"]
        })

    return state


def leads_sin_contacto(state, minutes=1440):
    now = datetime.now(timezone.utc)
    result = []

    for o in state:
        created = datetime.fromtimestamp(o["created_at"] / 1000)
        if o["stage"] == "Lead Entrante" and now - created > timedelta(minutes=minutes):
            result.append(o)

    return result
