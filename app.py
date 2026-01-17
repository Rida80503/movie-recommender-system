import streamlit as st
import pandas as pd
import pickle
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

# ------------------ CONSTANTS ------------------
API_KEY = st.secrets.get("TMDB_API_KEY", "")
PLACEHOLDER_POSTER = "https://via.placeholder.com/500x750?text=No+Poster"

# ------------------ LOAD MOVIES ------------------
@st.cache_data
def load_movies():
    with open("movies.pkl", "rb") as f:
        movies_dict = pickle.load(f)
    return pd.DataFrame(movies_dict)

movies = load_movies()

# ------------------ COMPUTE SIMILARITY (SMALL + FAST) ------------------
@st.cache_resource
def compute_similarity():
    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(movies["tags"]).toarray()
    return cosine_similarity(vectors)

similarity = compute_similarity()

# ------------------ POSTER FETCH ------------------
def fetch_poster(movie_id):
    if API_KEY == "":
        return PLACEHOLDER_POSTER

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {"api_key": API_KEY}
        data = requests.get(url, params=params).json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
        return PLACEHOLDER_POSTER

    except:
        return PLACEHOLDER_POSTER

# ------------------ RECOMMENDER ------------------
def recommend(movie):
    idx = movies[movies["title"] == movie].index[0]
    distances = similarity[idx]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names, posters = [], []
    for i in movie_list:
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movies.iloc[i[0]].movie_id))

    return names, posters

# ------------------ UI ------------------
selected_movie = st.selectbox("Select a movie", movies["title"].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
