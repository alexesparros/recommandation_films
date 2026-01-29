import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from yt_dlp import YoutubeDL

def is_valid_image(url):
    try:
        response = requests.head(url, timeout=2)
        return response.status_code == 200 and 'image' in response.headers.get('Content-Type', '')
    except:
        return False
    

def session_states():
    st.session_state.setdefault("query", "")
    st.session_state.setdefault("last_query", "")
    st.session_state.setdefault("page_num", 0)
    st.session_state.setdefault("film_selectionne", None)
    st.session_state.setdefault("page", "Accueil")
    st.session_state.setdefault("reset", False)


@st.cache_data(show_spinner=False)
def scrap_video(movie_title):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "proxy": ""
    }
    query = f"ytsearch1:{movie_title} bande annonce"
    with YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(query, download=False)
            entry = result["entries"][0]
            url = entry.get("url") if isinstance(entry, dict) else None
            if url and isinstance(url, str) and not url.startswith("http"):
                return f"https://www.youtube.com/watch?v={url}"
            return url
        except:
            return None