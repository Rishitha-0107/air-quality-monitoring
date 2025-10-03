from src.config.supabase_client import SupabaseConnection

class ThresholdDAO:
    def __init__(self):
        self.client = SupabaseConnection().get_client()

    def get_by_pollutant(self, pollutant):
        response = (
            self.client.table("threshold")
            .select("*")
            .eq("pollutant", pollutant)
            .execute()
        )
        if response.data and len(response.data) > 0:
            return response.data[0]   # return the first row as dict
        return None

    def get_all(self):
        return self.client.table("threshold").select("*").execute()
