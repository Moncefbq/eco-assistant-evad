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

# --- Fonction principale ---
def ask_model(description: str):
    data = {
        "model": "mistralai/mistral-7b-instruct",  # modèle rapide et gratuit
        "messages": [
            {"role": "system", "content": "Tu es un assistant expert en projets écologiques."},
            {"role": "user", "content": f"Analyse ce projet et rédige : un titre, une description, un type, et une estimation des revenus.\nProjet : {description}"}
        ],
        "temperature": 0.6,
        "max_tokens": 400
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        message = result["choices"][0]["message"]["content"]
        return {
            "Titre": "Projet Écologique Proposé",
            "Description": message,
            "Type": "À déterminer",
            "Revenus": "À estimer"
        }
    except Exception as e:
        return {"error": str(e)}

# --- Simulation NoCoDB ---
def save_to_nocodb(data: dict):
    print("✅ Données prêtes à être envoyées à NoCoDB :")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return {"status": "success"}
