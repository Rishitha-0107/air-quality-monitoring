import plotly.express as px
import pandas as pd

class Plotter:
    @staticmethod
    def line_chart(data, pollutant):
        df = pd.DataFrame(data, columns=["timestamp", "value"])
        fig = px.line(df, x="timestamp", y="value", title=f"{pollutant.upper()} Trend")
        return fig
