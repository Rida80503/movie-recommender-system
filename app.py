import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=51656fd41c4e49796aeb1958d8915320&language=en-US"
    response = requests.get(url)
    data = response.json()
    
    # Safely check if 'poster_path' exists
    if 'poster_path' in data and data['poster_path'] is not None:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        # Fallback image if no poster is found
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = i[0]
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommended_movies, recommended_movies_posters

st.title("Movie Recommender System")

movie_dict = pickle.load(open('movies.pkl', 'rb'))
movies= pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

slected_movie_name = st.selectbox(
    'How Would you like to be contacted?', movies['title'].values)
if st.button('Recommend'):
    names, posters = recommend(slected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    
    with col4:
        st.text(names[3])
        st.image(posters[3])
        
    with col5:
        st.text(names[4])
        st.image(posters[4])

