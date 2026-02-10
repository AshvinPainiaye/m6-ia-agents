from dotenv import load_dotenv
load_dotenv()

import os
import json
from typing import Any, Dict, List, Literal, Optional, Tuple
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ALLOWED_DECISIONS = Literal["ASK_PATH", "READ_CODE", "EXPLAIN"]

def intention_model(user_text: str) -> Dict[str, Any]:
    model = "gpt-5-nano"
    
    prompt_system = """
    Tu es un classificateur d'intention pour un mini-agent code.

    Tu dois répondre UNIQUEMENT en JSON valide, sans texte autour.

    Types de fichiers autorisés :
    - Python (.py)
    - JavaScript (.js)
    - TypeScript (.ts)
    - CSS (.css)
    - HTML (.html)
    - JSON (.json)
    - Markdown (.md)

    Décisions possibles :

    - ASK_PATH : il manque une information (souvent le nom de fichier)
    args: {"question":"...question courte..."}

    - READ_CODE : l'utilisateur veut lire/afficher un fichier existant
    args: {"path":"nom_du_fichier.ext"}

    - EXPLAIN : l'utilisateur veut une explication d'un fichier existant
    args: {"path":"nom_du_fichier.ext"}

    - GENERATE_CODE : l'utilisateur veut générer un NOUVEAU fichier et l'écrire dans project/generated/
    args: {
        "filename":"nouveau_fichier.ext",
        "description":"ce que doit faire le nouveau fichier (1-2 phrases)",
        "source_path":"fichier_source.ext"  // optionnel: si l'utilisateur veut se baser/corriger un fichier existant
    }

    Règles :
    1) Tu dois extraire le nom du fichier depuis le message utilisateur si présent.
    2) Si un fichier est requis (path ou filename) et n'est pas clairement présent : ASK_PATH.
    3) Si l'utilisateur demande une explication (explique, comprendre, détails, comment ça marche) : EXPLAIN (avec args.path).
    4) Si l'utilisateur demande juste lire/afficher/ouvrir/voir le fichier : READ_CODE (avec args.path).
    5) Si l'utilisateur demande de "créer/générer/écrire" un nouveau fichier : GENERATE_CODE.
    - args.filename DOIT être présent (avec extension). Si absent : ASK_PATH ("Quel nom de fichier dois-je créer ?").
    - N'invente jamais de nom de fichier.
    6) Pour GENERATE_CODE, si l'utilisateur mentionne un fichier existant comme base (ex: "corrige buggy_code.py") mets-le dans args.source_path.
    7) Ne retourne JAMAIS ASK_PATH si un nom de fichier avec extension est clairement mentionné et qu'il correspond à ce qui est demandé.

    Exemples :
    User: "lis le fichier index.js"
    {"decision":"READ_CODE","args":{"path":"index.js"}}

    User: "peux-tu expliquer le style.css ?"
    {"decision":"EXPLAIN","args":{"path":"style.css"}}

    User: "crée un fichier buggy_code_fixed.py qui corrige buggy_code.py"
    {"decision":"GENERATE_CODE","args":{"filename":"buggy_code_fixed.py","description":"Corriger les exceptions possibles et sécuriser les accès (division par zéro, None, types).","source_path":"buggy_code.py"}}

    User: "crée un nouveau fichier qui corrige le code"
    {"decision":"ASK_PATH","args":{"question":"Quel nom de fichier dois-je créer ?"}}
    """
    
    response = client.responses.create(
        model=model,
        instructions=prompt_system,
        input=user_text
    )
    
    data = json.loads(response.output_text)
    return data


def explain_model(code: str) -> str:
    model = "gpt-5-nano"

    instructions = """
    Explique clairement le fichier de code fourni.
    Quel que soit le langage, structure ta réponse ainsi :
    1) Rôle global du fichier
    2) Éléments principaux (fonctions, classes, styles, sections…)
    3) Comment il est utilisé
    4) Points d'amélioration possibles
    Réponds en texte, pas en JSON.
    """

    resp = client.responses.create(
        model=model,
        instructions=instructions,
        input=f"CODE:\n{code}"
    )

    return (resp.output_text or "").strip()


def generate_code_model(description: str, source_code: Optional[str] = None) -> str:
    """Génère du code (réponse = code uniquement) à partir d'une description + contexte optionnel."""
    model = "gpt-5-nano"

    instructions = """
    Tu es un assistant développeur.

    Tu dois RENVOYER UNIQUEMENT le contenu du fichier (du code), sans markdown, sans explication, sans triple backticks.

    Contraintes :
    - Si tu génères du Python, le code doit être exécutable et inclure des docstrings ou commentaires courts.
    - Ne fais pas d'import inutile.
    - Si un contexte de code source est fourni et que la demande est de "corriger", produis une version plus robuste (checks, exceptions claires).
    - Le résultat doit être un fichier complet (pas un patch).
    """

    prompt = f"DEMANDE:\n{description}\n"
    if source_code:
        prompt += "\nCODE SOURCE (contexte):\n" + source_code

    resp = client.responses.create(
        model=model,
        instructions=instructions,
        input=prompt
    )
    return (resp.output_text or "").strip()
