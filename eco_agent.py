import requests
import os
import json

# --- Configuration Hugging Face ---
HF_TOKEN = os.getenv("HF_TOKEN")  # ta clé se trouve dans Streamlit Secrets
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# --- Fonction principale ---
def ask_model(description: str):
    payload = {
        "inputs": f"Tu es un assistant expert en projets écologiques. Analyse et structure l'idée suivante : {description}",
        "parameters": {"temperature": 0.5, "max_new_tokens": 400}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Extraction propre du texte généré
        message = ""
        if isinstance(data, list) and "generated_text" in data[0]:
            message = data[0]["generated_text"]
        elif isinstance(data, dict) and "generated_text" in data:
            message = data["generated_text"]
        else:
            message = json.dumps(data, indent=2, ensure_ascii=False)

        return {
            "Titre": "Projet Écologique Proposé",
            "Description": message,
            "Type": "À déterminer selon le contexte",
            "Revenus": "Estimation à compléter"
        }

    except Exception as e:
        return {"error": str(e)}

# --- Simulation d’enregistrement NoCoDB ---
def save_to_nocodb(data: dict):
    print("✅ Données prêtes à être envoyées à NoCoDB :")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return {"status": "success"}
