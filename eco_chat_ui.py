import streamlit as st
import json
from eco_agent import ask_model, save_to_nocodb

# --- Configuration de la page ---
st.set_page_config(page_title="Assistant Éco-Intelligent", page_icon="🌿", layout="centered")

st.title("🌿 Assistant Éco-Intelligent")
st.markdown("""
Décris ton projet écologique ci-dessous :  
L’assistant va :  
1️⃣ Analyser ton idée  
2️⃣ Proposer les champs (**Titre**, **Description**, **Type**, **Revenus**)  
3️⃣ Te permettre de les **modifier avant l’enregistrement dans NoCoDB**
""")

# --- Entrée utilisateur ---
description = st.text_area(
    "📝 Décris ton projet :",
    placeholder="Ex : Mettre en place des jardins potagers communautaires dans les écoles..."
)

# --- Analyse du projet ---
if st.button("🔍 Analyser le projet"):
    if not description.strip():
        st.warning("⚠️ Merci d’ajouter une description avant de lancer l’analyse.")
    else:
        with st.spinner("🧠 Analyse du projet en cours..."):
            data = ask_model(description)

        if "error" in data:
            st.error(f"❌ Erreur : {data['error']}")
        else:
            st.success("💡 Proposition générée avec succès !")

            # --- Champs modifiables ---
            st.markdown("### ✏️ Modifie les champs si nécessaire avant enregistrement :")

            titre_edit = st.text_input("📘 Titre :", value=data.get("Titre", "").strip(": ").strip())
            desc_edit = st.text_area("📄 Description :", value=data.get("Description", "").strip(": ").strip(), height=150)
            type_edit = st.text_input("🏷️ Type de projet :", value=data.get("Type", "").strip(": ").strip())
            rev_edit = st.text_area("💰 Estimation des revenus :", value=data.get("Revenus", "").strip(": ").strip(), height=100)

            # --- Résumé final ---
            st.markdown("### 📊 Résumé final :")
            cleaned_data = {
                "Titre": titre_edit.strip(": ").strip(),
                "Description": desc_edit.strip(": ").strip(),
                "Type": type_edit.strip(": ").strip(),
                "Revenus": rev_edit.strip(": ").strip(),
            }
            st.json(cleaned_data)

            # --- Enregistrement ---
            if st.button("💾 Enregistrer dans NoCoDB"):
                result = save_to_nocodb(cleaned_data)
                if result.get("status") == "success":
                    st.success("✅ Projet enregistré dans NoCoDB avec succès !")
                else:
                    st.error(f"❌ Erreur : {result.get('message')}")
