# Système de recommandation de films

Site Streamlit de recommandation de films basé sur des similarités (KNN) et des critères textuels. Le projet exploite des données issues d’IMDb et TMDB pour proposer des recommandations pertinentes.

## Fonctionnalités
- Recherche par titre ou nom d’acteur
- Fiche film détaillée (année, genres, acteurs, résumé)
- Recommandations associées
- Lecture de bande‑annonce via YouTube (yt‑dlp)

## Prérequis
- Python 3.10+ recommandé
- Accès Internet (images, bande‑annonces)

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Lancer l’application
```bash
streamlit run app.py
```
L’application est accessible sur `http://localhost:8501`.

## Structure du projet
```
reco_films_wcs/
├─ app.py                    # Entrée Streamlit
├─ utils.py                  # Fonctions utilitaires (images, vidéos)
├─ requirements.txt          # Dépendances Python
├─ page/                     # Pages Streamlit
│  ├─ page_accueil.py
│  ├─ page_recherche.py
│  ├─ page_espace_decouverte.py
│  └─ page_reco.py
├─ csv/                      # Données (films + recommandations)
└─ Jupyter/                  # Notebooks d’analyse
```

## Données
- Jeux de données IMDb et TMDB
- Données structurées (films, genres, réalisateurs, acteurs, années)

## Méthodologie
- Nettoyage et préparation des données
- Feature engineering (genres, réalisateurs, acteurs, titres)
- Utilisation d’un algorithme de type KNN
- Évaluation qualitative des recommandations
