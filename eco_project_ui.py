# -*- coding: utf-8 -*-
import streamlit as st
import requests
import re
import base64
import json

# --- EN-TÊTE EVAD (logo centré) ---
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
        <hr style='border:none;height:2px;background-color:#cfeee7;margin:5px 0 20px 0;'>
    """, unsafe_allow_html=True)

# --- STYLE GLOBAL ---
st.markdown("""
<style>
div.stForm {background-color:#018262!important;border-radius:20px;padding:25px!important;box-shadow:0 4px 15px rgba(0,0,0,.15);}
div.stForm>div{background-color:#cfeee7!important;color:#014d3b!important;border-radius:15px;padding:20px;margin:0;}
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div{background-color:#fff!important;color:#000!important;border-radius:6px;border:1px solid #555!important;}
.stButton button{background-color:#018262!important;color:white!important;border-radius:8px;font-weight:bold;}
.stButton button:hover{background-color:#01614c!important;}
</style>
""", unsafe_allow_html=True)

# --- CONFIGURATION ---
st.set_page_config(page_title="Formulaire Pilote d'impact", page_icon="🏡", layout="centered")

# --- INTRO ---
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

# ==============================
# ⚡ MULTI-AGENT INTELLIGENT
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
    text = (title + description + objectif + localisation).lower()
    english_keywords = ["project", "community", "garden", "green", "development", "objective", "plan", "impact", "solution", "action"]
    score = sum(1 for w in english_keywords if w in text)
    lang = "english" if score >= 2 else "french"
    st.markdown(f"🌐 **Langue détectée : {lang}**")

    if lang == "english":
        role = (
            "You are a collaborative system of 4 expert agents (AnalystAgent, EcoAgent, PlannerAgent, CoordinatorAgent). "
            "Analyze the following project and produce a structured synthesis strictly in this format:\n\n"
            "Solution: (short paragraph)\n"
            "Ecological Impact: (1-2 sentences)\n"
            "Social Impact: (1-2 sentences)\n"
            "Economic Impact: (1-2 sentences)\n"
            "Action Plan: (3 to 5 clear and numbered steps)\n\n"
            "⚠️ IMPORTANT: Always include all section titles exactly as written above, in English."
        )
    else:
        role = (
            "Tu es un système collaboratif composé de 4 experts (AnalystAgent, EcoAgent, PlannerAgent et CoordinatorAgent). "
            "Analyse le projet suivant et produis une synthèse structurée avec ce format précis :\n\n"
            "Solution: (court paragraphe)\n"
            "Impact écologique: (1-2 phrases)\n"
            "Impact social: (1-2 phrases)\n"
            "Impact économique: (1-2 phrases)\n"
            "Plan d’action: (3 à 5 étapes claires et numérotées)\n\n"
            "⚠️ IMPORTANT : Inclure tous les titres de section exactement comme ci-dessus, en français."
        )

    user_input = f"Project title: {title}\nDescription: {description}\nObjective: {objectif}\nLocation: {localisation}"
    
    try:
        response = ask_agent(role, user_input)
        # 🔍 Vérifie si les sections attendues existent
        if not any(keyword.lower() in response.lower() for keyword in ["impact", "solution", "plan"]):
            # 🧠 Si mal structuré, reformate automatiquement
            role_fix = (
                "Reformat this text into a structured summary using the exact section headers "
                f"in {'English' if lang=='english' else 'French'} as specified previously."
            )
            response = ask_agent(role_fix, response)
    except Exception as e:
        response = f"⚠️ AI generation error: {e}"

    return response, lang

# ==============================
# 🧾 FORMULAIRE PRINCIPAL
# ==============================
if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1

with st.form("user_form"):
    st.markdown("<h2>📘 Présentation du projet</h2>", unsafe_allow_html=True)
    title = st.text_input("🏷️ Nom du projet")
    description = st.text_area("📝 Description du projet", height=100)
    objectif = st.text_area("🎯 Objectif du projet", height=100)
    localisation = st.text_input("📍 Localisation")

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
# 🚀 ANALYSE
# ==============================
if submitted:
    if not all([title, description, objectif, localisation]):
        st.warning("Merci de remplir tous les champs avant l’analyse.")
    else:
        with st.spinner("🌱 Analyse du projet en cours..."):
            try:
                final_result, detected_lang = MultiAgentFusion(title, description, objectif, localisation)
                st.session_state.final_result = final_result
                st.session_state.detected_lang = detected_lang
                st.success("✅ Analyse du projet terminée avec succès !")
            except Exception as e:
                st.error(f"Erreur IA : {e}")

# ==============================
# 🧩 SYNTHÈSE MULTILINGUE
# ==============================
if "final_result" in st.session_state:
    with st.form("synthese_form"):
        st.subheader("📋 Synthèse du projet")

        text = st.session_state.final_result
        lang = st.session_state.get("detected_lang", "french")

        def extract_section(text, keys):
            pattern = rf"({'|'.join(keys)})\s*[:：\-–]?\s*(.*?)(?=\n(?:Solution|Impact|Plan|$))"
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            return match.group(2).strip() if match else ""

        objectif = extract_section(text, ["Solution", "Project Objective", "Objective"])
        impact_eco = extract_section(text, ["Impact écologique", "Ecological Impact"])
        impact_social = extract_section(text, ["Impact social", "Social Impact"])
        impact_econ = extract_section(text, ["Impact économique", "Economic Impact"])
        plan_action = extract_section(text, ["Plan d’action", "Action Plan"])

        def first_sentence(text):
            text = re.sub(r'\s+', ' ', text.strip())
            match = re.match(r'^(.*?[.!?])(\s|$)', text)
            if match:
                return match.group(1).strip()
            return text.split('.')[0].strip() + '.'

        impact_eco = first_sentence(impact_eco)
        impact_social = first_sentence(impact_social)
        impact_econ = first_sentence(impact_econ)

        st.session_state.objectif = st.text_area("🎯 Objectif du projet", objectif, height=100)
        st.session_state.impact_eco = st.text_area("🌿 Impact écologique", impact_eco, height=70)
        st.session_state.impact_social = st.text_area("🤝 Impact social", impact_social, height=70)
        st.session_state.impact_econ = st.text_area("💰 Impact économique", impact_econ, height=70)
        st.session_state.plan_action = st.text_area("🧭 Plan d’action", plan_action, height=140)

        validated = st.form_submit_button("✅ Valider et ajouter les informations du porteur")
        if validated:
            st.session_state.validation_ok = True
            st.success("✅ Sections validées avec succès !")



