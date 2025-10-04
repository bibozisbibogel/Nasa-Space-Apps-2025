"""Decision logic for launch go/no-go determination."""
from typing import Dict, Any, List
from datetime import datetime
from sites import LAUNCH_SITES
from integrations.meteomatics import get_weather
from integrations.swpc import get_space_weather
from integrations.spacetrack import get_conjunction_risk


def calculate_risk_score(
    weather: Dict[str, Any],
    space_weather: Dict[str, Any],
    conjunction: Dict[str, Any],
    limits: Dict[str, Any]
) -> int:
    """
    Calculate risk score 0-100.
    0 = perfect conditions
    100 = highly unfavorable
    """
    score = 0

    # Weather risk factors
    wind_ratio = weather["wind_speed_kn"] / limits["max_wind_kn"]
    if wind_ratio >= 1:
        score += 40
    elif wind_ratio >= 0.8:
        score += 20
    elif wind_ratio >= 0.6:
        score += 10

    # Precipitation - severe penalty for exceeding limits
    precip_ratio = weather["precipitation_mm"] / limits["max_precipitation_mm"]
    if precip_ratio >= 5:  # 5x over limit = scrub
        score += 50
    elif precip_ratio >= 2:  # 2x over limit = high risk
        score += 35
    elif precip_ratio >= 1:  # Over limit
        score += 25
    elif precip_ratio >= 0.7:  # Approaching limit
        score += 15

    # Cloud ceiling - lower clouds = higher risk
    if weather["cloud_ceiling_ft"] < 1000:  # Very low clouds
        score += 40
    elif weather["cloud_ceiling_ft"] < 2000:
        score += 30
    elif weather["cloud_ceiling_ft"] < 3000:
        score += 20
    elif weather["cloud_ceiling_ft"] < limits["max_cloud_ceiling_ft"]:
        score += 10

    temp = weather["temperature_c"]
    if temp > limits["max_temp_c"] or temp < limits["min_temp_c"]:
        score += 25
    elif temp > limits["max_temp_c"] - 5 or temp < limits["min_temp_c"] + 5:
        score += 10

    # Space weather risk
    kp = space_weather["kp_index"]
    if kp >= 7:
        score += 30
    elif kp >= 5:
        score += 15
    elif kp >= 3:
        score += 5

    if space_weather["has_solar_storm"]:
        score += 20

    # Conjunction risk
    if conjunction["has_high_risk"]:
        score += 40
    elif conjunction["close_approaches"] > 0:
        score += 10

    return min(score, 100)


def determine_verdict(risk_score: int) -> str:
    """Determine GO/NO-GO/MARGINAL verdict based on risk score."""
    if risk_score >= 70:
        return "NO-GO"
    elif risk_score >= 40:
        return "MARGINAL"
    else:
        return "GO"


def generate_explanation(
    weather: Dict[str, Any],
    space_weather: Dict[str, Any],
    conjunction: Dict[str, Any],
    limits: Dict[str, Any],
    risk_score: int
) -> str:
    """Generate human-readable explanation of the decision."""
    issues = []

    # Weather issues
    if weather["wind_speed_kn"] > limits["max_wind_kn"] * 0.8:
        issues.append(f"Wind speed {weather['wind_speed_kn']:.1f} kn approaching limit {limits['max_wind_kn']} kn")

    if weather["precipitation_mm"] > limits["max_precipitation_mm"] * 0.5:
        issues.append(f"Precipitation {weather['precipitation_mm']:.1f} mm near limit {limits['max_precipitation_mm']} mm")

    if weather["cloud_ceiling_ft"] < limits["max_cloud_ceiling_ft"]:
        issues.append(f"Cloud ceiling {weather['cloud_ceiling_ft']:.0f} ft below limit {limits['max_cloud_ceiling_ft']} ft")

    if weather["temperature_c"] > limits["max_temp_c"] - 5:
        issues.append(f"Temperature {weather['temperature_c']:.1f}°C approaching upper limit")

    if weather["temperature_c"] < limits["min_temp_c"] + 5:
        issues.append(f"Temperature {weather['temperature_c']:.1f}°C approaching lower limit")

    # Space weather issues
    if space_weather["kp_index"] >= 5:
        issues.append(f"Elevated Kp index at {space_weather['kp_index']:.0f} (geomagnetic storm conditions)")

    if space_weather["has_solar_storm"]:
        issues.append("Active solar storm detected")

    # Conjunction issues
    if conjunction["has_high_risk"]:
        issues.append("High debris conjunction risk detected")

    if not issues:
        return "All parameters within acceptable limits for launch"

    return "; ".join(issues)


def get_rule_citations(
    weather: Dict[str, Any],
    space_weather: Dict[str, Any],
    conjunction: Dict[str, Any],
    limits: Dict[str, Any]
) -> List[str]:
    """Generate list of applicable rule citations."""
    citations = []

    if weather["cloud_ceiling_ft"] < limits["max_cloud_ceiling_ft"]:
        citations.append("NASA-STD-4010A §4.1.8 (Thick Cloud Layers)")

    if weather["wind_speed_kn"] > limits["max_wind_kn"] * 0.8:
        citations.append(f"Vehicle SOP: Pad Wind Limit {limits['max_wind_kn']} kn")

    if weather["precipitation_mm"] > limits["max_precipitation_mm"] * 0.5:
        citations.append("NASA-STD-4010A §4.1.10 (Precipitation)")

    if space_weather["kp_index"] >= 5:
        citations.append("SWPC Kp advisory - Geomagnetic Storm Watch")

    if conjunction["has_high_risk"]:
        citations.append("COLA (Collision Avoidance) Analysis - High Risk")

    if not citations:
        citations.append("All parameters nominal")

    return citations


async def make_decision(site_code: str, launch_time: datetime) -> Dict[str, Any]:
    """
    Main decision function - determines GO/NO-GO for a launch.

    Args:
        site_code: Launch site code (e.g., "KSC", "VAFB")
        launch_time: Proposed launch datetime

    Returns:
        Decision dict with verdict, risk_score, explanation, and rule_citations
    """
    if site_code not in LAUNCH_SITES:
        return {
            "verdict": "ERROR",
            "risk_score": 100,
            "why": f"Unknown launch site: {site_code}",
            "rule_citations": []
        }

    site = LAUNCH_SITES[site_code]
    limits = site["limits"]

    # Gather data from all sources
    weather = await get_weather(site["lat"], site["lon"], launch_time)
    space_weather = await get_space_weather()
    conjunction = await get_conjunction_risk(site["lat"], site["lon"], launch_time)

    # Calculate risk and make decision
    risk_score = calculate_risk_score(weather, space_weather, conjunction, limits)
    verdict = determine_verdict(risk_score)
    explanation = generate_explanation(weather, space_weather, conjunction, limits, risk_score)
    citations = get_rule_citations(weather, space_weather, conjunction, limits)

    return {
        "verdict": verdict,
        "risk_score": risk_score,
        "why": explanation,
        "rule_citations": citations,
        "data": {
            "weather": weather,
            "space_weather": space_weather,
            "conjunction": conjunction
        }
    }
