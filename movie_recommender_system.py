import pickle
import streamlit as st
import requests
import pandas as pd

# The following pushing helps to fetch the poster from the TMDB database
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b2852079fe8ea2bcb2825fb3f22420a4&language=en-US"
    data = requests.get(url)
    data = data.json()

    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# The function that recommend the 5 common movies using cosine_similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for movie_idx, score in distances[1:6]:
        movie_id = movies.iloc[movie_idx].movie_id
        recommended_movie_names.append(movies.iloc[movie_idx].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


st.header('🎬 Movie Recommender System')
# Loading the dictionary which I converted to dataframe and loaded our cosine_similarity
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
# After the button press, 5 movies appear with their poster path
if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])




