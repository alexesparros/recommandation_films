import streamlit as st
import pandas as pd
import plotly.express as px
from utils import is_valid_image
from yt_dlp import YoutubeDL

def session_states():
    st.session_state.setdefault("query", "")
    st.session_state.setdefault("last_query", "")
    st.session_state.setdefault("page_num", 0)
    st.session_state.setdefault("film_selectionne", None)
    st.session_state.setdefault("page", "Accueil")
    st.session_state.setdefault("reset", False)
   

def scrap_video(movie_title):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True
    }
    query = f"ytsearch1:{movie_title} bande annonce"
    with YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(query, download=False)
            return result["entries"][0]["url"]
        except:
            return None

def recherche():
    df = st.session_state["df_final_translated"]

    # Suggestions films + personnes
    titres = df['originalTitle'].dropna().unique().tolist()
    noms = df['noms'].dropna().tolist()
    personnes = set()
    for liste in noms:
        try:
            personnes.update(eval(liste))
        except:
            pass
    suggestions = sorted(set(titres) | personnes)
    # Barre de recherche
    query = st.selectbox(
        "🔎 Tape un film ou un nom",
        options=[""] + suggestions,
        index=0,
        placeholder="🔎 Tape un nom de film ou d'acteur pour commencer ta recherche."
    )

    # Boutons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Rechercher"):
            st.session_state.query = query
            st.session_state.page_num = 0
            st.rerun()
    with col2:
        if st.button("Réinitialiser"):
            st.session_state.query = ""
            st.session_state.page_num = 0
            st.rerun()

    if not st.session_state.query:
        return

    q = st.session_state.query.lower()
    filtres = df[
        df['originalTitle'].str.lower().str.contains(q, na=False) |
        df['noms'].str.lower().str.contains(q, na=False) |
        df['primaryTitle'].str.lower().str.contains(q, na=False) 
    ]

    page = st.session_state.page_num
    start, end = page * 9, (page + 1) * 9
    for i in range(start, min(end, len(filtres)), 3):
        cols = st.columns(3)
        for j, (_, row) in enumerate(filtres.iloc[i:i+3].iterrows()):
            with cols[j]:
                image_url = row["url_complet"]
                if image_url:
                    st.image(image_url, width=150)
                else:
                    st.image("image/Pas_d_image.png", width=150)

                st.markdown(f"**{row['originalTitle']}** ({row['startYear']})")
                #st.write(', '.join(eval(row.get("genres", "[]"))))
                if st.button("Accéder", key=f"btn_{i}_{j}"):
                    st.session_state["film_selectionne"] = row.name
                    st.session_state["page"] = "Reco"
                    st.rerun()

    total_pages = (len(filtres) - 1) // 9 + 1
    st.markdown(f"Page {page+1} / {total_pages}")

    col1, col2 = st.columns(2)
    with col1:
        if page > 0 and st.button("⬅️ Précédente"):
            st.session_state.page_num -= 1
            st.rerun()
    with col2:
        if end < len(filtres) and st.button("➡️ Suivante"):
            st.session_state.page_num += 1
            st.rerun()