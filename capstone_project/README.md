# 🛒 Capstone Project — Autonomous Retail Shelf Restocking Simulator

### Overview
This project simulates **AI-powered retail shelf restocking** using autonomous robots.  
It integrates:
- A **Streamlit Dashboard** for visualization,
- A **Chatbot Interface** for quick queries,
- And modular AI logic for future integration (LangChain / Vertex AI).

### Key Features
- Shelf & stock simulation with random depletion and replenishment
- Robot path planning using BFS / A* algorithms
- Task batching and priority-based assignment
- Real-time dashboard visualization (Plotly / Matplotlib)
- Chatbot Q&A on robot status, stock levels, and dataset preview
- Optional integration with Google Cloud Vertex AI (Agent3)

### How to Run
```bash
pip install -r requirements.txt
streamlit run main.py
