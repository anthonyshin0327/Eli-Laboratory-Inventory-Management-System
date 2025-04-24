import streamlit as st
from utils import get_inventory_data, update_inventory_data, log_action
import pandas as pd

st.title("🧪 Add or Use Inventory Item")

df = get_inventory_data()
item_names = df["Name"].dropna().unique().tolist()

mode = st.radio("Mode", ["Add New", "Use Item"])
selected_item = st.selectbox("Select Item", item_names) if mode == "Use Item" else None

# --- ADD NEW ITEM ---
if mode == "Add New":
    with st.form("add_form"):
        name = st.text_input("Name")
        category = st.selectbox("Category", ["Manufacturing (MFG)", "Research & Development (R&D)"])
        quantity = st.number_input("Quantity", min_value=0)
        unit = st.selectbox("Unit", ["aliquot", "pg", "ng", "µg", "mg", "g", "kg", "µL", "mL", "L"])
        location = st.text_input("Location")
        lot = st.text_input("Lot Number")
        expiry = st.date_input("Expiry Date", pd.Timestamp.today())
        supplier = st.text_input("Supplier")
        submitted = st.form_submit_button("Add Item")
        min_threshold = st.number_input("Minimum Stock Threshold", min_value=0, value=5)


    if submitted:
        new_data = pd.DataFrame([{
            "Name": name,
            "Category": category,
            "Quantity": quantity,
            "Unit": unit,
            "Location": location,
            "Lot": lot,
            "Expiry": expiry,
            "Supplier": supplier,
            "Threshold": min_threshold
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        update_inventory_data(df)
        log_action("Add", f"{name} ({quantity} {unit}) at {location}")
        st.success("Item added successfully.")

# --- USE ITEM (SUBTRACT QUANTITY) ---
elif mode == "Use Item" and selected_item:
    item_row = df[df["Name"] == selected_item].iloc[0]
    current_qty = item_row["Quantity"]
    unit = item_row["Unit"]

    st.markdown(f"**Current stock of `{selected_item}`:** {current_qty} {unit}")
    use_amount = st.number_input(f"How much to use ({unit})?", min_value=0.0, step=0.1)

    if st.button("Confirm Usage"):
        if use_amount > current_qty:
            st.error("Not enough stock available!")
        else:
            df.loc[df["Name"] == selected_item, "Quantity"] = current_qty - use_amount
            update_inventory_data(df)
            log_action("Use", f"{use_amount} {unit} of {selected_item} used")
            st.success(f"Used {use_amount} {unit} of {selected_item}. New stock: {current_qty - use_amount} {unit}")
