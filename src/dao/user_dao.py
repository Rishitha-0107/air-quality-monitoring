from src.config.supabase_client import SupabaseConnection

class UserDAO:
    def __init__(self):
        self.client = SupabaseConnection().get_client()

    def register(self, name, email, phone):
        return self.client.table("User").insert({
            "name": name,
            "email": email,
            "phone": phone
        }).execute()

    def get_by_email(self, email):
        return self.client.table("User").select("*").eq("email", email).execute()

    def get_all(self):
        return self.client.table("User").select("*").execute()
