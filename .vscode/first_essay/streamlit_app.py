import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Macro FX Analyzer", layout="wide")

st.title("Macroeconomic FX Structural Analyzer")
st.markdown("Quantitative multi-horizon exchange rate dashboard.")

# Sidebar for user inputs
st.sidebar.header("Parameters")
currency = st.sidebar.text_input("Forex Pair Ticker (Yahoo Finance)", value="AUDNZD=X")

# Fetch full historical data
@st.cache_data(ttl=3600)
def load_data(ticker):
    data = yf.download(ticker, period="max", interval="1d")
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data = data.dropna(subset=["Close", "High", "Low"])
    return data

try:
    df_max = load_data(currency)

    latest_date = df_max.index.max()
    df_1y = df_max.loc[df_max.index >= (latest_date - pd.DateOffset(years=1))].copy()
    df_10y = df_max.loc[df_max.index >= (latest_date - pd.DateOffset(years=10))].copy()

    def render_horizon_tab(df_slice, label, color):
        df_slice["Log_Return"] = np.log(df_slice["Close"] / df_slice["Close"].shift(1))
        ann_return = df_slice["Log_Return"].mean() * 252
        ann_vol = df_slice["Log_Return"].std() * np.sqrt(252)
        mean_p = float(df_slice["Close"].mean())
        ath = float(df_slice["High"].max())
        atl = float(df_slice["Low"].min())

        # Display Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ann. Return", f"{ann_return:.2%}")
        c2.metric("Ann. Volatility", f"{ann_vol:.2%}")
        c3.metric("High (ATH)", f"{ath:.4f}")
        c4.metric("Low (ATL)", f"{atl:.4f}")

        # Plotly Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_slice.index, y=df_slice["Close"], mode="lines", name=currency, line=dict(color=color, width=1.5)))
        fig.add_hline(y=mean_p, line=dict(color="#FFB300", dash="dash"), annotation_text=f"Mean ({mean_p:.4f})")
        fig.update_layout(template="plotly_dark", height=450, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)

    tab1, tab2, tab3 = st.tabs(["1-Year Horizon", "10-Year Horizon", "All-Time History"])
    with tab1:
        render_horizon_tab(df_1y, "1-Year", "#00D4FF")
    with tab2:
        render_horizon_tab(df_10y, "10-Year", "#7C4DFF")
    with tab3:
        render_horizon_tab(df_max, "All-Time", "#00E676")

except Exception as e:
    st.error(f"Error fetching data for ticker '{currency}': {e}")
