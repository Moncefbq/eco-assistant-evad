# -*- coding: utf-8 -*-
import streamlit as st
import requests
import re
import base64
import json

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="Formulaire Pilote d'impact", page_icon="🏡", layout="centered")

# --- Sélecteur langue en haut à droite ---
col1, col2, col3 = st.columns([4, 1, 1])
with col3:
    langue = st.selectbox("🌐", ["Français", "English"], index=0, label_visibility="collapsed")

# --- Dictionnaire de texte bilingue ---
TEXTS = {
    "Français": {
        "form_title": "Formulaire Pilote d'impact",
        "intro_title": "🌍 Rejoignez EVAD pour co-développer votre projet de lieux régénératif !",
        "intro_text": "Bienvenue dans **EVAD – Écosystème Vivant Autonome et Décentralisé**, une plateforme de pilotage d’impact conçue pour la création de lieux partagés durables *(tiers-lieux, éco-lieux, coworking, fermes, etc.)* grâce à une intelligence collaborative, open-source et régénérative.",
        "proj_presentation": "📘 Présentation du projet",
        "proj_info": "Informations sur le projet de lieu durable",
        "proj_name": "🏷️ Nom du projet",
        "proj_desc": "📝 Description du projet",
        "proj_goal": "🎯 Objectif du projet",
        "proj_loc": "📍 Localisation",
        "add_space": "➕ Ajouter un espace",
        "upload_doc": "📄 Document lié (optionnel)",
        "analyze": "🚀 Lancer l’analyse du projet",
        "analyzing": "🌱 Analyse du projet en cours...",
        "analyze_done": "✅ Analyse du projet terminée avec succès !",
        "fill_warn": "Merci de remplir tous les champs avant l’analyse.",
        "synth_title": "📋 Synthèse du projet",
        "leader": "Nom du porteur de projet",
        "email": "Email de contact",
        "status": "📊 Étape du projet",
        "save": "💾 Enregistrer dans la base EVAD",
        "success": "🌿 Projet enregistré avec succès dans la base EVAD !",
        "toast": "Projet enregistré avec succès"
    },
    "English": {
        "form_title": "Impact Pilot Form",
        "intro_title": "🌍 Join EVAD to co-develop your regenerative place project!",
        "intro_text": "Welcome to **EVAD – Living Autonomous & Decentralized Ecosystem**, a platform designed to guide the creation of shared sustainable places *(third places, eco-farms, coworking hubs, etc.)* through collaborative, open-source and regenerative intelligence.",
        "proj_presentation": "📘 Project Overview",
        "proj_info": "Information about the sustainable place project",
        "proj_name": "🏷️ Project Name",
        "proj_desc": "📝 Project Description",
        "proj_goal": "🎯 Project Objective",
        "proj_loc": "📍 Location",
        "add_space": "➕ Add a space",
        "upload_doc": "📄 Related Document (optional)",
        "analyze": "🚀 Launch Project Analysis",
        "analyzing": "🌱 Analyzing project...",
        "analyze_done": "✅ Project analysis completed successfully!",
        "fill_warn": "Please fill in all fields before analysis.",
        "synth_title": "📋 Project Summary",
        "leader": "Project Leader Name",
        "email": "Contact Email",
        "status": "📊 Project Stage",
        "save": "💾 Save to EVAD database",
        "success": "🌿 Project successfully saved to EVAD database!",
        "toast": "Project saved successfully"
    }
}
t = TEXTS[langue]

# --- EN-TÊTE EVAD ---
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
                {t["form_title"]}
            </h1>
        </div>
        <hr style="border:none;height:2px;background-color:#cfeee7;margin:5px 0 20px 0;">
    """, unsafe_allow_html=True)

# --- STYLE GLOBAL ---
st.markdown("""
<style>
body {background-color:#fff;color:#000!important}
div.block-container {background:#fff!important;padding:25px!important}
div.stForm {background:#018262!important;border-radius:20px;padding:25px!important;box-shadow:0 4px 15px rgba(0,0,0,.15)}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:#fff!important;color:#000!important;border-radius:6px;border:1px solid #555!important}
.stButton button{background:#018262!important;color:white!important;border-radius:8px;font-weight:bold}
.stButton button:hover{background:#01614c!important}
</style>
""", unsafe_allow_html=True)

# --- INTRO ---
st.markdown(f"### {t['intro_title']}\n{t['intro_text']}")

# --- CONFIG API ---
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
NOCODB_API_TOKEN = st.secrets["NOCODB_API_TOKEN"]
NOCODB_API_URL = st.secrets["NOCODB_API_URL"]

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}

# ==============================
# ⚡ IA MULTI-LANGUE
# ==============================
def ask_agent(langue, title, description, objectif, localisation):
    if langue == "Français":
        role = ("Tu es un système collaboratif composé de 4 experts : AnalystAgent, EcoAgent, PlannerAgent et CoordinatorAgent. "
                "Réponds uniquement en français avec les sections : Solution, Impact écologique, Impact social, Impact économique, Plan d’action.")
    else:
        role = ("You are a collaborative system of 4 experts: AnalystAgent, EcoAgent, PlannerAgent, and CoordinatorAgent. "
                "Answer only in English with the sections: Solution, Ecological Impact, Social Impact, Economic Impact, Action Plan.")
    payload = {
        "model": "mistralai/mistral-nemo",
        "messages": [{"role": "system", "content": role},
                     {"role": "user", "content": f"Title: {title}\nDescription: {description}\nGoal: {objectif}\nLocation: {localisation}"}],
        "temperature": 0.7,
        "max_tokens": 800
    }
    try:
        requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    except:
        pass

# ==============================
# FORMULAIRE PRINCIPAL
# ==============================
if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1

with st.form("user_form"):
    st.markdown(f"<h2>{t['proj_presentation']}</h2><p><i>{t['proj_info']}</i></p>", unsafe_allow_html=True)
    title = st.text_input(t["proj_name"])
    description = st.text_area(t["proj_desc"], height=100)
    objectif = st.text_area(t["proj_goal"], height=100)
    localisation = st.text_input(t["proj_loc"])

    espaces = []
    for i in range(st.session_state.nb_espaces):
        espaces.append(st.text_area(f"🏠 Espace {i+1}", key=f"espace_{i+1}", height=80))

    if st.session_state.nb_espaces < 5:
        if st.form_submit_button(t["add_space"]):
            st.session_state.nb_espaces += 1
            st.rerun()

    uploaded_doc = st.file_uploader(t["upload_doc"], type=["pdf", "png", "jpg", "jpeg", "docx"])
    submitted = st.form_submit_button(t["analyze"])

# --- Analyse IA ---
if submitted:
    if not all([title, description, objectif, localisation]):
        st.warning(t["fill_warn"])
    else:
        ask_agent(langue, title, description, objectif, localisation)
        st.session_state.final_result = True

# ==============================
# ENREGISTREMENT FINAL
# ==============================
if st.session_state.get("final_result"):
    with st.form("porteur_form"):
        st.subheader("👤 Présentation du porteur")
        leader = st.text_input(t["leader"])
        email = st.text_input(t["email"])
        status = st.selectbox(t["status"], ["Thinking", "Modélisation", "Construction", "Développement", "Financement", "Student"])
        saved = st.form_submit_button(t["save"])

        if saved:
            st.success(t["success"])
            st.toast(t["toast"], icon="🌱")


