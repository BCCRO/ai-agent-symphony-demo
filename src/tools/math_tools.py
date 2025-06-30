from langchain.agents import tool

@tool
def add_numbers(input_str: str) -> str:
    """
    Takes two numbers separated by a space and returns their sum.

    Args:
        input_str (str): Two numbers in the form "A B", e.g. "3 5"

    Returns:
        str: The sum A + B, or an error message if parsing fails.
    """
    try:
        a, b = map(float, input_str.split())
        return str(a + b)
    except Exception:
        return "error: please send two numbers separated by space, e.g. '3 5'"

@tool
def subtract_numbers(input_str: str) -> str:
    """
    Takes two numbers separated by a space and returns the result of A - B.

    Args:
        input_str (str): Two numbers in the form "A B", e.g. "8 3"

    Returns:
        str: The difference A − B, or an error message if parsing fails.
    """
    try:
        a, b = map(float, input_str.split())
        return str(a - b)
    except Exception:
        return "error: please send two numbers separated by space, e.g. '8 3'"