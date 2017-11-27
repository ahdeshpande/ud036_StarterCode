# Import Statements
import json
import media
import fresh_tomatoes
import requests
from random import shuffle

# API Key for The Movie DB (https://www.themoviedb.org/)
MOVIE_DB_API_KEY = 'you_need_a_TMDb_API_key'


def get_movie_data(movie_title):
    """
        Fetch data from The Movie DB (https://www.themoviedb.org/)
        using the movie name

    Args:
        movie_title: Name of the movie

    Returns:
        JSON data of the details of the movie
    """

    # Call the API to get the details and convert the response string to JSON
    r = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' +
                     MOVIE_DB_API_KEY +
                     '&query=' + movie_title)
    json_data = r.json()

    # If response is not None, get video url using the movie id,
    # else empty
    if json is not None:
        m_data = json_data['results'][0]
        m_data['youtube_url'] = 'http://www.youtube.com/watch?v=' + \
                                get_video(str(m_data['id']))
    else:
        m_data = {}

    # Return the fetched data
    return m_data


def get_video(movie_id):
    """
        Fetch YouTube key of the specified movie id using the The Movie DB
        (https://www.themoviedb.org/) API

    Args:
        movie_id: ID of the movie

    Returns:
        YouTube key of the movie
    """

    # Call the API to get the details and convert the response string to JSON
    r = requests.get('https://api.themoviedb.org/3/movie/' +
                     movie_id +
                     '?api_key=' +
                     MOVIE_DB_API_KEY +
                     '&append_to_response=videos')

    json_data = r.json()

    # If response is not None, get YouTube key from the results
    # else empty
    if json is not None:
        youtube_key = json_data['videos']['results'][0]['key']
    else:
        youtube_key = ''

    return youtube_key


try:
    # List of movie names
    movie_list = json.load(open('movies.json'))['movies']

    # List of the objects of class Movie
    all_movies = []

    # check if movie list is none
    if movie_list is None:
        print("Error in movies.json file!")
    else:
        # Iterate through the list and create objects using the data retrieved
        for movie in movie_list:
            movie_data = get_movie_data(movie)

            movie_object = media.Movie(movie_data['title'],
                                       movie_data['overview'],
                                       'https://image.tmdb.org/t/p/w500' +
                                       movie_data[
                                           'poster_path'],
                                       movie_data['youtube_url'],
                                       str(movie_data['release_date'])[:4],
                                       str(movie_data['vote_average']) + '/10')
            all_movies.append(movie_object)

        # Shuffle the objects in the list
        shuffle(all_movies)

        # Create the webpage
        fresh_tomatoes.open_movies_page(all_movies)
except KeyError:
    print("Error in movies.json file!")
