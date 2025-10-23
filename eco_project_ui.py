import streamlit as st
from eco_agent import clean_text  # tu peux réutiliser tes fonctions utilitaires
import requests
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Assistant Projet Écologique", page_icon="🌍", layout="centered")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"
NOCODB_PROJECTS_TABLE = "https://app.nocodb.com/api/v2/tables/<mzaor3uiob3gbe2>/records"

# --- Titre principal ---
st.title("🌱 Créateur de Projets Écologiques Intelligents")
st.markdown("""
Décris ton idée, et l'IA t’aidera à générer :
- une **solution écologique adaptée**
- un **impact social, écologique et économique**
- un **plan d’action clair**
""")

# --- 1️⃣ Formulaire utilisateur ---
with st.form("project_form"):
    name = st.text_input("🏷️ Nom du projet")
    description = st.text_area("📝 Description du projet", placeholder="Décris ton idée écologique...")
    project_type = st.text_input("🌿 Type de projet (ex: Jardin, Énergie, Recyclage...)")
    localisation = st.text_input("📍 Localisation du projet")

    submitted = st.form_submit_button("🚀 Analyser avec l'IA")

# --- 2️⃣ Analyse IA ---
if submitted:
    if not all([name, description, project_type, localisation]):
        st.warning("Merci de remplir tous les champs avant d’analyser.")
    else:
        with st.spinner("Analyse intelligente en cours..."):
            payload = {
                "model": "mistralai/mistral-nemo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Tu es un expert en projets durables. À partir du nom, de la description, du type et de la localisation, "
                            "génère un plan d’action clair structuré comme suit :\n\n"
                            "Solution : (stratégie ou approche écologique proposée)\n"
                            "Impact écologique : (effet positif sur l’environnement)\n"
                            "Impact social : (bénéfices pour la communauté)\n"
                            "Impact économique : (modèle de durabilité financière)\n"
                            "Plan d’action : (liste claire d’étapes à suivre)\n\n"
                            "Réponds dans ce format exact, sans texte inutile."
                        )
                    },
                    {"role": "user", "content": f"Nom: {name}\nDescription: {description}\nType: {project_type}\nLocalisation: {localisation}"}
                ]
            }

            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
                response.raise_for_status()
                content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

                st.session_state.ai_result = content
                st.success("✅ Analyse IA terminée ! Modifie si besoin avant validation.")
            except Exception as e:
                st.error(f"Erreur d’appel IA : {e}")

# --- 3️⃣ Affichage & édition du résultat ---
if "ai_result" in st.session_state:
    st.markdown("### ✏️ Résumé du projet généré par l’IA :")
    ai_text = st.text_area("Résultat IA :", value=st.session_state.ai_result, height=250)
    st.session_state.ai_result = ai_text

    if st.button("✅ Valider et ajouter le porteur du projet"):
        st.session_state.validation_ok = True

# --- 4️⃣ Formulaire final du porteur ---
if st.session_state.get("validation_ok"):
    st.markdown("### 👤 Informations du porteur de projet")
    leader_name = st.text_input("Nom complet")
    leader_email = st.text_input("Email de contact")

    if st.button("💾 Enregistrer le projet dans NoCoDB"):
        if not leader_name or not leader_email:
            st.warning("Merci de renseigner le nom et l’email du porteur.")
        else:
            with st.spinner("Sauvegarde dans la base..."):
                payload = {
                    "Name": name,
                    "Description": description,
                    "Type": project_type,
                    "Localisation": localisation,
                    "AI_Result": st.session_state.ai_result,
                    "Leader_Name": leader_name,
                    "Leader_Email": leader_email
                }

                headers = {"xc-token": NOCODB_API_TOKEN, "Content-Type": "application/json"}
                try:
                    response = requests.post(NOCODB_PROJECTS_TABLE, headers=headers, json=payload, timeout=20)
                    if response.status_code in (200, 201):
                        st.success("🌿 Projet enregistré avec succès dans la table `projects` !")
                        st.balloons()
                    else:
                        st.error(f"Erreur {response.status_code} : {response.text}")
                except Exception as e:
                    st.error(f"Erreur de sauvegarde : {e}")
