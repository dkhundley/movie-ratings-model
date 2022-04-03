# Importing the necessary Python libraries
import os
import sys
import json
import yaml
import cloudpickle
import numpy as np
import pandas as pd
import tmdbv3api
from imdb import IMDb
from omdb import OMDBClient
from rotten_tomatoes_scraper.rt_scraper import MovieScraper
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Importing the inference helper functions
sys.path.insert(0, '../model-training/')
from helpers import *



## API INSTANTIATION
## ----------------------------------------------------------------
# Instantiating FastAPI
api = FastAPI()

# Checking for Heroku environment variable
IS_HEROKU = os.getenv('IS_HEROKU')

# Loading the models from the serialized pickle files
if IS_HEROKU == 'Yes':
    with open(os.path.join(os.getcwd(), './models/binary_classification_pipeline.pkl'), 'rb') as f:
        binary_classification_pipeline = cloudpickle.load(f)
    with open(os.path.join(os.getcwd(), './models/regression_pipeline.pkl'), 'rb') as f:
        regression_pipeline = cloudpickle.load(f)
else:
    with open('../../models/binary_classification_pipeline.pkl', 'rb') as f:
    	binary_classification_pipeline = cloudpickle.load(f)
    with open('../../models/regression_pipeline.pkl', 'rb') as f:
    	regression_pipeline = cloudpickle.load(f)

# Loading the API keys from respective sources
if IS_HEROKU == 'Yes':
    # Getting the keys from the Heroku environment variables
    tmdb_key = os.getenv('TMDB_KEY')
    omdb_key = os.getenv('OMDB_KEY')
else:
    # Loading local YAML file containing keys
    with open('../../keys/keys.yml', 'r') as f:
        keys_yaml = yaml.safe_load(f)

    # Extracting the API keys from the loaded YAML
    tmdb_key = keys_yaml['api_keys']['tmdb_key']
    omdb_key = keys_yaml['api_keys']['omdb_key']

# Defining which features to keep from each respective source
TMDB_FEATS = ['tmdb_id', 'imdb_id', 'budget', 'primary_genre', 'secondary_genre',
			  'tmdb_popularity', 'revenue', 'runtime', 'tmdb_vote_average', 'tmdb_vote_count']
IMDB_FEATS = ['imdb_rating', 'imdb_votes', 'year']
OMDB_FEATS = ['rt_critic_score', 'metascore']
ROTT_FEATS = ['rt_audience_score']
ALL_FEATS = TMDB_FEATS + IMDB_FEATS + OMDB_FEATS + ROTT_FEATS

# Instantiating the TMDb objects and setting the API key
tmdb = tmdbv3api.TMDb()
tmdb_search = tmdbv3api.Search()
tmdb_movies = tmdbv3api.Movie()
tmdb.api_key = tmdb_key

# Instantiating the IMDbPY search object
imdb_search = IMDb()

# Instantiating the OMDb client
omdb_client = OMDBClient(apikey = omdb_key)



## API ENDPOINTS
## ----------------------------------------------------------------
@api.post('/predict')
async def predict(request: Request):

    print(await request.body())

    # Getting JSON from the body of the request and loading as Pandas DataFrame
    df = pd.DataFrame([await request.json()])

    # Extracting the movie name from the DataFrame
    movie_name = df['movie_name'][0]

    # Getting TMDb full search results
    tmdb_search_results = tmdb_search.movies({'query': movie_name})

    # Extracting tmdb_id if search results exist
    if len(tmdb_search_results) != 0:
        tmdb_id = tmdb_search_results[0]['id']
    else:
        print(f'Results not found for title: {movie_name}.')

    # Getting the details of the movie using the tmdb_id
    tmdb_details = dict(tmdb_movies.details(tmdb_id))

    # Adding tmdb_id to tmdb_details dictionary
    tmdb_details['tmdb_id'] = tmdb_id

    # Checking the length of TMDb genres to see if there is a secondary genre
    tmdb_genre_length = len(tmdb_details['genres'])

    # Separating the primary_genre from the 'genres' nested child dictionary if it exists
    if tmdb_genre_length == 0:
        tmdb_details['primary_genre'] = np.nan
    else:
        tmdb_details['primary_genre'] = tmdb_details['genres'][0]['name']

    # Separating the secondary_genre from the 'genres' nested child dictionary if it exists
    if tmdb_genre_length >= 2:
        tmdb_details['secondary_genre'] = tmdb_details['genres'][1]['name']
    else:
        tmdb_details['secondary_genre'] = np.nan

    # Renaming some TMDb columns appropriately
    tmdb_details['tmdb_popularity'] = tmdb_details.pop('popularity')
    tmdb_details['tmdb_vote_average'] = tmdb_details.pop('vote_average')
    tmdb_details['tmdb_vote_count'] = tmdb_details.pop('vote_count')

    # Adding the TMDb features to df
    for feat in TMDB_FEATS:
        df[feat] = tmdb_details[feat]

    # Getting imdb_id from TMDb output and removing unnecessary characters
    imdb_id = df['imdb_id'][0]
    imdb_id = imdb_id[2:]

    # Using IMDbPY to get movie details using the IMDb ID
    imdb_details = dict(imdb_search.get_movie(imdb_id))

    # Renaming the features appropriately
    imdb_details['imdb_rating'] = imdb_details.pop('rating')
    imdb_details['imdb_votes'] = imdb_details.pop('votes')

    # Adding the IMDb features to df
    for feat in IMDB_FEATS:
        df[feat] = imdb_details[feat]

    # Using the OMDb client to search for the movie results using the IMDb ID
    omdb_details = omdb_client.imdbid(df['imdb_id'][0])

    # Setting the Rotten Tomatoes critic score based on availability
    if len(omdb_details['ratings']) > 0:
        for rater in omdb_details['ratings']:
            if rater['source'] == 'Rotten Tomatoes':
                omdb_details['rt_critic_score'] = rater['value']
    else:
        omdb_details['rt_critic_score'] = np.nan

    # Adding the OMDb features to df
    for feat in OMDB_FEATS:
        df[feat] = omdb_details[feat]

    # Setting the Rotten Tomatoes audience score to be null if RT critic score is not present from OMDb output
    if str(df['rt_critic_score'][0]) == 'nan':
        rt_movie_details = {'rt_audience_score': np.nan}
    else:
        # Setting the Rotten Tomatoes audience score appropriately from the RT scraper object if present
        try:
            # Getting the movie metadata from the RT scraper
            movie_name = df['movie_name'][0]
            rt_movie_scraper = MovieScraper(movie_title = movie_name)
            rt_movie_scraper.extract_metadata()

            # Extracting the critic and audience scores from the metadata
            rt_critic_score = rt_movie_scraper.metadata['Score_Rotten']
            rt_audience_score = rt_movie_scraper.metadata['Score_Audience']

            # Comparing the rt_critic_score from the RT scraper to the OMDb output
            if rt_critic_score == df['rt_critic_score'][0][:2]:
                rt_movie_details = {'rt_audience_score': rt_audience_score}
            else:
                rt_movie_details = {'rt_audience_score': np.nan}

        # Setting the Rotten Tomatoes audience score to be null if RT critic score is not present from OMDb output
        except:
            rt_movie_details = {'rt_audience_score': np.nan}

    # Adding the ROTT features to df
    for feat in ROTT_FEATS:
        df[feat] = rt_movie_details[feat]

    # Getting the inference for the Biehn "yes or no" approval
    df['biehn_yes_or_no'] = binary_classification_pipeline.predict(df[ALL_FEATS])

    # Getting the inference for the Biehn Scale score
    df['biehn_scale_score'] = regression_pipeline.predict(df[ALL_FEATS])
    print(df[['movie_name', 'biehn_yes_or_no', 'biehn_scale_score']])

    # Establishing final output as a dictionary
    output_dict = {'movie_name': df['movie_name'][0],
                   'biehn_yes_or_no': df['biehn_yes_or_no'][0],
                   'biehn_scale_score': df['biehn_scale_score'][0]
                   }

    # Crafting the final response
    final_response = jsonable_encoder(output_dict)

    return JSONResponse(content = final_response)