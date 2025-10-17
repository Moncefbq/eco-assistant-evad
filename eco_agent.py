import requests
import os
import json

# --- Configuration OpenRouter ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def ask_model(description: str):
    """
    Interroge le modèle OpenRouter pour générer un projet écologique structuré.
    """
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "Tu es un assistant expert en projets écologiques. Fournis une réponse claire et bien structurée."},
            {"role": "user", "content": f"Analyse ce projet écologique et fournis :\n1️⃣ Un titre\n2️⃣ Une courte description\n3️⃣ Le type de projet\n4️⃣ Une estimation des revenus.\n\nProjet : {description}"}
        ],
        "temperature": 0.6,
        "max_tokens": 600
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # ✅ Extraction du contenu du modèle
        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0].get("message", {}).get("content", "")
        else:
            message = json.dumps(result, indent=2, ensure_ascii=False)

        if not message.strip():
            message = "Le modèle n’a pas généré de description. Essaie un autre texte."

        return {
            "Titre": "Projet Écologique Proposé",
            "Description": message.strip(),
            "Type": "À déterminer",
            "Revenus": "À estimer"
        }

    except Exception as e:
        return {"error": str(e)}


# --- Connexion à NoCoDB ---
def save_to_nocodb(data: dict):
    # ✅ Configuration
    NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/m6zxxbaq2f869a0/records"  # ← remplace par ton TABLE ID exact
    NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"  # ← ton token personnel

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
