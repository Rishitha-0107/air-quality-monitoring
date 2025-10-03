import os
import requests
from datetime import datetime, timedelta
from src.dao.air_quality_dao import AirQualityDAO

class APIService:
    BASE_URL = "https://api.waqi.info/feed"

    def __init__(self):
        self.dao = AirQualityDAO()
        self.api_key = os.getenv("WAQI_API_KEY")
        if not self.api_key:
            raise RuntimeError("WAQI_API_KEY not set in .env")

    def fetch_and_store(self, city):
        url = f"{APIService.BASE_URL}/{city}/?token={self.api_key}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        j = resp.json()

        if j.get("status") != "ok":
            raise RuntimeError(f"API error: {j}")

        data = j["data"]
        pollutants = data.get("iaqi", {})
        timestamp = data["time"]["s"]

        records = []
        for pollutant, obj in pollutants.items():
            records.append({
                "city": city,
                "pollutant": pollutant,
                "value": obj.get("v"),
                "timestamp": timestamp
            })

        for r in records:
            self.dao.insert(r)

        return {"status": "success", "inserted": len(records), "city": city}

    def fetch_history(self, city, days=7):
        """
        Fetch last N days historical data for a city.
        Note: WAQI provides daily averages via /feed endpoint (not full archives).
        """
        url = f"{APIService.BASE_URL}/{city}/?token={self.api_key}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        j = resp.json()

        if j.get("status") != "ok":
            raise RuntimeError(f"API error: {j}")

        data = j["data"]

        history = []
        # WAQI has 'forecast' & 'history' sections for some cities
        if "forecast" in data and "daily" in data["forecast"]:
            for pollutant, entries in data["forecast"]["daily"].items():
                for entry in entries:
                    dt = entry["day"]
                    if datetime.fromisoformat(dt) >= datetime.now() - timedelta(days=days):
                        history.append({
                            "pollutant": pollutant,
                            "date": dt,
                            "avg": entry.get("avg"),
                            "min": entry.get("min"),
                            "max": entry.get("max"),
                        })

        return history
