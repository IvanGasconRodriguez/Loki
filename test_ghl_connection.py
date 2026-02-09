print(">>> SCRIPT ARRANCA <<<")

import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

print("ALL ENV KEYS:", list(os.environ.keys()))

print(">>> ENV CARGADO <<<")

GHL_ACCESS_TOKEN = os.getenv("GHL_ACCESS_TOKEN")
GHL_LOCATION_ID = os.getenv("GHL_LOCATION_ID")

print("TOKEN PRESENTE:", bool(GHL_ACCESS_TOKEN))

BASE_URL = "https://services.leadconnectorhq.com"

HEADERS = {
    "Authorization": f"Bearer {GHL_ACCESS_TOKEN}",
    "Version": "2021-07-28",
    "Content-Type": "application/json"
}
'''async def test_connection():
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            f"{BASE_URL}/opportunities/search",
            json={
                "locationId": GHL_LOCATION_ID,
                "limit": 5
            },
            headers=HEADERS
        )
        r.raise_for_status()
        data = r.json()
        print(f"✅ Conexión OK — oportunidades encontradas: {len(data.get('opportunities', []))}")

asyncio.run(test_connection())'''

async def test_connection():
    print(">>> TEST OPORTUNIDADES <<<")

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            f"{BASE_URL}/opportunities/search",
            json={
                "locationId": GHL_LOCATION_ID,
                "limit": 5
            },
            headers=HEADERS
        )

        print("STATUS:", r.status_code)
        print("BODY:", r.text)

asyncio.run(test_connection())


