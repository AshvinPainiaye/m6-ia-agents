import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "project")
)

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".css",
    ".html",
    ".json",
    ".md",
}

def safe_path(path: str) -> str:
    full = os.path.abspath(os.path.join(BASE_DIR, path))

    if not full.startswith(BASE_DIR):
        raise ValueError("Accès interdit : hors du dossier project")

    ext = os.path.splitext(full)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Type de fichier non autorisé ({ext}). "
            f"Extensions autorisées : {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    return full


def read_file(path: str, max_chars: int = 12000) -> str:
    full = safe_path(path)
    with open(full, "r", encoding="utf-8") as f:
        return f.read()[:max_chars]

PATH_RE = re.compile(
    r"([A-Za-z0-9_\-./\\]+\.(py|js|ts|css|html|json|md))",
    re.IGNORECASE
)
def extract_path(text: str) -> str | None:
    m = PATH_RE.search(text)
    return m.group(1) if m else None