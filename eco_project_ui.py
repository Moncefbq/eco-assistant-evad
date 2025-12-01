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
# ⚡ FUSION INTELLIGENTE MULTI-AGENTS (corrigée et bilingue stable)
# ==============================
import re, requests

def detect_language_from_content(*parts):
    """Détection robuste basée uniquement sur le contenu saisi par l'utilisateur"""
    text = " ".join([p for p in parts if p]).strip()
    has_fr_accents = bool(re.search(r"[éèêëàâîïôûùçÉÈÊËÀÂÎÏÔÛÙÇ]", text))
    fr_hits = len(re.findall(r"\b(le|la|les|des|du|de|un|une|et|pour|projet|objectif|localisation|impact|plan|action|communaut|écolog|économiq)\b", text, re.IGNORECASE))
    en_hits = len(re.findall(r"\b(the|and|project|objective|location|impact|plan|action|community|ecolog|econom)\b", text, re.IGNORECASE))

    if has_fr_accents or fr_hits > en_hits:
        return "French"
    if en_hits > fr_hits:
        return "English"
    return "French" if st.session_state.get("lang") == "Français" else "English"


def clean_text(text):
    """Nettoyage général du texte brut"""
    text = re.sub(r"[^\x00-\x7FÀ-ÿ\n\.\,\;\:\!\?\-\(\)\'’\"\s]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    return text.strip()


def MultiAgentFusion(title, description, objectif, localisation):
    """Fusion intelligente multilingue et structurée"""
    detected_lang = detect_language_from_content(title, description, objectif, localisation)

    # 🧩 Préparation du contenu utilisateur dans la langue détectée
    if detected_lang == "French":
        user_input = (
            f"Projet : {title}\n"
            f"Description : {description}\n"
            f"Objectif : {objectif}\n"
            f"Localisation : {localisation}"
        )
        role = (
            "Tu es un collectif d’experts composé de AnalystAgent, EcoAgent, SocialAgent, EconomicAgent et PlannerAgent. "
            "Analyse ce projet et produis **un rapport complet et structuré en français**, selon ce format précis :\n\n"
            "1. Objectif du projet :\n(Décris clairement le but principal du projet.)\n\n"
            "2. Impact écologique :\n(Décris les effets environnementaux et de durabilité.)\n\n"
            "3. Impact social :\n(Décris comment ce projet profite à la communauté ou aux citoyens.)\n\n"
            "4. Impact économique :\n(Décris les effets économiques locaux.)\n\n"
            "5. Plan d’action :\n(Donne 3 à 5 étapes concrètes et réalistes pour la mise en œuvre.)\n\n"
            "IMPORTANT : Réponds uniquement en français clair et professionnel, sans mots anglais."
        )
        model_name = "mistralai/mistral-nemo"  # tu peux le changer en mistralai/mistral-large-2402 si dispo
    else:
        user_input = (
            f"Project: {title}\n"
            f"Description: {description}\n"
            f"Objective: {objectif}\n"
            f"Location: {localisation}"
        )
        role = (
            "You are a multi-agent expert team composed of AnalystAgent, EcoAgent, SocialAgent, EconomicAgent, and PlannerAgent. "
            "Analyze this project and produce **a complete structured report in English** with this format:\n\n"
            "1. Project Objective:\n(Clearly define the main goal.)\n\n"
            "2. Ecological Impact:\n(Describe environmental and sustainability effects.)\n\n"
            "3. Social Impact:\n(Describe community and social benefits.)\n\n"
            "4. Economic Impact:\n(Describe local or financial implications.)\n\n"
            "5. Action Plan:\n(Create 3–5 realistic implementation steps.)\n\n"
            "IMPORTANT: Answer only in clear professional English."
        )
        model_name = "mistralai/mistral-nemo"

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": role},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 900
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()
        content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        text = clean_text(content)

        # 🧠 Extraction structurée
        patterns = {
            "objectif":     r"(?:Project Objective|Objectif du projet)\s*[:\-–]\s*(.+?)(?=(?:Ecological Impact|Impact écologique|$))",
            "impact_eco":   r"(?:Ecological Impact|Impact écologique)\s*[:\-–]\s*(.+?)(?=(?:Social Impact|Impact social|$))",
            "impact_social":r"(?:Social Impact|Impact social)\s*[:\-–]\s*(.+?)(?=(?:Economic Impact|Impact économique|$))",
            "impact_econ":  r"(?:Economic Impact|Impact économique)\s*[:\-–]\s*(.+?)(?=(?:Action Plan|Plan d[’']action|$))",
            "plan_action":  r"(?:Action Plan|Plan d[’']action)\s*[:\-–]\s*(.+)"
        }

        sections = {k: "" for k in ["objectif", "impact_eco", "impact_social", "impact_econ", "plan_action"]}
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                sections[key] = clean_text(match.group(1))

        # Fallback global si aucune section extraite
        if not any(sections.values()):
            sections["objectif"] = text

        return sections

    except Exception as e:
        st.error(f"❌ Error during AI fusion: {e}")
        return {k: "Error" for k in ["objectif", "impact_eco", "impact_social", "impact_econ", "plan_action"]}


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
                # 🧠 Lancement de l’analyse multilingue
                final_result = MultiAgentFusion(title, description, objectif, localisation)

                # 🪄 Enregistre chaque section dans le session_state
                st.session_state.objectif = final_result["objectif"]
                st.session_state.impact_eco = final_result["impact_eco"]
                st.session_state.impact_social = final_result["impact_social"]
                st.session_state.impact_econ = final_result["impact_econ"]
                st.session_state.plan_action = final_result["plan_action"]

                # 💾 Garde la version brute si besoin ailleurs
                st.session_state.final_result = final_result

                # ✅ Message de réussite bilingue
                st.success(message_success)
                st.session_state.validation_ok = True


            except Exception as e:
                msg_error = (
                    f"❌ Error during analysis: {e}"
                    if st.session_state.lang == "English"
                    else f"❌ Erreur pendant l’analyse : {e}"
                )
                st.error(msg_error)

# ==============================
# 🧠 MIND MAP AUTOMATIQUE
# ==============================

import streamlit as st
import math

def generate_mindmap(objective, eco, social, econ, actions):

    # Colors for bubbles
    bubble_colors = [
        "#A7C7E7",  # blue
        "#F7C5C5",  # red
        "#C7F7D4",  # green
        "#FBE7A1",  # yellow
        "#E3C7F7",  # purple
    ]

    impacts = [eco, social, econ]
    action_items = [a.strip() for a in actions.split("\n") if len(a.strip()) > 2]

    html = """
    <style>

    .mindmap-wrapper {
        width: 100%;
        display: flex;
        justify-content: center;
    }

    .mindmap {
        width: 900px;
        height: 600px;
        position: relative;
        background: #fafafa;
        border-radius: 20px;
        margin-top: 20px;
        overflow: hidden;
    }

    .bubble {
        padding: 15px 25px;
        border-radius: 40px;
        position: absolute;
        font-weight: 600;
        font-family: 'Arial';
        font-size: 18px;
        text-align: center;
        color: #333;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.15);
    }

    .center-bubble {
        background: #FFD86B;
        padding: 20px 40px;
        font-size: 22px;
        border-radius: 45px;
        top: 50%;
        left: 50%;
        transform: translate(-50%,-50%);
        z-index: 10;
    }

    .line {
        position: absolute;
        width: 2px;
        background: #bbb;
        transform-origin: top left;
    }

    </style>

    <div class="mindmap-wrapper">
    <div class="mindmap">
        <div class="bubble center-bubble">{objective}</div>
    """.format(objective=objective)

    # ---- IMPACTS AROUND THE CENTER ----
    radius1 = 200
    angle_step1 = 2 * math.pi / len(impacts)

    for i, txt in enumerate(impacts):
        angle = i * angle_step1
        x = 450 + radius1 * math.cos(angle)
        y = 300 + radius1 * math.sin(angle)

        color = bubble_colors[i % len(bubble_colors)]

        html += f"""
        <div class="bubble" style="left:{x}px; top:{y}px; background:{color};">
            {txt}
        </div>
        """

        # draw a line from center to bubble
        cx, cy = 450, 300
        dx, dy = x - cx + 80, y - cy + 20
        dist = math.sqrt(dx*dx + dy*dy)
        angle_deg = math.degrees(math.atan2(dy, dx))

        html += f"""
        <div class="line" style="
            left: {cx}px;
            top: {cy}px;
            height: {dist}px;
            transform: rotate({angle_deg}deg);
        "></div>
        """

    # ---- ACTIONS OUTER RING ----
    radius2 = 330
    angle_step2 = 2 * math.pi / max(1, len(action_items))

    for i, txt in enumerate(action_items):
        angle = i * angle_step2
        x = 450 + radius2 * math.cos(angle)
        y = 300 + radius2 * math.sin(angle)

        color = bubble_colors[(i+3) % len(bubble_colors)]

        html += f"""
        <div class="bubble" style="left:{x}px; top:{y}px; background:{color}; font-size:16px;">
            {txt}
        </div>
        """

        cx, cy = 450, 300
        dx, dy = x - cx + 80, y - cy + 20
        dist = math.sqrt(dx*dx + dy*dy)
        angle_deg = math.degrees(math.atan2(dy, dx))

        html += f"""
        <div class="line" style="
            left: {cx}px;
            top: {cy}px;
            height: {dist}px;
            transform: rotate({angle_deg}deg);
        "></div>
        """

    html += "</div></div>"

    st.markdown(html, unsafe_allow_html=True)



if st.session_state.get("validation_ok"):
    st.markdown("## 🧠 Mind Mapping du projet")

    generate_mindmap(
        st.session_state.objectif,
        st.session_state.impact_eco,
        st.session_state.impact_social,
        st.session_state.impact_econ,
        st.session_state.plan_action
    )



# ==============================
# 🧑‍💼 ENREGISTREMENT FINAL (version corrigée et alignée NoCoDB)
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
            # --- Upload du document éventuel ---
            UPLOAD_URL = "https://app.nocodb.com/api/v2/storage/upload"
            headers = {"xc-token": NOCODB_API_TOKEN, "Accept": "application/json"}

            file_attachment = []

            if uploaded_doc is not None:
                try:
                    files = {"file": (uploaded_doc.name, uploaded_doc.getvalue())}
                    up = requests.post(UPLOAD_URL, headers=headers, files=files)
                    up.raise_for_status()
                    data = up.json()

                    # Vérifie les formats possibles de réponse NoCoDB
                    if isinstance(data, dict) and "list" in data:
                        f = data["list"][0]
                    elif isinstance(data, list) and len(data) > 0:
                        f = data[0]
                    else:
                        f = None

                    if f:
                        url = f.get("url", "")
                        signed = f.get("signedUrl", "")
                        title_doc = f.get("title", uploaded_doc.name)
                        mimetype = f.get("mimetype", uploaded_doc.type or "image/png")

                        path = f.get("path", "")
                        if not path:
                            if "/nc/" in url:
                                path = url[url.index("/nc/"):]
                            elif "/nc/" in signed:
                                path = signed[signed.index("/nc/"):]
                            else:
                                path = f"/nc/uploads/{title_doc}"

                        file_attachment = [{
                            "title": title_doc,
                            "path": path,
                            "url": signed or url,
                            "mimetype": mimetype
                        }]

                        st.toast("📎 Fichier uploadé avec succès", icon="📤")

                        try:
                            st.image(uploaded_doc.getvalue(), caption=title_doc, use_container_width=True)
                        except:
                            pass

                except Exception as e:
                    st.error(f"Erreur lors de l’upload : {e}")

            # --- Construction du payload EXACT pour NoCoDB ---
            payload = {
                "Title": title,
                "Description": description,
                "Localisation": localisation,
                "Project Leader": leader,
                "Email": email,
                "Status": status,

                # 🟩 CHAMPS SYNTHÈSE EXACTS SELON NOCoDB
                "objectif_synthese": st.session_state.objectif,
                "impact_eco": st.session_state.impact_eco,
                "impact_social": st.session_state.impact_social,
                "impact_econ": st.session_state.impact_econ,
                "plan_action": st.session_state.plan_action,

                # 🏠 ESPACES (OK)
                "espace 1": espaces[0] if len(espaces) > 0 else "",
                "espace 2": espaces[1] if len(espaces) > 1 else "",
                "espace 3": espaces[2] if len(espaces) > 2 else "",
                "espace 4": espaces[3] if len(espaces) > 3 else "",
                "espace 5": espaces[4] if len(espaces) > 4 else "",
            }

            # Ajout du fichier si présent
            if file_attachment:
                payload["Logo + docs"] = file_attachment

            # --- Envoi API vers NoCoDB ---
            try:
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
                    st.toast("🌱 Project saved successfully", icon="🌱")
                else:
                    st.error(f"❌ API Error {r.status_code} : {r.text}")

            except Exception as e:
                st.error(f"❌ Erreur lors de l’envoi à NoCoDB : {e}")
