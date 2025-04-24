import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

def get_inventory_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Inventory", ttl=0)
    df.dropna(how="all", inplace=True)
    return df

def update_inventory_data(df: pd.DataFrame):
    conn = st.connection("gsheets", type=GSheetsConnection)
    conn.update(worksheet="Inventory", data=df)

def get_log_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df = conn.read(worksheet="Logs", ttl=0)
        df.dropna(how="all", inplace=True)
        return df
    except:
        return pd.DataFrame(columns=["Timestamp", "User", "Action", "Details"])

def log_action(action: str, details: str, user: str = "anonymous"):
    log_df = get_log_data()
    new_entry = pd.DataFrame([{
        "Timestamp": pd.Timestamp.now(),
        "User": user,
        "Action": action,
        "Details": details
    }])
    updated_log = pd.concat([log_df, new_entry], ignore_index=True)

    conn = st.connection("gsheets", type=GSheetsConnection)
    conn.update(worksheet="Logs", data=updated_log)
