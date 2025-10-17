import requests
import os
import json

# --- Configuration Hugging Face ---
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# --- Fonction principale ---
def ask_model(description: str):
    prompt = f"""
    Tu es un assistant expert en projets écologiques. 
    Analyse et structure le projet suivant de façon claire :
    - Titre
    - Description
    - Type (ex : énergie, recyclage, mobilité, etc.)
    - Estimation de revenus ou bénéfices
    Projet : {description}
    """

    payload = {"inputs": prompt, "parameters": {"temperature": 0.6, "max_new_tokens": 500}}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Extraction du texte de réponse
        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            message = data[0]["generated_text"]
        else:
            message = json.dumps(data, indent=2, ensure_ascii=False)

        return {
            "Titre": "Projet Écologique Proposé",
            "Description": message,
            "Type": "À déterminer",
            "Revenus": "À estimer"
        }

    except Exception as e:
        return {"error": str(e)}

# --- Simulation d'enregistrement NoCoDB ---
def save_to_nocodb(data: dict):
    print("✅ Données prêtes à être envoyées à NoCoDB :")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return {"status": "success"}
