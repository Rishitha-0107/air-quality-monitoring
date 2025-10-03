from src.config.supabase_client import SupabaseConnection

class AlertDAO:
    def __init__(self):
        self.client = SupabaseConnection().get_client()

    def insert(self, alert_type, user_id, data_id=None, threshold_id=None):
        return (
            self.client.table("alert")
            .insert({
                "alert_type": alert_type,
                "user_id": user_id,
                "data_id": data_id,
                "threshold_id": threshold_id,
            })
            .execute()
        )

    def get_all_for_user(self, user_id):
        return (
            self.client.table("alert")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
