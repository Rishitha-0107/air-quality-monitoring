# src/app/main.py
import sys
import os
import streamlit as st

# --- Ensure project root in sys.path ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import pages
from src.app.dashboard import main as dashboard_main
from src.app.history import main as history_main
from src.app.settings import main as settings_main
from src.app.login import login_page

st.set_page_config(page_title="Air Quality Monitoring", layout="wide")

# --- Check if logged in ---
if "user" not in st.session_state:
    login_page()
else:
    st.sidebar.title(f"👋 Welcome, {st.session_state['user']['name']}")
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Dashboard", "📜 History", "⚙️ Settings"]
    )

    if page == "🏠 Dashboard":
        dashboard_main()
    elif page == "📜 History":
        history_main()
    elif page == "⚙️ Settings":
        settings_main()
