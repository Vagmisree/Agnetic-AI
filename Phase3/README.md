# CampusRoute — Phase 2 (with RAG Agent)

Phase 2 extends CampusRoute by adding a Retrieval-Augmented-Generation (RAG) agent:
- Uses local document retrieval (TF-IDF) over the `data/` files.
- Fetches top context and sends it to Google Gemini (via `google-genai`) for generation.
- Streamlit UI for Student/Parent and Admin.
- Live (simulated) bus map and admin controls.

## Quick start

1. Create & activate virtualenv (recommended)
2. Install dependencies:
```bash
pip install -r requirements.txt
