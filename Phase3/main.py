import os
from pathlib import Path
import streamlit as st
from streamlit_folium import st_folium
import folium

# make sure package path is found when running locally
from langchain_agent.agent_executor import ask_agent
from langchain_agent.tools import simulate_bus_movement, BUSES, ROUTES, STUDENTS

st.set_page_config(page_title="CampusRoute Phase2 (RAG)", layout="wide")
st.title("🚍 CampusRoute – Phase 2 (RAG Agent)")

# Sidebar
st.sidebar.header("Settings")
use_gemini = st.sidebar.checkbox("Use Gemini (requires GOOGLE_API_KEY)", value=False)
if use_gemini:
    st.sidebar.info("Make sure GOOGLE_API_KEY is set in the environment.")
role = st.sidebar.radio("Login as", ["Student / Parent", "Administrator"])

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Chatbot (RAG Agent)")
    question = st.text_input("Ask about bus, schedule, incidents, or payments:")
    if st.button("Ask"):
        reply = ask_agent(question, use_gemini=use_gemini)
        st.markdown("**Agent reply:**")
        st.write(reply)
        st.session_state.setdefault("history", []).append({"q": question, "a": reply})

    st.markdown("### Recent Questions")
    for h in reversed(st.session_state.get("history", [])[-8:]):
        st.markdown(f"**Q:** {h['q']}")
        st.markdown(f"**A:** {h['a']}")

with col2:
    st.header("Live Bus Map (simulated)")
    simulate_bus_movement()
    m = folium.Map(location=[12.973, 77.594], zoom_start=13)
    for bus_id, info in BUSES.items():
        folium.Marker(
            [info["lat"], info["lon"]],
            tooltip=f"{bus_id} ({info.get('status','unknown')})",
            popup=f"{bus_id} — {info.get('driver','')}"
        ).add_to(m)
    st_folium(m, width=350, height=400)

if role == "Administrator":
    st.markdown("---")
    st.subheader("Admin Dashboard")
    b = st.selectbox("Select Bus", list(BUSES.keys()))
    if st.button("Mark as Delayed"):
        BUSES[b]["status"] = "delayed"
        st.success(f"{b} marked delayed.")
    st.markdown("**Incidents**")
    import json
    incidents_path = Path("data/incidents.json")
    if incidents_path.exists():
        st.json(json.loads(incidents_path.read_text()))
    else:
        st.write("No incidents file found.")
