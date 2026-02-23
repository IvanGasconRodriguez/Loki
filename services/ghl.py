import httpx
from config import GHL_ACCESS_TOKEN, GHL_LOCATION_ID

BASE_URL = "https://services.leadconnectorhq.com"

HEADERS = {
    "Authorization": f"Bearer {GHL_ACCESS_TOKEN}",
    "Version": "2021-04-15",
    "Content-Type": "application/json",
}


async def get_opportunities():
    # Para buscar oportunidades en la v2 con la versión 2021-04-15,
    # se usa el método POST y el locationId va en el cuerpo (JSON)
    url = f"{BASE_URL}/opportunities/search"

    payload = {"locationId": GHL_LOCATION_ID.strip()}

    async with httpx.AsyncClient(timeout=15) as client:
        # Enviamos la petición como POST con json=payload
        r = await client.post(url, json=payload, headers=HEADERS)

        if r.status_code != 200:
            print(f"Error de GHL detallado: {r.text}")

        r.raise_for_status()

        # GHL devuelve un objeto que contiene una lista llamada 'opportunities'
        data = r.json()
        return data.get("opportunities", [])




async def move_opportunity_stage(opportunity_id, new_stage_id):
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.put(
            f"{BASE_URL}/opportunities/{opportunity_id}",
            json={
                "pipelineStageId": new_stage_id
            },
            headers=HEADERS
        )
        return r.status_code, r.text