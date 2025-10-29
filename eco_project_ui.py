import streamlit as st
import requests
import re
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Formulaire Pilote d'impact", page_icon="🏡", layout="centered")

# 🎨 Thème vert foncé
st.markdown(
    """
    <style>
    body {
        background-color: #003300; /* Vert foncé */
        color: white;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #004d00; /* Vert plus clair */
        color: white;
        border-radius: 8px;
    }
    .stButton button {
        background-color: #00b300;
        color: white;
        border-radius: 8px;
    }
    .stButton button:hover {
        background-color: #009900;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
NOCODB_API_TOKEN = st.secrets["NOCODB_API_TOKEN"]
NOCODB_API_URL = st.secrets["NOCODB_API_URL"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# ⚙️ Données NoCoDB
NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"
NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/mzaor3uiob3gbe2/records"
UPLOAD_URL = "https://app.nocodb.com/api/v2/storage/upload"

# --- Upload fichier vers NoCoDB ---
def upload_to_nocodb(file):
    headers = {"xc-token": NOCODB_API_TOKEN}
    files = {"files": (file.name, file, file.type or "application/octet-stream")}
    try:
        response = requests.post(UPLOAD_URL, headers=headers, files=files, timeout=15)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and "url" in result[0]:
            return result[0]["url"]
    except Exception as e:
        st.error(f"Erreur upload fichier : {e}")
    return None


# --- 🏡 Interface principale ---
st.title("🏡 Formulaire Pilote d'impact")

st.markdown("""
### 🌍 Rejoignez EVAD pour co-développer votre projet de lieux régénératif !

Bienvenue dans **EVAD - Ecosystème Vivant Autonome et Décentralisé**, une platefome de pilotage d’impact conçue pour faciliter la création de lieux partagés durables *(tiers-lieux, éco-lieux, coworking, ferme, etc.)* grâce à des outils open-source, une économie régénérative et une intelligence collaborative.
""")

# --- 1️⃣ Formulaire utilisateur ---
with st.form("user_form"):
    title = st.text_input("🏷️ Nom du projet")
    description = st.text_area("📝_



