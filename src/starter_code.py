"""
Mini-atelier — Boucle décisionnelle autour d’un modèle IA
Point d’entrée : exécuter ce script et tester différents prompts.

Objectif pédagogique :
- implémenter une boucle de décision (state -> decision -> action -> state)
- garder le code lisible et modulaire (actions / decisions / modèle)
"""

from dataclasses import dataclass, field
from typing import List, Literal, Tuple

from model_openai import intention_model
from actions import ask_path, explain, read_code, refuse


Decision = Literal["ASK_PATH", "READ_CODE", "EXPLAIN", "REFUSE"]


@dataclass
class State:
    user_input: str
    model_output: str = ""
    decision: Decision = "REFUSE"
    history: List[Tuple[str, str]] = field(default_factory=list)  # (user, system)


def run_once(user_text: str, state: State) -> State:
    # 1) Appel au modèle
    model_output = intention_model(user_text)
    
    state.user_input = user_text
    state.model_output = model_output
    
    # 2) Décision
    decision = model_output.get("decision", "")
    args = model_output.get("args", {}) or {}
    state.decision = decision
    print(decision, args)
    
    # 3) Action
    if decision == "ASK_PATH":
        final = args.get("question") or ask_path()

    elif decision == "READ_CODE":
        chosen_path = args.get("path")
        final = read_code(chosen_path)
    elif decision == "EXPLAIN":
        chosen_path = args.get("path")
        final = explain(chosen_path)
    else:
        final = refuse("Décision invalide")

    state.history.append((user_text, final))
    return state

def main() -> None:
    print("=== Mini-atelier — Boucle décisionnelle IA ===")
    print("Commande: explique chemin.py. 'quit' pour sortir.\n")

    state = State(user_input="")

    while True:
        user_text = input("> ").strip()
        if user_text.lower() in {"quit", "exit"}:
            break
        if not user_text:
            continue

        state = run_once(user_text, state)

        # Trace minimale (à enrichir dans le TP)
        print(f"\n[decision={state.decision}]")
        print(state.history[-1][1])
        print("")

    print("Fin.\n")


if __name__ == "__main__":
    main()