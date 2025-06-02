import requests

def classify_agent(message):
    """
    Uses an LLM to classify which agent should handle the message.
    Returns: 1, 2, or 3 (agent ID)
    """
    prompt = (
        "Given the following user message, decide which agent should handle it: "
        "SQL Query Generator, Calculator, or General Assistant. "
        "Respond with only the agent name.\n\n"
        f"User message: {message}"
    )

    # Example Ollama API call (adjust URL/model as needed)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",  # e.g., "llama3" or "codestral"
            "prompt": prompt,
            "stream": False
        }
    )
    agent_name = response.json()["response"].strip().lower()

    if "sql" in agent_name:
        return 2
    elif "calculator" in agent_name:
        return 3
    else:
        return 1