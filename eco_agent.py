import requests
import os
import re

# --- Configuration OpenRouter ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}


# --- Nettoyage du texte ---
def clean_text(text: str) -> str:
    """Nettoie le texte des caractères parasites, préfixes inutiles et espaces."""
    if not text:
        return ""

    text = re.sub(r"[*#`>_]+", "", text)  # caractères Markdown
    text = re.sub(r"[0-9️⃣🧠💡⚡🌍🔹🔸•]+", "", text)
    text = re.sub(r"\s{2,}", " ", text)

    # Supprimer préfixes inutiles
    text = re.sub(
        r"^(s\s*[:\-–]\s*|de\s*projet\s*[:\-–]\s*|projet\s*[:\-–]\s*|le\s*projet\s*[:\-–]\s*|[:\-–]\s*)",
        "",
        text.strip(),
        flags=re.IGNORECASE,
    )

    # Nettoyage final
    text = text.strip().strip('"').strip("'")
    text = re.sub(r"^[\s:;,\-–]+", "", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


# --- Extraction simple ---
def extract_field(text, start, end=None):
    """Extrait une section spécifique avec une recherche rapide."""
    if end:
        pattern = rf"{start}\s*[:\-–]?\s*(.*?){end}"
    else:
        pattern = rf"{start}\s*[:\-–]?\s*(.*)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


# --- Suppression légère de redondances entre sections ---
def deduplicate_fields(fields: dict) -> dict:
    """Élimine les phrases répétées entre sections (rapide et léger)."""
    desc = fields.get("Description", "")
    type_proj = fields.get("Type", "")
    revenus = fields.get("Revenus", "")

    # Retirer phrases dupliquées par simple inclusion de texte
    for phrase in type_proj.split(". "):
        if phrase.strip() and phrase.strip() in desc:
            desc = desc.replace(phrase, "").strip()

    for phrase in revenus.split(". "):
        if phrase.strip() and phrase.strip() in desc:
            desc = desc.replace(phrase, "").strip()
        if phrase.strip() and phrase.strip() in type_proj:
            type_proj = type_proj.replace(phrase, "").strip()

    fields["Description"] = clean_text(desc)
    fields["Type"] = clean_text(type_proj)
    fields["Revenus"] = clean_text(revenus)
    return fields


# --- Appel du modèle ---
def ask_model(description: str):
    """Analyse le projet écologique et renvoie un dictionnaire propre sans redondances."""
    payload = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant expert en projets écologiques. "
                    "Analyse le projet et retourne quatre sections claires : "
                    "Titre, Description, Type, Revenus. "
                    "Le type doit être précis (ex : énergie renouvelable, agriculture durable, gestion de l’eau, etc.). "
                    "Ne répète pas les phrases entre les sections. Aucun emoji ni Markdown."
                ),
            },
            {
                "role": "user",
                "content": f"Analyse ce projet écologique et fournis :\n1. Titre\n2. Description\n3. Type\n4. Revenus\n\nProjet : {description}",
            },
        ],
        "temperature": 0.4,
        "max_tokens": 600,
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
            "Type": clean_text(type_proj or "Type non précisé"),
            "Revenus": clean_text(revenus or "À estimer"),
        }

        return deduplicate_fields(result)

    except Exception as e:
        return {"error": str(e)}


# --- Enregistrement NoCoDB ---
def save_to_nocodb(data: dict):
    """Enregistre les données nettoyées dans NoCoDB."""
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
        response = requests.post(NOCODB_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return {"status": "success", "response": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
