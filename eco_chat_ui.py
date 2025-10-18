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

# --- Initialisation de l'état ---
if "data" not in st.session_state:
    st.session_state.data = None

# --- Saisie utilisateur ---
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
            result = ask_model(description)
        if "error" in result:
            st.error(f"❌ Erreur : {result['error']}")
        else:
            st.success("💡 Proposition générée avec succès !")
            st.session_state.data = result  # 🔥 Stocke les données pour les garder persistantes

# --- Si une analyse a été faite ---
if st.session_state.data:
    data = st.session_state.data

    st.markdown("### ✏️ Modifie les champs si nécessaire avant enregistrement :")

    # Champs modifiables
    titre_edit = st.text_input("📘 Titre :", value=data.get("Titre", ""), key="titre_edit")
    desc_edit = st.text_area("📄 Description :", value=data.get("Description", ""), height=150, key="desc_edit")
    type_edit = st.text_input("🏷️ Type de projet :", value=data.get("Type", ""), key="type_edit")
    rev_edit = st.text_area("💰 Estimation des revenus :", value=data.get("Revenus", ""), height=100, key="rev_edit")

    # Données finales mises à jour
    final_data = {
        "Titre": titre_edit.strip(),
        "Description": desc_edit.strip(),
        "Type": type_edit.strip(),
        "Revenus": rev_edit.strip()
    }

    st.markdown("### 📊 Résumé final :")
    st.json(final_data)  # 🔥 Affiche UNIQUEMENT les champs modifiés

    # --- Enregistrement dans NoCoDB ---
    if st.button("💾 Enregistrer dans NoCoDB"):
        with st.spinner("Enregistrement en cours..."):
            result = save_to_nocodb(final_data)
        if result.get("status") == "success":
            st.success("✅ Projet enregistré dans NoCoDB avec succès !")
        else:
            st.error(f"❌ Erreur : {result.get('message')}")
