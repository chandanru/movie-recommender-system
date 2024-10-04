import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = 'b2b382d6'

def fetch_movie_details(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
    data = requests.get(url).json()
    poster_url = data.get('Poster', "https://via.placeholder.com/500x750?text=No+Image+Available")
    overview = data.get('Plot', "No overview available.")
    cast = data.get('Actors', "No cast information available.")
    year = data.get('Year', "Unknown year")
    rating = data.get('imdbRating', "No rating available")
    genre = data.get('Genre', "No genre information available.")
    director = data.get('Director', "No director information available.")
    language = data.get('Language', "No language information available.")
    return poster_url, overview, genre, cast, director, language, year, rating

def recommend(movie, similarity, movies):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        poster_url, overview, genre, cast, director, language, year, rating = fetch_movie_details(movie_title)
        recommend_movies.append({
            "title": movie_title,
            "poster": poster_url,
            "overview": overview,
            "genre": genre,
            "cast": cast,
            "director": director,
            "language": language,
            "year": year,
            "rating": rating
        })
    return recommend_movies

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    recommended_movies = recommend(selected_movie_name, similarity, movies)
    st.write('Recommended Movies:')

    for movie in recommended_movies:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(movie['poster'], caption=movie['title'])
        with col2:
            st.write(f"**Overview:** {movie['overview']}")
            st.write(f"**Genre:** {movie['genre']}")
            st.write(f"**Cast:** {movie['cast']}")
            st.write(f"**Director:** {movie['director']}")
            st.write(f"**Language:** {movie['language']}")
            st.write(f"**Year:** {movie['year']}")
            st.write(f"**Rating:** {movie['rating']}")
