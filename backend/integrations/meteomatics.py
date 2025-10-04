"""Meteomatics Weather API integration."""
import os
import httpx
from datetime import datetime, timezone
from typing import Dict, Any

METEOMATICS_USER = os.getenv("METEOMATICS_USER", "")
METEOMATICS_PASSWORD = os.getenv("METEOMATICS_PASSWORD", "")

# Cache for weather data (simple in-memory cache)
_cache: Dict[str, tuple[float, Any]] = {}
CACHE_TTL = 180  # 3 minutes


async def get_weather(lat: float, lon: float, dt: datetime) -> Dict[str, Any]:
    """
    Fetch weather data from Meteomatics API.

    Parameters:
    - lat, lon: coordinates
    - dt: datetime for forecast

    Returns weather dict with:
    - wind_speed_kn
    - precipitation_mm
    - cloud_ceiling_ft
    - temperature_c
    """
    cache_key = f"{lat},{lon},{dt.isoformat()}"
    now = datetime.now().timestamp()

    # Check cache
    if cache_key in _cache:
        cached_time, cached_data = _cache[cache_key]
        if now - cached_time < CACHE_TTL:
            return cached_data

    # Format datetime for Meteomatics API (use current time if forecast is too far)
    max_forecast_days = 7  # Meteomatics free tier typically supports 7 days
    now_utc = datetime.now(timezone.utc)

    # Make dt timezone-aware if it isn't
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    time_diff = (dt - now_utc).days

    if time_diff > max_forecast_days:
        # Use nearest available time
        dt = now_utc.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)

    dt_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Parameters to fetch
    params = [
        "wind_speed_10m:ms",  # Wind speed at 10m
        "precip_1h:mm",  # Precipitation
        "cloud_base_agl:m",  # Cloud base above ground level
        "t_2m:C"  # Temperature at 2m
    ]
    params_str = ",".join(params)

    url = f"https://api.meteomatics.com/{dt_str}/{params_str}/{lat},{lon}/json"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                url,
                auth=(METEOMATICS_USER, METEOMATICS_PASSWORD)
            )
            response.raise_for_status()
            data = response.json()

        # Parse response
        result = {
            "wind_speed_kn": 0.0,
            "precipitation_mm": 0.0,
            "cloud_ceiling_ft": 10000.0,
            "temperature_c": 20.0
        }

        for param_data in data.get("data", []):
            param = param_data.get("parameter", "")
            values = param_data.get("coordinates", [{}])[0].get("dates", [{}])
            if not values:
                continue
            value = values[0].get("value", 0)

            if "wind_speed" in param:
                # Convert m/s to knots
                result["wind_speed_kn"] = value * 1.94384
            elif "precip" in param:
                result["precipitation_mm"] = value
            elif "cloud_base" in param:
                # Convert meters to feet
                result["cloud_ceiling_ft"] = value * 3.28084
            elif "t_2m" in param:
                result["temperature_c"] = value

        # Cache result
        _cache[cache_key] = (now, result)
        return result

    except Exception as e:
        # Return safe defaults on error
        return {
            "wind_speed_kn": 0.0,
            "precipitation_mm": 0.0,
            "cloud_ceiling_ft": 10000.0,
            "temperature_c": 20.0,
            "error": str(e)
        }
