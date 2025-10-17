import streamlit as st
import json
from eco_agent import ask_model, save_to_nocodb

# Configuration de la page
st.set_page_config(page_title="Assistant Éco-Intelligent", page_icon="🌿", layout="centered")

st.title("🌿 Assistant Éco-Intelligent")
st.markdown("""
Décris ton projet écologique ci-dessous.  
L’assistant va :
1️⃣ Analyser ton idée  
2️⃣ Proposer les champs (Titre, Description, Type, Revenus)  
3️⃣ Et t’aider à l’enregistrer dans **NoCoDB**
""")

description = st.text_area("📝 Décris ton projet :", height=150, placeholder="Ex: Ferme solaire communautaire pour un village...")

if st.button("Analyser le projet 🌍"):
    if not description.strip():
        st.warning("⚠️ Merci d’ajouter une description avant de lancer l’analyse.")
    else:
        with st.spinner("Analyse en cours..."):
            result = ask_model(description)

        if "error" in result:
            st.error(f"❌ Une erreur est survenue : {result['error']}")
        else:
            st.success("💡 Proposition générée avec succès !")

            # --- Affichage stylisé ---
            st.markdown("### 🪴 Résultat de l’analyse")
            st.markdown(f"#### 🏷️ **{result['Titre']}**")
            st.markdown(result["Description"])
            st.markdown(f"**🧭 Type de projet :** {result['Type']}")
            st.markdown(f"**💰 Revenus estimés :** {result['Revenus']}")

            st.divider()

            if st.button("Enregistrer dans NoCoDB ✅"):
                try:
                    save_to_nocodb(result)
                    st.success("🎉 Projet enregistré dans NoCoDB avec succès !")
                except Exception as e:
                    st.error(f"⚠️ Erreur lors de l’enregistrement : {e}")
