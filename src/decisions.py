"""
Règles de décision explicites.
Les apprenants doivent :
- définir des seuils
- justifier les choix
- traiter quelques cas sensibles
"""

from typing import Literal


Decision = Literal["ANSWER", "REPHRASE", "REFUSE", "ESCALATE"]


SENSITIVE_KEYWORDS = {"suicide", "diagnostic", "virement", "banque", "carte bleue", "urgence"}


def choose_decision(user_text: str, model_output: str, confidence: float) -> Decision:
    text = user_text.lower()

    # 1) Cas sensibles -> escalade (règle simple, assumée)
    if any(k in text for k in SENSITIVE_KEYWORDS):
        return "ESCALATE"

    # 2) Refus si confiance trop faible
    if confidence < 0.45:
        return "REFUSE"

    # 3) Reformulation si confiance moyenne
    if 0.45 <= confidence < 0.70:
        return "REPHRASE"

    # 4) Réponse directe si confiance élevée
    return "ANSWER"