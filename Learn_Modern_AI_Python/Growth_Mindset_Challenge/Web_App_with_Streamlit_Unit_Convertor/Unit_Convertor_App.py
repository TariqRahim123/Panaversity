import streamlit as st
import pandas as pd
import os
from io import BytesIO
import matplotlib.pyplot as plt

# --- Streamlit App Config ---
st.set_page_config(page_title="Unit Converter App by Tariq Rahim", layout="wide")

# --- Styling ---
def inject_css():
    st.markdown("""
        <style>
            .main { background-color: #f7f9fb; }
            .block-container {
                padding: 2rem;
                border-radius: 12px;
                background-color: #ffffff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1, h2 { color: #004080; }
            .stButton>button {
                background-color: #004080;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 0.5rem 1rem;
            }
            .stButton>button:hover { background-color: #0066cc; }
        </style>
    """, unsafe_allow_html=True)

# --- Conversion Functions ---
def convert_length(value, from_unit, to_unit):
    conversions = {
        'meters': 1,
        'kilometers': 0.001,
        'miles': 0.000621371,
        'feet': 3.28084,
        'inches': 39.3701
    }
    return value / conversions[from_unit] * conversions[to_unit]

def convert_weight(value, from_unit, to_unit):
    conversions = {
        'grams': 1,
        'kilograms': 0.001,
        'pounds': 0.00220462,
        'ounces': 0.035274
    }
    return value / conversions[from_unit] * conversions[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    elif from_unit == 'Celsius':
        return (value * 9/5 + 32) if to_unit == 'Fahrenheit' else value + 273.15
    elif from_unit == 'Fahrenheit':
        return (value - 32) * 5/9 if to_unit == 'Celsius' else (value - 32) * 5/9 + 273.15
    elif from_unit == 'Kelvin':
        return value - 273.15 if to_unit == 'Celsius' else (value - 273.15) * 9/5 + 32

def convert_time(value, from_unit, to_unit):
    conversions = {
        'seconds': 1,
        'minutes': 1/60,
        'hours': 1/3600,
        'days': 1/86400
    }
    return value / conversions[from_unit] * conversions[to_unit]

def convert_speed(value, from_unit, to_unit):
    conversions = {
        'm/s': 1,
        'km/h': 3.6,
        'mph': 2.23694,
        'ft/s': 3.28084
    }
    return value / conversions[from_unit] * conversions[to_unit]

# --- Main App ---
def main():
    inject_css()
    st.title("🔄 Multi Unit Converter App")

    # Sidebar for History
    if "history" not in st.session_state:
        st.session_state.history = []

    st.sidebar.header("📜 Conversion History")
    if st.session_state.history:
        hist_df = pd.DataFrame(st.session_state.history[-30:], columns=["Category", "Input", "From", "To", "Result"])
        st.sidebar.dataframe(hist_df, use_container_width=True)
        buffer = BytesIO()
        hist_df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        st.sidebar.download_button("📥 Download History (Excel)", data=buffer, file_name="conversion_history.xlsx")

    emojis = {
        "Length": "📏", "Weight": "⚖️", "Temperature": "🌡️",
        "Time": "⏱️", "Speed": "🚗"
    }
    category = st.selectbox("Choose Conversion Type:", list(emojis.keys()), format_func=lambda x: f"{emojis[x]} {x}")

    col1, col2 = st.columns([3, 2])
    with col1:
        values = st.text_area("Enter values (comma separated):", "1, 10, 100")
        try:
            values = [float(v.strip()) for v in values.split(",") if v.strip()]
        except:
            st.error("Please enter valid numbers separated by commas.")
            return

    with col2:
        if category == "Length":
            units = ["meters", "kilometers", "miles", "feet", "inches"]
            convert_func = convert_length
        elif category == "Weight":
            units = ["grams", "kilograms", "pounds", "ounces"]
            convert_func = convert_weight
        elif category == "Temperature":
            units = ["Celsius", "Fahrenheit", "Kelvin"]
            convert_func = convert_temperature
        elif category == "Time":
            units = ["seconds", "minutes", "hours", "days"]
            convert_func = convert_time
        elif category == "Speed":
            units = ["m/s", "km/h", "mph", "ft/s"]
            convert_func = convert_speed

        from_unit = st.selectbox("From Unit:", units)
        to_unit = st.selectbox("To Unit:", units)

    if st.button("Convert"):
        results = [convert_func(v, from_unit, to_unit) for v in values]
        result_df = pd.DataFrame({
            "Input": values,
            f"Converted ({to_unit})": results
        })
        st.dataframe(result_df, use_container_width=True)

        # Add history (max 30)
        for v, r in zip(values, results):
            st.session_state.history.append([category, v, from_unit, to_unit, round(r, 4)])
        st.session_state.history = st.session_state.history[-30:]

        # Plot results
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.bar(range(len(values)), results, color='skyblue')
        ax.set_xticks(range(len(values)))
        ax.set_xticklabels([str(v) for v in values])
        ax.set_ylabel(f"{to_unit}")
        ax.set_xlabel("Input")
        ax.set_title(f"Converted Values: {from_unit} → {to_unit}")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
