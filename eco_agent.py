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


# --- Fonction principale ---
def ask_model(description: str):
    """
    Analyse le projet écologique via Mistral-Nemo et retourne un JSON propre.
    """
    data = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant expert en projets écologiques. "
                    "Analyse le projet fourni et renvoie un JSON propre avec les champs : "
                    "Titre, Description, Type, Revenus. "
                    "Ne commence aucun champ par des caractères comme ':' ou 's:'. "
                    "Chaque champ doit être concis et bien formaté."
                )
            },
            {"role": "user", "content": description}
        ],
        "temperature": 0.4,
        "max_tokens": 700
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        message = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        if not message:
            return {"error": "Aucune réponse du modèle."}

        titre = extract_field(message, "titre")
        description_text = extract_field(message, "description")
        type_text = extract_field(message, "type")
        revenus = extract_field(message, "revenus")

        return {
            "Titre": clean_field(titre),
            "Description": clean_field(description_text),
            "Type": clean_field(type_text),
            "Revenus": clean_field(revenus),
        }

    except Exception as e:
        return {"error": str(e)}


# --- Extraction & nettoyage ---
def extract_field(text: str, field: str):
    pattern = re.compile(rf"{field}\s*[:\-–]\s*(.+?)(?=\n[A-ZÉÈÊÂÎÔÙÛÜÇa-z]*[:\-–]|$)", re.IGNORECASE | re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def clean_field(value: str):
    if not value:
        return ""
    value = value.strip()
    value = re.sub(r"^[\s:]*", "", value)
    value = re.sub(r"^s\s*[:\-–]?\s*", "", value)
    value = re.sub(r"\s*\.\s*$", "", value)
    value = re.sub(r"\s+", " ", value)
    value = value.strip('"').strip("'")
    return value.strip()


# --- Connexion à NoCoDB ---
def save_to_nocodb(data: dict):
    NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/m6zxxbaq2f869a0/records"
    NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"

    headers = {
        "xc-token": NOCODB_API_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "Title": clean_field(data.get("Titre")),
        "Description": clean_field(data.get("Description")),
        "Type": clean_field(data.get("Type")),
        "Revenues": clean_field(data.get("Revenus")),
    }

    try:
        response = requests.post(NOCODB_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        print("✅ Enregistrement réussi :", response.json())
        return {"status": "success", "response": response.json()}
    except Exception as e:
        print("❌ Erreur lors de l’enregistrement :", str(e))
        return {"status": "error", "message": str(e)}


# --- Test universel (accessible partout) ---
def run_test():
    """
    Teste l’agent avec un exemple concret (exécutable localement ou en ligne).
    """
    example_description = (
        "Installer des systèmes de récupération d’eau de pluie dans les écoles rurales "
        "pour réduire la consommation d’eau potable et promouvoir la durabilité."
    )

    print("🌿 Lancement du test du modèle avec exemple :")
    print("📝 Description envoyée :", example_description)
    result = ask_model(example_description)
    print("\n--- Résultat ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


# --- Exécution si lancé directement ---
if __name__ == "__main__":
    run_test()
