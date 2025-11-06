# -*- coding: utf-8 -*-
import streamlit as st
import requests
import base64
import json

# --- CONFIGURATION GLOBALE ---
st.set_page_config(page_title="Formulaire Pilote d'impact", page_icon="🏡", layout="centered")

# --- SÉLECTEUR DE LANGUE ---
if "langue" not in st.session_state:
    st.session_state.langue = "Français"

def switch_langue():
    st.session_state.langue = "English" if st.session_state.langue == "Français" else "Français"

# --- TEXTES MULTILINGUES ---
TEXTS = {
    "Français": {
        "title": "Formulaire Pilote d'impact",
        "intro_title": "🌍 Rejoignez EVAD pour co-développer votre projet de lieux régénératif !",
        "intro_text": "Bienvenue dans **EVAD – Écosystème Vivant Autonome et Décentralisé**, une plateforme de pilotage d’impact conçue pour la création de lieux partagés durables *(tiers-lieux, éco-lieux, coworking, fermes, etc.)* grâce à une intelligence collaborative, open-source et régénérative.",
        "presentation": "📘 Présentation du projet",
        "presentation_sub": "Informations sur le projet de lieu durable",
        "details": "📑 Détails du projet par espace",
        "name": "🏷️ Nom du projet",
        "desc": "📝 Description du projet",
        "goal": "🎯 Objectif du projet",
        "loc": "📍 Localisation",
        "add_space": "➕ Ajouter un espace",
        "upload": "📄 Document lié (optionnel)",
        "analyze": "🚀 Lancer l’analyse du projet",
        "fill_warn": "Merci de remplir tous les champs avant l’analyse.",
        "analyzing": "🌱 Analyse du projet en cours...",
        "analyze_done": "✅ Analyse du projet terminée avec succès !",
        "synthese": "📋 Synthèse du projet",
        "ecological": "🌿 Impact écologique",
        "social": "🤝 Impact social",
        "economic": "💰 Impact économique",
        "action": "🗺️ Plan d’action",
        "validate": "✅ Valider et ajouter les informations du porteur",
        "validated": "✅ Sections validées avec succès !",
        "leader": "👤 Nom du porteur de projet",
        "email": "✉️ Email de contact",
        "status": "📊 Étape du projet",
        "save": "💾 Enregistrer dans la base EVAD",
        "success": "🌿 Projet enregistré avec succès dans la base EVAD !",
        "toast": "Projet enregistré avec succès",
    },
    "English": {
        "title": "Impact Pilot Form",
        "intro_title": "🌍 Join EVAD to co-develop your regenerative place project !",
        "intro_text": "Welcome to **EVAD – Living Autonomous & Decentralized Ecosystem**, a platform designed to guide the creation of shared sustainable places *(third places, eco-farms, coworking hubs, etc.)* through collaborative, open-source and regenerative intelligence.",
        "presentation": "📘 Project Overview",
        "presentation_sub": "Information about your sustainable place project",
        "details": "📑 Project Details by Space",
        "name": "🏷️ Project name",
        "desc": "📝 Project description",
        "goal": "🎯 Project objective",
        "loc": "📍 Location",
        "add_space": "➕ Add another space",
        "upload": "📄 Related document (optional)",
        "analyze": "🚀 Launch project analysis",
        "fill_warn": "Please fill in all fields before analysis.",
        "analyzing": "🌱 Analyzing your project...",
        "analyze_done": "✅ Project analysis completed successfully !",
        "synthese": "📋 Project synthesis",
        "ecological": "🌿 Ecological Impact",
        "social": "🤝 Social Impact",
        "economic": "💰 Economic Impact",
        "action": "🗺️ Action Plan",
        "validate": "✅ Validate and add project leader information",
        "validated": "✅ Sections validated successfully !",
        "leader": "👤 Project leader name",
        "email": "✉️ Contact email",
        "status": "📊 Project stage",
        "save": "💾 Save to EVAD database",
        "success": "🌿 Project successfully saved to EVAD database !",
        "toast": "Project saved successfully",
    },
}
t = TEXTS[st.session_state.langue]

# --- EN-TÊTE EVAD (Logo + Titre + Bouton langue) ---
@st.cache_data
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

logo_base64 = get_base64_image("evad_logo.png")
col1, col2 = st.columns([8, 1])
with col1:
    if logo_base64:
        st.markdown(
            f"<div style='text-align:center;'><img src='data:image/png;base64,{logo_base64}' width='240'><h3>{t['title']}</h3></div>",
            unsafe_allow_html=True)
    else:
        st.markdown(f"<h3 style='text-align:center;'>{t['title']}</h3>", unsafe_allow_html=True)
with col2:
    st.button("🌐 " + ("EN" if st.session_state.langue == "Français" else "FR"), on_click=switch_langue)
st.markdown("<hr style='border:none;height:2px;background-color:#cfeee7;margin:5px 0 20px 0;'>", unsafe_allow_html=True)

# --- STYLE GLOBAL ---
st.markdown("""
<style>
div.stForm {background-color:#018262!important;border-radius:20px;padding:25px!important;box-shadow:0 4px 15px rgba(0,0,0,.15);}
div.stForm>div{background-color:#cfeee7!important;color:#014d3b!important;border-radius:15px;padding:20px;margin:0;}
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div{
background-color:#fff!important;color:#000!important;border-radius:6px;border:1px solid #555!important;}
.stButton button{background-color:#018262!important;color:white!important;border-radius:8px;font-weight:bold;}
.stButton button:hover{background-color:#01614c!important;}
</style>
""", unsafe_allow_html=True)

# --- INTRO ---
st.markdown(f"### {t['intro_title']}\n{t['intro_text']}")

# --- FORMULAIRE PRINCIPAL ---
if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1

with st.form("user_form"):
    st.markdown(f"<h2>{t['presentation']}</h2><p><i>{t['presentation_sub']}</i></p>", unsafe_allow_html=True)
    title = st.text_input(t["name"])
    description = st.text_area(t["desc"], height=100)
    objectif = st.text_area(t["goal"], height=100)
    localisation = st.text_input(t["loc"])

    st.markdown(f"<h4>{t['details']}</h4><p><i>{t['presentation_sub']}</i></p>", unsafe_allow_html=True)
    espaces = []
    for i in range(st.session_state.nb_espaces):
        espaces.append(st.text_area(f"🏠 Espace {i+1}", key=f"espace_{i+1}", height=80))
    if st.session_state.nb_espaces < 5:
        if st.form_submit_button(t["add_space"]):
            st.session_state.nb_espaces += 1
            st.rerun()

    uploaded_doc = st.file_uploader(t["upload"], type=["pdf", "png", "jpg", "jpeg", "docx"])
    submitted = st.form_submit_button(t["analyze"])

if submitted:
    if not all([title, description, objectif, localisation]):
        st.warning(t["fill_warn"])
    else:
        st.success(t["analyze_done"])
        st.markdown(f"### {t['synthese']}")
        objectif_gen = st.text_area(t["goal"], "Exemple : Aménager un espace durable et éducatif...", height=80)
        eco = st.text_area(t["ecological"], "Exemple : Réduire l'empreinte carbone grâce à des matériaux locaux.", height=80)
        social = st.text_area(t["social"], "Exemple : Favoriser la cohésion sociale par des activités communautaires.", height=80)
        eco2 = st.text_area(t["economic"], "Exemple : Créer des emplois verts et des partenariats locaux.", height=80)
        plan = st.text_area(t["action"], "Exemple : Planifier en 3 étapes l'aménagement et la maintenance durable.", height=80)
        if st.button(t["validate"]):
            st.session_state.final_result = True
            st.success(t["validated"])

if st.session_state.get("final_result"):
    with st.form("porteur_form"):
        st.subheader("👤 " + t["leader"])
        leader = st.text_input(t["leader"])
        email = st.text_input(t["email"])
        status = st.selectbox(t["status"], ["Thinking", "Modélisation", "Construction", "Développement", "Financement", "Student"], index=0)
        saved = st.form_submit_button(t["save"])
        if saved:
            st.success(t["success"])
            st.toast(t["toast"], icon="🌱")

