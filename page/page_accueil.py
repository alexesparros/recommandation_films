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
        
def accueil():

    st.image("image/Vlad_3.png", width=200)

    # Sous-titre bleu, un peu plus petit (niveau H2)
    st.markdown("<h2 style='font-size:50px; color:#1f6feb; border-radius:10px;'>Notre ADN</h2>", unsafe_allow_html=True)  # H2 = deuxième niveau

    st.markdown(
        """
        Bienvenue sur notre site, vous êtes sur la bonne destination qui vous permettra de découvrir et explorer tout le meilleur du cinéma.

        Notre ADN repose sur la passion du 7ème art, le partage d'idées et l'inspiration.

        
        Des recommandations qui vous correspondent grâce à une analyse ciblée du marché du cinéma français.
        Des données mises à jour en temps réel en fonction des dernières sorties et avis du public.
        Des sélections de films exclusivement orientées selon les attentes des spectateurs français.""")

    df1 = pd.DataFrame({
        'Année': list(range(2015, 2025)),
        'Films français': [90, 95, 97, 92, 89, 25, 35, 50, 65, 55],
        'Films américains': [110, 115, 100, 90, 115, 20, 30, 40, 50, 45],
        'Films européens': [20, 22, 25, 28, 20, 8, 12, 18, 20, 25]
    })

    df2 = pd.DataFrame({
        'Année': list(range(2007, 2025)),
        'Entrées (millions)': [178, 190, 201, 207, 217, 203, 193, 209, 205, 213,
                              209, 201, 213, 65, 95, 152, 180, 181]
    })

    df1_melted = df1.melt(id_vars='Année', var_name='Nationalité', value_name='Entrées')
    fig1 = px.line(df1_melted, x='Année', y='Entrées', color='Nationalité',
                   markers=True, title="Entrées en salle par nationalité (2015–2024)", height=400)

    fig2 = px.bar(df2, x='Année', y='Entrées (millions)', text='Entrées (millions)',
                  title="Entrées totales en millions (2007–2024)", height=400)
    fig2.update_traces(textposition='outside')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)