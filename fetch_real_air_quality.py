"""Fetch Delhi 2025 CAMS-modelled air-quality estimates from Open-Meteo."""
from pathlib import Path
import requests
import pandas as pd

BASE = Path(__file__).resolve().parent
URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
PARAMS = {
    "latitude": 28.6139, "longitude": 77.2090,
    "hourly": "pm2_5,pm10,nitrogen_dioxide",
    "start_date": "2025-01-01", "end_date": "2025-12-31",
    "timezone": "Asia/Kolkata", "domains": "cams_global",
}
response = requests.get(URL, params=PARAMS, timeout=90)
response.raise_for_status()
data = response.json()
if "hourly" not in data:
    raise ValueError(f"Missing hourly measurements: {data}")
df = pd.DataFrame(data["hourly"])
df["time"] = pd.to_datetime(df["time"])
assert {"time", "pm2_5", "pm10", "nitrogen_dioxide"} <= set(df.columns)
df.to_csv(BASE / "real_cams_air_quality_2025_delhi.csv", index=False)
print(f"Saved {len(df)} hourly rows from Open-Meteo/CAMS.")
