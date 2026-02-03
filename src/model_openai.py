from dotenv import load_dotenv
load_dotenv()

import os
import json
from typing import Any, Dict, List, Literal, Tuple
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
    - ASK_PATH : aucun fichier n'est mentionné
    args: {"question":"Quel fichier veux-tu que je lise ?"}

    - READ_CODE : l'utilisateur veut lire/afficher un fichier
    args: {"path":"nom_du_fichier.ext"}

    - EXPLAIN : l'utilisateur veut une explication d'un fichier
    args: {"path":"nom_du_fichier.ext"}

    Règles :
    1) Tu dois extraire le nom du fichier depuis le message utilisateur si présent.
    2) Si aucun nom fichier avec extension n'est présent : ASK_PATH.
    3) Si l'utilisateur demande une explication (explique, comprendre, détails, comment ça marche) : EXPLAIN (avec args.path).
    4) Sinon si l'utilisateur demande juste lire/afficher/ouvrir/voir le fichier : READ_CODE (avec args.path).
    5) N'invente jamais de nom de fichier.
    6) Ne retourne JAMAIS ASK_PATH si un fichier est clairement mentionné.

    Exemples :
    User: "lis le fichier index.js"
    {"decision":"READ_CODE","args":{"path":"index.js"}}

    User: "peux-tu expliquer le style.css ?"
    {"decision":"EXPLAIN","args":{"path":"style.css"}}

    User: "ouvre README.md"
    {"decision":"READ_CODE","args":{"path":"README.md"}}

    User: "explique ce fichier"
    {"decision":"ASK_PATH","args":{"question":"Quel fichier veux-tu que je lise ?"}}
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