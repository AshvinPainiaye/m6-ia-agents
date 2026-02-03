"""
Petit module de démonstration pour un agent de code.
"""

def greet(name: str) -> str:
    """
    Retourne un message de salutation.
    """
    return f"Bonjour {name} !"


def is_even(number: int) -> bool:
    """
    Vérifie si un nombre est pair.
    """
    return number % 2 == 0


def main() -> None:
    """
    Point d'entrée du script.
    """
    user_name = "Alice"
    value = 4

    print(greet(user_name))

    if is_even(value):
        print(f"{value} est un nombre pair.")
    else:
        print(f"{value} est un nombre impair.")


if __name__ == "__main__":
    main()
