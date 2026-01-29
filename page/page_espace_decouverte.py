import streamlit as st
import pandas as pd
from utils import is_valid_image

def espace_decouverte():

    # 📁 Chargement du DataFrame
    df = st.session_state["df_final_translated"]

    # 🧼 Nettoyage des genres
    df["genres_list"] = df["genres_list"].fillna("")
    df["genres_list"] = df["genres_list"].str.replace("{", "", regex=False)\
                                .str.replace("}", "", regex=False)\
                                .str.replace("'", "", regex=False)\
                                .str.split(",")

    # # 🧼 Nettoyage des pays
    # df["production_countries"] = df["production_countries"].fillna("")
    # df["production_countries"] = df["production_countries"].str.replace("{", "", regex=False)\
    #                                                        .str.replace("}", "", regex=False)\
    #                                                        .str.replace("'", "", regex=False)\
    #                                                        .str.split(",")
    # df_exploded_countries = df.explode("production_countries")
    # df_exploded_countries["country_clean"] = df_exploded_countries["production_countries"].str.strip()
    # all_countries = sorted(df_exploded_countries["country_clean"].dropna().unique())

    # 📅 Filtre par année
    min_year, max_year = int(df["startYear"].min()), int(df["startYear"].max())
    selected_year_range = st.slider("📅 Intervalle d'années", min_year, max_year, (min_year, max_year))

    # # 🌍 Filtre par pays
    # selected_countries = st.multiselect("🌍 Pays de production", options=all_countries)

    # # Application des filtres année
    df = df[(df["startYear"] >= selected_year_range[0]) & (df["startYear"] <= selected_year_range[1])]

    # if selected_countries:
    #     df = df[df["production_countries"].apply(lambda countries: any(p.strip() in countries for p in selected_countries))]

    # 🔍 Extraire tous les genres uniques
    df_exploded = df.explode("genres_list")
    df_exploded["genre_unique"] = df_exploded["genres_list"].str.strip()
    all_genres = sorted(df_exploded["genre_unique"].dropna().unique())

    # 🎯 Genres principaux à afficher en priorité
    main_genres = [
        "Comedy", "Drama", "Action", "Adventure", "Animation",
        "Thriller", "Sci-Fi", "Fantasy", "Romance", "Horror"
    ]
    other_genres = sorted(set(all_genres) - set(main_genres))

    # ✅ Sélection des genres principaux (2 lignes × 5 genres)
    st.header("🎬 Genres principaux")
    selected_genres = []

    rows = [main_genres[:5], main_genres[5:]]  # 2 lignes de 5 genres

    for row in rows:
        cols = st.columns(5)
        for col, genre in zip(cols, row):
            if col.checkbox(genre, key=f"main_{genre}"):
                selected_genres.append(genre)

    # ✅ Genres secondaires dans un expander
    with st.expander("📚 Afficher plus de genres"):
        cols = st.columns(3)
        for i, genre in enumerate(other_genres):
            if cols[i % 3].checkbox(genre, key=f"other_{genre}"):
                selected_genres.append(genre)

    # 🔍 Filtrage des films selon les genres sélectionnés
    if selected_genres:
        df_filtered = df[df["genres_list"].apply(lambda genres: all(g in genres for g in selected_genres))]

        # 🔢 Tri par note moyenne sans reset_index (on garde les vrais ID de film)
        filtres = df_filtered.sort_values(by="averageRating", ascending=False)

        if not filtres.empty:
            st.subheader(f"{len(filtres)} film(s) trouvé(s)")

            # 📄 Initialisation de la pagination dédiée à cette page
            if "page_num_decouverte" not in st.session_state:
                st.session_state.page_num_decouverte = 0

            page = st.session_state.page_num_decouverte
            films_par_page = 6
            start, end = page * films_par_page, (page + 1) * films_par_page

            page_films = filtres.iloc[start:end]

            # 🎞️ Affichage en 2 lignes de 3 colonnes
            for i in range(0, len(page_films), 3):
                cols = st.columns(3)
                for j, (idx, row) in enumerate(page_films.iloc[i:i+3].iterrows()):
                    with cols[j]:
                        image_url = row['url_complet']
                        if is_valid_image(image_url):
                            st.image(image_url, width=150)
                        else:
                            st.image("image/Pas_d_image.png", width=150)

                        st.markdown(f"**{row['originalTitle']}** ({row['startYear']})")

                        if st.button("Accéder", key=f"btn_decouverte_{idx}"):
                            st.session_state["film_selectionne"] = idx
                            st.session_state["page"] = "Reco"
                            st.rerun()

            # 🔁 Pagination
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("⬅️ Précédent") and page > 0:
                    st.session_state.page_num_decouverte -= 1
                    st.rerun()
            with col3:
                if st.button("Suivant ➡️") and end < len(filtres):
                    st.session_state.page_num_decouverte += 1
                    st.rerun()
        else:
            st.warning("Aucun film ne correspond exactement aux genres sélectionnés.")
    else:
        st.info("Coche un ou plusieurs genres pour afficher les films.")