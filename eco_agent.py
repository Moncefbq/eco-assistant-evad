import requests
import os
import re
import difflib

# --- Configuration OpenRouter ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}


# --- Nettoyage du texte ---
def clean_text(text: str) -> str:
    """Nettoie le texte et supprime les répétitions, symboles et débuts inutiles."""
    if not text:
        return ""

    # Nettoyage général : suppression des symboles, balises et emojis
    text = re.sub(r"[*#`>_]+", "", text)
    text = re.sub(r"[0-9️⃣🧠💡⚡🌍🔹🔸•]+", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = text.strip().strip('"').strip("'")

    # Supprimer les préfixes ou débuts erronés (comme "s:", "de projet:", "projet:", etc.)
    text = re.sub(
        r"^(s\s*[:\-–]\s*|de\s*projet\s*[:\-–]\s*|projet\s*[:\-–]\s*|le\s*projet\s*[:\-–]\s*)",
        "",
        text.strip(),
        flags=re.IGNORECASE,
    )

    # Supprimer les doublons de phrases similaires
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    unique_sentences = []
    for s in sentences:
        if not any(
            difflib.SequenceMatcher(None, s.lower(), u.lower()).ratio() > 0.8
            for u in unique_sentences
        ):
            unique_sentences.append(s)
    text = " ".join(unique_sentences)

    # Nettoyage final
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"[\s.]+$", "", text)

    return text.strip()


# --- Extraction de sections ---
def extract_field(text, start, end=None):
    """Extrait une section spécifique dans le texte du modèle."""
    if end:
        pattern = rf"{start}(.*?){end}"
    else:
        pattern = rf"{start}(.*)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


# --- Appel du modèle ---
def ask_model(description: str):
    """
    Analyse un projet écologique et retourne un dictionnaire propre (Titre, Description, Type, Revenus)
    avec nettoyage automatique et sans redondance.
    """
    data = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant expert en projets écologiques. "
                    "Analyse le projet et retourne quatre sections claires : "
                    "Titre, Description, Type, Revenus. "
                    "Le type doit être précis (ex : énergie renouvelable, agriculture durable, gestion de l’eau, etc.). "
                    "Ne répète pas les phrases entre les sections. Aucun emoji ni Markdown."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Analyse ce projet écologique et fournis :\n"
                    f"1. Titre\n2. Description\n3. Type\n4. Revenus\n\n"
                    f"Projet : {description}"
                ),
            },
        ],
        "temperature": 0.4,
        "max_tokens": 700,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()

        message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not message.strip():
            return {"error": "Réponse vide du modèle."}

        # Extraction des sections
        titre = extract_field(message, r"Titre[:\-–]*", r"Description[:\-–]*")
        desc = extract_field(message, r"Description[:\-–]*", r"Type[:\-–]*")
        type_proj = extract_field(message, r"Type[:\-–]*", r"(Revenu|Estimation)[:\-–]*")
        revenus = extract_field(message, r"Revenu[:\-–]*")

        return {
            "Titre": clean_text(titre or "Titre non précisé"),
            "Description": clean_text(desc or "Description non précisée"),
            "Type": clean_text(type_proj or "Type non précisé"),
            "Revenus": clean_text(revenus or "À estimer"),
        }

    except Exception as e:
        return {"error": str(e)}


# --- Envoi vers NoCoDB ---
def save_to_nocodb(data: dict):
    """
    Envoie les données nettoyées vers la table NoCoDB configurée.
    """
    NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/m6zxxbaq2f869a0/records"
    NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"

    headers = {
        "xc-token": NOCODB_API_TOKEN,
        "Content-Type": "application/json",
    }

    payload = {
        "Title": data.get("Titre"),
        "Description": data.get("Description"),
        "Type": data.get("Type"),
        "Revenues": data.get("Revenus"),
    }

    try:
        response = requests.post(NOCODB_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return {"status": "success", "response": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
