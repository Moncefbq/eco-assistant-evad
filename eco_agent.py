import streamlit as st
import requests
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Assistant Projet Écologique", page_icon="🌱", layout="centered")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"
NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/<ID_DE_TA_TABLE_PROJECTS>/records"
UPLOAD_URL = "https://app.nocodb.com/api/v2/storage/upload"

# --- FONCTION : Upload fichier vers NoCoDB ---
def upload_to_nocodb(file):
    headers = {"xc-token": NOCODB_API_TOKEN}
    files = {"files": (file.name, file, file.type or "image/png")}
    try:
        response = requests.post(UPLOAD_URL, headers=headers, files=files, timeout=15)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and "url" in result[0]:
            return result[0]["url"]
    except Exception as e:
        st.error(f"Erreur upload fichier : {e}")
    return None

# --- INTERFACE PRINCIPALE ---
st.title("🌍 Créateur de Projets Écologiques")
st.markdown("Décris ton idée et laisse l'IA enrichir ton projet !")

# --- 1️⃣ Formulaire initial utilisateur ---
with st.form("user_form"):
    title = st.text_input("🏷️ Nom du projet")
    description = st.text_area("📝 Description du projet")
    project_type = st.text_input("🌿 Type de projet (ex: Jardin, Solaire, Recyclage...)")
    localisation = st.text_input("📍 Localisation du projet")
    submitted = st.form_submit_button("🚀 Générer avec l’IA")

# --- 2️⃣ Analyse IA ---
if submitted:
    if not all([title, description, project_type, localisation]):
        st.warning("Merci de remplir tous les champs avant l'analyse.")
    else:
        with st.spinner("Analyse IA en cours..."):
            payload = {
                "model": "mistralai/mistral-nemo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Tu es un expert en développement durable. "
                            "À partir du nom, description, type et localisation, "
                            "génère une analyse structurée avec les sections suivantes :\n\n"
                            "Solution : (approche écologique ou innovation proposée)\n"
                            "Impact écologique : (effets positifs sur l’environnement)\n"
                            "Impact social : (bénéfices pour la communauté)\n"
                            "Impact économique : (modèle ou avantage financier durable)\n"
                            "Plan d’action : (étapes concrètes à suivre)\n\n"
                            "Réponds uniquement avec ces sections."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Nom: {title}\nDescription: {description}\nType: {project_type}\nLocalisation: {localisation}"
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 700
            }

            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
                response.raise_for_status()
                ai_text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                st.session_state.ai_result = ai_text
                st.success("✅ Analyse IA terminée !")
            except Exception as e:
                st.error(f"Erreur lors de la requête IA : {e}")

# --- 3️⃣ Résultat IA modifiable ---
if "ai_result" in st.session_state:
    st.markdown("### ✏️ Résumé du projet généré :")
    st.session_state.ai_result = st.text_area("🧠 Résultat IA :", st.session_state.ai_result, height=300)

    if st.button("✅ Valider et ajouter les informations du porteur"):
        st.session_state.validate = True

# --- 4️⃣ Saisie finale : porteur de projet + image ---
if st.session_state.get("validate"):
    st.markdown("### 👤 Informations du porteur de projet")
    leader = st.text_input("Nom du porteur de projet")
    email = st.text_input("Adresse email")
    uploaded_file = st.file_uploader("📎 Logo ou document du projet (optionnel)", type=["png", "jpg", "jpeg", "pdf"])

    if st.button("💾 Enregistrer le projet dans NoCoDB"):
        if not leader or not email:
            st.warning("Merci de renseigner le nom et l’email du porteur.")
        else:
            with st.spinner("Enregistrement du projet..."):
                logo_data = []
                if uploaded_file:
                    url = upload_to_nocodb(uploaded_file)
                    if url:
                        logo_data = [{"url": url}]

                payload = {
                    "Title": title,
                    "Description": description + "\n\n" + st.session_state.ai_result,
                    "Localisation": localisation,
                    "Type": project_type,
                    "Project Leader": leader,
                    "Email": email,
                    "Status": "En cours",
                    "Logo + docs": logo_data
                }

                headers = {"xc-token": NOCODB_API_TOKEN, "Content-Type": "application/json"}
                try:
                    response = requests.post(NOCODB_API_URL, headers=headers, json=payload, timeout=20)
                    if response.status_code in (200, 201):
                        st.success("🌿 Projet enregistré avec succès dans la table `Projects` !")
                        st.balloons()
                    else:
                        st.error(f"Erreur API : {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Erreur lors de la sauvegarde : {e}")

