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

st.markdown("""
### 🌍 Rejoignez EVAD pour co-développer votre projet de lieux régénératif !

Bienvenue dans **EVAD - Ecosystème Vivant Autonome et Décentralisé** — une platefome de pilotage d’impact nouvelle génération conçue pour faciliter la création de lieux partagés durables *(tiers-lieux, éco-lieux, coworking, ferme, etc.)* grâce à des outils open-source, une économie régénérative et une intelligence collaborative.

Nous invitons des porteurs de projet de lieux à rejoindre l'aventure pour co-construire un système résilient, décentralisé et gamifié, alignant les personnes, les projets et les ressources vers des résultats régénératifs mesurables.

---

### 🌱 Pourquoi EVAD ?

Le monde a besoin de nouveaux modèles de vie et de travail collectif, transparents, adaptatifs et ancrés dans une régénération concrète.

Pour cela, **EVAD intègre :**

✅ **Un commun régénératif open-source** : une base collaborative de solutions durables, d’indicateurs d’impact et de compétences pour créer le monde de demain.  
✅ **Un tableau de bord dynamique** : des widgets gamifiés pour suivre l'avancement du projet et ses métriques écologiques, sociales et économiques.  
✅ **Une modélisation 3D** : simulez et validez vos initiatives avant leur mise en œuvre réelle.  
✅ **Une assistance IA (Deva)** : aide locale pour l’audit, la sélection d’indicateurs et le suivi de projet.

EVAD n’est pas qu’un outil, c’est un écosystème vivant où **pilotes d'impact (porteurs de projet)**, **bâtisseurs d'impact (particuliers)** et **semeurs d'impact (financeurs)** co-créent des hubs autonomes et florissants fonctionnant en réseau.

✨ Imaginons un avenir durable… et construisons-le ensemble ! 🌱
""")

# --- 1️⃣ Formulaire utilisateur ---
with st.form("user_form"):
    title = st.text_input("🏷️ Nom du projet")
    description = st.text_area("📝 Description du projet")
    localisation = st.text_input("📍 Localisation")

    # 🌿 Type de projet (vide par défaut)
    project_types = st.multiselect(
        "🌿 Type de projet",
        ["Third-place", "Eco-lieu", "Association", "Coworking", "Autres", "Permaculture"],
        default=[]
    )

    # 📄 Document lié
    uploaded_doc = st.file_uploader("📄 Document lié au projet (optionnel)", type=["pdf", "png", "jpg", "jpeg", "docx"])

    submitted = st.form_submit_button("🚀 Lancer l’analyse")

# --- 2️⃣ Appel au modèle IA ---
if submitted:
    if not all([title, description, localisation]):
        st.warning("Merci de remplir tous les champs avant l’analyse.")
    else:
        with st.spinner("🔎 Recherche en cours..."):
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
                            "Type suggéré : (Third-place, Eco-lieu, Association, Coworking, Autres, Permaculture)\n"
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
                st.success("✅ Recherche terminée avec succès !")
            except Exception as e:
                st.error(f"Erreur IA : {e}")

# --- 3️⃣ Résultat IA affiché et modifiable ---
if "ai_result" in st.session_state:
    st.markdown("### ✏️ Synthèse IA (modifiable avant validation)")
    st.session_state.ai_result = st.text_area("🧠 Résultat généré :", st.session_state.ai_result, height=300)

    st.markdown("### 🔖 Ajuste le type et le statut")
    selected_type = st.multiselect(
        "Type de projet",
        ["Third-place", "Eco-lieu", "Association", "Coworking", "Autres", "Permaculture"],
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

