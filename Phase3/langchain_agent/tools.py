"""
tools.py
Simulated data + utility functions used by the RAG agent and Streamlit app.
"""
import random
from datetime import datetime

# Simulated Data (default values). These are duplicated in data JSON for persistence,
# but we keep an in-memory object for faster access in the app.
BUSES = {
    "Bus1": {"lat": 12.9716, "lon": 77.5946, "status": "on-route", "driver": "Ravi"},
    "Bus2": {"lat": 12.9750, "lon": 77.5900, "status": "delayed", "driver": "Anita"},
    "Bus3": {"lat": 12.9800, "lon": 77.5850, "status": "on-route", "driver": "Kumar"},
}

ROUTES = {
    "RouteA": [
        {"stop": "Main Gate", "lat": 12.9719, "lon": 77.5960, "time": "07:30"},
        {"stop": "Library",   "lat": 12.9740, "lon": 77.5930, "time": "07:45"},
        {"stop": "Hostel",    "lat": 12.9765, "lon": 77.5910, "time": "08:00"},
    ]
}

STUDENTS = {
    "S1001": {"name": "Asha",  "bus": "Bus1", "route": "RouteA", "fee_paid": True},
    "S1002": {"name": "Rohit", "bus": "Bus2", "route": "RouteA", "fee_paid": False},
}


def simulate_bus_movement():
    """Small jitter movement to show different marker positions each refresh."""
    for b in BUSES.values():
        b["lat"] += random.uniform(-0.0008, 0.0008)
        b["lon"] += random.uniform(-0.0008, 0.0008)
        b["status"] = random.choice(["on-route", "delayed", "on-route"])
        b["updated"] = str(datetime.utcnow())


def simple_router(text: str) -> str:
    """Fallback router for simple keyword answers (used if Gemini unavailable)."""
    t = text.lower()
    if "where" in t and "bus" in t:
        bid = "Bus1" if "1" in t else "Bus2" if "2" in t else "Bus3"
        bus = BUSES.get(bid, {})
        return f"{bid}: {bus.get('status','unknown')} at ({bus.get('lat',0):.4f},{bus.get('lon',0):.4f})"
    if "schedule" in t or "route" in t:
        stops = "\n".join([f"{s['stop']} — {s['time']}" for s in ROUTES["RouteA"]])
        return f"RouteA Schedule:\n{stops}"
    if "fee" in t or "paid" in t:
        s = STUDENTS.get("S1001")
        return f"{s['name']}'s fee: {'PAID' if s['fee_paid'] else 'NOT PAID'}"
    if "report" in t or "breakdown" in t or "incident" in t:
        return "Thanks — the incident has been recorded (admin notified)."
    return "Sorry, I didn't understand that. Try: 'Where is Bus1?', 'Show schedule', or 'Has S1001 paid?'"
