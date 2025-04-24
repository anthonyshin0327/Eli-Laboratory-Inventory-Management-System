import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_inventory_data

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 LIMS Dashboard")

df = get_inventory_data()

# Ensure Threshold column exists and is numeric
if "Threshold" not in df.columns:
    df["Threshold"] = 5  # default if missing
df["Threshold"] = pd.to_numeric(df["Threshold"], errors='coerce').fillna(5)

# Low stock = Quantity <= Threshold
low_stock = df[df["Quantity"] <= df["Threshold"]]
good_stock = df[df["Quantity"] > df["Threshold"]]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("🧪 Total Items", df.shape[0])
col2.metric("⚠️ Low Stock (custom)", len(low_stock))
col3.metric("✅ Good Stock", len(good_stock))

# Chart
st.subheader("📦 Stock Level Overview")
fig = px.bar(df, x='Name', y='Quantity', color='Quantity',
             color_continuous_scale='RdYlGn', title="Stock Levels by Item")
st.plotly_chart(fig, use_container_width=True)

# Optional table
with st.expander("🔎 View Low Stock Items"):
    st.dataframe(low_stock, use_container_width=True)
