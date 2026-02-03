"""
Mini-atelier — Boucle décisionnelle autour d’un modèle IA
Point d’entrée : exécuter ce script et tester différents prompts.

Objectif pédagogique :
- implémenter une boucle de décision (state -> decision -> action -> state)
- garder le code lisible et modulaire (actions / decisions / modèle)
"""

from dataclasses import dataclass, field
from typing import List, Literal, Tuple

from model_stub import call_model
from decisions import choose_decision
from actions import answer, rephrase, refuse, escalate


Decision = Literal["ANSWER", "REPHRASE", "REFUSE", "ESCALATE"]


@dataclass
class State:
    user_input: str
    model_output: str = ""
    confidence: float = 0.0
    decision: Decision = "REFUSE"
    history: List[Tuple[str, str]] = field(default_factory=list)  # (user, system)


def run_once(user_text: str, state: State) -> State:
    """
    Exécute un cycle de la boucle décisionnelle :
    1) appel modèle
    2) décision
    3) action
    4) update état
    """
    # 1) Appel au modèle (stub ou API)
    model_output, confidence = call_model(user_text)

    state.user_input = user_text
    state.model_output = model_output
    state.confidence = confidence

    # 2) Décision (règles explicites)
    decision: Decision = choose_decision(
        user_text=user_text,
        model_output=model_output,
        confidence=confidence,
    )
    state.decision = decision

    # 3) Action
    if decision == "ANSWER":
        final = answer(model_output)
    elif decision == "REPHRASE":
        final = rephrase(model_output)
    elif decision == "ESCALATE":
        final = escalate(user_text, model_output)
    else:
        final = refuse(user_text)

    # 4) Mise à jour historique
    state.history.append((user_text, final))
    return state


def main() -> None:
    print("=== Mini-atelier — Boucle décisionnelle IA ===")
    print("Tapez un message. 'quit' pour sortir.\n")

    state = State(user_input="")

    while True:
        user_text = input("> ").strip()
        if user_text.lower() in {"quit", "exit"}:
            break
        if not user_text:
            continue

        state = run_once(user_text, state)

        # Trace minimale (à enrichir dans le TP)
        print(f"\n[decision={state.decision} | confidence={state.confidence:.2f}]")
        print(state.history[-1][1])
        print("")

    print("Fin.\n")


if __name__ == "__main__":
    main()