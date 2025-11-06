# -*- coding: utf-8 -*-
import streamlit as st
import requests
import re
import base64
import json

# --- EN-TÊTE EVAD (logo centré, net et sans cadre) ---
@st.cache_data
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

logo_base64 = get_base64_image("evad_logo.png")

if logo_base64:
    st.markdown(f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 10px;
        ">
            <img src="data:image/png;base64,{logo_base64}"
                 width="240"
                 style="margin: 0 auto; display: block; image-rendering: -webkit-optimize-contrast; -ms-interpolation-mode: nearest-neighbor;">
            <h1 style="font-size: 2.1em; color: #014d3b; margin-top: 10px; margin-bottom: 5px; text-align: center;">
                Formulaire Pilote d'impact
            </h1>
        </div>
        <hr style="border: none; height: 2px; background-color: #cfeee7; margin: 5px 0 20px 0;">
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <h1 style="text-align:center; color:#014d3b;">Formulaire Pilote d'impact</h1>
        <hr style="border: none; height: 2px; background-color: #cfeee7; margin: 10px 0 20px 0;">
    """, unsafe_allow_html=True)

# --- STYLE GLOBAL ---
st.markdown("""
<style>
body {
    background-color: #ffffff;
    color: #000000 !important;
}
div.block-container {
    background-color: #ffffff !important;
    padding: 25px !important;
}
div.stForm {
    background-color: #018262 !important;
    border-radius: 20px;
    padding: 25px !important;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
}
div.stForm > div {
    background-color: #cfeee7 !important;
    color: #014d3b !important;
    border-radius: 15px;
    padding: 20px;
    margin: 0;
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
    background-color: #018262 !important;
    color: white !important;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}
.stButton button:hover {
    background-color: #01614c !important;
}
</style>
""", unsafe_allow_html=True)

# --- CONFIGURATION ---
st.set_page_config(page_title="Formulaire Pilote d'impact", page_icon="🏡", layout="centered")

# --- Sélecteur de langue stylisé ---
st.markdown("""
<style>
.lang-switch {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 25px;
}
.lang-button {
  border: 2px solid #018262;
  color: #018262;
  background-color: white;
  font-weight: bold;
  padding: 8px 20px;
  border-radius: 30px;
  margin: 0 5px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}
.lang-button:hover {
  background-color: #cfeee7;
  color: #014d3b;
}
.lang-active {
  background-color: #018262;
  color: white;
  border-color: #018262;
}
</style>
""", unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state.lang = "Français"

col1, col2 = st.columns(2)
with col1:
    if st.button("🇫🇷 Français", key="fr_button", 
                 help="Basculer l'interface en Français",
                 use_container_width=True):
        st.session_state.lang = "Français"
        st.rerun()
with col2:
    if st.button("🇬🇧 English", key="en_button", 
                 help="Switch interface to English",
                 use_container_width=True):
        st.session_state.lang = "English"
        st.rerun()

# --- Sous-titre descriptif (corrigé) ---
if st.session_state.lang == "English":
    st.markdown("""
    ### 🌍 Join EVAD to co-develop your regenerative place project!
    Welcome to **EVAD - Autonomous and Decentralized Living Ecosystem**, a platform for impact management
    designed to create sustainable shared spaces *(third places, eco-spaces, coworking, farms, etc.)*
    through collaborative, open-source, and regenerative intelligence.
    """)
else:
    st.markdown("""
    ### 🌍 Rejoignez EVAD pour co-développer votre projet de lieux régénératif !
    Bienvenue dans **EVAD - Écosystème Vivant Autonome et Décentralisé**, une plateforme de pilotage
    d’impact conçue pour la création de lieux partagés durables *(tiers-lieux, éco-lieux, coworking, fermes, etc.)*
    grâce à une intelligence collaborative, open-source et régénérative.
    """)

# --- SECRETS ---
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
NOCODB_API_TOKEN = st.secrets["NOCODB_API_TOKEN"]
NOCODB_API_URL = st.secrets["NOCODB_API_URL"]

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}

# --- NoCoDB CONFIG ---
NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"
NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/mzaor3uiob3gbe2/records"

# ==============================
# ⚡ FUSION INTELLIGENTE MULTI-AGENTS
# ==============================
def ask_agent(role_description, user_input):
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

def MultiAgentFusion(title, description, objectif, localisation):
    if st.session_state.lang == "English":
        role = (
            "You are a collaborative system composed of 4 experts: AnalystAgent, EcoAgent, PlannerAgent, and CoordinatorAgent. "
            "Together, you analyze the project and produce the following sections formatted exactly as follows:\n\n"
            "Solution: ...\n"
            "Ecological impact: ...\n"
            "Social impact: ...\n"
            "Economic impact: ...\n"
            "Action plan: ... (3 to 5 concrete steps)\n\n"
            "Be concise, professional, and clear."
        )
    else:
        role = (
            "Tu es un système collaboratif composé de 4 experts : AnalystAgent, EcoAgent, PlannerAgent et CoordinatorAgent. "
            "Ensemble, vous analysez le projet et produisez les sections suivantes, formatées exactement comme ceci :\n\n"
            "Solution: ...\n"
            "Impact écologique: ...\n"
            "Impact social: ...\n"
            "Impact économique: ...\n"
            "Plan d’action: ... (3 à 5 étapes concrètes)\n\n"
            "Sois concis, professionnel et clair dans chaque section."
        )

    user_input = f"Project: {title}\nDescription: {description}\nObjective: {objectif}\nLocation: {localisation}"
    return ask_agent(role, user_input)

# ==============================
# INTERFACE STREAMLIT
# ==============================
if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1

with st.form("user_form"):
    st.markdown("""
        <h2 style='margin-bottom: 0;'>📘 Présentation du projet</h2>
        <p style='margin-top: 2px; color:#014d3b; font-style: italic;'>
            Informations sur le projet de lieu durable
        </p>
    """, unsafe_allow_html=True)

    title = st.text_input("🏷️ Nom du projet")
    description = st.text_area("📝 Description du projet", height=100)
    objectif = st.text_area("🎯 Objectif du projet", height=100)
    localisation = st.text_input("📍 Localisation")

    # Espaces dynamiques
    st.markdown("""
        <h3 style='margin-bottom: 0;'>📂 Détails du projet par espace</h3>
        <p style='margin-top: 2px; color:#014d3b; font-style: italic;'>
            Informations sur chaque espace qui compose le projet
        </p>
    """, unsafe_allow_html=True)

    espaces = []
    for i in range(st.session_state.nb_espaces):
        espaces.append(st.text_area(f"🏠 Espace {i+1}", key=f"espace_{i+1}", height=80))

    if st.session_state.nb_espaces < 5:
        if st.form_submit_button("➕ Ajouter un espace"):
            st.session_state.nb_espaces += 1
            st.rerun()

    uploaded_doc = st.file_uploader("📄 Document lié (optionnel)", type=["pdf", "png", "jpg", "jpeg", "docx"])
    submitted = st.form_submit_button("🚀 Lancer l’analyse du projet")

# ==============================
#  ANALYSE DU PROJET
# ==============================
if submitted:
    if not all([title, description, objectif, localisation]):
        st.warning("Merci de remplir tous les champs avant l’analyse.")
    else:
        with st.spinner("🌱 Analyse du projet en cours..."):
            try:
                final_result = MultiAgentFusion(title, description, objectif, localisation)
                st.session_state.final_result = final_result
                st.success("✅ Analyse du projet terminée avec succès !")
                st.rerun()
            except Exception as e:
                st.error(f"Erreur pendant l’analyse : {e}")

# ==============================
#  SYNTHÈSE DU PROJET
# ==============================
if "final_result" in st.session_state:
    with st.form("synthese_form"):
        st.subheader("📋 Synthèse du projet")

        def extract_section(text, section):
            pattern = rf"{section}\s*[:：\-–]?\s*(.*?)(?=\n(?:Solution|Objectif|Impact|Plan|$))"
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else ""

        text = st.session_state.final_result

        objectif = extract_section(text, "Solution")
        impact_eco = extract_section(text, "Impact écologique") or extract_section(text, "Ecological impact")
        impact_social = extract_section(text, "Impact social") or extract_section(text, "Social impact")
        impact_econ = extract_section(text, "Impact économique") or extract_section(text, "Economic impact")
        plan_action = extract_section(text, "Plan d’action") or extract_section(text, "Action plan")

        st.session_state.objectif = st.text_area("🎯 Objectif du projet", objectif, height=100)
        st.session_state.impact_eco = st.text_area("🌿 Impact écologique", impact_eco, height=70)
        st.session_state.impact_social = st.text_area("🤝 Impact social", impact_social, height=70)
        st.session_state.impact_econ = st.text_area("💰 Impact économique", impact_econ, height=70)
        st.session_state.plan_action = st.text_area("🧭 Plan d’action", plan_action, height=140)
# --- Si le plan d’action est vide → régénération automatique ---
if not plan_action or len(plan_action) < 10:
    try:
        role = (
            "Tu es un expert en développement durable. "
            "Génère un plan d’action clair avec 3 à 5 étapes courtes et concrètes."
        )
        user_input = f"Projet: {objectif}\nImpacts: {impact_eco}, {impact_social}, {impact_econ}"
        payload = {
            "model": "mistralai/mistral-nemo",
            "messages": [
                {"role": "system", "content": role},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.6,
            "max_tokens": 200
        }
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()
        plan_action = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except Exception as e:
        plan_action = f"(Erreur génération du plan : {e})"


        validated = st.form_submit_button("✅ Valider et ajouter les informations du porteur")
        if validated:
            st.session_state.validation_ok = True
            st.success("✅ Sections validées avec succès !")

# ==============================
# 🧑‍💼 ENREGISTREMENT FINAL
# ==============================
if st.session_state.get("validation_ok"):
    with st.form("porteur_form"):
        st.subheader("👤 Présentation du porteur")
        leader = st.text_input("Nom du porteur de projet")
        email = st.text_input("Email de contact")
        status = st.selectbox(
            "📊 Étape du projet",
            ["Thinking", "Modélisation", "Construction", "Développement", "Financement", "Student"],
            index=0
        )

        saved = st.form_submit_button("💾 Enregistrer dans la base EVAD")

        if saved:
            headers = {"xc-token": NOCODB_API_TOKEN, "Accept": "application/json"}

            payload = {
                "Title": title,
                "Description": description,
                "Localisation": localisation,
                "Project Leader": leader,
                "Email": email,
                "Status": status,
                "Objectif du projet": st.session_state.objectif,
                "Impact écologique": st.session_state.impact_eco,
                "Impact social": st.session_state.impact_social,
                "Impact économique": st.session_state.impact_econ,
                "Plan d’action": st.session_state.plan_action,
            }

            try:
                r = requests.post(NOCODB_API_URL, headers=headers, json=payload)
                if r.status_code in (200, 201):
                    st.success("🌿 Projet enregistré avec succès dans la base EVAD !")
                    st.toast("Projet enregistré avec succès", icon="🌱")
                else:
                    st.error(f"Erreur API {r.status_code} : {r.text}")
            except Exception as e:
                st.error(f"❌ Erreur lors de l’envoi à NoCoDB : {e}")


