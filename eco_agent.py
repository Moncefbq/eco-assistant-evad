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
    if not text:
        return ""
    text = re.sub(r"[*#`>_]+", "", text)
    text = re.sub(r"[0-9️⃣🧠💡⚡🌍🔹🔸•]+", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    text = re.sub(r"[\s.]+$", "", text)
    text = text.strip().strip('"').strip("'")
    return text


# --- Détection automatique du type ---
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


# --- Mapping des types valides NoCoDB ---
def map_type_to_valid(value: str, description: str = "") -> str:
    """Associe un type écologique ou une description à un type NoCoDB."""
    mapping = {
        "solaire": "Parc solaire",
        "énergie": "Parc solaire",
        "panneau": "Parc solaire",
        "renouvelable": "Parc solaire",
        "forêt": "Parc national",
        "biodiversité": "Parc national",
        "reforestation": "Parc national",
        "exposition": "Exposition center",
        "éducation": "Exposition center",
        "environnementale": "Exposition center",
        "déchet": "Ferme urbaine",
        "recyclage": "Ferme urbaine",
        "compost": "Ferme urbaine",
        "eau": "Jardin partagé",
        "irrigation": "Jardin partagé",
        "jardin": "Jardin partagé",
        "urbain": "Jardin partagé",
        "partagé": "Jardin partagé",
        "expérimental": "Experimental lab",
        "laboratoire": "Experimental lab",
        "coworking": "Coworking",
        "entreprise": "Coworking"
    }

    value_norm = (value or "").strip().lower()
    desc_norm = (description or "").strip().lower()

    # 🔍 Analyse des mots-clés du type
    for keyword, valid in mapping.items():
        if keyword in value_norm:
            return valid

    # 🔍 Analyse secondaire dans la description si "écologique" ou "projet" est trop vague
    if "écologique" in value_norm or "projet" in value_norm:
        for keyword, valid in mapping.items():
            if keyword in desc_norm:
                return valid

    # Valeur par défaut plus logique
    if any(k in desc_norm for k in ["jardin", "urbain", "partagé"]):
        return "Jardin partagé"

    return "Parc solaire"


# --- Extraction ---
def extract_field(text, start, end=None):
    if end:
        pattern = rf"{start}\s*[:\-–]?\s*(.*?){end}"
    else:
        pattern = rf"{start}\s*[:\-–]?\s*(.*)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


# --- Appel du modèle ---
def ask_model(description: str):
    """Analyse le projet écologique et génère les champs avec revenus automatiques."""
    payload = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant expert en analyse de projets écologiques et durables. "
                    "Analyse attentivement la description du projet et produis une réponse avec les sections suivantes :\n\n"
                    "Titre : (formule claire et concise du projet)\n"
                    "Description : (résumé structuré et professionnel, sans répétition inutile)\n"
                    "Type : (catégorie principale du projet — choisis parmi : Parc solaire, Jardin partagé, Ferme urbaine, Parc national, Exposition center, Coworking, Experimental lab)\n"
                    "Revenus : (décris les sources possibles de revenus ou de financement : subventions, ventes, partenariats, tourisme, ateliers, production d'énergie, etc. "
                    "Si elles ne sont pas mentionnées, déduis-les logiquement selon le type de projet.)\n\n"
                    "⚠️ Réponds uniquement avec ces quatre champs dans cet ordre, sans texte supplémentaire ni emojis."
                )
            },
            {"role": "user", "content": f"Projet : {description}"}
        ],
        "temperature": 0.7,
        "max_tokens": 700
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        message = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

        titre = extract_field(message, r"Titre", r"Description")
        desc = extract_field(message, r"Description", r"Type")
        type_proj = extract_field(message, r"Type", r"(Revenu|Estimation)")
        revenus = extract_field(message, r"Revenu")

        # --- Application du mapping sur le type ---
        raw_type = clean_text(type_proj or detect_type(description))
        mapped_type = map_type_to_valid(raw_type, description)

        # --- Nettoyage du revenu généré par Mistral ---
        revenus_clean = clean_text(revenus or "À estimer")
        revenus_clean = re.sub(r'^[Ss]\s*[:\-–]?\s*', '', revenus_clean)  # 🔹 enlève les "s:" ou "S:" au début

        return {
            "Titre": clean_text(titre or "Titre non précisé"),
            "Description": clean_text(desc or "Description non précisée"),
            "Type": mapped_type,
            "Revenus": revenus_clean,
        }

    except Exception as e:
        return {"error": str(e)}


# --- Upload d'image ---
def upload_image_to_nocodb(file, token):
    """Upload une image vers NoCoDB et renvoie son URL."""
    upload_url = "https://app.nocodb.com/api/v2/storage/upload"
    headers = {"xc-token": token}

    file.seek(0)
    files = {"files": (file.name, file, file.type or "image/png")}
    try:
        response = requests.post(upload_url, headers=headers, files=files, timeout=15)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and len(result) > 0 and "url" in result[0]:
            return result[0]["url"]
        return None
    except Exception as e:
        print("❌ Erreur upload image :", e)
        return None


# --- Sauvegarde dans NoCoDB ---
def save_to_nocodb(data: dict):
    """Sauvegarde les données dans la table Places."""
    NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/m6zxxbaq2f869a0/records"
    NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"

    headers = {"xc-token": NOCODB_API_TOKEN, "Content-Type": "application/json"}

    # 🔹 Upload de l’image si présente
    picture_data = []
    if data.get("Picture"):
        image_url = upload_image_to_nocodb(data["Picture"], NOCODB_API_TOKEN)
        if image_url:
            picture_data = [{"url": image_url}]

    # 🔹 Conversion du type vers une valeur valide pour NoCoDB
    type_value = map_type_to_valid(data.get("Type", ""), data.get("Description", ""))

    # 🔹 Construction du payload
    payload = {
        "Title": data.get("Titre", ""),
        "Description": data.get("Description", ""),
        "Type": type_value,
        "Revenues": data.get("Revenus", ""),
        "Picture": picture_data
    }

    try:
        response = requests.post(NOCODB_API_URL, headers=headers, json=payload, timeout=20)
        if response.status_code in (200, 201):
            return {"status": "success", "response": response.json()}
        else:
            return {"status": "error", "message": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
