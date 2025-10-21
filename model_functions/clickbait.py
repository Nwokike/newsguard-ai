"""
Clickbait detection stub.
Developer should add model and return a formatted string.
Provide function: is_clickbait(headline_text) -> str ("Yes" or "No")
"""

def is_clickbait(headline_text: str) -> str:
    if not headline_text.strip():
        return "No headline provided"
    return "Coming Soon"
