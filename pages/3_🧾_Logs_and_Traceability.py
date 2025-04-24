import streamlit as st
import pandas as pd
from utils import get_log_data

st.title("🧾 Logs & Traceability")

log_df = get_log_data()
st.dataframe(log_df, use_container_width=True)
