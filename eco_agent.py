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


# --- Nettoyage intelligent du texte ---
def clean_text(text: str) -> str:
    """
    Nettoie le texte : supprime les caractères parasites, préfixes inutiles et espaces multiples.
    """
    if not text:
        return ""

    # Supprimer les caractères Markdown et emojis
    text = re.sub(r"[*#`>_]+", "", text)
    text = re.sub(r"[0-9️⃣🧠💡⚡🌍🔹🔸•]+", "", text)

    # Supprimer les préfixes comme ":", "s:", "de projet:", "Projet:" au début du texte
    text = re.sub(r"^(s\s*[:\-–])", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"^(de\s*projet\s*[:\-–]*)", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"^(projet\s*[:\-–]*)", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"^[\s:.,;-]+", "", text)

    # Nettoyage des espaces
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s([.,;:!?])", r"\1", text)

    # Supprimer les points ou espaces inutiles à la fin
    text = re.sub(r"[\s.]+$", "", text)

    # Supprimer guillemets parasites
    text = text.strip().strip('"').strip("'")

    return text.strip()



# --- Extraction de section (Titre, Description, etc.) ---
def extract_field(text, start_pattern, end_pattern=None):
    """Extrait une section entre deux motifs."""
    if end_pattern:
        pattern = rf"{start_pattern}(.*?){end_pattern}"
    else:
        pattern = rf"{start_pattern}(.*)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


# --- Analyse du projet écologique ---
def ask_model(description: str):
    """
    Analyse un projet écologique et renvoie un texte structuré (Titre, Description, Type, Revenus).
    Utilise le modèle Mistral Nemo : rapide et précis.
    """
    data = {
        "model": "mistralai/mistral-nemo",  # ✅ Nouveau modèle rapide
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant expert en projets écologiques. "
                    "Analyse le projet et donne quatre sections claires : "
                    "Titre, Description, Type, Revenus. "
                    "Aucune mise en forme Markdown, aucun emoji, seulement du texte clair."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Analyse ce projet écologique et fournis :\n"
                    f"1. Titre\n2. Description\n3. Type de projet\n4. Estimation des revenus.\n\n"
                    f"Projet : {description}"
                ),
            },
        ],
        "temperature": 0.4,   # 🔥 Moins de variabilité → plus cohérent
        "max_tokens": 650,    # Suffisant pour un texte détaillé
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()

        message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not message.strip():
            return {"error": "Réponse vide du modèle."}

        # --- Nettoyage et extraction ---
        message = message.strip()
        titre = extract_field(message, r"Titre[:\-–]*", r"Description[:\-–]*")
        desc = extract_field(message, r"Description[:\-–]*", r"Type[:\-–]*")
        type_proj = extract_field(
    message,
    r"Type\s*(?:de projet)?[:\-–]*",
    r"(?:Revenu|Estimation\s+des\s+revenus|Sources\s+de\s+revenus)[:\-–]*"
)
        revenus = extract_field(message, r"Revenu[:\-–]*")

        # --- Valeurs par défaut ---
        titre = clean_text(titre or "Titre non précisé")
        desc = clean_text(desc or message[:300])
        type_proj = clean_text(type_proj or "Non défini")
        revenus = clean_text(revenus or "À estimer")

        return {
            "Titre": titre,
            "Description": desc,
            "Type": type_proj,
            "Revenus": revenus,
        }

    except Exception as e:
        return {"error": str(e)}


# --- Envoi vers NoCoDB ---
def save_to_nocodb(data: dict):
    """
    Enregistre les données dans la table NoCoDB.
    """
    NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/m6zxxbaq2f869a0/records"
    NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"  # ⚠️ Ton token personnel

    headers = {
        "xc-token": NOCODB_API_TOKEN,
        "Content-Type": "application/json",
    }

    payload = {
        "Title": data.get("Titre"),
        "Description": data.get("Description"),
        "Type": data.get("Type"),
        "Revenues": data.get("Revenus"),
    }

    try:
        response = requests.post(NOCODB_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        print("✅ Enregistrement réussi :", response.json())
        return {"status": "success", "response": response.json()}

    except Exception as e:
        print("❌ Erreur lors de l’enregistrement :", str(e))
        return {"status": "error", "message": str(e)}


