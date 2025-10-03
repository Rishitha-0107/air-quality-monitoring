# src/app/history.py
import streamlit as st
import pandas as pd
import plotly.express as px
from src.services.api_service import APIService

def main():
    st.header("📜 Air Quality History")

    api_service = APIService()
    city = st.text_input("Enter City for history", "Delhi")

    if st.button("📥 Fetch Last 7 Days History"):
        try:
            history_data = api_service.fetch_history(city, days=7)
            if not history_data:
                st.warning("⚠️ No historical data found for this city.")
                return

            st.subheader(f"📊 History for {city} (Last 7 Days)")
            df = pd.DataFrame(history_data)

            # Average pollutant levels
            avg_df = df.groupby("pollutant", as_index=False)["avg"].mean()
            st.plotly_chart(
                px.bar(avg_df, x="pollutant", y="avg", color="pollutant",
                       title="Average Pollutant Levels (7 days)"),
                use_container_width=True,
            )

            # Time-series trend
            pollutant = st.selectbox("Choose Pollutant", df["pollutant"].unique())
            df_filtered = df[df["pollutant"] == pollutant]
            fig = px.line(df_filtered, x="date", y="avg",
                          title=f"{pollutant.upper()} - Historical Trend")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Failed to fetch history: {e}")
