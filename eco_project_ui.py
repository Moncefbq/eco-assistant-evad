# -*- coding: utf-8 -*-
import streamlit as st
import requests
import re
import base64
import json

# ============================================
# 🔰 EN-TÊTE EVAD AVEC LOGO
# ============================================
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
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;margin-top:20px;margin-bottom:10px;">
            <img src="data:image/png;base64,{logo_base64}" width="240" style="margin:0 auto;display:block;">
            <h1 style="font-size:2.1em;color:#014d3b;margin-top:10px;margin-bottom:5px;text-align:center;">
                Formulaire Pilote d'impact
            </h1>
        </div>
        <hr style="border:none;height:2px;background-color:#cfeee7;margin:5px 0 20px 0;">
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <h1 style="text-align:center;color:#014d3b;">Formulaire Pilote d'impact</h1>
        <hr style="border:none;height:2px;background-color:#cfeee7;margin:10px 0 20px 0;">
    """, unsafe_allow_html=True)

# ============================================
# 🎨 STYLE GLOBAL
# ============================================
st.markdown("""
<style>
body{background-color:#fff;color:#000!important;}
div.block-container{background-color:#fff!important;padding:25px!important;}
div.stForm{background-color:#018262!important;border-radius:20px;padding:25px!important;box-shadow:0 4px 15px rgba(0,0,0,0.15);}
div.stForm>div{background-color:#cfeee7!important;color:#014d3b!important;border-radius:15px;padding:20px;margin:0;}
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div{background-color:#fff!important;color:#000!important;border-radius:6px;border:1px solid #555!important;}
h1,h2,h3,h4,h5,h6,label,p,span,div{color:#000!important;}
.stButton button{background-color:#018262!important;color:white!important;border-radius:8px;border:none;font-weight:bold;}
.stButton button:hover{background-color:#01614c!important;}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Formulaire Pilote d'impact", page_icon="🏡", layout="centered")

# ============================================
# 🌐 CHOIX DE LANGUE
# ============================================
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

# ============================================
# 🗣️ DICTIONNAIRE MULTILINGUE
# ============================================
if st.session_state.lang == "English":
    T = {
        "intro_title": "🌍 Join EVAD to co-develop your regenerative place project!",
        "intro_desc": "Welcome to **EVAD - Autonomous and Decentralized Living Ecosystem**, a platform for impact management designed to create sustainable shared spaces *(third places, eco-spaces, coworking, farms, etc.)* through collaborative, open-source, and regenerative intelligence.",
        "form_title": "📘 Project Overview",
        "form_desc": "Information about your sustainable place project",
        "name": "🏷️ Project Name",
        "desc": "📝 Project Description",
        "obj": "🎯 Project Objective",
        "loc": "📍 Location",
        "space_title": "📂 Project Details by Space",
        "space_desc": "Information about each space in the project",
        "add_space": "➕ Add a Space",
        "doc": "📄 Related Document (optional)",
        "launch": "🚀 Launch Project Analysis",
        "analyzing": "🌱 Project analysis in progress...",
        "success_analysis": "✅ Project analysis completed successfully!",
        "warn_fill": "Please fill all required fields before analysis.",
        "summary": "📋 Project Summary",
        "eco": "🌿 Ecological Impact",
        "social": "🤝 Social Impact",
        "econ": "💰 Economic Impact",
        "plan": "🧭 Action Plan",
        "validate": "✅ Validate and Add Project Owner Info",
        "success_validate": "✅ Sections validated successfully!",
        "owner": "👤 Project Owner Information",
        "leader": "Project Leader Name",
        "email": "Contact Email",
        "status": "📊 Project Stage",
        "save": "💾 Save to EVAD Database",
        "success_save": "🌿 Project saved successfully to EVAD database!",
        "err_analysis": "Error during project analysis:",
    }
else:
    T = {
        "intro_title": "🌍 Rejoignez EVAD pour co-développer votre projet de lieux régénératif !",
        "intro_desc": "Bienvenue dans **EVAD - Écosystème Vivant Autonome et Décentralisé**, une plateforme de pilotage d’impact conçue pour la création de lieux partagés durables *(tiers-lieux, éco-lieux, coworking, fermes, etc.)* grâce à une intelligence collaborative, open-source et régénérative.",
        "form_title": "📘 Présentation du projet",
        "form_desc": "Informations sur le projet de lieu durable",
        "name": "🏷️ Nom du projet",
        "desc": "📝 Description du projet",
        "obj": "🎯 Objectif du projet",
        "loc": "📍 Localisation",
        "space_title": "📂 Détails du projet par espace",
        "space_desc": "Informations sur chaque espace qui compose le projet",
        "add_space": "➕ Ajouter un espace",
        "doc": "📄 Document lié (optionnel)",
        "launch": "🚀 Lancer l’analyse du projet",
        "analyzing": "🌱 Analyse du projet en cours...",
        "success_analysis": "✅ Analyse du projet terminée avec succès !",
        "warn_fill": "Merci de remplir tous les champs avant l’analyse.",
        "summary": "📋 Synthèse du projet",
        "eco": "🌿 Impact écologique",
        "social": "🤝 Impact social",
        "econ": "💰 Impact économique",
        "plan": "🧭 Plan d’action",
        "validate": "✅ Valider et ajouter les informations du porteur",
        "success_validate": "✅ Sections validées avec succès !",
        "owner": "👤 Présentation du porteur",
        "leader": "Nom du porteur de projet",
        "email": "Email de contact",
        "status": "📊 Étape du projet",
        "save": "💾 Enregistrer dans la base EVAD",
        "success_save": "🌿 Projet enregistré avec succès dans la base EVAD !",
        "err_analysis": "Erreur pendant l’analyse :",
    }

# ============================================
# 🧩 INTRODUCTION
# ============================================
st.markdown(f"### {T['intro_title']}")
st.markdown(T["intro_desc"])

# ============================================
# 🔑 SECRETS ET API
# ============================================
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
NOCODB_API_TOKEN = st.secrets["NOCODB_API_TOKEN"]
NOCODB_API_URL = st.secrets["NOCODB_API_URL"]

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}

# NoCoDB config
NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"
NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/mzaor3uiob3gbe2/records"

# ============================================
# ⚡ BACKEND ORIGINAL (IA + MultiAgent)
# ============================================
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
    role = (
        "Tu es un système collaboratif composé de 4 experts : AnalystAgent, EcoAgent, PlannerAgent et CoordinatorAgent. "
        "Ensemble, vous analysez le projet et produisez :\n"
        "Solution : ...\nImpact écologique : ...\nImpact social : ...\nImpact économique : ...\nPlan d’action : ... (3 à 5 étapes concrètes)."
    )
    user_input = f"Projet : {title}\nDescription : {description}\nObjectif : {objectif}\nLocalisation : {localisation}"
    return ask_agent(role, user_input)

# ============================================
# 🧾 FORMULAIRE PRINCIPAL
# ============================================
if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1

with st.form("user_form"):
    st.markdown(f"<h2>{T['form_title']}</h2><p style='font-style:italic'>{T['form_desc']}</p>", unsafe_allow_html=True)
    title = st.text_input(T["name"])
    description = st.text_area(T["desc"], height=100)
    objectif = st.text_area(T["obj"], height=100)
    localisation = st.text_input(T["loc"])

    st.markdown(f"<h3>{T['space_title']}</h3><p style='font-style:italic'>{T['space_desc']}</p>", unsafe_allow_html=True)
    espaces = []
    for i in range(st.session_state.nb_espaces):
        espaces.append(st.text_area(f"🏠 {T['space_title']} {i+1}", key=f"espace_{i+1}", height=80))

    if st.session_state.nb_espaces < 5:
        if st.form_submit_button(T["add_space"]):
            st.session_state.nb_espaces += 1
            st.rerun()

    uploaded_doc = st.file_uploader(T["doc"], type=["pdf", "png", "jpg", "jpeg", "docx"])
    submitted = st.form_submit_button(T["launch"])

# ============================================
# 🔍 ANALYSE DU PROJET
# ============================================
if submitted:
    if not all([title, description, objectif, localisation]):
        st.warning(T["warn_fill"])
    else:
        with st.spinner(T["analyzing"]):
            try:
                final_result = MultiAgentFusion(title, description, objectif, localisation)
                st.session_state.final_result = final_result
                st.success(T["success_analysis"])
            except Exception as e:
                st.error(f"{T['err_analysis']} {e}")

# ============================================
# 📊 SYNTHÈSE DU PROJET
# ============================================
if "final_result" in st.session_state:
    with st.form("synthese_form"):
        st.subheader(T["summary"])
        def extract_section(text, section):
            pattern = rf"{section}\s*[:：\-–]?\s*(.*?)(?=\n(?:Solution|Objectif|Impact|Plan|$))"
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else ""
        text = st.session_state.final_result
        objectif = extract_section(text, "Solution")
        impact_eco = extract_section(text, "Impact écologique")
        impact_social = extract_section(text, "Impact social")
        impact_econ = extract_section(text, "Impact économique")
        plan_action = extract_section(text, "Plan d’action")

        st.session_state.objectif = st.text_area(T["obj"], objectif, height=100)
        st.session_state.impact_eco = st.text_area(T["eco"], impact_eco, height=70)
        st.session_state.impact_social = st.text_area(T["social"], impact_social, height=70)
        st.session_state.impact_econ = st.text_area(T["econ"], impact_econ, height=70)
        st.session_state.plan_action = st.text_area(T["plan"], plan_action, height=140)

        validated = st.form_submit_button(T["validate"])
        if validated:
            st.session_state.validation_ok = True
            st.success(T["success_validate"])

# ============================================
# 🧑‍💼 ENREGISTREMENT FINAL (NOCODB)
# ============================================
if st.session_state.get("validation_ok"):
    with st.form("porteur_form"):
        st.subheader(T["owner"])
        leader = st.text_input(T["leader"])
        email = st.text_input(T["email"])
        status = st.selectbox(
            T["status"],
            ["Thinking", "Modeling", "Construction", "Development", "Funding", "Student"] if st.session_state.lang == "English"
            else ["Réflexion", "Modélisation", "Construction", "Développement", "Financement", "Étudiant"],
            index=0
        )

        saved = st.form_submit_button(T["save"])
        if saved:
            st.success(T["success_save"])


