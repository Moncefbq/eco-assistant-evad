# -*- coding: utf-8 -*-
import streamlit as st
import requests
import re
import base64
import json

# ===============================
# 🏡 CONFIGURATION ET STYLE
# ===============================
st.set_page_config(page_title="Formulaire Pilote d'impact", page_icon="🏡", layout="centered")

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
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 20px; margin-bottom: 10px;">
            <img src="data:image/png;base64,{logo_base64}" width="240" style="margin: 0 auto; display: block;">
            <h1 style="font-size: 2.1em; color: #014d3b; margin-top: 10px; margin-bottom: 5px; text-align: center;">
                Formulaire Pilote d'impact
            </h1>
        </div>
        <hr style="border: none; height: 2px; background-color: #cfeee7; margin: 5px 0 20px 0;">
    """, unsafe_allow_html=True)

# --- STYLE GLOBAL ---
st.markdown("""
<style>
body { background-color: #ffffff; color: #000000 !important; }
div.block-container { background-color: #ffffff !important; padding: 25px !important; }
div.stForm { background-color: #018262 !important; border-radius: 20px; padding: 25px !important; box-shadow: 0px 4px 15px rgba(0,0,0,0.15); }
div.stForm > div { background-color: #cfeee7 !important; color: #014d3b !important; border-radius: 15px; padding: 20px; margin: 0; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div, .stMultiSelect > div > div {
    background-color: #ffffff !important; color: #000000 !important; border-radius: 6px; border: 1px solid #555 !important;
}
.stButton button { background-color: #018262 !important; color: white !important; border-radius: 8px; border: none; font-weight: bold; }
.stButton button:hover { background-color: #01614c !important; }
</style>
""", unsafe_allow_html=True)

# ===============================
# 🌐 SÉLECTEUR DE LANGUE
# ===============================
if "lang" not in st.session_state:
    st.session_state.lang = "Français"

col1, col2 = st.columns(2)
with col1:
    if st.button("🇫🇷 Français", use_container_width=True):
        st.session_state.lang = "Français"
        st.rerun()
with col2:
    if st.button("🇬🇧 English", use_container_width=True):
        st.session_state.lang = "English"
        st.rerun()

# ===============================
# 🗣️ TEXTES MULTILINGUES
# ===============================
if st.session_state.lang == "English":
    T = {
        "intro_title": "🌍 Join EVAD to co-develop your regenerative place project!",
        "intro_desc": (
            "Welcome to **EVAD - Autonomous and Decentralized Living Ecosystem**, "
            "a platform for impact management designed to create sustainable shared spaces "
            "(*third places, eco-spaces, coworking, farms, etc.*) "
            "through collaborative, open-source, and regenerative intelligence."
        ),
        "form_title": "📘 Project Overview",
        "form_desc": "Information about your sustainable place project",
        "project_name": "🏷️ Project Name",
        "description": "📝 Project Description",
        "objective": "🎯 Project Objective",
        "location": "📍 Location",
        "space_details": "📂 Project Details by Space",
        "space_desc": "Information about each space within the project",
        "add_space": "➕ Add a Space",
        "upload_doc": "📄 Related Document (optional)",
        "analyze": "🚀 Launch Project Analysis",
        "summary": "📋 Project Summary",
        "eco_impact": "🌿 Ecological Impact",
        "social_impact": "🤝 Social Impact",
        "econ_impact": "💰 Economic Impact",
        "plan_action": "🧭 Action Plan",
        "validate": "✅ Validate and Add Project Owner Information",
        "owner_title": "👤 Project Owner Information",
        "owner_name": "Project Leader Name",
        "owner_email": "Contact Email",
        "status": "📊 Project Stage",
        "save": "💾 Save to EVAD Database",
        "success_analysis": "✅ Project analysis completed successfully!",
        "success_save": "🌿 Project successfully saved to the EVAD database!",
        "analysis_loading": "🌱 Analyzing your project...",
        "fill_warning": "Please fill out all required fields before launching the analysis.",
    }
else:
    T = {
        "intro_title": "🌍 Rejoignez EVAD pour co-développer votre projet de lieux régénératif !",
        "intro_desc": (
            "Bienvenue dans **EVAD - Écosystème Vivant Autonome et Décentralisé**, "
            "une plateforme de pilotage d’impact conçue pour la création de lieux partagés durables "
            "(*tiers-lieux, éco-lieux, coworking, fermes, etc.*) "
            "grâce à une intelligence collaborative, open-source et régénérative."
        ),
        "form_title": "📘 Présentation du projet",
        "form_desc": "Informations sur le projet de lieu durable",
        "project_name": "🏷️ Nom du projet",
        "description": "📝 Description du projet",
        "objective": "🎯 Objectif du projet",
        "location": "📍 Localisation",
        "space_details": "📂 Détails du projet par espace",
        "space_desc": "Informations sur chaque espace qui compose le projet",
        "add_space": "➕ Ajouter un espace",
        "upload_doc": "📄 Document lié (optionnel)",
        "analyze": "🚀 Lancer l’analyse du projet",
        "summary": "📋 Synthèse du projet",
        "eco_impact": "🌿 Impact écologique",
        "social_impact": "🤝 Impact social",
        "econ_impact": "💰 Impact économique",
        "plan_action": "🧭 Plan d’action",
        "validate": "✅ Valider et ajouter les informations du porteur",
        "owner_title": "👤 Présentation du porteur",
        "owner_name": "Nom du porteur de projet",
        "owner_email": "Email de contact",
        "status": "📊 Étape du projet",
        "save": "💾 Enregistrer dans la base EVAD",
        "success_analysis": "✅ Analyse du projet terminée avec succès !",
        "success_save": "🌿 Projet enregistré avec succès dans la base EVAD !",
        "analysis_loading": "🌱 Analyse du projet en cours...",
        "fill_warning": "Merci de remplir tous les champs avant l’analyse.",
    }

# ===============================
# 🌍 INTRODUCTION
# ===============================
st.markdown(f"### {T['intro_title']}")
st.markdown(T["intro_desc"])

# ===============================
# ⚙️ CONFIG API
# ===============================
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
NOCODB_API_TOKEN = st.secrets["NOCODB_API_TOKEN"]
NOCODB_API_URL = st.secrets["NOCODB_API_URL"]

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}

# ===============================
# 🤖 MULTI-AGENT AI
# ===============================
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

def MultiAgentFusion(title, description, objectif, localisation, lang):
    if lang == "English":
        role = (
            "You are a collaborative system made of 4 experts: AnalystAgent, EcoAgent, PlannerAgent, and CoordinatorAgent. "
            "Together you analyze the project and generate these sections:\n\n"
            "Solution: ...\nEcological impact: ...\nSocial impact: ...\nEconomic impact: ...\nAction plan: ... (3 to 5 concrete steps)"
        )
        user_input = f"Project: {title}\nDescription: {description}\nObjective: {objectif}\nLocation: {localisation}"
    else:
        role = (
            "Tu es un système collaboratif composé de 4 experts : AnalystAgent, EcoAgent, PlannerAgent et CoordinatorAgent. "
            "Ensemble, vous analysez le projet et produisez les sections suivantes : "
            "Solution, Impact écologique, Impact social, Impact économique, Plan d’action (3 à 5 étapes concrètes)."
        )
        user_input = f"Projet: {title}\nDescription: {description}\nObjectif: {objectif}\nLocalisation: {localisation}"
    return ask_agent(role, user_input)

# ===============================
# 🧾 FORMULAIRE PRINCIPAL
# ===============================
if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1

with st.form("user_form"):
    st.markdown(f"<h2>{T['form_title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#014d3b; font-style:italic;'>{T['form_desc']}</p>", unsafe_allow_html=True)

    title = st.text_input(T["project_name"])
    description = st.text_area(T["description"], height=100)
    objectif = st.text_area(T["objective"], height=100)
    localisation = st.text_input(T["location"])

    st.markdown(f"<h3>{T['space_details']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#014d3b; font-style:italic;'>{T['space_desc']}</p>", unsafe_allow_html=True)

    espaces = []
    for i in range(st.session_state.nb_espaces):
        espaces.append(st.text_area(f"🏠 {'Space' if st.session_state.lang == 'English' else 'Espace'} {i+1}", key=f"espace_{i+1}", height=80))

    if st.session_state.nb_espaces < 5:
        if st.form_submit_button(T["add_space"]):
            st.session_state.nb_espaces += 1
            st.rerun()

    uploaded_doc = st.file_uploader(T["upload_doc"], type=["pdf", "png", "jpg", "jpeg", "docx"])
    submitted = st.form_submit_button(T["analyze"])

# ===============================
# 🔍 ANALYSE DU PROJET
# ===============================
if submitted:
    if not all([title, description, objectif, localisation]):
        st.warning(T["fill_warning"])
    else:
        with st.spinner(T["analysis_loading"]):
            try:
                final_result = MultiAgentFusion(title, description, objectif, localisation, st.session_state.lang)
                st.session_state.final_result = final_result
                st.success(T["success_analysis"])
            except Exception as e:
                st.error(f"Error: {e}")

# ===============================
# 📋 SYNTHÈSE DU PROJET
# ===============================
if "final_result" in st.session_state:
    with st.form("synthese_form"):
        st.subheader(T["summary"])

        def extract_section(text, section):
            pattern = rf"{section}\s*[:：\-–]?\s*(.*?)(?=\n(?:Solution|Impact|Plan|$))"
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else ""

        text = st.session_state.final_result
        objectif = extract_section(text, "Solution")
        impact_eco = extract_section(text, "Impact écologique") or extract_section(text, "Ecological impact")
        impact_social = extract_section(text, "Impact social") or extract_section(text, "Social impact")
        impact_econ = extract_section(text, "Impact économique") or extract_section(text, "Economic impact")
        plan_action = extract_section(text, "Plan d’action") or extract_section(text, "Action plan")

        st.session_state.objectif = st.text_area(T["objective"], objectif, height=100)
        st.session_state.impact_eco = st.text_area(T["eco_impact"], impact_eco, height=70)
        st.session_state.impact_social = st.text_area(T["social_impact"], impact_social, height=70)
        st.session_state.impact_econ = st.text_area(T["econ_impact"], impact_econ, height=70)
        st.session_state.plan_action = st.text_area(T["plan_action"], plan_action, height=140)

        validated = st.form_submit_button(T["validate"])
        if validated:
            st.session_state.validation_ok = True
            st.success("✅ OK")

# ===============================
# 👤 INFORMATIONS PORTEUR
# ===============================
if st.session_state.get("validation_ok"):
    with st.form("porteur_form"):
        st.subheader(T["owner_title"])
        leader = st.text_input(T["owner_name"])
        email = st.text_input(T["owner_email"])
        status = st.selectbox(T["status"], ["Thinking", "Modeling", "Construction", "Development", "Funding", "Student"])
        saved = st.form_submit_button(T["save"])

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
                    st.success(T["success_save"])
                else:
                    st.error(f"Erreur API {r.status_code} : {r.text}")
            except Exception as e:
                st.error(f"❌ Error: {e}")



