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
# ⚡ FUSION INTELLIGENTE MULTI-AGENTS (bilingue et complète)
# ==============================
import re, requests

def detect_language(text):
    """Détection simple de la langue"""
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
    """Nettoyage du texte brut"""
    text = re.sub(r"[^\x00-\x7FÀ-ÿ\n\.\,\;\:\!\?\-\(\)\'\"\s]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    return text.strip()

def MultiAgentFusion(title, description, objectif, localisation):
    """Fusion intelligente avec réponse complète dans la langue détectée"""
    user_input = f"Title: {title}\nDescription: {description}\nObjective: {objectif}\nLocation: {localisation}"
    detected_lang = detect_language(user_input)

    if detected_lang == "English":
        role = (
            "You are a multi-agent expert team composed of AnalystAgent, EcoAgent, SocialAgent, EconomicAgent, and PlannerAgent. "
            "Analyze this project and generate **a complete, structured report entirely in English**, with the following format:\n\n"
            "1. Project Objective:\n(Describe the main goal of the project clearly.)\n\n"
            "2. Ecological Impact:\n(Explain environmental and sustainability effects.)\n\n"
            "3. Social Impact:\n(Explain how this project benefits the community or people.)\n\n"
            "4. Economic Impact:\n(Explain financial or local economic effects.)\n\n"
            "5. Action Plan:\n(Create 3–5 realistic steps for implementation.)\n\n"
            "Keep tone professional, concise, and coherent. Do not use foreign languages."
        )
    else:
        role = (
            "Tu es un système collaboratif composé de plusieurs experts : AnalystAgent, EcoAgent, SocialAgent, EconomicAgent et PlannerAgent. "
            "Analyse ce projet et génère **un rapport complet et structuré entièrement en français**, avec le format suivant :\n\n"
            "1. Objectif du projet :\n(Décris clairement le but principal du projet.)\n\n"
            "2. Impact écologique :\n(Explique les effets environnementaux et de durabilité.)\n\n"
            "3. Impact social :\n(Explique comment ce projet bénéficie à la communauté ou aux citoyens.)\n\n"
            "4. Impact économique :\n(Explique les effets financiers ou économiques locaux.)\n\n"
            "5. Plan d’action :\n(Donne 3 à 5 étapes réalistes et concrètes pour la mise en œuvre.)\n\n"
            "Sois professionnel, cohérent et évite d’utiliser d’autres langues."
        )

    payload = {
        "model": "mistralai/mistral-nemo",
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

        # 🧠 Découpage des sections
        sections = {
            "objectif": "",
            "impact_eco": "",
            "impact_social": "",
            "impact_econ": "",
            "plan_action": ""
        }

        # 🔍 Extraction automatique selon les labels
        patterns = {
            "objectif": r"(?:Project Objective|Objectif du projet)\s*[:\-–]\s*(.+?)(?=(?:Ecological Impact|Impact écologique|$))",
            "impact_eco": r"(?:Ecological Impact|Impact écologique)\s*[:\-–]\s*(.+?)(?=(?:Social Impact|Impact social|$))",
            "impact_social": r"(?:Social Impact|Impact social)\s*[:\-–]\s*(.+?)(?=(?:Economic Impact|Impact économique|$))",
            "impact_econ": r"(?:Economic Impact|Impact économique)\s*[:\-–]\s*(.+?)(?=(?:Action Plan|Plan d’action|$))",
            "plan_action": r"(?:Action Plan|Plan d’action)\s*[:\-–]\s*(.+)"
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                sections[key] = clean_text(match.group(1))

        # Si IA n’a pas respecté la structure → fallback global
        if not any(sections.values()):
            sections["objectif"] = text
            sections["impact_eco"] = text
            sections["impact_social"] = text
            sections["impact_econ"] = text
            sections["plan_action"] = text

        return sections

    except Exception as e:
        st.error(f"❌ Error during AI fusion: {e}")
        return {
            "objectif": "Error",
            "impact_eco": "Error",
            "impact_social": "Error",
            "impact_econ": "Error",
            "plan_action": "Error"
        }

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

            except Exception as e:
                msg_error = (
                    f"❌ Error during analysis: {e}"
                    if st.session_state.lang == "English"
                    else f"❌ Erreur pendant l’analyse : {e}"
                )
                st.error(msg_error)

# ==============================
# 🧩 SYNTHÈSE DU PROJET — version finale bilingue stable
# ==============================
if "final_result" in st.session_state:
    with st.form("synthese_form"):
        st.subheader(titre_synthese)

        import re, requests

        # --- Récupération directe des données ---
        data = st.session_state.final_result
        objectif = data.get("objectif", "")
        impact_eco = data.get("impact_eco", "")
        impact_social = data.get("impact_social", "")
        impact_econ = data.get("impact_econ", "")
        plan_action = data.get("plan_action", "")

        # =======================
        # 🧹 Fonctions de nettoyage
        # =======================
        def clean_text_field(text):
            if not text or text.strip() in [".", "-", "•"]:
                return ""
            text = re.sub(r"\*+", "", text)
            text = re.sub(r"^[\-\*\d\.\)]+\s*", "", text, flags=re.MULTILINE)
            text = re.sub(r"\s+", " ", text.strip())
            return text.strip().capitalize()

        def first_sentence(text):
            text = clean_text_field(text)
            match = re.match(r'^(.*?[.!?])(\s|$)', text)
            return match.group(1).strip() if match else text.split('.')[0].strip() + '.'

        def format_action_plan(plan_text):
            """Nettoie et structure le plan d’action (3 étapes max)."""
            plan_text = clean_text_field(plan_text)
            steps = re.split(r'[.!?]', plan_text)
            steps = [s.strip() for s in steps if len(s.strip()) > 5]
            steps = steps[:3]
            if not steps:
                return ""
            return "\n".join([f"{i+1}. {step.capitalize()}." for i, step in enumerate(steps)])

        def detect_language(text):
            """Détecte rapidement si le texte est en anglais ou français."""
            english_kw = len(re.findall(r"\b(the|and|project|plan|step|impact|development|based|renewable|energy)\b", text, re.I))
            french_kw = len(re.findall(r"\b(le|la|et|projet|plan|étape|impact|développement|durable|énergie)\b", text, re.I))
            return "English" if english_kw > french_kw else "French"

        # ============================
        # 🧠 Préparation et nettoyage
        # ============================
        objectif = clean_text_field(objectif)
        impact_eco = first_sentence(impact_eco)
        impact_social = first_sentence(impact_social)
        impact_econ = first_sentence(impact_econ)
        plan_action = format_action_plan(plan_action)

        # ============================
        # 🌍 Vérifie et traduit si besoin
        # ============================
        detected_lang = detect_language(plan_action)

        if plan_action and st.session_state.lang == "French" and detected_lang == "English":
            try:
                role = "Tu es traducteur professionnel. Traduis ce plan d’action en français clair et fluide, garde la numérotation 1, 2, 3."
                payload = {
                    "model": "mistralai/mistral-nemo",
                    "messages": [
                        {"role": "system", "content": role},
                        {"role": "user", "content": plan_action}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 250
                }
                response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
                response.raise_for_status()
                plan_action = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            except Exception as e:
                plan_action = f"(Erreur de traduction automatique : {e})"

        elif plan_action and st.session_state.lang == "English" and detected_lang == "French":
            try:
                role = "You are a professional translator. Translate this action plan into English, keeping clear numbering 1, 2, 3."
                payload = {
                    "model": "mistralai/mistral-nemo",
                    "messages": [
                        {"role": "system", "content": role},
                        {"role": "user", "content": plan_action}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 250
                }
                response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
                response.raise_for_status()
                plan_action = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            except Exception as e:
                plan_action = f"(Translation error: {e})"

        # ============================
        # 🧾 Champs affichés à l’utilisateur
        # ============================
        st.session_state.objectif = st.text_area(
            "🎯 Objectif du projet" if st.session_state.lang == "French" else "🎯 Project Objective",
            objectif, height=100
        )
        st.session_state.impact_eco = st.text_area(
            "🌿 Impact écologique" if st.session_state.lang == "French" else "🌿 Ecological Impact",
            impact_eco, height=70
        )
        st.session_state.impact_social = st.text_area(
            "🤝 Impact social" if st.session_state.lang == "French" else "🤝 Social Impact",
            impact_social, height=70
        )
        st.session_state.impact_econ = st.text_area(
            "💰 Impact économique" if st.session_state.lang == "French" else "💰 Economic Impact",
            impact_econ, height=70
        )
        st.session_state.plan_action = st.text_area(
            "🧭 Plan d’action" if st.session_state.lang == "French" else "🧭 Action Plan",
            plan_action, height=150
        )

        # ============================
        # ✅ Validation du formulaire
        # ============================
        validated = st.form_submit_button(
            "✅ Valider et ajouter les informations du porteur"
            if st.session_state.lang == "French"
            else "✅ Validate and Add Project Owner Information"
        )

        if validated:
            st.session_state.validation_ok = True
            st.success(
                "✅ Sections validées avec succès ! Vous pouvez maintenant ajouter les informations du porteur."
                if st.session_state.lang == "French"
                else "✅ Sections successfully validated! You can now add the project owner information."
            )

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
