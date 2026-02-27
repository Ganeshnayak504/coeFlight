import streamlit as st
import pickle
import numpy as np

# -----------------------------
# Load Trained Model
# -----------------------------
with open("flight_model.pkl", "rb") as f:
    model = pickle.load(f)

# -----------------------------
# App Title
# -----------------------------
st.title("✈ Flight Price Prediction App")
st.write("Enter flight details below to predict price")

# -----------------------------
# Input Fields
# -----------------------------

Total_Stops = st.selectbox("Total Stops", [0, 1, 2, 3])

Day = st.slider("Journey Day", 1, 31, 15)
Month = st.slider("Journey Month", 1, 12, 6)
Year = 2019  # Fixed because dataset contains 2019

Dep_hour = st.slider("Departure Hour", 0, 23, 10)
Dep_min = st.slider("Departure Minute", 0, 59, 30)

Arrival_hour = st.slider("Arrival Hour", 0, 23, 12)
Arrival_min = st.slider("Arrival Minute", 0, 59, 15)

Duration_hour = st.slider("Duration Hour", 0, 20, 2)
Duration_min = st.slider("Duration Minute", 0, 59, 45)

# -----------------------------
# Airline Selection
# -----------------------------

airline = st.selectbox("Select Airline", [
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

# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Price"):

    # Create airline one-hot encoding
    airline_list = [
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
    ]

    airline_features = [0] * 11
    airline_index = airline_list.index(airline)
    airline_features[airline_index] = 1

    # Arrange input in exact same order as training
    input_data = np.array([[
        Total_Stops,
        Day,
        Month,
        Year,
        Dep_hour,
        Dep_min,
        Arrival_hour,
        Arrival_min,
        Duration_hour,
        Duration_min,
        *airline_features
    ]])

    # Prediction
    prediction = model.predict(input_data)

    st.success(f"💰 Estimated Flight Price: ₹ {int(prediction[0])}")