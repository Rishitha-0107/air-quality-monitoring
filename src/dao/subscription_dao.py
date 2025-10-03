from src.config.supabase_client import SupabaseConnection

class SubscriptionDAO:
    def __init__(self):
        self.client = SupabaseConnection().get_client()

    def add_subscription(self, user_id, alert_type):
        return self.client.table("subscription").insert({
            "user_id": user_id,
            "alert_type": alert_type,
            "active": True
        }).execute()

    def get_by_user(self, user_id):
        return self.client.table("subscription").select("*").eq("user_id", user_id).execute()

    def deactivate(self, sub_id):
        return self.client.table("subscription").update({"active": False}).eq("sub_id", sub_id).execute()
