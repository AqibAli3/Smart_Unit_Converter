import streamlit as st
import requests
from datetime import datetime, timedelta

# Set page title and favicon with the desired title and emoji
st.set_page_config(page_title="Smart Unit Converter by Aqib Ali", page_icon="🧮")

# Add custom CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css?family=Raleway:300,400,600');

    body {
        font-family: 'Raleway', sans-serif;
        background-color: #f0f2f6;
        padding: 20px;
    }
    .stApp {
        background-color: #fff;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }
    h1 {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 20px;
    }
    # h1::before {
    #     content: "🔄";
    #     font-size: 2.5rem;
    #     margin-right: 10px;
    # }
    # h1::after {
    #     content: "🔄";
    #     font-size: 2.5rem;
    #     margin-left: 10px;
    # }
    .stTextInput label {
        font-size: 1.1rem;
        color: #333;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-top: 10px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stSelectbox label {
        font-size: 1.1rem;
        color: #333;
    }
    .stNumberInput label {
        font-size: 1.1rem;
        color: #333;
    }
    .swap-button {
        background-color: #007BFF;
        color: white;
        font-size: 16px;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-top: 10px;
    }
    .swap-button:hover {
        background-color: #0056b3;
    }
    .warning {
        color: red;
        font-weight: bold;
    }
    .result {
        color: #4CAF50;
        font-weight: bold;
        font-size: 1.5rem;
        margin-top: 10px;
        font-family: 'Times New Roman', Times, serif !important;
        border: 2px solid #4CAF50;
        padding: 10px;
        border-radius: 4px;
        background-color: #e8f5e9;
        position: relative;
        text-align: center;
    }
    .contact-details {
        font-size: 1.2rem;
        margin-top: 30px;
        text-align: center;
    }
    .contact-details a {
        margin: 0 10px;
        text-decoration: none;
    }
    .contact-details a img {
        width: 40px;
        height: 40px;
        transition: transform 0.3s ease;
    }
    .contact-details a:hover img {
        transform: scale(1.1);
    }
    .modal {
        display: none; 
        position: fixed; 
        z-index: 1; 
        left: 0;
        top: 0;
        width: 100%; 
        height: 100%; 
        overflow: auto; 
        background-color: rgba(0, 0, 0, 0.4);
    }
    .modal-content {
        background-color: #fefefe;
        margin: 15% auto; 
        padding: 20px;
        border: 1px solid #888;
        width: 80%; 
        text-align: center;
        border-radius: 10px;
    }
    .close {
        color: #aaa;
        float: right;
        font-size: 28px;
        font-weight: bold;
    }
    .close:hover,
    .close:focus {
        color: black;
        text-decoration: none;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# JavaScript for the modal
st.markdown(
    """
    <script>
    function showModal(result) {
        document.getElementById("modal-result").innerText = result;
        document.getElementById("myModal").style.display = "block";
    }
    function closeModal() {
        document.getElementById("myModal").style.display = "none";
    }
    </script>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.markdown('<div class="sidebar-header">More Converters Coming Soon!</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="coming-soon">🌟 Currency Converter 🌟</div>', unsafe_allow_html=True)

# Title and description with an emoji in the title
st.title("🧮 Smart Unit Converter by Aqib Ali")
st.write("Convert units easily with my Smart converter. 🌐📐🧮")

# Dropdown for unit types
unit_types = ["Length", "Weight", "Volume", "Area", "Data Transfer Rate", "Digital Storage", "Temperature"]
unit_type = st.selectbox("Select Unit Type", unit_types)

# Conversion logic
def convert_units(value, from_unit, to_unit, unit_type):
    conversions = {
        "Length": {"Meter": 1, "Kilometer": 0.001, "Centimeter": 100},
        "Weight": {"Kilogram": 1, "Gram": 1000, "Pound": 2.20462},
        "Volume": {"Liter": 1, "Milliliter": 1000, "Cubic Meter": 0.001},
        "Area": {"Square Meter": 1, "Square Kilometer": 0.000001, "Square Centimeter": 10000},
        "Data Transfer Rate": {"Bits per second": 1, "Kilobits per second": 0.001, "Megabits per second": 0.000001},
        "Digital Storage": {"Byte": 1, "Kilobyte": 0.001, "Megabyte": 0.000001},
        "Temperature": {"Celsius": lambda x: x, "Fahrenheit": lambda x: (x * 9/5) + 32}
    }
    if unit_type == "Temperature":
        from_func = conversions[unit_type][from_unit]
        to_func = conversions[unit_type][to_unit]
        if from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        elif from_unit == "Celsius" and to_unit == "Fahrenheit":
            return to_func(from_func(value))
        return value  # Both units are the same
    return value * (conversions[unit_type][to_unit] / conversions[unit_type][from_unit])

# Unit selection
units = {
    "Length": ["Meter", "Kilometer", "Centimeter"],
    "Weight": ["Kilogram", "Gram", "Pound"],
    "Volume": ["Liter", "Milliliter", "Cubic Meter"],
    "Area": ["Square Meter", "Square Kilometer", "Square Centimeter"],
    "Data Transfer Rate": ["Bits per second", "Kilobits per second", "Megabits per second"],
    "Digital Storage": ["Byte", "Kilobyte", "Megabyte"],
    "Temperature": ["Celsius", "Fahrenheit"]
}

# Initialize session state values for from_unit and to_unit if not already set
if 'from_unit' not in st.session_state:
    st.session_state.from_unit = units[unit_type][0]
if 'to_unit' not in st.session_state:
    st.session_state.to_unit = units[unit_type][1]

def swap_units():
    st.session_state.from_unit, st.session_state.to_unit = st.session_state.to_unit, st.session_state.from_unit

# Remove default index values; let session state dictate the selections
from_unit = st.selectbox("From Unit", units[unit_type], key="from_unit")
to_unit = st.selectbox("To Unit", [unit for unit in units[unit_type] if unit != st.session_state.from_unit], key="to_unit")

st.button("Swap Units", on_click=swap_units, key="swap_units")

# User input
value = st.number_input("Enter Value", value=1.0)

# Conversion button
if st.button("Convert"):
    if st.session_state.from_unit == st.session_state.to_unit:
        st.write('<p class="warning">From Unit and To Unit cannot be the same. Please select different units.</p>', unsafe_allow_html=True)
    else:
        result = convert_units(value, st.session_state.from_unit, st.session_state.to_unit, unit_type)
        st.write(f'<p class="result">{value} {st.session_state.from_unit} is equal to {result} {st.session_state.to_unit}.</p>', unsafe_allow_html=True)
        st.markdown(
            f'<script>showModal("{value} {st.session_state.from_unit} is equal to {result} {st.session_state.to_unit}");</script>',
            unsafe_allow_html=True
        )

# Modal HTML
st.markdown(
    """
    <div id="myModal" class="modal">
      <div class="modal-content">
        <span class="close" onclick="closeModal()">&times;</span>
        <p id="modal-result"></p>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Contact details
st.markdown(
    """
    <div class="contact-details">
        <p>Contact Me:</p>
        <a href="https://www.linkedin.com/in/syed-aqib-ali/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn">
        </a>
        <a href="https://github.com/AqibAli3" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub">
        </a>
        <a href="https://wa.me/+923158796106" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp">
        </a>
        <a href="mailto:shaali254@gmail.com">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Mail_%28iOS%29.svg" alt="Email">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
