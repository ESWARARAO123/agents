from langchain_community.llms import Ollama
from memory.episodic_memory import PostgresMemory
import logging
from .config import OLLAMA_MODEL, OLLAMA_BASE_URL, OLLAMA_TEMPERATURE, OLLAMA_TIMEOUT

logger = logging.getLogger(__name__)
memory = PostgresMemory()

def agent1(message, session_id="default"):
    """
    General Conversation Agent using Ollama with episodic memory and recall
    """
    try:
        if message.strip().lower() == "test":
            llm = Ollama(
                model=OLLAMA_MODEL,
                base_url=OLLAMA_BASE_URL,
                temperature=OLLAMA_TEMPERATURE,
                timeout=OLLAMA_TIMEOUT
            )
            prompt = f"You are a friendly AI assistant. Respond to the following:\n\nUser: {message}\nAssistant:"
            response = llm.invoke(prompt)
            return response.strip()

        relevant_history = memory.get_relevant_history(session_id, message)
        history_text = ""
        if relevant_history:
            history_text = "\n".join(
                [f"{role.capitalize()}: {msg}" for role, msg, _ in reversed(relevant_history)]
            )

        llm = Ollama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=OLLAMA_TEMPERATURE,
            timeout=OLLAMA_TIMEOUT
        )
        prompt = f"""You are a friendly AI assistant. Here is some relevant past conversation for context:
{history_text}

Now, respond appropriately to the user's message, whether it's a greeting, question, or general conversation.

User: {message}
Assistant:"""
        response = llm.invoke(prompt)
        agent_response = response.strip()
        return agent_response

    except Exception as e:
        agent_response = f"Agent1 encountered an error processing your request: {str(e)}"
        return agent_response
