"""
Modèle simulé.
But : permettre de tester la boucle sans dépendances externes.

Option : remplacer call_model() par un wrapper API (Ollama / OpenAI / HF).
"""

from typing import Tuple


def call_model(user_text: str) -> Tuple[str, float]:
    text = user_text.lower()

    # Heuristiques simples pour simuler un "score"
    if any(k in text for k in ["urgence", "suicide", "médical", "diagnostic", "banque", "virement"]):
        return ("Je ne suis pas certain de pouvoir répondre correctement à ce sujet.", 0.35)

    if any(k in text for k in ["explique", "définis", "comment", "pourquoi"]):
        return ("Voici une explication structurée et accessible du sujet demandé.", 0.78)

    if len(text) < 12:
        return ("Pouvez-vous préciser votre demande ?", 0.45)

    return ("Voici une réponse possible, à vérifier selon le contexte.", 0.62)

