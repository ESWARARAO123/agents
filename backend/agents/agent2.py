from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)

def agent2(message):
    """
    SQL Query Generator Agent using Ollama
    Converts natural language to SQL queries using the codestral model
    """
    try:
        # Using codestral model which is good for code generation
        llm = Ollama(
            model="mistral",
            base_url="http://localhost:11434",
            temperature=0.3,  # Lower temperature for more precise SQL generation
            timeout=30
        )
        
        prompt = f"""Convert the following natural language request into a SQL query. 
        Only return the SQL query without any explanation.
        
        Request: {message}
        
        SQL Query:"""
        
        logger.info(f"Sending SQL generation request to Ollama: {message}")
        response = llm.invoke(prompt)
        logger.info(f"Generated SQL query: {response}")
        
        # Clean up the response to ensure it's just the SQL query
        response = response.strip()
        if not response.lower().startswith(('select', 'insert', 'update', 'delete', 'create')):
            return "I apologize, but I couldn't generate a valid SQL query. Please try rephrasing your request."
            
        return f"Generated SQL Query:\n{response}"
    except Exception as e:
        error_message = str(e)
        logger.error(f"SQL generation error: {error_message}")
        
        if "connection" in error_message.lower():
            return "I apologize, but I'm unable to connect to the Ollama service. Please make sure Ollama is running on your system."
        return f"I apologize, but I encountered an error while generating the SQL query: {error_message}"
