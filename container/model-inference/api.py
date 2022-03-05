# Importing the necessary Python libraries
import yaml
# import cloudpickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request
import tmdbv3api
# from imdb import IMDb
# from omdb import OMDBClient
# from rotten_tomatoes_scraper.rt_scraper import MovieScraper
# from datetime import datetime
# from category_encoders.one_hot import OneHotEncoder
# from sklearn.preprocessing import FunctionTransformer
# from sklearn.preprocessing import StandardScaler
# from sklearn.compose import ColumnTransformer
# from sklearn.linear_model import Lasso
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.pipeline import Pipeline



## API INSTANTIATION
## ----------------------------------------------------------------
# Instantiating FastAPI
api = FastAPI()

# Loading the models from the serialized pickle files
# with open('../../models/binary_classification_pipeline.pkl', 'rb') as f:
#     binary_classification_pipeline = cloudpickle.load(f)
# with open('../../models/regression_pipeline.pkl', 'rb') as f:
#     regression_pipeline = cloudpickle.load(f)

# Loading the API keys from the separate, secret YAML file
with open('../../keys/keys.yml', 'r') as f:
    keys_yaml = yaml.safe_load(f)

# Extracting the API keys from the loaded YAML
tmdb_key = keys_yaml['api_keys']['tmdb_key']
omdb_key = keys_yaml['api_keys']['omdb_key']

# Instantiating the TMDb objects and setting the API key
tmdb = tmdbv3api.TMDb()
tmdb_search = tmdbv3api.Search()
tmdb_movies = tmdbv3api.Movie()
tmdb.api_key = tmdb_key



## API ENDPOINTS
## ----------------------------------------------------------------
@api.post('/predict')
async def predict(request: Request):

	# Getting the JSON from the body of the request
	json_input = await request.json()

	# Converting JSON to Pandas DataFrame
	df_input = pd.DataFrame([json_input])

	# Extracting the movie name from the input
	movie_name = df_input['movie_name'][0]
	print(movie_name)

	# Getting TMDb full search results
	tmdb_search_results = tmdb_search.movies({'query': movie_name})
	print(tmdb_search_results)

#     # Extracting tmdb_id if search results exist
#     if len(tmdb_search_results) != 0:
#         tmdb_id = tmdb_search_results[0]['id']
#     else:
#         return 'Results not found for title'
#
# 	# Getting the details of the movie using the tmdb_id
#     tmdb_details = dict(tmdb_movies.details(tmdb_id))
#     print(tmdb_details)

#     # Checking the length of TMDb genres to see if there is a secondary genre
#     tmdb_genre_length = len(tmdb_details['genres'])
#
#     # Separating the primary_genre from the 'genres' nested child dictionary if it exists
#     if tmdb_genre_length == 0:
#         df_input['primary_genre'] = np.nan
#     else:
#         df_input['primary_genre'] = tmdb_details['genres'][0]['name']
#
#     # Separating the secondary_genre from the 'genres' nested child dictionary if it exists
#     if tmdb_genre_length >= 2:
#         df_input['secondary_genre'] = tmdb_details['genres'][1]['name']
#     else:
#         df_input['secondary_genre'] = np.nan
#
#     # Slimming down tmdb_details with only the features we want to keep
#     tmdb_details = {key: value for key, value in tmdb_details.items() if key in tmdb_feats}
#
#     # Converting the tmdb_details dictionary to a Pandas DataFrame
#     new_tmdb_entry = pd.DataFrame.from_dict([tmdb_details])
#
#     # Appending the new movie entry to the overall df_tmdb DataFrame
#     df_tmdb = df_tmdb.append(new_tmdb_entry, ignore_index = True)

