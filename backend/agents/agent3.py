import re
import operator

def agent3(message):
    """
    Calculator Agent
    Performs basic arithmetic calculations
    """
    # Dictionary of operators
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': operator.pow
    }
    
    # Regular expression to match numbers and operators
    pattern = r'(\d+\.?\d*)\s*([+\-*/^])\s*(\d+\.?\d*)'
    
    # Find all matches in the message
    matches = re.findall(pattern, message)
    
    if not matches:
        return "No valid calculation found. Please provide a calculation like '2 + 2' or '10 * 5'"
    
    results = []
    for match in matches:
        num1 = float(match[0])
        op = match[1]
        num2 = float(match[2])
        
        if op in operators:
            try:
                result = operators[op](num1, num2)
                results.append(f"{num1} {op} {num2} = {result}")
            except ZeroDivisionError:
                results.append(f"Error: Division by zero")
            except Exception as e:
                results.append(f"Error: {str(e)}")
    
    return "\n".join(results)
