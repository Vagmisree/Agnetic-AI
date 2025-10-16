import os
from google import genai
from .tools import simple_router

# ================================
# Ask Gemini (RAG-like) + Data Router
# ================================
def ask_agent(user_input: str) -> str:
    """Ask Gemini (Google GenAI) first, then append data-driven info."""
    os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "")
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Answer conversationally: {user_input}"
        ).text
    except Exception as e:
        resp = f"[Gemini unavailable: {e}]"
    data_resp = simple_router(user_input)
    return f"{resp}\n\n{data_resp}"
