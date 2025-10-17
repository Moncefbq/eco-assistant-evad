import requests
import os
import json
import re

# --- Configuration OpenRouter ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}


# --- Fonction utilitaire pour nettoyer le texte ---
def clean_text(text: str) -> str:
    """Nettoie le texte des balises markdown et espaces inutiles."""
    text = re.sub(r"[*#`>_]+", "", text)  # retire **, ###, etc.
    text = re.sub(r"\s+", " ", text)      # espaces multiples → un seul
    return text.strip()


# --- Fonction utilitaire pour extraire un champ ---
def extract_field(text, start_pattern, end_pattern=None):
    """Extrait un champ à partir du texte entre deux motifs."""
    if end_pattern:
        pattern = rf"{start_pattern}(.*?){end_pattern}"
    else:
        pattern = rf"{start_pattern}(.*)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


# --- Génération du projet écologique via OpenRouter ---
def ask_model(description: str):
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant expert en projets écologiques. "
                    "Donne une réponse bien structurée avec ces sections claires : "
                    "Titre, Description, Type, Revenus."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Analyse ce projet écologique et fournis :\n"
                    f"1️⃣ Titre\n2️⃣ Description\n3️⃣ Type de projet\n4️⃣ Estimation des revenus.\n\n"
                    f"Projet : {description}"
                )
            }
        ],
        "temperature": 0.6,
        "max_tokens": 600
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        message = ""
        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0].get("message", {}).get("content", "")
        if not message.strip():
            return {"error": "Réponse vide du modèle."}

        # --- Nettoyage initial du texte ---
        message = message.replace("###", "").replace("**", "").strip()

        # --- Extraction des sections ---
        titre = extract_field(message, r"Titre[:\-–]*", r"Description[:\-–]*")
        desc = extract_field(message, r"Description[:\-–]*", r"Type[:\-–]*")
        type_proj = extract_field(message, r"Type[:\-–]*", r"Revenu[:\-–]*")
        revenus = extract_field(message, r"Revenu[:\-–]*")

        # --- Nettoyage final des valeurs ---
        titre = titre or "Titre non précisé"
        desc = desc or message[:300]
        type_proj = type_proj or "Non défini"
        revenus = revenus or "À estimer"

        return {
            "Titre": titre.strip(),
            "Description": desc.strip(),
            "Type": type_proj.strip(),
            "Revenus": revenus.strip()
        }

    except Exception as e:
        return {"error": str(e)}


# --- Connexion à NoCoDB ---
def save_to_nocodb(data: dict):
    """
    Envoie les données structurées vers NoCoDB via son API REST.
    """
    NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/m6zxxbaq2f869a0/records"  # ← TABLE ID exact
    NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"  # ← Ton token personnel

    headers = {
        "xc-token": NOCODB_API_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "Title": data.get("Titre"),
        "Description": data.get("Description"),
        "Type": data.get("Type"),
        "Revenues": data.get("Revenus")
    }

    try:
        response = requests.post(NOCODB_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        print("✅ Enregistrement réussi :", response.json())
        return {"status": "success", "response": response.json()}

    except Exception as e:
        print("❌ Erreur lors de l’enregistrement :", str(e))
        return {"status": "error", "message": str(e)}
