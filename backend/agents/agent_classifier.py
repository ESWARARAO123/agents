import re

def classify_agent(message):
    """
    Classifies which agent should handle the message based on its content
    Returns: 1, 2, or 3 (agent ID)
    """
    message = message.lower()
    
    # SQL Query patterns
    sql_patterns = [
        r"select|from|where|join|table|database|sql|query",
        r"show.*from|get.*from|list.*from|display.*from",
        r"find.*in|search.*in|look.*in",
        r"how many|count|sum|average|max|min"
    ]
    
    # Calculator patterns
    calc_patterns = [
        r"calculate|compute|what is|what's",
        r"\d+\s*[\+\-\*\/\^]\s*\d+",  # Matches expressions like "5 + 3" or "10*5"
        r"add|subtract|multiply|divide|plus|minus|times",
        r"sum of|difference between|product of|quotient of"
    ]
    
    # Check for SQL patterns
    for pattern in sql_patterns:
        if re.search(pattern, message):
            return 2  # SQL Query Generator
    
    # Check for Calculator patterns
    for pattern in calc_patterns:
        if re.search(pattern, message):
            return 3  # Calculator
    
    # Default to Agent 1 if no specific patterns are matched
    return 1 