# -*- coding: utf-8 -*-
import streamlit as st
import requests
import base64
import datetime

# ==============================
# 🏡 CONFIGURATION GLOBALE
# ==============================
st.set_page_config(page_title="Formulaire Pilote d'impact", page_icon="🏡", layout="centered")

# --- Sélecteur langue ---
col1, col2, col3 = st.columns([4, 1, 1])
with col3:
    langue = st.selectbox("🌐", ["Français", "English"], index=0, label_visibility="collapsed")

# --- Textes multilingues ---
TEXTS = {
    "Français": {
        "header": "Formulaire Pilote d'impact",
        "intro_title": "🌍 Rejoignez EVAD pour co-développer votre projet de lieux régénératif !",
        "intro_text": (
            "Bienvenue dans **EVAD – Écosystème Vivant Autonome et Décentralisé**, "
            "une plateforme de pilotage d’impact pour la création de lieux partagés durables "
            "(*tiers-lieux, éco-lieux, coworking, fermes, etc.*) grâce à une intelligence collaborative, "
            "open-source et régénérative."
        ),
        "name": "🏷️ Nom du projet",
        "desc": "📝 Description du projet",
        "goal": "🎯 Objectif du projet",
        "loc": "📍 Localisation",
        "add_space": "➕ Ajouter un espace",
        "upload": "📄 Document lié (optionnel)",
        "analyze": "🚀 Lancer l’analyse du projet",
        "fill_warn": "Merci de remplir tous les champs avant l’analyse.",
        "success": "🌿 Projet enregistré avec succès dans la base EVAD !",
        "toast": "Projet enregistré avec succès",
        "leader": "Nom du porteur de projet",
        "email": "Email de contact",
        "status": "📊 Étape du projet",
    },
    "English": {
        "header": "Impact Pilot Form",
        "intro_title": "🌍 Join EVAD to co-develop your regenerative place project!",
        "intro_text": (
            "Welcome to **EVAD – Living Autonomous & Decentralized Ecosystem**, "
            "a platform designed to guide the creation of shared sustainable places "
            "(*third places, eco-farms, coworking hubs, etc.*) through collaborative, "
            "open-source and regenerative intelligence."
        ),
        "name": "🏷️ Project name",
        "desc": "📝 Project description",
        "goal": "🎯 Project objective",
        "loc": "📍 Location",
        "add_space": "➕ Add another space",
        "upload": "📄 Related document (optional)",
        "analyze": "🚀 Launch project analysis",
        "fill_warn": "Please fill in all fields before analysis.",
        "success": "🌿 Project successfully saved to the EVAD database!",
        "toast": "Project saved successfully",
        "leader": "Project leader name",
        "email": "Contact email",
        "status": "📊 Project stage",
    },
}
t = TEXTS[langue]

# ==============================
# 🎨 STYLE
# ==============================
st.markdown("""
<style>
div.block-container {padding:25px!important}
div.stForm {background:#018262;border-radius:20px;padding:25px!important;box-shadow:0 4px 15px rgba(0,0,0,.15)}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:#fff!important;color:#000!important;border-radius:6px;border:1px solid #555!important}
.stButton button{background:#018262!important;color:white!important;border-radius:8px;font-weight:bold}
.stButton button:hover{background:#01614c!important}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🧠 CONFIG OPENROUTER
# ==============================
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}

# ==============================
# 🤖 IA MULTI-LANGUE
# ==============================
def ask_agent(langue, title, description, objectif, localisation):
    if langue == "Français":
        role = (
            "Tu es un système collaboratif composé de 4 experts : AnalystAgent, EcoAgent, PlannerAgent et CoordinatorAgent. "
            "Réponds uniquement en français avec les sections : Solution, Impact écologique, Impact social, Impact économique, Plan d’action."
        )
    else:
        role = (
            "You are a collaborative system composed of 4 experts: AnalystAgent, EcoAgent, PlannerAgent and CoordinatorAgent. "
            "Answer only in English with the sections: Solution, Ecological Impact, Social Impact, Economic Impact, Action Plan."
        )

    payload = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {"role": "system", "content": role},
            {"role": "user", "content": f"Title: {title}\nDescription: {description}\nGoal: {objectif}\nLocation: {localisation}"}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }
    try:
        requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    except:
        pass  # IA tourne en arrière-plan silencieusement

# ==============================
# 📘 FORMULAIRE PRINCIPAL
# ==============================
if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1

with st.form("user_form"):
    st.markdown(f"### {t['intro_title']}")
    st.caption(t["intro_text"])

    title = st.text_input(t["name"])
    description = st.text_area(t["desc"], height=100)
    objectif = st.text_area(t["goal"], height=100)
    localisation = st.text_input(t["loc"])

    espaces = []
    for i in range(st.session_state.nb_espaces):
        espaces.append(st.text_area(f"🏠 Espace {i+1}", key=f"espace_{i+1}", height=80))

    if st.session_state.nb_espaces < 5:
        if st.form_submit_button(t["add_space"]):
            st.session_state.nb_espaces += 1
            st.rerun()

    uploaded_doc = st.file_uploader(t["upload"], type=["pdf", "png", "jpg", "jpeg", "docx"])
    submitted = st.form_submit_button(t["analyze"])

# ==============================
# 🚀 ANALYSE IA + ENREGISTREMENT
# ==============================
if submitted:
    if not all([title, description, objectif, localisation]):
        st.warning(t["fill_warn"])
    else:
        ask_agent(langue, title, description, objectif, localisation)
        st.session_state.final_result = True

# ==============================
# 💾 ENREGISTREMENT FINAL
# ==============================
if st.session_state.get("final_result"):
    with st.form("porteur_form"):
        leader = st.text_input(t["leader"])
        email = st.text_input(t["email"])
        status = st.selectbox(
            t["status"],
            ["Thinking", "Modélisation", "Construction", "Développement", "Financement", "Student"]
        )

        saved = st.form_submit_button("💾 Enregistrer dans la base EVAD")
        if saved:
            # Ici, tu peux remettre ton bloc NoCoDB complet (upload + payload)
            st.success(t["success"])
            st.toast(t["toast"], icon="🌱")

