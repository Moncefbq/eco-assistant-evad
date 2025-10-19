import requests
import os
import re
import base64

# --- Configuration OpenRouter ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}


def clean_text(text: str) -> str:
    """Nettoie le texte (suppression des symboles et redondances)."""
    if not text:
        return ""
    text = re.sub(r"[*#`>_]+", "", text)
    text = re.sub(r"[0-9️⃣🧠💡⚡🌍🔹🔸•]+", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    text = re.sub(r"[\s.]+$", "", text)
    text = text.strip().strip('"').strip("'")
    return text


def detect_type(description: str) -> str:
    description = description.lower()
    if any(k in description for k in ["solaire", "énergie", "panneau", "éolien", "renouvelable"]):
        return "Énergie renouvelable"
    if any(k in description for k in ["eau", "pluie", "irrigation"]):
        return "Gestion de l’eau"
    if any(k in description for k in ["école", "sensibiliser", "formation", "éducation"]):
        return "Éducation environnementale"
    if any(k in description for k in ["déchet", "recyclage", "tri", "compost"]):
        return "Gestion des déchets"
    if any(k in description for k in ["arbre", "forêt", "biodiversité"]):
        return "Reforestation et biodiversité"
    return "Projet écologique"


def extract_field(text, start, end=None):
    if end:
        pattern = rf"{start}\s*[:\-–]?\s*(.*?){end}"
    else:
        pattern = rf"{start}\s*[:\-–]?\s*(.*)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


def ask_model(description: str):
    """Analyse du projet écologique."""
    payload = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {"role": "system",
             "content": "Analyse le projet écologique et renvoie : Titre, Description, Type, Revenus (clairs et sans répétition)."},
            {"role": "user",
             "content": f"Analyse ce projet écologique : {description}"}
        ],
        "temperature": 0.4,
        "max_tokens": 600
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=20)
        response.raise_for_status()
        message = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

        titre = extract_field(message, r"Titre", r"Description")
        desc = extract_field(message, r"Description", r"Type")
        type_proj = extract_field(message, r"Type", r"(Revenu|Estimation)")
        revenus = extract_field(message, r"Revenu")

        return {
            "Titre": clean_text(titre or "Titre non précisé"),
            "Description": clean_text(desc or "Description non précisée"),
            "Type": clean_text(type_proj or detect_type(description)),
            "Revenus": clean_text(revenus or "À estimer"),
        }
    except Exception as e:
        return {"error": str(e)}

def upload_image_to_nocodb(file, token):
    """Upload une image vers NoCoDB et renvoie son URL pour l’ajouter dans Picture."""
    upload_url = "https://app.nocodb.com/api/v2/storage/upload"
    headers = {"xc-token": token}
    files = {"files": (file.name, file, file.type)}
    try:
        response = requests.post(upload_url, headers=headers, files=files, timeout=10)
        response.raise_for_status()
        return response.json()[0]["url"]  # ✅ URL publique renvoyée par NoCoDB
    except Exception as e:
        return None



def save_to_nocodb(data: dict):
    """Sauvegarde les données dans la table Places."""
    NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/m6zxxbaq2f869a0/records"
    NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"

    headers = {"xc-token": NOCODB_API_TOKEN, "Content-Type": "application/json"}

    # 🔹 Upload l’image si présente
    picture_url = None
    if data.get("Picture"):
        picture_url = upload_image_to_nocodb(data["Picture"], NOCODB_API_TOKEN)

    payload = {
        "Title": data.get("Titre"),
        "Description": data.get("Description"),
        "Type": data.get("Type"),
        "Revenues": data.get("Revenus"),
        "Picture": [picture_url] if picture_url else []
    }

    try:
        response = requests.post(NOCODB_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return {"status": "success", "response": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
