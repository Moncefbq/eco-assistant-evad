import streamlit as st
import requests
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Formulaire Pilote d'impact", page_icon="🏡", layout="centered")

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
NOCODB_API_TOKEN = st.secrets["NOCODB_API_TOKEN"]
NOCODB_API_URL = st.secrets["NOCODB_API_URL"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# ⚙️ Données NoCoDB
NOCODB_API_TOKEN = "0JKfTbXfHzFC03lFmWwbzmB_IvhW5_Sd-S7AFcZe"
NOCODB_API_URL = "https://app.nocodb.com/api/v2/tables/mzaor3uiob3gbe2/records"
UPLOAD_URL = "https://app.nocodb.com/api/v2/storage/upload"


# --- Upload fichier vers NoCoDB ---
def upload_to_nocodb(file):
    headers = {"xc-token": NOCODB_API_TOKEN}
    files = {"files": (file.name, file, file.type or "application/octet-stream")}
    try:
        response = requests.post(UPLOAD_URL, headers=headers, files=files, timeout=15)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and "url" in result[0]:
            return result[0]["url"]
    except Exception as e:
        st.error(f"Erreur upload fichier : {e}")
    return None


# --- 🏡 Interface principale ---
st.title("🏡 Formulaire Pilote d'impact")
st.markdown("Décris ton idée, et l'IA t’aide à la structurer selon ton modèle NoCoDB.")

# --- 1️⃣ Formulaire utilisateur ---
with st.form("user_form"):
    title = st.text_input("🏷️ Nom du projet")
    description = st.text_area("📝 Description du projet")
    localisation = st.text_input("📍 Localisation")

    # ✅ Liste de types conforme à NoCoDB
    project_types = st.multiselect(
        "🌿 Type de projet",
        ["Third-place", "Eco-lieu", "Association", "Coworking", "Other", "Minecraft", "Permaculture"],
        default=["Eco-lieu"]
    )

    # ✅ Upload de document
    uploaded_doc = st.file_uploader("📄 Document lié au projet (optionnel)", type=["pdf", "png", "jpg", "jpeg", "docx"])

    submitted = st.form_submit_button("🚀 Lancer l’analyse")

# --- 2️⃣ Appel au modèle IA ---
if submitted:
    if not all([title, description, localisation]):
        st.warning("Merci de remplir tous les champs avant l’analyse.")
    else:
        with st.spinner("Analyse IA en cours..."):
            payload = {
                "model": "mistralai/mistral-nemo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Tu es un expert en gestion de projets à impact écologique et social. "
                            "Analyse les informations fournies et renvoie une réponse formatée ainsi :\n\n"
                            "Solution : ...\n"
                            "Impact écologique : ...\n"
                            "Impact social : ...\n"
                            "Impact économique : ...\n"
                            "Plan d’action : ...\n"
                            "Type suggéré : (choisir parmi : Third-place, Eco-lieu, Association, Coworking, Other, Minecraft, Permaculture)\n"
                            "Statut suggéré : (Thinking, Modélisation, Construction, Développement, Financement, Student)"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Projet: {title}\nDescription: {description}\nLocalisation: {localisation}"
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 800
            }

            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
                response.raise_for_status()
                ai_result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                st.session_state.ai_result = ai_result
                st.success("✅ Analyse IA terminée avec succès !")
            except Exception as e:
                st.error(f"Erreur IA : {e}")

# --- 3️⃣ Résultat IA affiché et modifiable ---
if "ai_result" in st.session_state:
    st.markdown("### ✏️ Synthèse IA (modifiable avant validation)")
    st.session_state.ai_result = st.text_area("🧠 Résultat généré :", st.session_state.ai_result, height=300)

    st.markdown("### 🔖 Ajuste le type et le statut")
    selected_type = st.multiselect(
        "Type de projet",
        ["Third-place", "Eco-lieu", "Association", "Coworking", "Other", "Minecraft", "Permaculture"],
        default=project_types
    )
    selected_status = st.selectbox(
        "Statut du projet",
        ["Thinking", "Modélisation", "Construction", "Développement", "Financement", "Student"],
        index=0
    )

    if st.button("✅ Valider et ajouter les informations du porteur"):
        st.session_state.validation_ok = True
        st.session_state.type = selected_type
        st.session_state.status = selected_status
        st.session_state.uploaded_doc = uploaded_doc


# --- 4️⃣ Informations du porteur + sauvegarde ---
if st.session_state.get("validation_ok"):
    st.markdown("### 👤 Informations du porteur")
    leader = st.text_input("Nom du porteur de projet")
    email = st.text_input("Email de contact")

    if st.button("💾 Enregistrer dans NoCoDB"):
        if not leader or not email:
            st.warning("Merci de remplir le nom et l’email.")
        else:
            with st.spinner("Sauvegarde du projet..."):
                doc_data = []
                if st.session_state.uploaded_doc:
                    url = upload_to_nocodb(st.session_state.uploaded_doc)
                    if url:
                        doc_data = [{"url": url}]

                payload = {
                    "Title": title,
                    "Description": description + "\n\n" + st.session_state.ai_result,
                    "Localisation": localisation,
                    "Type": st.session_state.type,
                    "Status": st.session_state.status,
                    "Project Leader": leader,
                    "Email": email,
                    "Documents": doc_data
                }

                headers = {"xc-token": NOCODB_API_TOKEN, "Content-Type": "application/json"}
                try:
                    r = requests.post(NOCODB_API_URL, headers=headers, json=payload, timeout=20)
                    if r.status_code in (200, 201):
                        st.success("🌿 Projet enregistré avec succès dans `Projects` !")
                        st.balloons()
                    else:
                        st.error(f"Erreur API {r.status_code} : {r.text}")
                except Exception as e:
                    st.error(f"Erreur de sauvegarde : {e}")
