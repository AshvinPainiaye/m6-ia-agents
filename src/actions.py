"""
Actions déclenchées par la décision.
But : rendre les comportements lisibles et testables.
"""

from typing import Optional


def answer(model_output: str) -> str:
    return model_output


def rephrase(model_output: str) -> str:
    # Reformulation "light" volontairement simple (pas d’appel IA)
    return f"(Reformulation) {model_output}".strip()


def refuse(user_text: str) -> str:
    return (
        "Je préfère ne pas répondre en l’état : il manque des éléments ou la confiance est trop faible.\n"
        "Pouvez-vous préciser (contexte, objectif, contraintes) ?"
    )


def escalate(user_text: str, model_output: str, contact: Optional[str] = None) -> str:
    # Dans un vrai système : ticket, notification, routage…
    target = contact or "un référent humain"
    return (
        f"Je propose d’escalader ce cas vers {target}.\n"
        "Raison : sujet sensible / fort impact / ambiguïté.\n"
        f"Contexte reçu : {user_text}\n"
        f"Sortie modèle : {model_output}"
    )