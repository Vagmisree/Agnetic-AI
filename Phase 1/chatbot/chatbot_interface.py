# This file makes chatbot a Python package
import streamlit as st
from .chatbot_logic import get_bus_info

st.title("CampusRoute Chatbot")

user_input = st.text_input("Ask about your bus:")

if st.button("Submit"):
    response = get_bus_info(user_input)
    st.write(response)
