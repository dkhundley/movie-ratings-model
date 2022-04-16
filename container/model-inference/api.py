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
from helpers import get_movie_inference



## API INSTANTIATION
## ---------------------------------------------------------------------------------------------------------------------
# Instantiating FastAPI object
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



## API ENDPOINTS
## ---------------------------------------------------------------------------------------------------------------------
@api.post('/predict')
async def predict(request: Request):

    # Getting the response from the body of the request
    response_body = await request.body()

    # Converting response from binary to standard string
    movie_name = response_body.decode('ascii')

    # Getting JSON from the body of the request and loading as Pandas DataFrame
    df = pd.DataFrame(data = [movie_name], columns = ['movie_name'])

    # Getting the movie review predictions appropriately
    final_scores = get_movie_inference(movie_name, tmdb_key, omdb_key, binary_classification_pipeline, regression_pipeline)

    # Crafting the final response
    final_response = jsonable_encoder(final_scores)

    return JSONResponse(content = final_response)