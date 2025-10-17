import requests
import os
import json

# --- Configuration Hugging Face ---
HF_TOKEN = os.getenv("HF_TOKEN")  # récupère ta clé depuis Streamlit Secrets
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"  # modèle stable & gratuit

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

        # Extraction du texte de la réponse
        message = data[0]["generated_text"] if isinstance(data, list) else data.get("generated_text", "Pas de réponse.")

        return {
            "Titre": "Projet Écologique Proposé",
            "Description": message,
            "Type": "À déterminer selon le contexte",
            "Revenus": "Estimation à compléter"
        }

    except Exception as e:
        return {"error": str(e)}

# --- Simulation d'enregistrement NoCoDB ---
def save_to_nocodb(data: dict):
    print("✅ Données prêtes à être envoyées à NoCoDB :")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return {"status": "success"}
