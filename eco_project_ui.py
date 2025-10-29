import streamlit as st
import requests
import re
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

    # 🌿 Type de projet
    project_types = st.multiselect(
        "🌿 Type de projet",
        ["Third-place", "Eco-lieu", "Association", "Coworking", "Autres", "Permaculture"],
        default=[]
    )

    # 📄 Document lié
    uploaded_doc = st.file_uploader("📄 Document lié au projet (optionnel)", type=["pdf", "png", "jpg", "jpeg", "docx"])

    submitted = st.form_submit_button("🚀 Lancer l’analyse")

# --- 2️⃣ Appel au modèle ---
if submitted:
    if not all([title, description, localisation]):
        st.warning("Merci de remplir tous les champs avant la recherche.")
    else:
        with st.spinner("🔎 Recherche en cours..."):
            payload = {
                "model": "mistralai/mistral-nemo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Tu es un expert en gestion de projets écologiques. "
                            "Analyse les informations et renvoie une réponse formatée ainsi :\n\n"
                            "Solution : ...\n"
                            "Impact écologique : ...\n"
                            "Impact social : ...\n"
                            "Impact économique : ...\n"
                            "Plan d’action : ..."
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
                ai_text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                st.session_state.ai_result = ai_text
                st.success("✅ Recherche terminée avec succès !")
            except Exception as e:
                st.error(f"Erreur pendant la génération : {e}")


# --- 3️⃣ Synthèse structurée et modifiable ---
if "ai_result" in st.session_state:
    st.markdown("## ✏️ Synthèse du projet (modifiable avant validation)")

    def extract_section(text, section):
        pattern = rf"{section}\s*:\s*(.*?)(?=\n[A-ZÉÈÊÂÎÔÙÇ]|$)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""

    solution = extract_section(st.session_state.ai_result, "Solution")
    impact_eco = extract_section(st.session_state.ai_result, "Impact écologique")
    impact_social = extract_section(st.session_state.ai_result, "Impact social")
    impact_econ = extract_section(st.session_state.ai_result, "Impact économique")
    plan_action = extract_section(st.session_state.ai_result, "Plan d’action")

    st.markdown('<div style="background-color:#e6f5ec; padding:12px; border-radius:10px;">💡 **Solution**</div>', unsafe_allow_html=True)
    solution = st.text_area("", value=solution, height=90, label_visibility="collapsed")

    st.markdown('<div style="background-color:#dff5e3; padding:12px; border-radius:10px;">🌿 **Impact écologique**</div>', unsafe_allow_html=True)
    impact_eco = st.text_area("", value=impact_eco, height=90, label_visibility="collapsed")

    st.markdown('<div style="background-color:#eaf6ff; padding:12px; border-radius:10px;">🤝 **Impact social**</div>', unsafe_allow_html=True)
    impact_social = st.text_area("", value=impact_social, height=90, label_visibility="collapsed")

    st.markdown('<div style="background-color:#fff4e6; padding:12px; border-radius:10px;">💰 **Impact économique**</div>', unsafe_allow_html=True)
    impact_econ = st.text_area("", value=impact_econ, height=90, label_visibility="collapsed")

    st.markdown('<div style="background-color:#f9eefb; padding:12px; border-radius:10px;">🧭 **Plan d’action**</div>', unsafe_allow_html=True)
    plan_action = st.text_area("", value=plan_action, height=110, label_visibility="collapsed")

    if st.button("✅ Valider et ajouter les informations du porteur"):
        st.session_state.validation_ok = True
        st.session_state.solution = solution
        st.session_state.impact_eco = impact_eco
        st.session_state.impact_social = impact_social
        st.session_state.impact_econ = impact_econ
        st.session_state.plan_action = plan_action
        st.session_state.type = project_types
        st.session_state.uploaded_doc = uploaded_doc


# --- 4️⃣ Enregistrement ---
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

                description_finale = f"""
**Solution :** {st.session_state.solution}

**Impact écologique :** {st.session_state.impact_eco}

**Impact social :** {st.session_state.impact_social}

**Impact économique :** {st.session_state.impact_econ}

**Plan d’action :** {st.session_state.plan_action}
"""

                payload = {
                    "Title": title,
                    "Description": description_finale,
                    "Localisation": localisation,
                    "Type": st.session_state.type,
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


