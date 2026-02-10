"""
Mini-atelier — Boucle décisionnelle autour d'un modèle IA
Point d'entrée : exécuter ce script et tester différents prompts.

Objectif pédagogique :
- implémenter une boucle de décision (state -> decision -> action -> state)
- garder le code lisible et modulaire (actions / decisions / modèle)
"""

from dataclasses import dataclass, field
from typing import Any, List, Literal, Optional, Tuple, Dict

from tools import extract_path
from model_openai import intention_model
from actions import ask_path, create_file, explain, generate_code, read_code, refuse


Decision = Literal["ASK_PATH", "READ_CODE", "EXPLAIN", "REFUSE", "GENERATE_CODE", "CREATE_FILE"]


@dataclass
class State:
    user_input: str
    model_output: Dict[str, Any] = field(default_factory=dict)
    decision: Decision = "REFUSE"
    history: List[Tuple[str, str]] = field(default_factory=list)

    pending_user_request: Optional[str] = None


def run_controlled(user_text: str, state: State, max_steps: int = 3) -> State:
    """Boucle contrôlée : une entrée utilisateur peut déclencher plusieurs étapes internes."""

    original_text = user_text

    # Si on a une demande en attente et que l'utilisateur envoie juste un nom de fichier,
    # on recolle les deux pour que le routeur puisse prendre la bonne décision.
    if state.pending_user_request:
        maybe_path = extract_path(user_text)
        if maybe_path:
            user_text = f"{state.pending_user_request} {maybe_path}"
            state.pending_user_request = None

    final_answer: Optional[str] = None

    for _ in range(max_steps):
        model_output = intention_model(user_text)

        state.user_input = original_text
        state.model_output = model_output

        decision = model_output.get("decision", "")
        args = model_output.get("args", {}) or {}
        state.decision = decision  # trace

        if decision == "ASK_PATH":
            # On mémorise la demande pour pouvoir enchaîner au prochain message.
            state.pending_user_request = original_text
            final_answer = args.get("question") or ask_path()
            break

        if decision == "READ_CODE":
            chosen_path = args.get("path")
            if not chosen_path:
                final_answer = refuse("Aucun chemin de fichier fourni.")
                state.decision = "REFUSE"
                break
            try:
                final_answer = read_code(chosen_path)
            except Exception as e:
                final_answer = refuse(str(e))
                state.decision = "REFUSE"
            break

        if decision == "EXPLAIN":
            chosen_path = args.get("path")
            if not chosen_path:
                final_answer = refuse("Aucun chemin de fichier fourni.")
                state.decision = "REFUSE"
                break
            try:
                final_answer = explain(chosen_path)
            except Exception as e:
                final_answer = refuse(str(e))
                state.decision = "REFUSE"
            break

        if decision == "GENERATE_CODE":
            filename = args.get("filename")
            description = args.get("description")
            source_path = args.get("source_path")

            if not filename:
                # Demande du nom de fichier (sans inventer)
                state.pending_user_request = original_text
                final_answer = ask_path("Quel nom de fichier dois-je créer (avec extension) ?")
                state.decision = "ASK_PATH"
                break

            if not description:
                state.pending_user_request = original_text
                final_answer = ask_path("Que doit faire ce nouveau fichier ? (1-2 phrases)")
                state.decision = "ASK_PATH"
                break

            source_code = None
            if source_path:
                try:
                    source_code = read_code(source_path)
                except Exception as e:
                    final_answer = refuse(f"Impossible de lire le fichier source '{source_path}': {e}")
                    state.decision = "REFUSE"
                    break

            try:
                generated = generate_code(description=description, source_code=source_code)
                created_msg = create_file(filename=filename, content=generated)

                # Petit aperçu (évite de spammer)
                lines = generated.splitlines()
                preview = "\n".join(lines[:40])
                if len(lines) > 40:
                    preview += "\n... (aperçu tronqué)"

                final_answer = created_msg + "\n\n--- Aperçu ---\n" + preview
            except Exception as e:
                final_answer = refuse(f"Erreur génération/écriture: {e}")
                state.decision = "REFUSE"
            break

        # --- fallback ---
        final_answer = refuse("Décision invalide")
        state.decision = "REFUSE"
        break

    if final_answer is None:
        final_answer = refuse("Max steps atteint (boucle contrôlée).")

    state.history.append((original_text, final_answer))
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