import streamlit as st 
import pickle
import streamlit.components.v1 as components

import requests

st.header('Flim Flix - a simple movie recommender')

movies = pickle.load(open('movies_list-Copy1.pk1', 'rb'))
similarity = pickle.load(open('sm-Copy1.pk1', 'rb'))
movies_list = movies['title'].values


select_value = st.selectbox("Select the movie title and click 'Show Movies' ", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse = True , key=lambda vector:vector[1])
    recommendation = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommendation.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))

    return recommendation, recommend_poster

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=65f5b3ef7590dd502b5f797e7bcfb26d&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path', None)
    if poster_path:
        fullpath = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        fullpath = "https://via.placeholder.com/500x750?text=No+Poster+Available"
    return fullpath

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")


imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
   
    ]


imageCarouselComponent(imageUrls=imageUrls, height=200)




if st.button("Show Movies"):
    movie_name, movie_poster = recommend(select_value)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])


