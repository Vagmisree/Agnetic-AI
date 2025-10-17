import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
from dashboard.simulation import SimulationManager

class DashboardUI:
    @staticmethod
    def run_simulation_page(dataset_preview):
        st.title("🛒 Retail Shelf Restocking Simulation")
        rows = st.sidebar.slider("Grid Rows", 5, 20, 10)
        cols = st.sidebar.slider("Grid Columns", 5, 20, 10)
        robots_n = st.sidebar.slider("Robots", 1, 5, 2)
        start = st.sidebar.button("🚀 Start Simulation")

        shelves, robots = SimulationManager.create_simulation(10, robots_n)
        if start:
            DashboardUI.run_simulation_loop(shelves, robots, rows, cols)

    @staticmethod
    def run_simulation_loop(shelves, robots, rows, cols):
        placeholder = st.empty()
        for t in range(15):
            z = np.zeros((rows, cols))
            for shelf in shelves:
                z[shelf.x][shelf.y] = 1 if not shelf.is_low() else -1
            for robot in robots:
                z[robot.x][robot.y] = 2
            fig = go.Figure(data=go.Heatmap(z=z, colorscale=[[0,"red"],[0.5,"green"],[1,"blue"]], showscale=False))
            fig.update_layout(title=f"Step {t+1} — Shelf & Robot View", width=800, height=600)
            placeholder.plotly_chart(fig)
            time.sleep(0.3)
