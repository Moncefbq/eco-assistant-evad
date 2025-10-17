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


# --- Nettoyage général du texte ---
def clean_text(text: str) -> str:
    """Supprime le markdown, les numéros et espaces inutiles."""
    text = re.sub(r"[#*`>_]+", "", text)  # markdown
    text = re.sub(r"[0-9️⃣]+", "", text)  # chiffres, emojis numérotés
    text = re.sub(r"\s+", " ", text)      # espaces multiples
    text = re.sub(r"[\[\](){}]", "", text)
    return text.strip()


# --- Extraction robuste des champs ---
def extract_field(text, label):
    """
    Extrait la section commençant par 'label' et se terminant avant la prochaine section connue.
    """
    # Sections possibles
    labels = ["Titre", "Description", "Type", "Revenu", "Estimation"]
    labels_regex = "|".join([l for l in labels if l.lower() != label.lower()])

    pattern = rf"{label}.*?:\s*(.*?)(?=(?:{labels_regex}).*?:|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


# --- Fonction principale : génération de projet ---
def ask_model(description: str):
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant expert en projets écologiques. "
                    "Fournis un texte clair et structuré avec les sections suivantes : "
                    "Titre, Description, Type, Revenus."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Analyse ce projet écologique et donne les sections suivantes :\n"
                    f"1️⃣ Titre\n2️⃣ Description\n3️⃣ Type de projet\n4️⃣ Estimation des revenus.\n\n"
                    f"Projet : {description}"
                )
            }
        ],
        "temperature": 0.6,
        "max_tokens": 700
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0].get("message", {}).get("content", "")
        else:
            return {"error": "Aucune réponse du modèle."}

        # Nettoyage global
        message = clean_text(message)

        # Extraction par section
        titre = extract_field(message, "Titre")
        desc = extract_field(message, "Description")
        type_proj = extract_field(message, "Type")
        revenus = extract_field(message, "Revenu")

        # Valeurs de secours si certaines sont vides
        titre = titre or "Titre non précisé"
        desc = desc or message[:400]
        type_proj = type_proj or "Non défini"
        revenus = revenus or "À estimer"

        return {
            "Titre": titre,
            "Description": desc,
            "Type": type_proj,
            "Revenus": revenus
        }

    except Exception as e:
        return {"error": str(e)}


# --- Connexion à NoCoDB ---
def save_to_nocodb(data: dict):
    """Envoie les données structurées vers NoCoDB via son API REST."""
    NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/m6zxxbaq2f869a0/records"
    NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"

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

