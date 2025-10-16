from langchain.llms import VertexAI

# Initialize LLM
llm = VertexAI(
    model_name="gemini-1.5-pro",
    project="smartcampus-route",
    location="us-central1"
)

def get_bus_info(query):
    """
    Sends user query to LLM and returns a response about bus info.
    """
    prompt = f"You are CampusRoute assistant. Answer clearly: {query}"
    return llm(prompt)
