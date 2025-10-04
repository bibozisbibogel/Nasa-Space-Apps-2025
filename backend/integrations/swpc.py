"""NOAA SWPC (Space Weather Prediction Center) API integration."""
import httpx
from typing import Dict, Any
from datetime import datetime

# Cache for space weather data
_cache: Dict[str, tuple[float, Any]] = {}
CACHE_TTL = 300  # 5 minutes


async def get_space_weather() -> Dict[str, Any]:
    """
    Fetch current space weather conditions from NOAA SWPC.

    Returns dict with:
    - kp_index: Kp index (0-9 scale)
    - solar_wind_speed: km/s
    - has_solar_storm: boolean
    """
    cache_key = "space_weather"
    now = datetime.now().timestamp()

    # Check cache
    if cache_key in _cache:
        cached_time, cached_data = _cache[cache_key]
        if now - cached_time < CACHE_TTL:
            return cached_data

    result = {
        "kp_index": 0,
        "solar_wind_speed": 400.0,
        "has_solar_storm": False
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Get Kp index from 3-day forecast
            kp_response = await client.get(
                "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
            )
            if kp_response.status_code == 200:
                kp_data = kp_response.json()
                if kp_data:
                    # Get the most recent Kp value
                    latest = kp_data[-1]
                    result["kp_index"] = float(latest.get("kp_index", 0))

            # Get solar wind data
            wind_response = await client.get(
                "https://services.swpc.noaa.gov/products/summary/solar-wind-speed.json"
            )
            if wind_response.status_code == 200:
                wind_data = wind_response.json()
                if wind_data:
                    result["solar_wind_speed"] = float(wind_data.get("WindSpeed", 400))

            # Check for solar storms (Kp >= 5 indicates geomagnetic storm)
            result["has_solar_storm"] = result["kp_index"] >= 5

        # Cache result
        _cache[cache_key] = (now, result)
        return result

    except Exception as e:
        result["error"] = str(e)
        return result
