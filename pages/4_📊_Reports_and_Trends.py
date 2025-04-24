import streamlit as st
import plotly.express as px
import pandas as pd
from utils import get_inventory_data

st.title("📊 Reports & Trends")

df = get_inventory_data()

tab1, tab2 = st.tabs(["📉 Stock Distribution", "📆 Expiry Timeline"])

with tab1:
    fig = px.pie(df, values='Quantity', names='Category', title='Stock Distribution by Category')
    st.plotly_chart(fig)

with tab2:
    df['Expiry'] = pd.to_datetime(df['Expiry'], errors='coerce')
    exp_chart = px.histogram(df, x='Expiry', nbins=20, title='Items by Expiry Date')
    st.plotly_chart(exp_chart)
