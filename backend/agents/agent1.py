from langchain_community.llms import Ollama

def agent1(message):
    """
    General purpose agent using Ollama with a smaller model
    """
    try:
        # Using mistral model which requires less memory
        llm = Ollama(model="mistral")
        response = llm.invoke(message)
        return response
    except Exception as e:
        error_message = str(e)
        if "memory" in error_message.lower():
            return "I apologize, but I'm currently experiencing memory constraints. Please try using the SQL Query Generator (for database queries) or Calculator (for mathematical operations) instead."
        return f"I apologize, but I encountered an error: {error_message}"
