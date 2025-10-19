import requests
import os
import re

# --- Configuration OpenRouter ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}


# --- Nettoyage du texte ---
def clean_text(text: str) -> str:
    """Nettoie le texte : supprime les caractères inutiles et les redondances simples."""
    if not text:
        return ""

    # Nettoyage basique
    text = re.sub(r"[*#`>_]+", "", text)
    text = re.sub(r"[0-9️⃣🧠💡⚡🌍🔹🔸•]+", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    text = re.sub(r"[\s.]+$", "", text)
    text = text.strip().strip('"').strip("'")

    # Supprimer les préfixes comme "Projet:", "s:", etc.
    text = re.sub(r"^(s\s*[:\-–]|de\s*projet\s*[:\-–]|projet\s*[:\-–]|le\s*projet\s*[:\-–]|[:\-–])", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^[\s:;,\-–]+", "", text)
    return text.strip()


# --- Détection automatique du type ---
def detect_type(description: str) -> str:
    """Déduit automatiquement le type de projet à partir de mots-clés."""
    description = description.lower()
    if any(k in description for k in ["solaire", "énergie", "panneau", "photovoltaïque", "éolien", "renouvelable"]):
        return "Énergie renouvelable"
    if any(k in description for k in ["eau", "pluie", "irrigation", "hydrique"]):
        return "Gestion de l’eau"
    if any(k in description for k in ["agriculture", "potager", "semence", "culture"]):
        return "Agriculture durable"
    if any(k in description for k in ["recyclage", "déchet", "tri", "compost"]):
        return "Gestion des déchets"
    if any(k in description for k in ["école", "sensibiliser", "formation", "atelier", "éducation"]):
        return "Éducation environnementale"
    if any(k in description for k in ["forêt", "arbre", "reboisement", "biodiversité"]):
        return "Reforestation et biodiversité"
    return "Projet écologique"


# --- Extraction ---
def extract_field(text, start, end=None):
    """Extrait une section entre deux mots-clés."""
    if end:
        pattern = rf"{start}\s*[:\-–]?\s*(.*?){end}"
    else:
        pattern = rf"{start}\s*[:\-–]?\s*(.*)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


# --- Dé-duplication intelligente ---
def deduplicate_fields(fields: dict) -> dict:
    """Supprime les phrases redondantes entre sections."""
    desc, type_proj, revenus = fields["Description"], fields["Type"], fields["Revenus"]

    # Enlever les répétitions directes
    for phrase in type_proj.split(". "):
        if phrase.strip() and phrase.strip() in desc:
            desc = desc.replace(phrase, "")
    for phrase in revenus.split(". "):
        if phrase.strip() and phrase.strip() in desc:
            desc = desc.replace(phrase, "")
        if phrase.strip() and phrase.strip() in type_proj:
            type_proj = type_proj.replace(phrase, "")

    fields["Description"] = clean_text(desc)
    fields["Type"] = clean_text(type_proj)
    fields["Revenus"] = clean_text(revenus)
    return fields


# --- Appel du modèle ---
def ask_model(description: str):
    """Analyse un projet écologique et renvoie des champs nettoyés et cohérents."""
    payload = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un expert en analyse de projets écologiques. "
                    "Analyse le projet et retourne 4 champs clairs : "
                    "Titre, Description, Type, Revenus. "
                    "Sois concis, pas de répétitions entre les sections. Aucun emoji ni Markdown."
                ),
            },
            {
                "role": "user",
                "content": f"Analyse ce projet écologique et fournis :\n1. Titre\n2. Description\n3. Type\n4. Revenus\n\nProjet : {description}",
            },
        ],
        "temperature": 0.4,
        "max_tokens": 700,
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=25)
        response.raise_for_status()
        message = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

        if not message.strip():
            return {"error": "Réponse vide du modèle."}

        titre = extract_field(message, r"Titre", r"Description")
        desc = extract_field(message, r"Description", r"Type")
        type_proj = extract_field(message, r"Type", r"(Revenu|Estimation)")
        revenus = extract_field(message, r"Revenu")

        result = {
            "Titre": clean_text(titre or "Titre non précisé"),
            "Description": clean_text(desc or "Description non précisée"),
            "Type": clean_text(type_proj or detect_type(description)),
            "Revenus": clean_text(revenus or "À estimer"),
        }

        # 🔥 Supprimer les redondances globales
        return deduplicate_fields(result)

    except Exception as e:
        return {"error": str(e)}


# --- Enregistrement NoCoDB ---
def save_to_nocodb(data: dict):
    """Enregistre les données dans NoCoDB."""
    NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/m6zxxbaq2f869a0/records"
    NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"

    headers = {
        "xc-token": NOCODB_API_TOKEN,
        "Content-Type": "application/json"
    }

    # ✅ Ajout du champ "Projects" pour éviter l’erreur 400
    payload = {
        "Title": data.get("Titre"),
        "Description": data.get("Description"),
        "Type": data.get("Type"),
        "Revenues": data.get("Revenus"),
        "Projects": None,  # ou un ID de projet existant si la relation est obligatoire
    }

    try:
        response = requests.post(NOCODB_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return {"status": "success", "response": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
