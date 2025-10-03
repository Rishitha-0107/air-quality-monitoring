from supabase import create_client, Client
from src.config.settings import SUPABASE_URL, SUPABASE_KEY
from dotenv import load_dotenv
load_dotenv()


class SupabaseConnection:
    _client: Client = None

    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase URL or Key not set in settings.py")
        if not SupabaseConnection._client:
            SupabaseConnection._client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def get_client(self) -> Client:
        return SupabaseConnection._client
