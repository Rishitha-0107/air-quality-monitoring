# src/dao/air_quality_dao.py
from src.config.supabase_client import SupabaseConnection

class AirQualityDAO:
    def __init__(self):
        self.client = SupabaseConnection().get_client()

    def insert(self, record):
        return self.client.table("airqualitydata").insert(record).execute()

    def get_latest(self, limit=20):
        return self.client.table("airqualitydata").select("*").order("timestamp", desc=True).limit(limit).execute()

    def get_latest_by_city(self, city, limit=20):
        return self.client.table("airqualitydata").select("*").eq("city", city).order("timestamp", desc=True).limit(limit).execute()

    def get_by_date_range(self, city, start_date, end_date):
        return self.client.table("airqualitydata").select("*").eq("city", city).gte("timestamp", start_date).lte("timestamp", end_date).order("timestamp", desc=True).execute()
