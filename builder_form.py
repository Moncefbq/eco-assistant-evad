# -*- coding: utf-8 -*-
import streamlit as st
import requests
import base64

# ==============================
# ⚙️ CONFIG GÉNÉRALE
# ==============================
st.set_page_config(
    page_title="Formulaire Bâtisseur",
    page_icon="🧑‍🌾",
    layout="centered"
)

# --- CONFIG NOCODB ---
NOCODB_API_TOKEN = st.secrets.get("NOCODB_API_TOKEN", "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe")

PROJECTS_API_URL = "https://app.nocodb.com/api/v2/tables/mzaor3uiob3gbe2/records"
BUILDERS_API_URL = "https://app.nocodb.com/api/v2/tables/mnh4vojl5zy7bvx/records"
UPLOAD_URL = "https://app.nocodb.com/api/v2/storage/upload"

HEADERS_NC = {
    "xc-token": NOCODB_API_TOKEN,
    "Accept": "application/json"
}

# ==============================
# 🖼️ LOGO
# ==============================
@st.cache_data
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo = get_base64_image("evad_logo.png")

if logo:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <img src="data:image/png;base64,{logo}" width="240">
        </div>
        <hr style="border:none;height:2px;background:#cfeee7;margin:10px 0 20px;">
        """,
        unsafe_allow_html=True
    )

# ==============================
# 🎨 STYLE GLOBAL
# ==============================
st.markdown("""
<style>
div.stForm {
    background-color: #018262 !important;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
}
div.stForm > div {
    background-color: #cfeee7 !important;
    border-radius: 15px;
    padding: 20px;
}
.stButton button {
    background-color: #018262 !important;
    color: white !important;
    border-radius: 8px;
    font-weight: bold;
}
.stButton button:hover {
    background-color: #01614c !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🌐 LANGUE
# ==============================
if "lang" not in st.session_state:
    st.session_state.lang = "Français"

col1, col2 = st.columns(2)
with col1:
    if st.button("🇫🇷 Français", key="lang_fr", use_container_width=True):
        st.session_state.lang = "Français"
        st.rerun()
with col2:
    if st.button("🇬🇧 English", key="lang_en", use_container_width=True):
        st.session_state.lang = "English"
        st.rerun()

# ==============================
# 🏷️ LIBELLÉS
# ==============================
if st.session_state.lang == "English":
    labels = {
        "builder_title": "🧑‍🌾 Builder Profile",
        "builder_intro": "Tell us more about yourself.",
        "name": "Full Name",
        "photo": "Profile Photo (optional)",
        "motivation": "Motivation",
        "localisation": "Preferred Location",
        "skills_acquired": "Skills already acquired",
        "skills_to_develop": "Skills to develop",
        "submit_builder": "🔍 Find matching project",
        "match_title": "🎯 Matching Project",
        "no_match": "No project found for this location.",
        "open_pilot": "➡️ Open project pilot form",
        "save_builder": "✅ Save my builder profile",
        "saved_ok": "🌿 Builder saved successfully!",
        "saved_err": "❌ Error while saving builder:",
        "project_name": "Project name",
        "project_location": "Project location",
        "project_plan": "Project action plan",
    }
else:
    labels = {
        "builder_title": "🧑‍🌾 Profil Bâtisseur",
        "builder_intro": "Parlez-nous de vous.",
        "name": "Nom complet",
        "photo": "Photo de profil (optionnel)",
        "motivation": "Motivation",
        "localisation": "Localisation souhaitée",
        "skills_acquired": "Compétences déjà acquises",
        "skills_to_develop": "Compétences à développer",
        "submit_builder": "🔍 Rechercher un projet correspondant",
        "match_title": "🎯 Projet correspondant",
        "no_match": "Aucun projet trouvé pour cette localisation.",
        "open_pilot": "➡️ Ouvrir le formulaire projet pilote",
        "save_builder": "✅ Enregistrer mon profil bâtisseur",
        "saved_ok": "🌿 Bâtisseur enregistré avec succès !",
        "saved_err": "❌ Erreur lors de l’enregistrement :",
        "project_name": "Nom du projet",
        "project_location": "Localisation du projet",
        "project_plan": "Plan d’action du projet",
    }

# ==============================
# 🧑‍🌾 FORMULAIRE
# ==============================
with st.form("builder_form"):
    st.markdown(f"<h2>{labels['builder_title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{labels['builder_intro']}</p>", unsafe_allow_html=True)

    name = st.text_input("👤 " + labels["name"])
    localisation = st.text_input("📍 " + labels["localisation"])
    motivation = st.text_area("📝 " + labels["motivation"])
    skills_acquired = st.text_area("✅ " + labels["skills_acquired"])
    skills_to_develop = st.text_area("🌱 " + labels["skills_to_develop"])
    photo = st.file_uploader("📷 " + labels["photo"], type=["png", "jpg", "jpeg"])

    submitted = st.form_submit_button(labels["submit_builder"], use_container_width=True)

# ==============================
# 🔎 RECHERCHE PROJET
# ==============================
if submitted:
    if not name or not localisation or not motivation:
        st.warning("⚠️ Merci de remplir tous les champs obligatoires.")
    else:
        st.session_state.builder_data = {
            "Name": name,
            "Localisation": localisation,
            "Motivation": motivation,
            "Skills_acquired": skills_acquired,
            "Skills_to_develop": skills_to_develop,
        }
        st.session_state.builder_photo = photo

        r = requests.get(PROJECTS_API_URL, headers=HEADERS_NC).json()
        projects = r.get("list", [])

        loc_norm = localisation.strip().lower()
        matches = [p for p in projects if str(p.get("Localisation", "")).strip().lower() == loc_norm]

        st.session_state.project = matches[0] if matches else None

# ==============================
# 🎨 PROJET CORRESPONDANT (CADRE)
# ==============================
if "builder_data" in st.session_state:

    project = st.session_state.project

    st.markdown("""
        <div style="background:#018262;padding:25px;border-radius:20px;margin-top:25px;
                    box-shadow:0 4px 15px rgba(0,0,0,0.15);">
            <div style="background:#cfeee7;padding:25px;border-radius:15px;">
    """, unsafe_allow_html=True)

    st.markdown(f"<h2>{labels['match_title']}</h2>", unsafe_allow_html=True)

    if project:
        st.markdown(f"**{labels['project_name']} :** {project.get('Title','—')}")
        st.markdown(f"**{labels['project_location']} :** {project.get('Localisation','—')}")
        st.markdown(f"**{labels['project_plan']} :**")
        st.markdown(f"<div style='white-space:pre-wrap;font-size:15px'>{project.get('plan_action','—')}</div>", unsafe_allow_html=True)
    else:
        st.warning(labels["no_match"])

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ==============================
    # 💾 ENREGISTREMENT BUILDER
    # ==============================
    if st.button(labels["save_builder"], key="save_btn", use_container_width=True):

        # Upload photo
        photo_attachment = []
        if st.session_state.builder_photo:
            up = requests.post(UPLOAD_URL, headers=HEADERS_NC,
                               files={"file": (st.session_state.builder_photo.name,
                                               st.session_state.builder_photo.getvalue())}).json()
            f = up["list"][0]
            photo_attachment = [{
                "title": f.get("title", ""),
                "path": f.get("path", ""),
                "url": f.get("signedUrl", ""),
                "mimetype": f.get("mimetype", "image/png")
            }]

        payload = st.session_state.builder_data.copy()
        payload["Suggested_Project"] = project.get("Title") if project else ""
        payload["Photo"] = photo_attachment

        r = requests.post(BUILDERS_API_URL, headers=HEADERS_NC, json=payload)

        if r.status_code in (200, 201):
            st.success(labels["saved_ok"])
        else:
            st.error(labels["saved_err"] + str(r.text))


