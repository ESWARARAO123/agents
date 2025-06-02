from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)

def agent1(message):
    """
    General purpose agent using Ollama with a smaller model
    """
    try:
        # Configure Ollama with explicit host and port
        llm = Ollama(
            model="mistral",
            base_url="http://localhost:11434",  # Default Ollama API endpoint
            temperature=0.7,
            timeout=30  # 30 second timeout
        )
        
        logger.info(f"Sending message to Ollama: {message}")
        response = llm.invoke(message)
        logger.info(f"Received response from Ollama: {response}")
        return response
    except Exception as e:
        error_message = str(e)
        logger.error(f"Ollama error: {error_message}")
        
        if "connection" in error_message.lower():
            return "I apologize, but I'm unable to connect to the Ollama service. Please make sure Ollama is running on your system."
        elif "memory" in error_message.lower():
            return "I apologize, but I'm currently experiencing memory constraints. Please try using the SQL Query Generator (for database queries) or Calculator (for mathematical operations) instead."
        return f"I apologize, but I encountered an error: {error_message}"
