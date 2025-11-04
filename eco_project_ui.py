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

# --- Sous-titre descriptif ---
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
    user_input = f"Projet: {title}\nDescription: {description}\nObjectif: {objectif}\nLocalisation: {localisation}"
    return ask_agent(role, user_input)

# ==============================
# 🏡 INTERFACE STREAMLIT
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
    submitted = st.form_submit_button("🚀 Lancer l’analyse du projet")  # ✅ Nouveau texte ici

# ==============================
# 🧠 ANALYSE DU PROJET
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
            except Exception as e:
                st.error(f"Erreur pendant l’analyse : {e}")

# ==============================
# ✏️ SYNTHÈSE DU PROJET (phrases complètes et naturelles)
# ==============================
if "final_result" in st.session_state:
    with st.form("synthese_form"):
        st.subheader("📋 Synthèse du projet")

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
        st.session_state.objectif = st.text_area("🎯 Objectif du projet", objectif, height=100)
        st.session_state.impact_eco = st.text_area("🌿 Impact écologique", impact_eco, height=70)
        st.session_state.impact_social = st.text_area("🤝 Impact social", impact_social, height=70)
        st.session_state.impact_econ = st.text_area("💰 Impact économique", impact_econ, height=70)
        st.session_state.plan_action = st.text_area("🧭 Plan d’action", plan_action, height=140)

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
        status = st.selectbox("📊 Étape du projet",
                              ["Thinking", "Modélisation", "Construction", "Développement", "Financement", "Student"], index=0)
        saved = st.form_submit_button("💾 Enregistrer dans la base EVAD")

if saved:
    UPLOAD_URL = "https://app.nocodb.com/api/v2/storage/upload"
    headers = {"xc-token": NOCODB_API_TOKEN, "Content-Type": "application/json"}

    # --- Upload du fichier s’il existe ---
    file_attachment = []
    if uploaded_doc is not None:
        try:
            files = {"file": (uploaded_doc.name, uploaded_doc.getvalue())}
            upload_response = requests.post(UPLOAD_URL, headers={"xc-token": NOCODB_API_TOKEN}, files=files)

            if upload_response.status_code in (200, 201):
                upload_data = upload_response.json()
                if "list" in upload_data and len(upload_data["list"]) > 0:
                    f = upload_data["list"][0]
                    file_attachment = [{
                        "title": uploaded_doc.name,
                        "path": f["path"],
                        "url": f.get("url", f"https://app.nocodb.com{f['path']}"),
                        "mimetype": f.get("mimetype", uploaded_doc.type)
                    }]
                    st.toast("📎 Fichier uploadé avec succès", icon="📤")
                else:
                    st.warning("⚠️ Aucun fichier valide retourné par NoCoDB.")
            else:
                st.error(f"⚠️ Erreur upload ({upload_response.status_code}) : {upload_response.text}")
        except Exception as e:
            st.error(f"Erreur lors de l’upload du fichier : {e}")

    # --- Préparation du payload principal ---
    payload = {
        "Title": title,
        "Description": description,
        "Localisation": localisation,
        "Project Leader": leader,
        "Email": email,
        "Status": status,
        "Solution": st.session_state.solution if "solution" in st.session_state else st.session_state.objectif,
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

    # --- Si fichier joint, l’ajouter au bon format LISTE (non JSON string) ---
    if file_attachment:
        payload["Logo + docs"] = file_attachment  # ✅ format correct attendu par NoCoDB

    # --- Envoi vers NoCoDB ---
    try:
        r = requests.post(NOCODB_API_URL, headers=headers, json=payload)
        if r.status_code in (200, 201):
            st.success("🌿 Projet enregistré avec succès dans la base EVAD !")
            st.toast("Projet enregistré avec succès", icon="🌱")
        else:
            st.error(f"Erreur API {r.status_code} : {r.text}")
    except Exception as e:
        st.error(f"❌ Erreur lors de l’envoi à NoCoDB : {e}")
