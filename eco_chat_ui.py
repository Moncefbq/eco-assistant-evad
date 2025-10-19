import streamlit as st
from eco_agent import ask_model, save_to_nocodb

# --- Configuration de la page ---
st.set_page_config(page_title="Assistant Éco-Intelligent", page_icon="🌿", layout="centered")

st.title("🌿 Assistant Éco-Intelligent")
st.markdown("""
Décris ton projet écologique ci-dessous :  
1️⃣ Analyse ton idée  
2️⃣ Propose les champs (**Titre**, **Description**, **Type**, **Revenus**)  
3️⃣ Te permet de les **modifier avant l’enregistrement dans NoCoDB**
""")

# --- État global ---
if "data" not in st.session_state:
    st.session_state.data = None
if "edited" not in st.session_state:
    st.session_state.edited = {}

# --- Entrée utilisateur ---
description = st.text_area(
    "📝 Décris ton projet :",
    placeholder="Ex : Installer des panneaux solaires pour produire de l’énergie propre."
)

# --- Bouton d’analyse ---
if st.button("🔍 Analyser le projet"):
    if not description.strip():
        st.warning("⚠️ Merci d’ajouter une description avant de lancer l’analyse.")
    else:
        with st.spinner("Analyse du projet en cours..."):
            st.session_state.data = ask_model(description)
        if "error" in st.session_state.data:
            st.error(f"❌ Erreur : {st.session_state.data['error']}")
        else:
            st.success("💡 Proposition générée avec succès !")
            st.session_state.edited = st.session_state.data.copy()

# --- Interface d’édition ---
if st.session_state.data:
    st.markdown("### ✏️ Modifie les champs si nécessaire avant enregistrement :")

    st.session_state.edited["Titre"] = st.text_input("📘 Titre :", value=st.session_state.edited.get("Titre", ""))
    st.session_state.edited["Description"] = st.text_area(
        "📄 Description :", value=st.session_state.edited.get("Description", ""), height=150
    )
    st.session_state.edited["Type"] = st.text_input("🏷️ Type de projet :", value=st.session_state.edited.get("Type", ""))
    st.session_state.edited["Revenus"] = st.text_area(
        "💰 Estimation des revenus :", value=st.session_state.edited.get("Revenus", ""), height=100
    )

    # --- Upload d'image ---
    uploaded_file = st.file_uploader("📸 Ajoute une image liée au projet (optionnel)", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        uploaded_file.seek(0)
        st.image(uploaded_file, caption="Aperçu de l’image", use_container_width=True)
        st.session_state.edited["Picture"] = uploaded_file
    else:
        st.session_state.edited["Picture"] = None

    # --- Enregistrement ---
    if st.button("💾 Enregistrer dans NoCoDB"):
        with st.spinner("Enregistrement en cours..."):
            result = save_to_nocodb(st.session_state.edited)
        if result.get("status") == "success":
            st.success("✅ Projet enregistré avec succès dans NoCoDB !")
        else:
            st.error(f"❌ Erreur : {result.get('message')}")
