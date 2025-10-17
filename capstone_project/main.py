import streamlit as st
from dashboard.simulation import SimulationManager
from chatbot.chatbot_logic import Chatbot
from dashboard.ui_elements import DashboardUI
import pandas as pd
import pdfplumber

st.set_page_config(page_title="🛒 Retail Shelf Simulation", layout="wide")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Page", ["Simulation", "Chatbot"])

# File upload (common)
st.sidebar.header("📂 Dataset Upload")
uploaded_file = st.sidebar.file_uploader("Upload PDF or CSV", type=["pdf", "csv"])

dataset_preview = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            dataset_preview = "\n".join([p.extract_text() for p in pdf.pages])
    else:
        df = pd.read_csv(uploaded_file)
        dataset_preview = df.head().to_string()

# Page Navigation
if page == "Simulation":
    DashboardUI.run_simulation_page(dataset_preview)
elif page == "Chatbot":
    Chatbot.run_chatbot_page(dataset_preview)
