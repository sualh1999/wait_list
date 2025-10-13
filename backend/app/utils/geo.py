import httpx
from typing import Optional

async def get_country_from_ip(ip_address: str) -> Optional[str]:
    if not ip_address or ip_address == "127.0.0.1": # Skip for localhost
        return None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://ip-api.com/json/{ip_address}")
            response.raise_for_status()
            data = response.json()
            if data and data.get("status") == "success":
                return data.get("country")
            else:
                print(f"Geo-IP lookup failed for {ip_address}: {data.get('message', 'Unknown error')}")
                return None
    except httpx.RequestError as e:
        print(f"HTTPX request failed for Geo-IP lookup: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during Geo-IP lookup: {e}")
        return None
