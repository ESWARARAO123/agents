import re

def agent2(message):
    """
    SQL Query Generator Agent
    Converts natural language to SQL queries
    """
    # Convert to lowercase for easier matching
    message = message.lower()
    
    # Basic patterns for common SQL operations
    select_pattern = r"show|get|list|display|select|find"
    from_pattern = r"from|in|of"
    where_pattern = r"where|with|having|that|which"
    
    # Extract table name
    table_match = re.search(rf"{from_pattern}\s+(\w+)", message)
    table_name = table_match.group(1) if table_match else "table_name"
    
    # Extract conditions
    conditions = []
    if re.search(where_pattern, message):
        # Simple condition extraction
        condition_match = re.search(rf"{where_pattern}\s+(.+)", message)
        if condition_match:
            conditions.append(condition_match.group(1))
    
    # Build the SQL query
    query = f"SELECT * FROM {table_name}"
    if conditions:
        query += f" WHERE {' AND '.join(conditions)}"
    
    return f"Generated SQL Query:\n{query}"
