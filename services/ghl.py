import httpx
from config import GHL_API_KEY, GHL_LOCATION_ID

BASE_URL = "https://services.leadconnectorhq.com"

HEADERS = {
    "Authorization": f"Bearer {GHL_API_KEY}",
    "Version": "2021-07-28",
    "Content-Type": "application/json"
}

async def get_opportunities():
    url = f"{BASE_URL}/opportunities/search"
    payload = {
        "locationId": GHL_LOCATION_ID,
        "limit": 100
    }

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(url, json=payload, headers=HEADERS)
        r.raise_for_status()
        return r.json().get("opportunities", [])
