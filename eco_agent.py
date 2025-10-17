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

def save_to_nocodb(data: dict):
    print("✅ Données prêtes à être envoyées à NoCoDB :")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return {"status": "success"}
