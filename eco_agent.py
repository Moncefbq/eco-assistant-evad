import streamlit as st
from eco_agent import ask_model, save_to_nocodb

st.set_page_config(page_title="Assistant Éco-Intelligent", page_icon="🌱", layout="centered")

# --- Interface principale ---
st.title("🌿 Assistant Éco-Intelligent")

st.markdown("""
Décris ton projet écologique ci-dessous :  

1️⃣ **Analyse ton idée**  
2️⃣ **Reçois une proposition automatique (Titre, Description, Type, Revenus)**  
3️⃣ **Modifie si besoin**  
4️⃣ **Enregistre dans NoCoDB ✅**
""")

# --- Zone de saisie ---
description = st.text_area(
    "📝 Décris ton projet :",
    placeholder="Ex : Installer des panneaux solaires dans les écoles rurales",
    height=120
)

# --- Bouton d’analyse ---
if st.button("🔍 Analyser le projet"):
    if not description.strip():
        st.warning("⚠️ Merci de décrire ton projet avant d'analyser.")
    else:
        with st.spinner("Analyse du projet en cours... ⏳"):
            data = ask_model(description)

        if "error" in data:
            st.error(f"❌ Erreur : {data['error']}")
        else:
            st.success("💡 Proposition générée avec succès !")

            # --- Champs modifiables par l’utilisateur ---
            st.markdown("### ✏️ Tu peux modifier les champs avant d’enregistrer :")

            titre = st.text_input("📘 Titre :", value=data.get("Titre", ""))
            desc = st.text_area("📄 Description :", value=data.get("Description", ""), height=150)
            type_proj = st.text_input("🏷️ Type de projet :", value=data.get("Type", ""))
            revenus = st.text_area("💰 Estimation des revenus :", value=data.get("Revenus", ""), height=100)

            # --- Affichage du JSON propre ---
            st.markdown("### 🧾 Aperçu des données à enregistrer :")
            st.json({
                "Titre": titre,
                "Description": desc,
                "Type": type_proj,
                "Revenus": revenus
            })

            # --- Enregistrement dans NoCoDB ---
            if st.button("💾 Enregistrer dans NoCoDB"):
                new_data = {
                    "Titre": titre,
                    "Description": desc,
                    "Type": type_proj,
                    "Revenus": revenus
                }

                with st.spinner("Enregistrement en cours..."):
                    result = save_to_nocodb(new_data)

                if result.get("status") == "success":
                    st.success("✅ Projet enregistré dans NoCoDB avec succès !")
                else:
                    st.error(f"❌ Erreur lors de l'enregistrement : {result.get('message')}")



