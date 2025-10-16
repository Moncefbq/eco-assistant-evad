import requests
import json

# --- Configuration DeepInfra ---
DEEPINFRA_KEY = "8yHS8APUhQuMouXKQS89EIBVKPl87Igq"  # 🔑 colle ta clé ici
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

# --- Fonction principale ---
def ask_model(description: str):
    headers = {"Authorization": f"Bearer {DEEPINFRA_KEY}"}
    data = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",  # modèle rapide et gratuit
        "messages": [
            {"role": "system", "content": "Tu es un assistant expert en projets écologiques. Rédige des analyses structurées et claires."},
            {"role": "user", "content": description}
        ],
        "temperature": 0.5,
        "max_tokens": 600
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        message = result["choices"][0]["message"]["content"]
        return {
            "Titre": "Projet Écologique Proposé",
            "Description": message,
            "Type": "À déterminer selon le contexte",
            "Revenus": "Estimation à compléter"
        }
    except Exception as e:
        return {"error": str(e)}

# --- Simulation d'enregistrement dans NoCoDB (facultatif) ---
def save_to_nocodb(data: dict):
    print("✅ Données prêtes à être envoyées à NoCoDB :")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return {"status": "success"}
