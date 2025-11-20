# ==============================
# 🎨 SECTION PROJET CORRESPONDANT (STYLE IDENTIQUE)
# ==============================
if "builder_data" in st.session_state:

    project = st.session_state.get("matched_project", None)
    project_found = st.session_state.get("project_found", False)

    # ---- Cadre externe vert foncé ----
    st.markdown("""
        <div style="
            background-color: #018262; 
            border-radius: 20px;
            padding: 25px;
            margin-top: 30px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
        ">
            <div style="
                background-color: #cfeee7; 
                border-radius: 15px; 
                padding: 25px;
                color: #014d3b;
            ">
    """, unsafe_allow_html=True)

    # ---- Titre ----
    st.markdown(
        f"<h2 style='margin-top: 0;'>{labels['match_title']}</h2>",
        unsafe_allow_html=True
    )

    # ---- SI PROJET TROUVÉ ----
    if project_found and project is not None:

        proj_title = project.get("Title", "—")
        proj_loc   = project.get("Localisation", "—")
        proj_plan  = (project.get("plan_action") or 
                      project.get("Plan d’action") or "—")

        # Nom du projet
        st.markdown(
            f"<p><b>{labels['project_name']} :</b> {proj_title}</p>",
            unsafe_allow_html=True
        )

        # Localisation
        st.markdown(
            f"<p><b>{labels['project_location']} :</b> {proj_loc}</p>",
            unsafe_allow_html=True
        )

        # Plan d’action (avec rendu propre)
        st.markdown(
            f"<p><b>{labels['project_plan']} :</b></p>",
            unsafe_allow_html=True
        )

        # ⚠️ IMPORTANT : pas de st.write() ici, sinon ça casse le bloc HTML
        st.markdown(
            f"<div style='white-space: pre-wrap; font-size: 15px;'>{proj_plan}</div>",
            unsafe_allow_html=True
        )

    # ---- SI Aucun projet trouvé ----
    else:
        st.markdown(
            f"<p style='color:#b30000; font-weight:bold;'>{labels['no_match']}</p>",
            unsafe_allow_html=True
        )

        pilot_url = "https://eco-assistant-evad-qr7cswdr5btwkxtbkmfbdu.streamlit.app/#rejoignez-evad-pour-co-developper-votre-projet-de-lieux-regeneratif"
        st.markdown(f"<a href='{pilot_url}'>{labels['open_pilot']}</a>", unsafe_allow_html=True)

    # ---- Fermeture des div ----
    st.markdown("</div></div>", unsafe_allow_html=True)



