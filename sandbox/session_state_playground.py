import streamlit as st
from streamlit import session_state as ss

st.title("🗒️ Session State Management Demo")

# Buttons

if "count" not in ss:
    ss.count = 0


def increment_count():
    ss.count += 1


def reset_count():
    ss.count = 0


col1, col2 = st.columns([1, 1])

with col1:
    st.button("Increment", on_click=increment_count)
with col2:
    st.button("Reset", on_click=reset_count)


st.write("Count = ", ss.count)

# Slider
if "celsius" not in ss:
    # set the initial default value of the slider widget
    ss["celsius"] = 50.0

ss["celsius"] = st.slider(
    "Temperature in Celsius",
    min_value=-100.0,
    max_value=100.0,
    value=ss["celsius"],
    key="celsius_slider",  # make this name different than the value itself to avoid session state dict key conflicts
)

celsius = ss["celsius"]  # Just so we can type less from now on.

# This will get the value of the slider widget
st.write(f"You selected {celsius}°C")

# Text input
if "farm_id" not in ss:
    ss["farm_id"] = ""

st.markdown("### 🔎 Please enter your **farm ID**")
ss["farm_id"] = st.text_input("#", value=ss["farm_id"])

farm_id = ss["farm_id"]  # Just so we can type less from now on.
if farm_id:
    # Call Functions
    st.write(f"Your farm ID: {farm_id}")
