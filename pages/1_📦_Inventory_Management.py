import streamlit as st
from utils import get_inventory_data

st.title("📦 Inventory Management")

# Load data
df = get_inventory_data()

# Search input
search_term = st.text_input("🔍 Search inventory (by any field)")

# Filtered results
if search_term:
    filtered_df = df[df.apply(
        lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1
    )]
else:
    filtered_df = df

# Display table
st.dataframe(filtered_df, use_container_width=True)

# Download button
st.download_button(
    label="⬇️ Download as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_inventory.csv",
    mime="text/csv"
)
