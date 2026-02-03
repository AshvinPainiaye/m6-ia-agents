"""
Actions déclenchées par la décision.
But : rendre les comportements lisibles et testables.
"""

from tools import read_file
from model_openai import explain_model

def ask_path() -> str:
    return "Quel est le chemin du fichier que vous souhaitez que j'analyse ?"


def refuse(reason: str) -> str:
    return f"Je ne peux pas traiter votre demande pour la raison suivante : {reason}"


def explain(path: str) -> str:
    code = read_code(path)
    return explain_model(code)

def read_code(path: str) -> str:
    return read_file(path)