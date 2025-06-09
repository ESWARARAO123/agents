from langchain_community.llms import Ollama
from memory.episodic_memory import PostgresMemory
import logging
from .config import OLLAMA_MODEL, OLLAMA_BASE_URL, OLLAMA_TEMPERATURE, OLLAMA_TIMEOUT

logger = logging.getLogger(__name__)
memory = PostgresMemory()

def agent3(message, session_id="default"):
    """
    Calculator Agent using Ollama with episodic memory and recall
    """
    try:
        if message.strip().lower() == "test":
            llm = Ollama(
                model=OLLAMA_MODEL,
                base_url=OLLAMA_BASE_URL,
                temperature=OLLAMA_TEMPERATURE,
                timeout=OLLAMA_TIMEOUT
            )
            prompt = f"Solve the following mathematical expression:\n\nExpression: {message}\n\nResult:"
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
        prompt = f"""Solve the following mathematical expression. Here is some relevant past conversation for context:
{history_text}

Only return the final numerical result without any explanation.
If the expression is not a valid mathematical calculation, respond with "Invalid calculation".

Expression: {message}

Result:"""
        response = llm.invoke(prompt)
        response = response.strip()
        try:
            result = float(response)
            agent_response = f"Result: {result}"
        except ValueError:
            if "invalid" in response.lower():
                agent_response = "I apologize, but I couldn't perform the calculation. Please provide a valid mathematical expression."
            else:
                agent_response = f"Calculation result: {response}"
        return agent_response

    except Exception as e:
        error_message = str(e)
        if "connection" in error_message.lower():
            agent_response = "I apologize, but I'm unable to connect to the Ollama service. Please make sure Ollama is running on your system."
        else:
            agent_response = f"I apologize, but I encountered an error while performing the calculation: {error_message}"
        return agent_response
