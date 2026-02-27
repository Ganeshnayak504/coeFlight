import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -----------------------------
# Load Model
# -----------------------------
try:
    model = joblib.load("flight_model.pkl")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.title("✈️ Flight Price Prediction")

# -----------------------------
# User Inputs
# -----------------------------
airline = st.selectbox("Airline", [
    "Air India",
    "GoAir",
    "IndiGo",
    "Jet Airways",
    "Jet Airways Business",
    "Multiple carriers",
    "Multiple carriers Premium economy",
    "SpiceJet",
    "Trujet",
    "Vistara",
    "Vistara Premium economy"
])

total_stops = st.selectbox("Total Stops", [0, 1, 2, 3, 4])

journey_date = st.date_input("Journey Date")
dep_time = st.time_input("Departure Time")
arrival_time = st.time_input("Arrival Time")

# -----------------------------
# Feature Engineering
# -----------------------------
Day = journey_date.day
Month = journey_date.month
Year = journey_date.year

Dep_hour = dep_time.hour
Dep_min = dep_time.minute

Arrival_hour = arrival_time.hour
Arrival_min = arrival_time.minute

Duration_hour = abs(Arrival_hour - Dep_hour)
Duration_min = abs(Arrival_min - Dep_min)

# -----------------------------
# Create Base Data
# -----------------------------
input_dict = {
    'Total_Stops': total_stops,
    'Day': Day,
    'Month': Month,
    'Year': Year,
    'Dep_hour': Dep_hour,
    'Dep_min': Dep_min,
    'Arrival_hour': Arrival_hour,
    'Arrival_min': Arrival_min,
    'Duration_hour': Duration_hour,
    'Duration_min': Duration_min,
}

# Add all airline columns as 0
airline_columns = [
    'Airline_Air India',
    'Airline_GoAir',
    'Airline_IndiGo',
    'Airline_Jet Airways',
    'Airline_Jet Airways Business',
    'Airline_Multiple carriers',
    'Airline_Multiple carriers Premium economy',
    'Airline_SpiceJet',
    'Airline_Trujet',
    'Airline_Vistara',
    'Airline_Vistara Premium economy'
]

for col in airline_columns:
    input_dict[col] = 0

# Set selected airline to 1
selected_airline_column = f"Airline_{airline}"
input_dict[selected_airline_column] = 1

# Convert to DataFrame
input_df = pd.DataFrame([input_dict])

# Ensure correct column order
model_columns = model.feature_names_in_
input_df = input_df[model_columns]

# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict Price 💰"):
    try:
        prediction = model.predict(input_df)
        st.success(f"Estimated Flight Price: ₹ {int(prediction[0])}")
    except Exception as e:
        st.error(f"Prediction error: {e}")