# -*- coding: utf-8 -*-
import streamlit as st
import requests
import re
# --- EN-TÊTE EVAD (logo centré et plus grand, version rapide) ---
import base64

@st.cache_data
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

logo_base64 = get_base64_image("evad_logo.png")

# ✅ Logo centré, un peu plus grand, sans ralentissement
if logo_base64:
    st.markdown(f"""
        <div style="
            text-align: center;
            margin-top: 15px;
            margin-bottom: 30px;
        ">
            <img src="data:image/png;base64,{logo_base64}" width="200" style="margin-bottom: 15px;">
            <h1 style="font-size: 2.1em; color: #014d3b; margin: 0;">
                Formulaire Pilote d'impact
            </h1>
        </div>
        <hr style="border: none; height: 2px; background-color: #cfeee7; margin: 20px 0 30px 0;">
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <h1 style="text-align:center; color:#014d3b;">Formulaire Pilote d'impact</h1>
        <hr style="border: none; height: 2px; background-color: #cfeee7; margin: 20px 0 30px 0;">
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

# 🌿 STYLE GLOBAL
st.markdown("""
<style>
body {
    background-color: #f5f5f5;
    color: #000000 !important;
}

/* ✅ Rectangle principal : vert clair */
section.main > div {
    background-color: #cfeee7 !important;
    border-radius: 20px;
    padding: 20px !important;
}

/* ✅ Formulaires internes : vert foncé */
.stForm, .stForm > div {
    background-color: #018262 !important;
    color: #000000 !important;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.25);
    margin-bottom: 25px;
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
    background-color: #00b300 !important;
    color: white !important;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}

.stButton button:hover {
    background-color: #009900 !important;
}
</style>
""", unsafe_allow_html=True)

# --- SECRETS ---
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
NOCODB_API_TOKEN = st.secrets["NOCODB_API_TOKEN"]
NOCODB_API_URL = st.secrets["NOCODB_API_URL"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}

# --- NoCoDB CONFIG ---
NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"
NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/mzaor3uiob3gbe2/records"
UPLOAD_URL = "https://app.nocodb.com/api/v2/storage/upload"

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

def MultiAgentFusion(title, description, localisation):
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
    user_input = f"Projet: {title}\nDescription: {description}\nLocalisation: {localisation}"
    return ask_agent(role, user_input)

# ==============================
# 🏡 INTERFACE STREAMLIT
# ==============================
if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1

with st.form("user_form"):
    st.subheader("🧾 Informations sur le projet")

    title = st.text_input("🏷️ Nom du projet")
    description = st.text_area("📝 Description du projet")
    localisation = st.text_input("📍 Localisation")

    # Espaces dynamiques
    st.markdown("### 🏡 Espaces du projet")
    espaces = []
    for i in range(st.session_state.nb_espaces):
        espaces.append(st.text_area(f"🏠 Espace {i+1}", key=f"espace_{i+1}", height=80))

    if st.session_state.nb_espaces < 5:
        if st.form_submit_button("➕ Ajouter un espace"):
            st.session_state.nb_espaces += 1
            st.rerun()

    uploaded_doc = st.file_uploader("📄 Document lié (optionnel)", type=["pdf", "png", "jpg", "jpeg", "docx"])
    submitted = st.form_submit_button("🚀 Lancer l’analyse collaborative")

# ==============================
# 🧠 ANALYSE COLLABORATIVE
# ==============================
if submitted:
    if not all([title, description, localisation]):
        st.warning("Merci de remplir tous les champs avant l’analyse.")
    else:
        with st.spinner("🌱 Analyse collaborative du projet en cours..."):
            try:
                final_result = MultiAgentFusion(title, description, localisation)
                st.session_state.final_result = final_result
                st.success("✅ Analyse collaborative terminée avec succès !")
            except Exception as e:
                st.error(f"Erreur pendant l’analyse : {e}")

# ==============================
# ✏️ SYNTHÈSE COLLABORATIVE
# ==============================
if "final_result" in st.session_state:
    with st.form("synthese_form"):
        st.subheader("📋 Synthèse collaborative du projet")

        def extract_section(text, section):
            pattern = rf"{section}\s*:\s*(.*?)(?=\n[A-ZÉÈÊÂÎÔÙÇ]|$)"
            match = re.search(pattern, text, re.DOTALL)
            return match.group(1).strip() if match else ""

        text = st.session_state.final_result

        st.session_state.solution = st.text_area("💡 Solution", extract_section(text, "Solution"), height=120)
        st.session_state.impact_eco = st.text_area("🌿 Impact écologique", extract_section(text, "Impact écologique"), height=120)
        st.session_state.impact_social = st.text_area("🤝 Impact social", extract_section(text, "Impact social"), height=120)
        st.session_state.impact_econ = st.text_area("💰 Impact économique", extract_section(text, "Impact économique"), height=120)
        st.session_state.plan_action = st.text_area("🧭 Plan d’action", extract_section(text, "Plan d’action"), height=140)

        validated = st.form_submit_button("✅ Valider et ajouter les informations du porteur")
        if validated:
            st.session_state.validation_ok = True
            st.success("✅ Sections validées avec succès !")

# ==============================
# 🧑‍💼 ENREGISTREMENT FINAL
# ==============================
if st.session_state.get("validation_ok"):
    with st.form("porteur_form"):
        st.subheader("👤 Informations du porteur")
        leader = st.text_input("Nom du porteur de projet")
        email = st.text_input("Email de contact")
        status = st.selectbox("📊 Statut du projet",
                              ["Thinking", "Modélisation", "Construction", "Développement", "Financement", "Student"], index=0)
        saved = st.form_submit_button("💾 Enregistrer dans NoCoDB")

        if saved:
            headers = {"xc-token": NOCODB_API_TOKEN, "Content-Type": "application/json"}
            payload = {
                "Title": title,
                "Description": description,
                "Localisation": localisation,
                "Project Leader": leader,
                "Email": email,
                "Status": status,
                "Solution": st.session_state.solution,
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
            r = requests.post(NOCODB_API_URL, headers=headers, json=payload)
            if r.status_code in (200, 201):
                st.success("🌿 Projet enregistré avec succès dans `Projects` !")
                st.toast("✅ Données synchronisées avec NoCoDB", icon="🌱")
            else:
                st.error(f"Erreur API {r.status_code} : {r.text}")




