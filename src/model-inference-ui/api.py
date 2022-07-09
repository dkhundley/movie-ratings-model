# Importing the necessary Python libraries
import os
import sys
import yaml
import cloudpickle
from fastapi import FastAPI, Request, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from helpers import *



## API INSTANTIATION
## ---------------------------------------------------------------------------------------------------------------------
# Instantiating the FastAPI object
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

# Instantiating an object to hold the HTML files
html_templates = Jinja2Templates(directory = 'webpage/html')

# Mounting the CSS file for use by the HTML rendered pages
api.mount('/css', StaticFiles(directory = 'webpage/css'), name = 'css')


## API ENDPOINTS
## ---------------------------------------------------------------------------------------------------------------------
@api.get('/', response_class = HTMLResponse)
async def homepage(request: Request):
    return html_templates.TemplateResponse('home.html', {'request': request})

@api.post('/', response_class = HTMLResponse)
async def results_page(request: Request, movie_name: str = Form(...)):

    # Getting JSON from the body of the request and loading as Pandas DataFrame
    df = pd.DataFrame(data = [movie_name], columns = ['movie_name'])

    # Getting the movie review predictions appropriately
    final_scores = get_movie_prediction(movie_name, tmdb_key, omdb_key, binary_classification_pipeline, regression_pipeline)

    # Crafting the final response
    final_response = jsonable_encoder(final_scores)

    return html_templates.TemplateResponse('results.html', {'request': request, 'result': final_response})

@api.post('/invocations')
async def predict(request: Request):

    # Getting the response from the body of the request
    response_body = await request.body()

    # Converting response from binary to standard string
    movie_name = 'The Matrix'

    # Getting JSON from the body of the request and loading as Pandas DataFrame
    df = pd.DataFrame(data = [movie_name], columns = ['movie_name'])

    # Getting the movie review predictions appropriately
    final_scores = get_movie_prediction(movie_name, tmdb_key, omdb_key, binary_classification_pipeline, regression_pipeline)

    # Crafting the final response
    final_response = jsonable_encoder(final_scores)

    return JSONResponse(content = final_response)

@api.get('/ping')
async def health():
    return JSONResponse(content = {'status': 'healthy!'}, status_code = 200)