"""
Actions déclenchées par la décision.
But : rendre les comportements lisibles et testables.
"""

from tools import read_file, write_generated_file
from model_openai import explain_model, generate_code_model

def ask_path() -> str:
    return "Quel est le chemin du fichier que vous souhaitez que j'analyse ?"


def refuse(reason: str) -> str:
    return f"Je ne peux pas traiter votre demande pour la raison suivante : {reason}"


def explain(path: str) -> str:
    code = read_code(path)
    return explain_model(code)

def read_code(path: str) -> str:
    return read_file(path)

def generate_code(description: str, source_code: str | None = None) -> str:
    return generate_code_model(description=description, source_code=source_code)

def create_file(filename: str, content: str) -> str:
    rel = write_generated_file(filename=filename, content=content, overwrite=False)
    return f"Fichier créé : {rel}"
