"""Launch site definitions with coordinates and limits."""

# Default launch limits for Big Refueler rocket
DEFAULT_LIMITS = {
    "max_wind_kn": 30,
    "max_precipitation_mm": 0.3,
    "max_cloud_ceiling_ft": 4500,
    "max_temp_c": 40,
    "min_temp_c": -10,
}

LAUNCH_SITES = {
    "KSC_LC39A": {
        "name": "Kennedy Space Center (LC-39A)",
        "lat": 28.6084,
        "lon": -80.6043,
        "limits": DEFAULT_LIMITS.copy()
    },
    "CCSFS_SLC40": {
        "name": "Cape Canaveral Space Force Station",
        "lat": 28.5618,
        "lon": -80.5772,
        "limits": DEFAULT_LIMITS.copy()
    },
    "VAFB": {
        "name": "Vandenberg Space Force Base",
        "lat": 34.7420,
        "lon": -120.5724,
        "limits": DEFAULT_LIMITS.copy()
    },
    "WFF": {
        "name": "Wallops Flight Facility",
        "lat": 37.9400,
        "lon": -75.4660,
        "limits": DEFAULT_LIMITS.copy()
    },
    "PSCA": {
        "name": "Pacific Spaceport Complex (Alaska)",
        "lat": 57.4352,
        "lon": -152.3394,
        "limits": DEFAULT_LIMITS.copy()
    },
    "GSC": {
        "name": "Guiana Space Centre (Kourou)",
        "lat": 5.2360,
        "lon": -52.7750,
        "limits": DEFAULT_LIMITS.copy()
    },
    "TSC": {
        "name": "Tanegashima Space Center",
        "lat": 30.4017,
        "lon": 130.9740,
        "limits": DEFAULT_LIMITS.copy()
    },
    "SDSC": {
        "name": "Satish Dhawan Space Centre",
        "lat": 13.7331,
        "lon": 80.2350,
        "limits": DEFAULT_LIMITS.copy()
    },
    "RL_Mahia": {
        "name": "Rocket Lab Launch Complex 1 (Māhia)",
        "lat": -39.2628,
        "lon": 177.8644,
        "limits": DEFAULT_LIMITS.copy()
    },
    "SPC_UK": {
        "name": "Spaceport Cornwall",
        "lat": 50.4400,
        "lon": -5.0100,
        "limits": DEFAULT_LIMITS.copy()
    }
}
