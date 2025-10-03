import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# ------------------------
# Supabase Configuration
# ------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ------------------------
# App General Settings
# ------------------------
APP_NAME = "Air Quality Monitoring"
DEFAULT_CITY = "Hyderabad"
DATA_FETCH_LIMIT = 50  # Default number of records to fetch from API or DB

# ------------------------
# Pollutant Threshold Defaults (fallbacks if DB missing)
# ------------------------
POLLUTANT_DEFAULT_THRESHOLDS = {
    "pm25": 60,       # µg/m³
    "co2": 1000,      # ppm
    "aqi": 100,       # AQI index
    "pm10": 100,
    "no2": 200,
    "so2": 80,
    "o3": 120,
}

# ------------------------
# Streamlit Page Defaults
# ------------------------
PAGE_LAYOUT = "wide"
PAGE_ICON = "🌍"
