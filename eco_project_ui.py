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
# ⚡ FUSION INTELLIGENTE MULTI-AGENTS (robuste et bilingue)
# ==============================
import re, requests

def detect_language(text):
    english_keywords = re.findall(
        r"\b(the|and|project|impact|plan|objective|location|space|environment|community|action)\b",
        text, re.IGNORECASE)
    french_keywords = re.findall(
        r"\b(le|la|et|projet|impact|plan|objectif|localisation|espace|environnement|communaut|action)\b",
        text, re.IGNORECASE)
    if len(english_keywords) > len(french_keywords):
        return "English"
    elif len(french_keywords) > len(english_keywords):
        return "French"
    else:
        return "French" if re.search(r"[éèàùçâêîôû]", text) else "English"

def clean_text(text):
    text = re.sub(r"[^\x00-\x7FÀ-ÿ\n\.\,\;\:\!\?\-\(\)\'\"\s]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    return text.strip()

def MultiAgentFusion(title, description, objectif, localisation):
    user_input = f"Title: {title}\nDescription: {description}\nObjective: {objectif}\nLocation: {localisation}"
    detected_lang = detect_language(user_input)

    if detected_lang == "English":
        role = (
            "You are a collaborative team of 4 experts: AnalystAgent, EcoAgent, PlannerAgent, and CoordinatorAgent. "
            "Analyze this project and generate **all outputs entirely in English** with the following structure:\n\n"
            "Solution:\nEcological Impact:\nSocial Impact:\nEconomic Impact:\nAction Plan (3–5 clear practical steps).\n\n"
            "Be clear, concise, and professional."
        )
    else:
        role = (
            "Tu es un système collaboratif composé de 4 experts : AnalystAgent, EcoAgent, PlannerAgent et CoordinatorAgent. "
            "Analyse ce projet et produis **toutes les sections en français** avec la structure suivante :\n\n"
            "Solution :\nImpact écologique :\nImpact social :\nImpact économique :\nPlan d’action (3 à 5 étapes concrètes et réalistes).\n\n"
            "Sois clair, concis et professionnel."
        )

    payload = {
        "model": "mistralai/mistral-nemo",
        "messages": [
            {"role": "system", "content": role},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.6,
        "max_tokens": 900
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        result = clean_text(result)

        # 🔁 Relance automatique si vide
        if len(result.strip()) < 30:
            st.warning("⚠️ Première réponse vide, relance automatique de l'analyse...")
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            result = clean_text(result)

        if not result:
            st.error("❌ Aucune réponse générée par l’IA.")
        return result

    except Exception as e:
        st.error(f"⚠️ Erreur lors de la génération IA : {e}")
        return "⚠️ Error during AI generation. Please try again."


# ==============================
# INTERFACE STREAMLIT
# ==============================
if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1
# --- TITRES MULTILINGUES FORMULAIRE ---
if st.session_state.lang == "English":
    titre_projet = "📘 Project Overview"
    sous_titre_projet = "Information about your sustainable place project"
    titre_espaces = "📂 Project Details by Space"
    sous_titre_espaces = "Information about each space included in the project"
    titre_synthese = "📋 Project Summary"
    titre_porteur = "👤 Project Leader Information"
else:
    titre_projet = "📘 Présentation du projet"
    sous_titre_projet = "Informations sur le projet de lieu durable"
    titre_espaces = "📂 Détails du projet par espace"
    sous_titre_espaces = "Informations sur chaque espace qui compose le projet"
    titre_synthese = "📋 Synthèse du projet"
    titre_porteur = "👤 Présentation du porteur"

# --- LABELS MULTILINGUES FORMULAIRE ---
if st.session_state.lang == "English":
    labels = {
        "project_name": "Project Name",
        "project_description": "Project Description",
        "project_objective": "Project Objective",
        "location": "Location",
        "space": "Space",
        "add_space": "➕ Add a Space",
        "upload_doc": "📄 Related Document (optional)",
        "submit_analysis": "🚀 Launch Project Analysis",
        "objective_summary": "🎯 Project Objective",
        "eco_impact": "🌿 Ecological Impact",
        "social_impact": "🤝 Social Impact",
        "economic_impact": "💰 Economic Impact",
        "action_plan": "🧭 Action Plan",
        "validate": "✅ Validate and Add Project Owner Information",
        "leader_name": "Project Leader Name",
        "email": "Contact Email",
        "status": "📊 Project Stage",
        "save": "💾 Save in EVAD Database"
    }
else:
    labels = {
        "project_name": "Nom du projet",
        "project_description": "Description du projet",
        "project_objective": "Objectif du projet",
        "location": "Localisation",
        "space": "Espace",
        "add_space": "➕ Ajouter un espace",
        "upload_doc": "📄 Document lié (optionnel)",
        "submit_analysis": "🚀 Lancer l’analyse du projet",
        "objective_summary": "🎯 Objectif du projet",
        "eco_impact": "🌿 Impact écologique",
        "social_impact": "🤝 Impact social",
        "economic_impact": "💰 Impact économique",
        "action_plan": "🧭 Plan d’action",
        "validate": "✅ Valider et ajouter les informations du porteur",
        "leader_name": "Nom du porteur de projet",
        "email": "Email de contact",
        "status": "📊 Étape du projet",
        "save": "💾 Enregistrer dans la base EVAD"
    }

# ✅ ICI commence ton formulaire
with st.form("user_form"):
    st.markdown(f"""
        <h2 style='margin-bottom: 0;'>{titre_projet}</h2>
        <p style='margin-top: 2px; color:#014d3b; font-style: italic;'>
            {sous_titre_projet}
        </p>
    """, unsafe_allow_html=True)

    title = st.text_input(f"🏷️ {labels['project_name']}")
    description = st.text_area(f"📝 {labels['project_description']}", height=100)
    objectif = st.text_area(f"🎯 {labels['project_objective']}", height=100)
    localisation = st.text_input(f"📍 {labels['location']}")

    # Section espaces
    st.markdown(f"""
        <h3 style='margin-bottom: 0;'>{titre_espaces}</h3>
        <p style='margin-top: 2px; color:#014d3b; font-style: italic;'>
            {sous_titre_espaces}
        </p>
    """, unsafe_allow_html=True)

    espaces = []
    for i in range(st.session_state.nb_espaces):
        espaces.append(st.text_area(f"🏠 {labels['space']} {i+1}", key=f"espace_{i+1}", height=80))

    if st.session_state.nb_espaces < 5:
        if st.form_submit_button(labels["add_space"]):
            st.session_state.nb_espaces += 1
            st.rerun()

    uploaded_doc = st.file_uploader(labels["upload_doc"], type=["pdf", "png", "jpg", "jpeg", "docx"])
    submitted = st.form_submit_button(labels["submit_analysis"])

# ==============================
# 🔍 ANALYSE DU PROJET
# ==============================
if submitted:
    if not all([title, description, objectif, localisation]):
        msg_warning = (
            "⚠️ Please fill in all fields before starting the analysis."
            if st.session_state.lang == "English"
            else "⚠️ Merci de remplir tous les champs avant l’analyse."
        )
        st.warning(msg_warning)
    else:
        message_loading = (
            "🌱 Project analysis in progress..."
            if st.session_state.lang == "English"
            else "🌱 Analyse du projet en cours..."
        )
        message_success = (
            "✅ Project analysis completed successfully!"
            if st.session_state.lang == "English"
            else "✅ Analyse du projet terminée avec succès !"
        )

        with st.spinner(message_loading):
            try:
                final_result = MultiAgentFusion(title, description, objectif, localisation)
                st.session_state.final_result = final_result
                st.success(message_success)

            except Exception as e:
                msg_error = (
                    f"❌ Error during analysis: {e}"
                    if st.session_state.lang == "English"
                    else f"❌ Erreur pendant l’analyse : {e}"
                )
                st.error(msg_error)


# ==============================
#  SYNTHÈSE DU PROJET 
# ==============================
if "final_result" in st.session_state:
    with st.form("synthese_form"):
        st.subheader(titre_synthese)

        import re, requests

        def extract_section(text, section):
            """Extraction robuste et propre"""
            pattern = rf"{section}\s*[:：\-–]?\s*(.*?)(?=\n(?:Solution|Objectif|Impact|Plan|$))"
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else ""

        text = st.session_state.final_result

        # --- Extraction des sections ---
        objectif = extract_section(text, "Solution")
        impact_eco = extract_section(text, "Impact écologique")
        impact_social = extract_section(text, "Impact social")
        impact_econ = extract_section(text, "Impact économique")
        plan_action = extract_section(text, "Plan d’action")

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

        # --- Garde une seule phrase complète par impact ---
        def first_sentence(text):
            text = re.sub(r'\s+', ' ', text.strip())
            match = re.match(r'^(.*?[.!?])(\s|$)', text)
            if match:
                return match.group(1).strip()
            return text.split('.')[0].strip() + '.'

        impact_eco = first_sentence(impact_eco)
        impact_social = first_sentence(impact_social)
        impact_econ = first_sentence(impact_econ)

        # --- Champs finaux ---
        st.session_state.objectif = st.text_area(labels["objective_summary"], objectif, height=100)
        st.session_state.impact_eco = st.text_area(labels["eco_impact"], impact_eco, height=70)
        st.session_state.impact_social = st.text_area(labels["social_impact"], impact_social, height=70)
        st.session_state.impact_econ = st.text_area(labels["economic_impact"], impact_econ, height=70)
        st.session_state.plan_action = st.text_area(labels["action_plan"], plan_action, height=140)

        validated = st.form_submit_button(labels["validate"])
        if validated:
            st.session_state.validation_ok = True
            msg_valide = "✅ Sections successfully validated!" if st.session_state.lang == "English" else "✅ Sections validées avec succès !"
            st.success(msg_valide)
 


# ==============================
# 🧑‍💼 ENREGISTREMENT FINAL (version corrigée et alignée)
# ==============================
if st.session_state.get("validation_ok"):
    with st.form("porteur_form"):
        st.subheader(titre_porteur)

        leader = st.text_input(labels["leader_name"])
        email = st.text_input(labels["email"])
        status = st.selectbox(
            labels["status"],
            ["Thinking", "Modélisation", "Construction", "Développement", "Financement", "Student"],
            index=0
        )

        saved = st.form_submit_button(labels["save"])

        if saved:
            UPLOAD_URL = "https://app.nocodb.com/api/v2/storage/upload"
            headers = {"xc-token": NOCODB_API_TOKEN, "Accept": "application/json"}

            file_attachment = []
            if uploaded_doc is not None:
                try:
                    files = {"file": (uploaded_doc.name, uploaded_doc.getvalue())}
                    up = requests.post(UPLOAD_URL, headers=headers, files=files)
                    up.raise_for_status()
                    data = up.json()

                    # Vérifie le format de la réponse (list ou dict)
                    if isinstance(data, dict) and "list" in data:
                        f = data["list"][0]
                    elif isinstance(data, list) and len(data) > 0:
                        f = data[0]
                    else:
                        f = None

                    if f:
                        url = f.get("url", "")
                        signed = f.get("signedUrl", "")
                        title = f.get("title", uploaded_doc.name)
                        mimetype = f.get("mimetype", uploaded_doc.type or "image/png")

                        # Correction du chemin
                        path = f.get("path", "")
                        if not path:
                            if "/nc/uploads/" in url:
                                path = url[url.index("/nc/"):]
                            elif "/nc/uploads/" in signed:
                                path = signed[signed.index("/nc/"):]
                            else:
                                path = f"/nc/uploads/{title}"

                        file_attachment = [{
                            "title": title,
                            "path": path,
                            "url": signed or url,
                            "mimetype": mimetype
                        }]

                        st.toast("📎 Fichier uploadé avec succès", icon="📤")
                        try:
                            st.image(uploaded_doc.getvalue(), caption=title, use_container_width=True)
                        except:
                            pass
                    else:
                        st.warning("⚠️ Aucun fichier détecté dans la réponse d’upload.")
                except Exception as e:
                    st.error(f"Erreur lors de l’upload : {e}")

            # --- Construction du payload principal ---
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
                "espace 1": espaces[0] if len(espaces) > 0 else "",
                "espace 2": espaces[1] if len(espaces) > 1 else "",
                "espace 3": espaces[2] if len(espaces) > 2 else "",
                "espace 4": espaces[3] if len(espaces) > 3 else "",
                "espace 5": espaces[4] if len(espaces) > 4 else "",
            }

            if file_attachment:
                payload["Logo + docs"] = file_attachment  # ✅ format correct pour NoCoDB

            # --- Envoi vers NoCoDB ---
            try:
                # 🔐 En-têtes pour NoCoDB
                headers = {
                    "xc-token": NOCODB_API_TOKEN,
                    "Accept": "application/json"
                }

                r = requests.post(NOCODB_API_URL, headers=headers, json=payload)

                if r.status_code in (200, 201):
                    msg_save = (
                        "🌿 Project successfully saved in the EVAD database!"
                        if st.session_state.lang == "English"
                        else "🌿 Projet enregistré avec succès dans la base EVAD !"
                    )
                    st.success(msg_save)

                    msg_toast = (
                        "🌱 Project saved successfully"
                        if st.session_state.lang == "English"
                        else "🌱 Projet enregistré avec succès"
                    )
                    st.toast(msg_toast, icon="🌱")

                else:
                    msg_error_api = (
                        f"❌ API Error {r.status_code}: {r.text}"
                        if st.session_state.lang == "English"
                        else f"❌ Erreur API {r.status_code} : {r.text}"
                    )
                    st.error(msg_error_api)

            except Exception as e:
                msg_error_noco = (
                    f"❌ Error while sending to NoCoDB: {e}"
                    if st.session_state.lang == "English"
                    else f"❌ Erreur lors de l’envoi à NoCoDB : {e}"
                )
                st.error(msg_error_noco)
