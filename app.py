import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# ---- LOAD MODEL + COLUMNS ----
model = joblib.load("flight_model.pkl")
model_columns = joblib.load("model_columns.pkl")

st.title("Flight Price Prediction")
st.write("     HAVE A HAPPY AND SAFE JOURNEY")

# ---- USER INPUTS ----
airlines = ["IndiGo", "Air India", "Vistara", "SpiceJet", "GoAir", "AirAsia"]
cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]

airline = st.selectbox("Airline", airlines)
source = st.selectbox("Source", cities)
destination = st.selectbox("Destination", cities)

if source == destination:
    st.warning("Source and destination cannot be same.")

date_input = st.date_input("Journey Date", value=datetime(2024, 5, 1))
duration_mins = st.number_input("Duration (minutes)", min_value=60, max_value=360, value=120)
total_stops = st.selectbox("Total Stops", [0, 1, 2])

# ---- PREDICT BUTTON ----
if st.button("Predict Price"):
    # 1) Create empty row with all model columns
    row = pd.DataFrame(columns=model_columns)
    row.loc[0] = 0   # fill everything with 0

    # 2) Set numeric features
    row.at[0, "duration_mins"] = duration_mins
    row.at[0, "duration_hours"] = duration_mins / 60
    row.at[0, "total_stops"] = total_stops
    row.at[0, "day"] = date_input.day
    row.at[0, "month"] = date_input.month
    row.at[0, "year"] = date_input.year

    # 3) Build route string
    route = f"{source}_{destination}"

    # 4) Set one-hot encoded columns if they exist
    for col in row.columns:
        if col == f"airline_{airline}":
            row.at[0, col] = 1
        if col == f"source_{source}":
            row.at[0, col] = 1
        if col == f"destination_{destination}":
            row.at[0, col] = 1
        if col == f"route_{route}":
            row.at[0, col] = 1

    # 5) Predict
    pred_price = model.predict(row)[0]

    st.success(f"Estimated Ticket Price: ₹ {int(pred_price):,}")
