# -*- coding: utf-8 -*-
import streamlit as st
import requests
import re
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
        "ai_result": "🧩 Résultat généré automatiquement :",
        "leader": "Nom du porteur de projet",
        "email": "Email de contact",
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
        "ai_result": "🧩 AI generated result:",
        "leader": "Project leader name",
        "email": "Contact email",
        "status": "📊 Project stage",
        "save": "💾 Save to EVAD database",
        "success": "🌿 Project successfully saved to the EVAD database !",
        "toast": "Project saved successfully",
    }
}
t = TEXTS[st.session_state.langue]

# --- EN-TÊTE EVAD (logo centré + bouton langue à droite) ---
@st.cache_data
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

logo_base64 = get_base64_image("evad_logo.png")

if logo_base64:
    col1, col2 = st.columns([8, 1])
    with col1:
        st.markdown(f"""
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;margin-top:20px;margin-bottom:10px;">
                <img src="data:image/png;base64,{logo_base64}" width="240" style="margin:0 auto;display:block;">
                <h1 style="font-size:2.1em;color:#014d3b;margin-top:10px;margin-bottom:5px;text-align:center;">
                    {t["title"]}
                </h1>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.button("🌐 " + ("EN" if st.session_state.langue == "Français" else "FR"), on_click=switch_langue)
    st.markdown("<hr style='border:none;height:2px;background-color:#cfeee7;margin:5px 0 20px 0;'>", unsafe_allow_html=True)
else:
    col1, col2 = st.columns([8, 1])
    with col1:
        st.markdown(f"<h1 style='text-align:center;color:#014d3b;'>{t['title']}</h1>", unsafe_allow_html=True)
    with col2:
        st.button("🌐 " + ("EN" if st.session_state.langue == "Français" else "FR"), on_click=switch_langue)
    st.markdown("<hr style='border:none;height:2px;background-color:#cfeee7;margin:10px 0 20px 0;'>", unsafe_allow_html=True)

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

# --- INTRO ---
st.markdown(f"### {t['intro_title']}\n{t['intro_text']}")

# --- CONFIGS ---
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
NOCODB_API_TOKEN = st.secrets["NOCODB_API_TOKEN"]
NOCODB_API_URL = st.secrets["NOCODB_API_URL"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}

# ==============================
# ⚡ FUSION IA (corrigée pour afficher la réponse)
# ==============================
def ask_agent(role_description, user_input):
    payload = {
        "model": "mistralai/mistral-nemo",
        "messages": [{"role": "system", "content": role_description}, {"role": "user", "content": user_input}],
        "temperature": 0.7, "max_tokens": 800
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    response.raise_for_status()
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

def MultiAgentFusion(title, description, objectif, localisation):
    if st.session_state.langue == "Français":
        role = "Tu es un système collaboratif composé de 4 experts : AnalystAgent, EcoAgent, PlannerAgent et CoordinatorAgent. Réponds uniquement en français avec les sections : Solution, Impact écologique, Impact social, Impact économique, Plan d’action."
    else:
        role = "You are a collaborative system composed of 4 experts. Respond only in English with the following sections: Solution, Ecological Impact, Social Impact, Economic Impact, Action Plan."
    user_input = f"Projet: {title}\nDescription: {description}\nObjectif: {objectif}\nLocalisation: {localisation}"
    return ask_agent(role, user_input)

# ==============================
# 🧾 FORMULAIRE PRINCIPAL
# ==============================
if "nb_espaces" not in st.session_state:
    st.session_state.nb_espaces = 1

with st.form("user_form"):
    st.markdown(f"<h2>{t['presentation']}</h2><p><i>{t['presentation_sub']}</i></p>", unsafe_allow_html=True)
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
# 🚀 ANALYSE DU PROJET (avec affichage du résultat IA)
# ==============================
if submitted:
    if not all([title, description, objectif, localisation]):
        st.warning(t["fill_warn"])
    else:
        with st.spinner(t["analyzing"]):
            try:
                final_result = MultiAgentFusion(title, description, objectif, localisation)
                st.session_state.final_result = final_result
                st.success(t["analyze_done"])
                st.markdown(f"### {t['ai_result']}")
                st.info(final_result)
            except Exception as e:
                st.error(f"Erreur IA : {e}")

# ==============================
# 🧑‍💼 ENREGISTREMENT FINAL (inchangé)
# ==============================
if st.session_state.get("final_result"):
    with st.form("porteur_form"):
        st.subheader("👤 Présentation du porteur")
        leader = st.text_input(t["leader"])
        email = st.text_input(t["email"])
        status = st.selectbox(
            t["status"],
            ["Thinking", "Modélisation", "Construction", "Développement", "Financement", "Student"],
            index=0
        )
        saved = st.form_submit_button(t["save"])
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
                        path = f.get("path", "")
                        if not path:
                            if "/nc/uploads/" in url:
                                path = url[url.index("/nc/"):]
                            elif "/nc/uploads/" in signed:
                                path = signed[signed.index("/nc/"):]
                            else:
                                path = f"/nc/uploads/{title}"

                        file_attachment = [{
                            "title": title, "path": path,
                            "url": signed or url, "mimetype": mimetype
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

            payload = {
                "Title": title, "Description": description, "Localisation": localisation,
                "Project Leader": leader, "Email": email, "Status": status,
                "Objectif du projet": objectif,
                "espace 1": espaces[0] if len(espaces) > 0 else "",
                "espace 2": espaces[1] if len(espaces) > 1 else "",
                "espace 3": espaces[2] if len(espaces) > 2 else "",
                "espace 4": espaces[3] if len(espaces) > 3 else "",
                "espace 5": espaces[4] if len(espaces) > 4 else "",
            }

            if file_attachment:
                payload["Logo + docs"] = file_attachment

            try:
                r = requests.post(NOCODB_API_URL, headers=headers, json=payload)
                if r.status_code in (200, 201):
                    st.success(t["success"])
                    st.toast(t["toast"], icon="🌱")
                else:
                    st.error(f"Erreur API {r.status_code} : {r.text}")
            except Exception as e:
                st.error(f"❌ Erreur lors de l’envoi à NoCoDB : {e}")




