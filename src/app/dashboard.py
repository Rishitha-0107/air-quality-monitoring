# src/app/dashboard.py
import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px

from src.dao.air_quality_dao import AirQualityDAO
from src.dao.threshold_dao import ThresholdDAO
from src.services.api_service import APIService
from src.services.alert_service import AlertService
from src.utils.plotting import Plotter


def main():
    st.header("📊 Dashboard")

    aq_dao = AirQualityDAO()
    threshold_dao = ThresholdDAO()
    api_service = APIService()
    alert_service = AlertService()

    # --- City Input ---
    city = st.text_input(
        "Enter a city in India (e.g., Delhi, Hyderabad, Lucknow)", "Delhi"
    )

    # --- Fetch Latest Data ---
    if st.button("🔄 Fetch Latest Data from API"):
        try:
            result = api_service.fetch_and_store(city)
            st.success(f"Inserted {result['inserted']} records for {city}")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to fetch data: {e}")

    # --- Query DB ---
    response = aq_dao.get_latest_by_city(city, limit=50)
    data = response.data if hasattr(response, "data") else response.get("data", [])

    if not data:
        st.warning("⚠️ No data available. Please fetch first.")
        return

    st.subheader(f"📌 Latest Records for {city}")

    # --- Pollutant Cards ---
    cols = st.columns(min(4, len(data[:8])))  # first 8 pollutants max
    for i, d in enumerate(data[:8]):
        pollutant = d["pollutant"].upper()
        value = d["value"]

        # Threshold check
        try:
            threshold = threshold_dao.get_by_pollutant(d["pollutant"].lower())
            limit = threshold["max_value"] if threshold else None
        except:
            limit = None

        color = "lightgreen"
        if limit and value > limit:
            color = "tomato"
        elif limit and value > (0.7 * limit):
            color = "orange"

        with cols[i % len(cols)]:
            st.markdown(
                f"""
                <div style="padding:15px; border-radius:10px; background-color:{color}">
                    <h4>{pollutant}</h4>
                    <p><b>{value}</b></p>
                    <small>Limit: {limit if limit else 'N/A'}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --- Bar & Pie Snapshot ---
    st.subheader("📊 Pollutant Snapshot")
    latest_snapshot = {d["pollutant"]: d["value"] for d in data[:10]}
    df_snapshot = pd.DataFrame(list(latest_snapshot.items()), columns=["Pollutant", "Value"])

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            px.bar(df_snapshot, x="Pollutant", y="Value", color="Pollutant",
                   title="Pollutants Bar Chart"),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            px.pie(df_snapshot, names="Pollutant", values="Value", hole=0.4,
                   title="Pollutants Share"),
            use_container_width=True,
        )

    # --- Time Series (Multi-select pollutants) ---
    pollutants = sorted({d["pollutant"].lower() for d in data})
    selected_pollutants = st.multiselect("Choose Pollutants", pollutants, default=[pollutants[0]])

    for pollutant in selected_pollutants:
        filtered = [
            (datetime.fromisoformat(d["timestamp"]), d["value"])
            for d in data if d["pollutant"].lower() == pollutant
        ]
        if filtered:
            fig = Plotter.line_chart(filtered, pollutant)
            try:
                threshold = threshold_dao.get_by_pollutant(pollutant)
                max_value = threshold["max_value"] if threshold else None
                if max_value:
                    fig.add_hline(y=max_value, line_dash="dash", line_color="red",
                                  annotation_text="Threshold", annotation_position="top right")
            except:
                pass
            st.plotly_chart(fig, use_container_width=True)
