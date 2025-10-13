import httpx
from typing import Optional
import logging

logger = logging.getLogger(__name__)

async def get_country_from_ip(ip_address: str) -> Optional[str]:
    if not ip_address or ip_address == "127.0.0.1": # Skip for localhost
        return None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://ipapi.co/{ip_address}/json/")
            response.raise_for_status()
            data = response.json()
            if data and data.get("country_name"): # ipapi.co returns 'country_name'
                return data.get("country_name")
            else:
                logger.warning(f"Geo-IP lookup failed for {ip_address}: {data.get('error', 'Unknown error')}")
                return None
    except httpx.RequestError as e:
        logger.error(f"HTTPX request failed for Geo-IP lookup: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during Geo-IP lookup: {e}", exc_info=True)
        return None
