import requests
import json
import os  # ✅ pour lire la clé depuis les variables d’environnement (sécurisé)

# --- Configuration Hugging Face ---
HF_TOKEN = os.getenv("HF_TOKEN")  # 🔒 ta clé stockée dans Streamlit Cloud (ou localement)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# --- Fonction principale ---
def ask_model(description: str):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": f"Tu es un assistant expert en projets écologiques. Analyse ce projet et rédige une proposition claire et détaillée : {description}",
        "parameters": {"temperature": 0.6, "max_new_tokens": 400},
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # --- Extraction du texte de sortie ---
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            message = result[0]["generated_text"]
        else:
            message = json.dumps(result, indent=2, ensure_ascii=False)

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
