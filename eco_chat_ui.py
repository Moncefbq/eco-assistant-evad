import streamlit as st
from eco_agent import ask_model, save_to_nocodb

# --- Configuration de la page ---
st.set_page_config(page_title="Assistant Éco-Intelligent", page_icon="🌿", layout="centered")

# --- En-tête ---
st.title("🌿 Assistant Éco-Intelligent")
st.markdown("""
Décris ton projet écologique ci-dessous.  
L’assistant va :  
1️⃣ Analyser ton idée  
2️⃣ Proposer les champs (**Titre**, **Description**, **Type**, **Revenus**)  
3️⃣ Et te permettre de **modifier le contenu** avant l’enregistrement dans **NoCoDB** 🌍
""")

# --- Zone de saisie utilisateur ---
description = st.text_area(
    "📝 Décris ton projet :",
    height=150,
    placeholder="Ex : Mettre en place des jardins potagers communautaires dans les écoles rurales..."
)

# --- Bouton principal ---
if st.button("Analyser le projet 🌍"):
    if not description.strip():
        st.warning("⚠️ Merci d’ajouter une description avant de lancer l’analyse.")
    else:
        with st.spinner("🔎 Analyse du projet en cours..."):
            result = ask_model(description)

        if "error" in result:
            st.error(f"❌ Erreur : {result['error']}")
        else:
            st.success("💡 Proposition générée avec succès !")

            # --- Champs modifiables par l'utilisateur ---
            st.markdown("### ✏️ Modifie les champs si nécessaire avant enregistrement :")

            titre_edit = st.text_input("📘 Titre :", value=result.get("Titre", ""))
            desc_edit = st.text_area("📄 Description :", value=result.get("Description", ""), height=150)
            type_edit = st.text_input("🏷️ Type de projet :", value=result.get("Type", ""))
            revenus_edit = st.text_area("💰 Estimation des revenus :", value=result.get("Revenus", ""), height=100)

            # --- Aperçu final ---
            st.markdown("### 📊 Résumé final :")
            st.json({
                "Titre": titre_edit,
                "Description": desc_edit,
                "Type": type_edit,
                "Revenus": revenus_edit
            })

            # --- Enregistrement dans NoCoDB ---
            if st.button("💾 Enregistrer dans NoCoDB"):
                data = {
                    "Titre": titre_edit.strip(),
                    "Description": desc_edit.strip(),
                    "Type": type_edit.strip(),
                    "Revenus": revenus_edit.strip()
                }

                result_noco = save_to_nocodb(data)
                if result_noco.get("status") == "success":
                    st.success("✅ Projet enregistré dans NoCoDB avec succès !")
                else:
                    st.error(f"⚠️ Erreur lors de l’enregistrement : {result_noco.get('message')}")
