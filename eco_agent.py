import streamlit as st
from eco_agent import ask_model, save_to_nocodb

st.set_page_config(page_title="Assistant Éco-Intelligent", page_icon="🌱", layout="centered")

st.title("🌱 Assistant Éco-Intelligent")
st.markdown("""
Décris ton projet écologique ci-dessous :
1️⃣ Analyse ton idée  
2️⃣ Propose les champs (**Titre**, **Description**, **Type**, **Revenus**)  
3️⃣ Tu peux les modifier avant l’enregistrement dans **NoCoDB**
""")

# --- Entrée utilisateur ---
description = st.text_area(
    "📄 Décris ton projet :",
    placeholder="Ex : Installer des systèmes de récupération d’eau de pluie dans les écoles rurales"
)

# --- Bouton d’analyse ---
if st.button("🔍 Analyser le projet"):
    if not description.strip():
        st.warning("Veuillez décrire votre projet avant de lancer l’analyse.")
    else:
        with st.spinner("Analyse du projet en cours... ⏳"):
            data = ask_model(description)

        if "error" in data:
            st.error(f"❌ Erreur : {data['error']}")
        else:
            st.success("💡 Proposition générée avec succès !")

            # --- Champs modifiables ---
            st.markdown("### 🧩 Vérifie ou modifie les champs avant enregistrement :")

            titre_edit = st.text_input("📘 Titre :", value=data.get("Titre", ""))
            desc_edit = st.text_area("📝 Description :", value=data.get("Description", ""), height=150)
            type_edit = st.text_input("🏷️ Type de projet :", value=data.get("Type", ""))
            rev_edit = st.text_area("💰 Estimation des revenus :", value=data.get("Revenus", ""), height=100)

            # --- Afficher un résumé clair ---
            st.markdown("### 📊 Aperçu des données à enregistrer :")
            st.json({
                "Titre": titre_edit,
                "Description": desc_edit,
                "Type": type_edit,
                "Revenus": rev_edit
            })

            # --- Enregistrement dans NoCoDB ---
            if st.button("💾 Enregistrer dans NoCoDB"):
                new_data = {
                    "Titre": titre_edit.strip(),
                    "Description": desc_edit.strip(),
                    "Type": type_edit.strip(),
                    "Revenus": rev_edit.strip()
                }
                result = save_to_nocodb(new_data)

                if result.get("status") == "success":
                    st.success("✅ Projet enregistré dans NoCoDB avec succès !")
                else:
                    st.error(f"❌ Erreur : {result.get('message')}")




