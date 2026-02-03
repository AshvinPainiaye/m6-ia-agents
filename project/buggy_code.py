"""
Module volontairement buggy pour tests d'agent.
"""

def divide(a, b):
    # BUG 1: division par zéro possible
    return a / b


def get_user_age(user):
    # BUG 2: KeyError si 'age' n'existe pas
    return user["age"]


def print_user(user):
    # BUG 3: peut planter si user est None
    print("User:", user["name"])


def main():
    user = None

    # BUG 4: division par zéro
    result = divide(10, 0)
    print("Result:", result)

    # BUG 5: accès à None
    print_user(user)

    # BUG 6: mauvais type (string au lieu de dict)
    age = get_user_age("Alice")
    print("Age:", age)


if __name__ == "__main__":
    main()
