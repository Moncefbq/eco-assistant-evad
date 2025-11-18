# -*- coding: utf-8 -*-
import streamlit as st
import requests
import re
import base64
import json

# ==============================
# ⚙️ CONFIG GÉNÉRALE
# ==============================
st.set_page_config(
    page_title="Formulaire Bâtisseur",
    page_icon="🧑‍🌾",
    layout="centered"
)

# --- CONFIG NOCODB ---
# Tu peux garder les secrets si tu veux, ou juste utiliser la clé en dur.
NOCODB_API_TOKEN = st.secrets.get("NOCODB_API_TOKEN", "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe")

# TABLE Projects (projets)
PROJECTS_API_URL = "https://app.nocodb.com/api/v2/tables/mzaor3uiob3gbe2/records"

# TABLE Builders (bâtisseurs)
BUILDERS_API_URL = "https://app.nocodb.com/api/v2/tables/mnh4vojl5zy7bvx/records"

# UPLOAD fichiers (Photo builder)
UPLOAD_URL = "https://app.nocodb.com/api/v2/storage/upload"

HEADERS_NC = {
    "xc-token": NOCODB_API_TOKEN,
    "Accept": "application/json"
}

# ==============================
# 🖼️ LOGO & STYLE GLOBAL (même que formulaire pilote)
# ==============================
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

        </div>
        <hr style="border: none; height: 2px; background-color: #cfeee7; margin: 5px 0 20px 0;">
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <h1 style="text-align:center; color:#014d3b;">Impact Builder Form</h1>
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

# ==============================
# 🌐 Sélecteur de langue
# ==============================
if "lang" not in st.session_state:
    st.session_state.lang = "Français"

col1, col2 = st.columns(2)
with col1:
    if st.button("🇫🇷 Français", key="fr_button_builder", use_container_width=True):
        st.session_state.lang = "Français"
        st.rerun()
with col2:
    if st.button("🇬🇧 English", key="en_button_builder", use_container_width=True):
        st.session_state.lang = "English"
        st.rerun()

# --- Sous-titre ---
if st.session_state.lang == "English":
    st.markdown("""
    ### 🧑‍🌾 Join EVAD as a Builder
    Tell us who you are and we’ll connect you with regenerative projects that match your location and skills.
    """)
else:
    st.markdown("""
    ### 🧑‍🌾 Rejoignez EVAD en tant que bâtisseur
    Présentez-vous et nous vous connectons avec des projets régénératifs proches de votre localisation et de vos compétences.
    """)

# ==============================
# 🏷️ Libellés multilingues
# ==============================
if st.session_state.lang == "English":
    labels = {
        "builder_title": "🧑‍🌾 Builder Profile",
        "builder_intro": "Tell us more about who you are and what you are looking for.",
        "name": "Full Name",
        "photo": "Profile Photo (optional)",
        "motivation": "Motivation",
        "localisation": "Preferred Location",
        "skills_acquired": "Skills you already have",
        "skills_to_develop": "Skills you want to develop",
        "submit_builder": "🔍 Find a matching project",
        "match_title": "🎯 Matching Project",
        "no_match": "No project was found for this location.",
        "open_pilot": "➡️ Open the project pilot form",
        "save_builder": "✅ Save my builder profile in EVAD",
        "saved_ok": "🌿 Builder successfully saved in the EVAD database!",
        "saved_err": "❌ Error while saving the builder in EVAD:",
        "project_name": "Project name",
        "project_location": "Project location",
        "project_plan": "Project action plan"
    }
else:
    labels = {
        "builder_title": "🧑‍🌾 Profil Bâtisseur",
        "builder_intro": "Parlez-nous de vous et de ce que vous cherchez.",
        "name": "Nom complet",
        "photo": "Photo de profil (optionnel)",
        "motivation": "Motivation",
        "localisation": "Localisation souhaitée",
        "skills_acquired": "Compétences déjà acquises",
        "skills_to_develop": "Compétences à développer",
        "submit_builder": "🔍 Rechercher un projet correspondant",
        "match_title": "🎯 Projet correspondant",
        "no_match": "Aucun projet n’a été trouvé pour cette localisation.",
        "open_pilot": "➡️ Ouvrir le formulaire pilote de projet",
        "save_builder": "✅ Enregistrer mon profil bâtisseur dans EVAD",
        "saved_ok": "🌿 Bâtisseur enregistré avec succès dans la base EVAD !",
        "saved_err": "❌ Erreur lors de l’enregistrement du bâtisseur dans EVAD :",
        "project_name": "Nom du projet",
        "project_location": "Localisation du projet",
        "project_plan": "Plan d’action du projet"
    }

# ==============================
# 🧑‍🌾 FORMULAIRE BÂTISSEUR
# ==============================
with st.form("builder_form"):
    st.markdown(f"""
        <h2 style='margin-bottom: 0;'>{labels['builder_title']}</h2>
        <p style='margin-top: 2px; color:#014d3b; font-style: italic;'>
            {labels['builder_intro']}
        </p>
    """, unsafe_allow_html=True)

    builder_name = st.text_input(f"👤 {labels['name']}")
    localisation = st.text_input(f"📍 {labels['localisation']}")
    motivation = st.text_area(f"📝 {labels['motivation']}", height=100)
    skills_acquired = st.text_area(f"✅ {labels['skills_acquired']}", height=80)
    skills_to_develop = st.text_area(f"🌱 {labels['skills_to_develop']}", height=80)
    photo_file = st.file_uploader(f"📷 {labels['photo']}", type=["png", "jpg", "jpeg"])

    submitted_builder = st.form_submit_button(labels["submit_builder"])

# ==============================
# 🔎 RECHERCHE PROJET APRÈS SOUMISSION
# ==============================
if submitted_builder:
    if not builder_name or not localisation or not motivation:
        if st.session_state.lang == "English":
            st.warning("⚠️ Please fill in at least name, location and motivation.")
        else:
            st.warning("⚠️ Merci de remplir au minimum le nom, la localisation et la motivation.")
    else:
        # On stocke les données du builder dans le session_state
        st.session_state.builder_data = {
            "Name": builder_name,
            "Localisation": localisation,
            "Motivation": motivation,
            "Skills_acquired": skills_acquired,
            "Skills_to_develop": skills_to_develop,
        }
        st.session_state.builder_photo_file = photo_file

        # Recherche de projet correspondant côté Projects
        try:
            r = requests.get(PROJECTS_API_URL, headers=HEADERS_NC)
            r.raise_for_status()
            data = r.json()
            project_list = data.get("list", data.get("results", []))

            # Filtre par localisation (insensible à la casse et aux espaces)
            loc_norm = localisation.strip().lower()
            matched_projects = [
                p for p in project_list
                if str(p.get("Localisation", "")).strip().lower() == loc_norm
            ]

            if matched_projects:
                st.session_state.matched_project = matched_projects[0]
                st.session_state.project_found = True
            else:
                st.session_state.matched_project = None
                st.session_state.project_found = False

        except Exception as e:
            st.error(f"❌ Erreur lors de la récupération des projets : {e}")
            st.session_state.matched_project = None
            st.session_state.project_found = False

# ==============================
# 🎯 AFFICHAGE DU RÉSULTAT MATCHING + BOUTON SAVE
# ==============================
if "builder_data" in st.session_state:
    builder_data = st.session_state.builder_data
    project = st.session_state.get("matched_project", None)
    project_found = st.session_state.get("project_found", False)

    st.markdown("---")

    if project_found and project is not None:
        # Projet trouvé
        st.subheader(labels["match_title"])

        proj_title = project.get("Title", "—")
        proj_loc = project.get("Localisation", "—")
        proj_plan = project.get("plan_action", "") or project.get("Plan d’action", "")

        st.markdown(f"**{labels['project_name']} :** {proj_title}")
        st.markdown(f"**{labels['project_location']} :** {proj_loc}")
        st.markdown(f"**{labels['project_plan']} :**")
        st.write(proj_plan)

        suggested_project = proj_title
        match_score = 100

    else:
        # Aucun projet trouvé
        st.warning(labels["no_match"])

        # Bouton vers le formulaire pilote
        pilot_url = "https://eco-assistant-evad-qr7cswdr5btwkxtbkmfbdu.streamlit.app/#rejoignez-evad-pour-co-developper-votre-projet-de-lieux-regeneratif"
        st.markdown(f"[{labels['open_pilot']}]({pilot_url})", unsafe_allow_html=True)

        suggested_project = ""
        match_score = 0

    # ==============================
    # 💾 BOUTON D'ENREGISTREMENT BUILDER
    # ==============================
    save_clicked = st.button(labels["save_builder"])

    if save_clicked:
        # Upload de la photo si fournie
        photo_attachment = []
        if st.session_state.get("builder_photo_file") is not None:
            try:
                uploaded = st.session_state.builder_photo_file
                files = {"file": (uploaded.name, uploaded.getvalue())}
                up = requests.post(UPLOAD_URL, headers=HEADERS_NC, files=files)
                up.raise_for_status()
                resp = up.json()

                if isinstance(resp, dict) and "list" in resp:
                    f = resp["list"][0]
                elif isinstance(resp, list) and len(resp) > 0:
                    f = resp[0]
                else:
                    f = None

                if f:
                    url = f.get("url", "")
                    signed = f.get("signedUrl", "")
                    title_doc = f.get("title", uploaded.name)
                    mimetype = f.get("mimetype", uploaded.type or "image/png")
                    path = f.get("path", "")

                    if not path:
                        if "/nc/" in url:
                            path = url[url.index("/nc/"):]
                        elif "/nc/" in signed:
                            path = signed[signed.index("/nc/"):]
                        else:
                            path = f"/nc/uploads/{title_doc}"

                    photo_attachment = [{
                        "title": title_doc,
                        "path": path,
                        "url": signed or url,
                        "mimetype": mimetype
                    }]

            except Exception as e:
                st.error(f"Erreur lors de l’upload de la photo : {e}")

        # Construction du payload pour la table builders
        payload_builder = {
            "Title": builder_data["Name"],
            "Name": builder_data["Name"],
            "Status": "New",
            "Motivation": builder_data["Motivation"],
            "Localisation": builder_data["Localisation"],
            "Skills_acquired": builder_data["Skills_acquired"],
            "Skills_to_develop": builder_data["Skills_to_develop"],
            "Suggested_Project": suggested_project,
            "Match_Score": match_score
        }

        if photo_attachment:
            payload_builder["Photo"] = photo_attachment

        try:
            r_save = requests.post(BUILDERS_API_URL, headers=HEADERS_NC, json=payload_builder)
            if r_save.status_code in (200, 201):
                st.success(labels["saved_ok"])
                st.toast(labels["saved_ok"], icon="🌿")
            else:
                st.error(f"{labels['saved_err']} {r_save.status_code} – {r_save.text}")
        except Exception as e:
            st.error(f"{labels['saved_err']} {e}")

