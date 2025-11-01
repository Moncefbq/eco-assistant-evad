# -*- coding: utf-8 -*-
import streamlit as st
import requests
import re
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Formulaire Pilote d'impact", page_icon="🏡", layout="centered")

# 🌿 STYLE GLOBAL : fond clair + blocs verts + textes noirs + champs blancs
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
        color: #000000 !important;
    }

    .stForm, .stForm > div {
        background-color: #018262 !important;
        color: #000000 !important;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.25);
        margin-bottom: 25px;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 6px;
        border: 1px solid #555 !important;
    }

    h1, h2, h3, h4, h5, h6, label, p, span, div {
        color: #000000 !important;
    }

    ::selection {
        background: #000000;
        color: #ffffff;
    }
    ::-moz-selection {
        background: #000000;
        color: #ffffff;
    }

    .stButton button {
        background-color: #00b300 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #009900 !important;
    }

    div[data-baseweb="tag"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    .stForm label, .stForm h3, .stForm h4, .stForm p {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SECRETS ---
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
NOCODB_API_TOKEN = st.secrets["NOCODB_API_TOKEN"]
NOCODB_API_URL = st.secrets["NOCODB_API_URL"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}

# --- NoCoDB CONFIG ---
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

Bienvenue dans **EVAD - Ecosystème Vivant Autonome et Décentralisé**, une plateforme de pilotage d’impact conçue pour faciliter la création de lieux partagés durables *(tiers-lieux, éco-lieux, coworking, fermes, etc.)* grâce à des outils open-source, une économie régénérative et une intelligence collaborative.
""")

# Initialisation du nombre d’espaces dans la session
if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1

# --- 1️⃣ Étape 1 : Formulaire utilisateur ---
with st.form("user_form"):
    st.subheader("🧾 Informations sur le projet")

    title = st.text_input("🏷️ Nom du projet")
    description = st.text_area("📝 Description du projet")

    # 🏠 Espaces dynamiques
    st.markdown("### 🏡 Espaces du projet")
    espaces = []
    for i in range(st.session_state.nb_espaces):
        espaces.append(st.text_area(f"🏠 Espace {i+1}", key=f"espace_{i+1}", height=80))

    # Bouton pour ajouter un nouvel espace (max 5)
    if st.session_state.nb_espaces < 5:
        add_space = st.form_submit_button("➕ Ajouter un espace")
        if add_space:
            st.session_state.nb_espaces += 1
            st.rerun()


    localisation = st.text_input("📍 Localisation")

    project_types = st.multiselect(
        "🌿 Type de projet",
        ["Third-place", "Eco-lieu", "Association", "Coworking", "Autres", "Permaculture"],
        default=[]
    )

    uploaded_doc = st.file_uploader("📄 Document lié au projet (optionnel)", type=["pdf", "png", "jpg", "jpeg", "docx"])
    submitted = st.form_submit_button("🚀 Lancer l’analyse")

# --- 2️⃣ Étape 2 : Analyse IA ---
if submitted:
    if not all([title, description, localisation]):
        st.warning("Merci de remplir tous les champs avant la recherche.")
    else:
        with st.spinner("🔎 Analyse du projet en cours..."):
            payload = {
                "model": "mistralai/mistral-nemo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Tu es un expert en gestion de projets écologiques. "
                            "Analyse les informations et renvoie une réponse formatée ainsi :\n\n"
                            "Solution : ...\n"
                            "Impact écologique : ...\n"
                            "Impact social : ...\n"
                            "Impact économique : ...\n"
                            "Plan d’action : ... (donne toujours un plan d’action clair avec au moins 3 étapes concrètes)"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Projet: {title}\nDescription: {description}\nLocalisation: {localisation}"
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 900
            }

            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
                response.raise_for_status()
                ai_text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                st.session_state.ai_result = ai_text
                st.session_state.espaces = espaces
                st.success("✅ Analyse terminée avec succès !")
            except Exception as e:
                st.error(f"Erreur pendant la génération : {e}")

# --- 3️⃣ Étape 3 : Synthèse du projet ---
if "ai_result" in st.session_state:
    with st.form("synthese_form"):
        st.subheader("✏️ Synthèse du projet (modifiable avant validation)")

        def extract_section(text, section):
            pattern = rf"{section}\s*:\s*(.*?)(?=\n[A-ZÉÈÊÂÎÔÙÇ]|$)"
            match = re.search(pattern, text, re.DOTALL)
            return match.group(1).strip() if match else ""

        solution = extract_section(st.session_state.ai_result, "Solution")
        impact_eco = extract_section(st.session_state.ai_result, "Impact écologique")
        impact_social = extract_section(st.session_state.ai_result, "Impact social")
        impact_econ = extract_section(st.session_state.ai_result, "Impact économique")
        plan_action = extract_section(st.session_state.ai_result, "Plan d’action")

        if not plan_action or len(plan_action.strip()) < 10:
            plan_action = (
                "1️⃣ Identifier les acteurs locaux et définir les priorités du projet.\n"
                "2️⃣ Lancer une phase pilote avec des indicateurs d’impact mesurables.\n"
                "3️⃣ Analyser les résultats, ajuster les actions et planifier l’expansion."
            )

        solution = st.text_area("💡 Solution", value=solution, height=100)
        impact_eco = st.text_area("🌿 Impact écologique", value=impact_eco, height=100)
        impact_social = st.text_area("🤝 Impact social", value=impact_social, height=100)
        impact_econ = st.text_area("💰 Impact économique", value=impact_econ, height=100)
        plan_action = st.text_area("🧭 Plan d’action", value=plan_action, height=130)

        validated = st.form_submit_button("✅ Valider et ajouter les informations du porteur")

        if validated:
            st.session_state.validation_ok = True
            st.session_state.solution = solution
            st.session_state.impact_eco = impact_eco
            st.session_state.impact_social = impact_social
            st.session_state.impact_econ = impact_econ
            st.session_state.plan_action = plan_action

# --- 4️⃣ Étape 4 : Informations du porteur ---
if st.session_state.get("validation_ok"):
    with st.form("porteur_form"):
        st.subheader("👤 Informations du porteur")

        leader = st.text_input("Nom du porteur de projet")
        email = st.text_input("Email de contact")
        status = st.selectbox("📊 Statut du projet",["Thinking", "Modélisation ", "Construction", "Développement", "Financement", "Student"],index=0)
        saved = st.form_submit_button("💾 Enregistrer dans NoCoDB")

        if saved:
            with st.spinner("💾 Sauvegarde du projet..."):
                doc_data = []
                if "uploaded_doc" in st.session_state and st.session_state.uploaded_doc:
                   url = upload_to_nocodb(st.session_state.uploaded_doc)
                   if url:
                        doc_data = [{"url": url}]


                payload = {
                    "Title": title,
                    "Description": description,
                    "Localisation": localisation,
                    "Type": project_types,
                    "Project Leader": leader,
                    "Email": email,
                    "Status": status,
                    "Documents": doc_data,
                    "espace 1": st.session_state.espaces[0] if len(st.session_state.espaces) > 0 else "",
                    "espace 2": st.session_state.espaces[1] if len(st.session_state.espaces) > 1 else "",
                    "espace 3": st.session_state.espaces[2] if len(st.session_state.espaces) > 2 else "",
                    "espace 4": st.session_state.espaces[3] if len(st.session_state.espaces) > 3 else "",
                    "espace 5": st.session_state.espaces[4] if len(st.session_state.espaces) > 4 else "",
                }

                headers = {"xc-token": NOCODB_API_TOKEN, "Content-Type": "application/json"}
                r = requests.post(NOCODB_API_URL, headers=headers, json=payload)
                if r.status_code in (200, 201):
                    st.success("🍃 Projet enregistré avec succès dans `Projects` ! 🌍")
                    st.toast("✅ Données synchronisées avec NoCoDB", icon="🌱")

                else:
                    st.error(f"Erreur API {r.status_code} : {r.text}")













