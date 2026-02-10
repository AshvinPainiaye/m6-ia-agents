"""
Mini-atelier — Boucle décisionnelle autour d'un modèle IA
Point d'entrée : exécuter ce script et tester différents prompts.

Objectif pédagogique :
- implémenter une boucle de décision (state -> decision -> action -> state)
- garder le code lisible et modulaire (actions / decisions / modèle)
"""

from dataclasses import dataclass, field
from typing import Any, List, Literal, Optional, Tuple, Dict

from model_openai import intention_model
from actions import ask_path, explain, read_code, refuse


Decision = Literal["ASK_PATH", "READ_CODE", "EXPLAIN", "REFUSE"]


@dataclass
class State:
    user_input: str
    model_output: Dict[str, Any] = field(default_factory=dict)
    decision: Decision = "REFUSE"
    history: List[Tuple[str, str]] = field(default_factory=list)

    goal: Optional[Literal["EXPLAIN"]] = None
    chosen_path: Optional[str] = None
    code_cache: Optional[str] = None
    step_count: int = 0

    awaiting_path: bool = False
    pending_goal: Optional[Literal["EXPLAIN"]] = None


def run_controlled(user_text: str, state: State, max_steps: int = 3) -> State:
    """
    Boucle contrôlée: pour UNE entrée utilisateur, l'agent peut faire plusieurs étapes internes.
    Stop conditions:
    - ASK_PATH => on a besoin de l'utilisateur (stop)
    - REFUSE / erreur => stop
    - EXPLAIN terminé => stop
    - max_steps atteint => stop
    """

    # Initialisation
    state.user_input = user_text
    state.step_count = 0
    state.goal = None
    state.chosen_path = None
    state.code_cache = None

    final_answer: Optional[str] = None

    while state.step_count < max_steps:
        state.step_count += 1

        # 1) Si on est en "phase interne" (on a un goal + path + code),
        # on peut enchaîner sans rappeler le modèle d'intention.
        if state.goal == "EXPLAIN" and state.chosen_path and state.code_cache is not None:
            final_answer = explain(state.chosen_path)
            state.decision = "EXPLAIN"
            break

        # Si on attend un chemin et que l'utilisateur répond juste un path, on enchaîne automatiquement vers l'objectif pending.
        if state.awaiting_path and user_text:
            state.awaiting_path = False
            state.chosen_path = user_text

            if state.pending_goal == "EXPLAIN":
                state.goal = "EXPLAIN"
                state.pending_goal = None

                # lire une fois
                try:
                    state.code_cache = read_code(state.chosen_path)
                except Exception as e:
                    final_answer = refuse(f"Erreur lecture fichier: {e}")
                    state.decision = "REFUSE"
                    state.history.append((user_text, final_answer))
                    return state

                continue

        # 2) Sinon, on appelle le modèle d'intention sur le texte utilisateur
        model_output = intention_model(user_text)
        state.model_output = model_output

        decision = model_output.get("decision", "")
        args = model_output.get("args", {}) or {}
        state.decision = decision  # trace

        # 3) Actions + mise à jour state
        if decision == "ASK_PATH":
            state.awaiting_path = True
            state.pending_goal = "EXPLAIN"

            final_answer = (args.get("question") or ask_path())
            break

        elif decision == "READ_CODE":
            path = args.get("path")
            if not path:
                final_answer = refuse("Aucun chemin de fichier fourni.")
                state.decision = "REFUSE"
                break

            state.chosen_path = path
            try:
                state.code_cache = read_code(path)
                final_answer = state.code_cache
            except Exception as e:
                final_answer = refuse(f"Erreur lecture fichier: {e}")
                state.decision = "REFUSE"
                break
            break

        elif decision == "EXPLAIN":
            path = args.get("path")
            if not path:
                final_answer = refuse("Aucun chemin de fichier fourni.")
                state.decision = "REFUSE"
                break

            state.goal = "EXPLAIN"
            state.chosen_path = path

            # Étape 1 interne: lire le code si pas déjà fait
            if state.code_cache is None:
                try:
                    state.code_cache = read_code(path)
                except Exception as e:
                    final_answer = refuse(f"Erreur lecture fichier: {e}")
                    state.decision = "REFUSE"
                    break
            continue

        else:
            final_answer = refuse("Décision invalide")
            state.decision = "REFUSE"
            break

    # Fallback si max_steps atteint sans réponse
    if final_answer is None:
        final_answer = refuse("Max steps atteint (boucle contrôlée).")
        state.decision = "REFUSE"

    state.history.append((user_text, final_answer))
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

        state = run_controlled(user_text, state, max_steps=3)

        # Trace minimale (à enrichir dans le TP)
        print(f"\n[decision={state.decision}]")
        print(state.history[-1][1])
        print("")

    print("Fin.\n")


if __name__ == "__main__":
    main()