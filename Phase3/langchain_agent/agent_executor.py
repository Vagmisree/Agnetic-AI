"""
agent_executor.py
RAG implementation:
- Loads documents (data/*.json)
- Builds TF-IDF retriever
- Retrieves top-k docs for a query and passes them as context to Gemini (if enabled)
- Falls back to local router if Gemini unavailable / API key missing
"""
import os
import json
from pathlib import Path
from typing import List
from google import genai

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .tools import simple_router

DATA_DIR = Path("data")


def _load_documents() -> List[str]:
    """Load JSON files in the data/ folder and convert them to short text docs."""
    docs = []
    for p in DATA_DIR.glob("*.json"):
        try:
            payload = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        # convert dict/list to readable text
        docs.append(f"--- {p.name} ---")
        if isinstance(payload, dict):
            for k, v in payload.items():
                docs.append(f"{k}: {json.dumps(v)}")
        elif isinstance(payload, list):
            for item in payload:
                docs.append(json.dumps(item))
        else:
            docs.append(str(payload))
    return docs


# Build TF-IDF index once
_DOCS = _load_documents()
_VECT = TfidfVectorizer(stop_words="english")
if _DOCS:
    try:
        _MAT = _VECT.fit_transform(_DOCS)
    except Exception:
        _MAT = None
else:
    _MAT = None


def _retrieve(query: str, top_k: int = 2) -> str:
    """Retrieve the top-k documents (concatenate them as context)."""
    if not _MAT:
        return ""
    qv = _VECT.transform([query])
    sims = cosine_similarity(qv, _MAT)[0]
    idxs = sims.argsort()[::-1][:top_k]
    retrieved = [ _DOCS[i] for i in idxs if sims[i] > 0.0 ]
    return "\n\n".join(retrieved)


def ask_agent(query: str, use_gemini: bool = True) -> str:
    """
    Main RAG entrypoint.
    - retrieve context
    - call Gemini (if use_gemini True and API key available)
    - append simple router fallback info
    """
    query = query.strip()
    context = _retrieve(query, top_k=3)
    # Always include small data-driven answer as fallback
    data_resp = simple_router(query)

    gemini_key = os.environ.get("GOOGLE_API_KEY", "")
    final_reply = ""

    if use_gemini and gemini_key:
        try:
            client = genai.Client(api_key=gemini_key)
            prompt = (
                "You are CampusRoute assistant. Use the provided CONTEXT to answer the user's question.\n\n"
                f"CONTEXT:\n{context}\n\n"
                f"USER QUESTION: {query}\n\n"
                "Answer concisely and mention any data from CONTEXT if relevant."
            )
            gen_resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            ).text
            final_reply = f"{gen_resp}\n\n[Data snippet]\n{data_resp}"
        except Exception as e:
            # On API error fall back
            final_reply = f"[Gemini error: {e}]\n\n{data_resp}"
    else:
        # No key or user disabled Gemini — return local RAG-like reply
        if context:
            final_reply = f"[Local retrieved context]\n{context}\n\n[Data snippet]\n{data_resp}"
        else:
            final_reply = f"{data_resp}"

    return final_reply
