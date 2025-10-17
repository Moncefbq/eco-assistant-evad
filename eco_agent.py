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


# --- Fonction utilitaire pour extraire un champ ---
def extract_field(text, pattern):
    """
    Extrait une section spécifique du texte à l’aide d’une expression régulière.
    """
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


# --- Génération du projet écologique via OpenRouter ---
def ask_model(description: str):
    """
    Interroge le modèle OpenRouter pour générer un projet écologique structuré.
    """
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant expert en projets écologiques. "
                    "Fournis des sections claires et séparées : "
                    "Titre, Description, Type, Revenus."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Analyse ce projet écologique et fournis les sections suivantes :\n"
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

        # ✅ Extraction du message du modèle
        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0].get("message", {}).get("content", "")
        else:
            message = json.dumps(result, indent=2, ensure_ascii=False)

        if not message.strip():
            message = "Le modèle n’a pas généré de texte."

        # 🧩 Extraction des différentes parties du texte
        titre = extract_field(message, r"(?:Titre[:*]*\s*)(.*?)(?:\n|$)")
        desc = extract_field(message, r"(?:Description[:*]*\s*)(.*?)(?:\n\*\*|$)")
        type_proj = extract_field(message, r"(?:Type.*?:\s*)(.*?)(?:\n\*\*|$)")
        revenus = extract_field(message, r"(?:Revenus[:*]*\s*)(.*?)(?:\n|$)")

        # ✅ Valeurs par défaut si vides
        titre = titre or "Titre non précisé"
        desc = desc or message.strip()[:400]
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
