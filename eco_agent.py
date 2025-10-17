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

# --- Fonction principale d’analyse du projet ---
def ask_model(description: str):
    """
    Interroge le modèle Mistral-Nemo via OpenRouter pour générer
    une analyse structurée d’un projet écologique.
    """
    data = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {"role": "system", "content": (
                "Tu es un assistant expert en projets écologiques. "
                "Analyse le texte fourni et renvoie un JSON structuré avec ces champs :\n"
                "- Titre\n- Description\n- Type\n- Revenus.\n"
                "Assure-toi que chaque champ soit clair, sans répétition ni marqueurs inutiles."
            )},
            {"role": "user", "content": f"Analyse ce projet écologique : {description}"}
        ],
        "temperature": 0.5,
        "max_tokens": 700
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # ✅ Extraction du message brut du modèle
        message = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        if not message:
            return {"error": "Aucune réponse du modèle."}

        # --- Extraction propre des champs à l’aide de regex ---
        titre = extract_field(message, r"(?:Titre|Nom du projet)[:\-–]\s*(.+)")
        description = extract_field(message, r"(?:Description)[:\-–]\s*(.+)")
        type_proj = extract_field(message, r"(?:Type|Catégorie|Nature du projet)[:\-–]\s*(.+)")
        revenus = extract_field(message, r"(?:Revenus|Estimation des revenus|Sources de financement)[:\-–]\s*(.+)")

        # --- Nettoyage final ---
        data_clean = {
            "Titre": clean_field(titre or "Projet écologique"),
            "Description": clean_field(description),
            "Type": clean_field(type_proj),
            "Revenus": clean_field(revenus)
        }

        return data_clean

    except Exception as e:
        return {"error": str(e)}


# --- Fonction d’extraction avec regex robuste ---
def extract_field(text: str, start_pattern: str):
    """
    Extrait le contenu après un motif donné jusqu’à la prochaine section.
    Exemple : de 'Description:' jusqu’à 'Type:'.
    """
    pattern = re.compile(start_pattern + r"([\s\S]*?)(?=\n[A-ZÉÈÊÂÎÔÙÛÜÇa-z]*[:\-–]|$)", re.IGNORECASE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


# --- Fonction de nettoyage général ---
def clean_field(value: str):
    if not value:
        return ""
    value = value.strip()
    value = re.sub(r"^[\s:]*", "", value)      # Supprime ':' ou 's:' au début
    value = re.sub(r"\s*\.\s*$", "", value)    # Supprime le '.' final
    value = re.sub(r"\s+", " ", value)         # Supprime les doubles espaces
    return value


# --- Connexion à NoCoDB ---
def save_to_nocodb(data: dict):
    """
    Enregistre les données nettoyées dans la table NoCoDB.
    """
    NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/m6zxxbaq2f869a0/records"
    NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"  # Ton token personnel

    headers = {
        "xc-token": NOCODB_API_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "Title": clean_field(data.get("Titre")),
        "Description": clean_field(data.get("Description")),
        "Type": clean_field(data.get("Type")),
        "Revenues": clean_field(data.get("Revenus"))
    }

    try:
        response = requests.post(NOCODB_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        print("✅ Enregistrement réussi :", response.json())
        return {"status": "success", "response": response.json()}

    except Exception as e:
        print("❌ Erreur lors de l’enregistrement :", str(e))
        return {"status": "error", "message": str(e)}


# --- Test local ---
if __name__ == "__main__":
    projet = "Installer des systèmes de récupération d'eau de pluie dans les écoles rurales"
    result = ask_model(projet)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    # save_to_nocodb(result)

