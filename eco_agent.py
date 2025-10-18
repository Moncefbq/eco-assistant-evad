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

# --- Nettoyage du texte ---
def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"[*#`>_]+", "", text)
    text = re.sub(r"[0-9️⃣🧠💡⚡🌍🔹🔸•]+", "", text)
    text = re.sub(r"^(s\s*[:\-–])", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"^(de\s*projet\s*[:\-–]*)", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"^(projet\s*[:\-–]*)", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"^[\s:.,;-]+", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s([.,;:!?])", r"\1", text)
    text = re.sub(r"[\s.]+$", "", text)
    text = text.strip().strip('"').strip("'")
    return text.strip()

# --- Extraction de section ---
def extract_field(text, start_pattern, end_pattern=None):
    if end_pattern:
        pattern = rf"{start_pattern}(.*?){end_pattern}"
    else:
        pattern = rf"{start_pattern}(.*)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""

# --- Analyse du projet ---
def ask_model(description: str):
    data = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {"role": "system", "content": (
                "Tu es un assistant expert en projets écologiques. "
                "Analyse le projet et donne quatre sections claires : "
                "Titre, Description, Type, Revenus. "
                "Pas de Markdown, pas d’emoji, juste du texte clair."
            )},
            {"role": "user", "content": (
                f"Analyse ce projet écologique et fournis :\n"
                f"1. Titre\n2. Description\n3. Type de projet\n4. Estimation des revenus.\n\n"
                f"Projet : {description}"
            )}
        ],
        "temperature": 0.4,
        "max_tokens": 650
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()

        message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not message.strip():
            return {"error": "Réponse vide du modèle."}

        titre = extract_field(message, r"Titre[:\-–]*", r"Description[:\-–]*")
        desc = extract_field(message, r"Description[:\-–]*", r"Type[:\-–]*")
        type_proj = extract_field(message, r"Type[:\-–]*", r"(Revenu|Estimation\s+des\s+revenus)[:\-–]*")
        revenus = extract_field(message, r"Revenu[:\-–]*")

        return {
            "Titre": clean_text(titre or "Titre non précisé"),
            "Description": clean_text(desc or message[:300]),
            "Type": clean_text(type_proj or "Non défini"),
            "Revenus": clean_text(revenus or "À estimer"),
        }

    except Exception as e:
        return {"error": str(e)}

# --- Enregistrement NoCoDB ---
def save_to_nocodb(data: dict):
    NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/m6zxxbaq2f869a0/records"
    NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"

    headers = {"xc-token": NOCODB_API_TOKEN, "Content-Type": "application/json"}
    payload = {
        "Title": data.get("Titre"),
        "Description": data.get("Description"),
        "Type": data.get("Type"),
        "Revenues": data.get("Revenus"),
    }

    try:
        response = requests.post(NOCODB_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return {"status": "success", "response": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
