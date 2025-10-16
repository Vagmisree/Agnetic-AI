# Optional memory module to store conversation history
conversation_history = []

def add_message(role: str, content: str):
    conversation_history.append({"role": role, "content": content})

def get_history():
    return conversation_history
