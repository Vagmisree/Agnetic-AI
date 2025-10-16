import os
import json
import random
from datetime import datetime
import streamlit as st
from streamlit_folium import st_folium
import folium

from langchain_agent.agent_executor import ask_agent
from langchain_agent.tools import simulate_bus_movement, BUSES, ROUTES, STUDENTS

# ================================
# Streamlit App
# ================================
st.set_page_config(page_title="CampusRoute Phase2", layout="wide")
st.title("🚍 CampusRoute – Phase 2 Demo")

role = st.sidebar.radio("Login as", ["Student / Parent", "Administrator"])
col1, col2 = st.columns([2,1])

with col1:
    st.header("Chatbot")
    question = st.text_input("Ask about bus, schedule, or payment:")
    if st.button("Ask"):
        reply = ask_agent(question)
        st.write(reply)
        st.session_state.setdefault("history", []).append({"q": question, "a": reply, "t": str(datetime.utcnow())})
    st.markdown("### Recent Questions")
    for h in reversed(st.session_state.get("history", [])[-5:]):
        st.markdown(f"*Q:* {h['q']}")
        st.markdown(f"*A:* {h['a']}")

with col2:
    st.header("Live Bus Map")
    simulate_bus_movement()
    m = folium.Map(location=[12.973, 77.594], zoom_start=13)
    for b, info in BUSES.items():
        folium.Marker([info["lat"], info["lon"]],
                      tooltip=f"{b} ({info['status']})",
                      popup=f"{b}").add_to(m)
    st_folium(m, width=350, height=400)

if role == "Administrator":
    st.markdown("---")
    st.subheader("Admin Dashboard")
    b = st.selectbox("Select Bus", list(BUSES.keys()))
    if st.button("Mark as Delayed"):
        BUSES[b]["status"] = "delayed"
        st.success(f"{b} marked delayed.")
