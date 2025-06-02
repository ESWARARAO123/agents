from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)

def agent3(message):
    """
    Calculator Agent using Ollama
    Performs mathematical calculations using the llama3 model
    """
    try:
        # Using llama3 model which is good for precise calculations
        llm = Ollama(
            model="llama3",
            base_url="http://localhost:11434",
            temperature=0.1,  # Very low temperature for precise calculations
            timeout=30
        )
        
        prompt = f"""Solve the following mathematical expression. 
        Only return the final numerical result without any explanation.
        If the expression is not a valid mathematical calculation, respond with "Invalid calculation".
        
        Expression: {message}
        
        Result:"""
        
        logger.info(f"Sending calculation request to Ollama: {message}")
        response = llm.invoke(prompt)
        logger.info(f"Calculation result: {response}")
        
        # Clean up the response
        response = response.strip()
        
        # Check if the response is a valid number
        try:
            result = float(response)
            return f"Result: {result}"
        except ValueError:
            if "invalid" in response.lower():
                return "I apologize, but I couldn't perform the calculation. Please provide a valid mathematical expression."
            return f"Calculation result: {response}"
            
    except Exception as e:
        error_message = str(e)
        logger.error(f"Calculation error: {error_message}")
        
        if "connection" in error_message.lower():
            return "I apologize, but I'm unable to connect to the Ollama service. Please make sure Ollama is running on your system."
        return f"I apologize, but I encountered an error while performing the calculation: {error_message}"
