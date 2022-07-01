import yaml
import cloudpickle
from fastapi import FastAPI, Request, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from helpers import *



## API INSTANTIATION
## ---------------------------------------------------------------------------------------------------------------------
# Instantiating the FastAPI object
api = FastAPI()

# Instantiating an object to hold the HTML files
html_templates = Jinja2Templates(directory = 'html_files')

# Loading the API keys from the separate, secret YAML file
with open('../../keys/keys.yml', 'r') as f:
    keys_yaml = yaml.safe_load(f)

# Extracting the API keys from the loaded YAML
tmdb_key = keys_yaml['api_keys']['tmdb_key']
omdb_key = keys_yaml['api_keys']['omdb_key']

# Loading the respective models from the serialized pickle files
with open('../../models/binary_classification_pipeline.pkl', 'rb') as f:
    binary_classification_pipeline = cloudpickle.load(f)
with open('../../models/regression_pipeline.pkl', 'rb') as f:
    regression_pipeline = cloudpickle.load(f)



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