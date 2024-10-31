import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

# Sidebar for Navigation with Custom Styling
st.sidebar.title("🎬 Movie Recommender")
menu = st.sidebar.radio("Navigate", ["Home", "About"])

# Function to fetch poster and description from the TMDB API
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', "")
    full_poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""
    description = data.get('overview', "Description not available.")
    return full_poster_url, description

# Load movie data and similarity model
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# Home Section
if menu == "Home":
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎥 Movie Recommender System</h1>", unsafe_allow_html=True)
    st.subheader("Find Your Next Favorite Movie")

    # Displaying Featured Movies in Carousel
   
    st.markdown("<h3 style='color: #FF4B4B;'>Choose a Movie</h3>", unsafe_allow_html=True)
    selectvalue = st.selectbox("Select a movie to get recommendations", movies_list)

    def recommend(movie):
        index = movies[movies['title'] == movie].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        recommend_movie = []
        recommend_movie_ids = []
        recommend_poster = []
        for i in distance[1:6]:
            movie_id = movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            recommend_movie_ids.append(movie_id)
            recommend_poster.append(fetch_movie_details(movie_id)[0])
        return recommend_movie, recommend_movie_ids, recommend_poster

    if st.button("💡 Show Recommendations"):
        st.write(f"Top Recommendations for: **{selectvalue}**")
        
        movie_names, movie_ids, movie_posters = recommend(selectvalue)
        for idx, movie_name in enumerate(movie_names):
            col = st.columns([1, 4, 1])[1]  # Center-align the cards
            with col:
                st.image(movie_posters[idx], use_column_width=True)
                st.markdown(f"**{movie_name}**")
                if st.button(f"Show Description for {movie_name}", key=f"description-{idx}"):
                    _, description = fetch_movie_details(movie_ids[idx])
                    st.info(description)

# About Section
elif menu == "About":
    st.title("About the Movie Recommender System")
    st.write(
        """
        This Movie Recommender System helps you discover movies based on similarity to your chosen title. 
        Built using machine learning and powered by The Movie Database (TMDb) API for fetching movie details and posters.
        
        **Features:**
        - A wide selection of popular movies
        - Smart recommendations based on your selection
        - Visual recommendations for an easy browsing experience
        
        **Technologies Used:** Streamlit, Python, TMDb API
        """
    )

# Footer
st.write("---")
st.write("© 2024 Movie Recommender System | Built with ❤️ by [Your Name]")
