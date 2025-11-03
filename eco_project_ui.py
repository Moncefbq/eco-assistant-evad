# -*- coding: utf-8 -*-
import streamlit as st
import requests
import re

# --- CONFIGURATION ---
st.set_page_config(page_title="Formulaire Pilote d'impact", page_icon="🏡", layout="centered")

# 🌿 STYLE GLOBAL
st.markdown("""
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
</style>
""", unsafe_allow_html=True)

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

# ==============================
# 🤖 SYSTEME MULTI-AGENTS
# ==============================

def ask_agent(role_description, user_input):
    """Appel OpenRouter pour un agent donné."""
    payload = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {"role": "system", "content": role_description},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    response.raise_for_status()
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")


def AnalystAgent(title, description, localisation):
    role = (
        "Tu es l'AnalystAgent. Ton rôle est d'étudier le projet et d’en faire un résumé clair, "
        "avec les objectifs principaux, les enjeux et les acteurs potentiels."
    )
    user_input = f"Projet: {title}\nDescription: {description}\nLocalisation: {localisation}"
    return ask_agent(role, user_input)


def EcoAgent(analysis):
    role = (
        "Tu es l'EcoAgent. À partir de l'analyse fournie, génère trois sections:\n"
        "- Impact écologique\n- Impact social\n- Impact économique"
    )
    return ask_agent(role, analysis)


def PlannerAgent(eco_report):
    role = (
        "Tu es le PlannerAgent. En te basant sur les impacts décrits, rédige un plan d’action "
        "structuré en 3 à 5 étapes concrètes avec priorités."
    )
    return ask_agent(role, eco_report)


def CoordinatorAgent(analysis, eco_report, plan):
    role = (
        "Tu es le CoordinatorAgent. Fusionne les résultats précédents pour générer un résumé global clair.\n"
        "Structure la réponse avec les titres suivants :\n"
        "Solution, Impact écologique, Impact social, Impact économique, Plan d’action."
    )
    full_text = f"{analysis}\n\n{eco_report}\n\n{plan}"
    return ask_agent(role, full_text)

# ==============================
# 🏡 INTERFACE STREAMLIT
# ==============================

st.title("🏡 Formulaire Pilote d'impact")
st.markdown("""
### 🌍 Rejoignez EVAD pour co-développer votre projet de lieux régénératif !

Bienvenue dans **EVAD - Écosystème Vivant Autonome et Décentralisé**, une plateforme de pilotage d’impact
conçue pour la création de lieux partagés durables *(tiers-lieux, éco-lieux, coworking, fermes, etc.)*
grâce à une intelligence multi-agents, open-source et régénérative.
""")

if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1

with st.form("user_form"):
    st.subheader("🧾 Informations sur le projet")

    title = st.text_input("🏷️ Nom du projet")
    description = st.text_area("📝 Description du projet")
    localisation = st.text_input("📍 Localisation")

    # Espaces
    st.markdown("### 🏡 Espaces du projet")
    espaces = []
    for i in range(st.session_state.nb_espaces):
        espaces.append(st.text_area(f"🏠 Espace {i+1}", key=f"espace_{i+1}", height=80))

    if st.session_state.nb_espaces < 5:
        if st.form_submit_button("➕ Ajouter un espace"):
            st.session_state.nb_espaces += 1
            st.rerun()

    uploaded_doc = st.file_uploader("📄 Document lié (optionnel)", type=["pdf", "png", "jpg", "jpeg", "docx"])
    submitted = st.form_submit_button("🚀 Lancer l’analyse multi-agents")

# ==============================
# 🧠 FLUX DES AGENTS
# ==============================
if submitted:
    if not all([title, description, localisation]):
        st.warning("Merci de remplir tous les champs avant l’analyse.")
    else:
        with st.spinner("🤖 Les agents coopèrent pour analyser votre projet..."):
            try:
                analysis = AnalystAgent(title, description, localisation)
                eco_report = EcoAgent(analysis)
                plan = PlannerAgent(eco_report)
                final_result = CoordinatorAgent(analysis, eco_report, plan)
                st.session_state.final_result = final_result
                st.success("🌿 Analyse multi-agents terminée avec succès !")
            except Exception as e:
                st.error(f"Erreur pendant l’analyse : {e}")

# ==============================
# ✏️ SYNTHÈSE ET ENREGISTREMENT
# ==============================
if "final_result" in st.session_state:
    st.subheader("📋 Synthèse générée par les agents")
    st.text_area("Résultat multi-agents", st.session_state.final_result, height=300)

    with st.form("porteur_form"):
        st.subheader("👤 Informations du porteur")
        leader = st.text_input("Nom du porteur de projet")
        email = st.text_input("Email de contact")
        status = st.selectbox("📊 Statut du projet", ["Thinking", "Modélisation ", "Construction", "Développement", "Financement", "Student"], index=0)
        saved = st.form_submit_button("💾 Enregistrer dans NoCoDB")

        if saved:
            headers = {"xc-token": NOCODB_API_TOKEN, "Content-Type": "application/json"}
            payload = {
                "Title": title,
                "Description": st.session_state.final_result,
                "Localisation": localisation,
                "Project Leader": leader,
                "Email": email,
                "Status": status,
                "espace 1": espaces[0] if len(espaces) > 0 else "",
                "espace 2": espaces[1] if len(espaces) > 1 else "",
                "espace 3": espaces[2] if len(espaces) > 2 else "",
                "espace 4": espaces[3] if len(espaces) > 3 else "",
                "espace 5": espaces[4] if len(espaces) > 4 else "",
            }
            r = requests.post(NOCODB_API_URL, headers=headers, json=payload)
            if r.status_code in (200, 201):
                st.success("🍃 Projet enregistré avec succès dans `Projects` ! 🌍")
                st.toast("✅ Données synchronisées avec NoCoDB", icon="🌱")
            else:
                st.error(f"Erreur API {r.status_code} : {r.text}")
