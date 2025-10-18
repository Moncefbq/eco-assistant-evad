import requests
import os
import re
import difflib

# --- Configuration OpenRouter ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}


# --- Nettoyage du texte ---
def clean_text(text: str) -> str:
    """Nettoie le texte : supprime les caractères inutiles, préfixes, espaces et redondances."""
    if not text:
        return ""

    # Supprimer symboles et caractères parasites
    text = re.sub(r"[*#`>_]+", "", text)
    text = re.sub(r"[0-9️⃣🧠💡⚡🌍🔹🔸•]+", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = text.strip().strip('"').strip("'")

    # Supprimer les débuts inutiles
    text = re.sub(
        r"^(s\s*[:\-–]\s*|de\s*projet\s*[:\-–]\s*|projet\s*[:\-–]\s*|le\s*projet\s*[:\-–]\s*|[:\-–]\s*)",
        "",
        text.strip(),
        flags=re.IGNORECASE,
    )

    # Supprimer ":" ou ";" restants en début
    text = re.sub(r"^[\s:;,\-–]+", "", text)

    # Supprimer doublons internes dans une même section
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    unique_sentences = []
    for s in sentences:
        if not any(
            difflib.SequenceMatcher(None, s.lower(), u.lower()).ratio() > 0.85
            for u in unique_sentences
        ):
            unique_sentences.append(s)
    text = " ".join(unique_sentences)

    # Nettoyage final
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"[\s.]+$", "", text)
    return text.strip()


# --- Extraction d'une section ---
def extract_field(text, start, end=None):
    """Extrait une section entre deux titres (Titre, Description, etc.)."""
    if end:
        pattern = rf"{start}\s*[:\-–]?\s*(.*?){end}"
    else:
        pattern = rf"{start}\s*[:\-–]?\s*(.*)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


# --- Nettoyage global entre sections ---
def remove_cross_redundancy(fields: dict) -> dict:
    """
    Supprime les phrases redondantes entre Description, Type et Revenus.
    """
    desc_sentences = set(re.split(r"(?<=[.!?])\s+", fields.get("Description", "")))
    type_sentences = set(re.split(r"(?<=[.!?])\s+", fields.get("Type", "")))
    rev_sentences = set(re.split(r"(?<=[.!?])\s+", fields.get("Revenus", "")))

    # Supprimer les phrases très similaires entre sections
    def filter_unique(sentences, others):
        result = []
        for s in sentences:
            s_clean = s.strip()
            if s_clean and not any(
                difflib.SequenceMatcher(None, s_clean.lower(), o.strip().lower()).ratio() > 0.75
                for o in others
            ):
                result.append(s_clean)
        return result

    fields["Description"] = " ".join(
        filter_unique(desc_sentences, type_sentences.union(rev_sentences))
    ).strip()

    fields["Type"] = " ".join(
        filter_unique(type_sentences, desc_sentences.union(rev_sentences))
    ).strip()

    fields["Revenus"] = " ".join(
        filter_unique(rev_sentences, desc_sentences.union(type_sentences))
    ).strip()

    return fields


# --- Appel du modèle OpenRouter ---
def ask_model(description: str):
    """Analyse un projet écologique et retourne un dictionnaire propre sans redondance."""
    data = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant expert en projets écologiques. "
                    "Analyse le projet et retourne quatre sections claires : "
                    "Titre, Description, Type, Revenus. "
                    "Le type doit être précis (énergie renouvelable, agriculture durable, gestion de l’eau, etc.). "
                    "Ne répète pas les phrases entre les sections. Aucun emoji ni Markdown."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Analyse ce projet écologique et fournis :\n"
                    f"1. Titre\n2. Description\n3. Type\n4. Revenus\n\n"
                    f"Projet : {description}"
                ),
            },
        ],
        "temperature": 0.4,
        "max_tokens": 700,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        message = result.get("choices", [{}])[0].get("message", {}).get("content", "")

        if not message.strip():
            return {"error": "Réponse vide du modèle."}

        # Extraction des champs
        titre = extract_field(message, r"Titre", r"Description")
        desc = extract_field(message, r"Description", r"Type")
        type_proj = extract_field(message, r"Type", r"(Revenu|Estimation)")
        revenus = extract_field(message, r"Revenu")

        fields = {
            "Titre": clean_text(titre or "Titre non précisé"),
            "Description": clean_text(desc or "Description non précisée"),
            "Type": clean_text(type_proj or "Type non précisé"),
            "Revenus": clean_text(revenus or "À estimer"),
        }

        # ✅ Supprimer les redondances entre sections
        return remove_cross_redundancy(fields)

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
        response = requests.post(NOCODB_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return {"status": "success", "response": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
