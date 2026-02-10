"""
Module volontairement buggy pour tests d'agent.
Fournit des versions robustes des fonctions avec validations et gestion des erreurs.
"""

def divide(a, b):
    """
    Divide two numbers with input validation.
    Returns the quotient as float if inputs are valid, otherwise raises an exception.

    Args:
        a (int|float): numerator
        b (int|float): denominator

    Returns:
        float: result of a / b

    Raises:
        ValueError: if a or b is None
        TypeError: if a or b is not a number
        ZeroDivisionError: if b == 0
    """
    if a is None or b is None:
        raise ValueError("Arguments 'a' and 'b' must not be None.")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments 'a' and 'b' must be numbers.")
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b


def get_user_age(user):
    """
    Retrieve user age with validation.

    Args:
        user (dict): should contain key 'age' with numeric value

    Returns:
        int|float: age value

    Raises:
        ValueError: if user is None
        TypeError: if user is not a dict or age is not numeric
        KeyError: if 'age' key is missing
    """
    if user is None:
        raise ValueError("User must not be None.")
    if not isinstance(user, dict):
        raise TypeError("User must be a dict.")
    if "age" not in user:
        raise KeyError("Missing 'age' key in user.")
    age = user["age"]
    if not isinstance(age, (int, float)):
        raise TypeError("Age must be a number.")
    return age


def print_user(user):
    """
    Safely print user information. If input is invalid, print a fallback message.

    Args:
        user (dict|None): user data with optional 'name' key
    """
    if not isinstance(user, dict):
        print("User: <invalid input>")
        return
    name = user.get("name")
    if name is None:
        print("User: <unknown>")
    else:
        print("User:", name)


def main():
    """
    Demonstration of robust usage with defensive checks.
    """
    user = None

    # Safe division
    try:
        result = divide(10, 2)
        print("Result:", result)
    except Exception as e:
        print("Error during division:", e)

    # Safe print
    print_user(user)

    # Valid user to retrieve age
    valid_user = {"name": "Alice", "age": 28}
    try:
        age = get_user_age(valid_user)
        print("Age:", age)
    except Exception as e:
        print("Error getting age:", e)

    # Missing age key
    invalid_user = {"name": "Bob"}  # missing 'age'
    try:
        print("Age (invalid):", get_user_age(invalid_user))
    except Exception as e:
        print("Expected error for invalid user:", e)

    # Division by zero handling
    try:
        _ = divide(10, 0)
    except Exception as e:
        print("Division by zero handled:", e)

    # Invalid types for division
    try:
        _ = divide("10", "2")
    except Exception as e:
        print("Type error in division:", e)

    # print_user with None
    print_user(None)


if __name__ == "__main__":
    main()