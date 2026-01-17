import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

# ---------------- CONSTANTS ----------------
PLACEHOLDER_POSTER = "https://via.placeholder.com/500x750?text=No+Poster"
API_KEY = st.secrets.get("TMDB_API_KEY", "")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    movies = pickle.load(open("movies.pkl", "rb"))
    movies = pd.DataFrame(movies)

    similarity = cosine_similarity(movies['tags'].apply(lambda x: list(map(float, x.split(','))).tolist()))
    return movies, similarity

movies, similarity = load_data()

# ---------------- FETCH POSTER ----------------
def fetch_poster(movie_id):
    if API_KEY == "":
        return PLACEHOLDER_POSTER

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        response = requests.get(url, params={"api_key": API_KEY})
        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return PLACEHOLDER_POSTER
    except:
        return PLACEHOLDER_POSTER

# ---------------- RECOMMENDER ----------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    names = []
    posters = []

    for i in distances:
        movie_id = movies.iloc[i[0]].id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters

# ---------------- UI ----------------
selected_movie = st.selectbox("Select a movie", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
