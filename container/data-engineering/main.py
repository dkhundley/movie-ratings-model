# Importing the necessary Python Libraries
import os
# import yaml
import pandas as pd
import tmdbv3api
from imdb import IMDb
from omdb import OMDBClient
from rotten_tomatoes_scraper.rt_scraper import MovieScraper

# Importing the helper functions from other adjacent files
from get_google_sheets_data import *
from generate_delta import *
from get_tmdb_data import *



## PROJECT SUPPORT
## ---------------------------------------------------------------------------------------------------------------------
# Pointing to the primary directory where data will be loaded and saved
PRIMARY_DIRECTORY = "/opt/ml/"

# Noting the subdirectories underneath the primary directory
INPUT_PATH = os.path.join(PRIMARY_DIRECTORY, 'input/data')
OUTPUT_PATH = os.path.join(PRIMARY_DIRECTORY, 'output')

# # Loading the API keys from the separate, secret YAML file
# with open('../keys/keys.yml', 'r') as f:
#     keys_yaml = yaml.safe_load(f)
#
# # Extracting the API keys from the loaded YAML
# tmdb_key = keys_yaml['api_keys']['tmdb_key']
# omdb_key = keys_yaml['api_keys']['omdb_key']
#
# # Loading in the raw data gathered from previous run
# df_previous_run = pd.read_csv(os.path.join(INPUT_PATH, 'all_data.csv'))



## SCRIPT INSTANTIATION
## ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Getting the raw data from the Google Spreadsheet
    print('Retrieving Google sheets data...')
    df_reviews = get_google_sheets_data(OUTPUT_PATH)
    print('Google sheets retrieval finished!')
    
#     # Slimming down the data to a delta to not duplicate data already gathered
#     print('Slimming down data to delta...')
#     df_reviews = generate_delta(df_reviews, df_previous_run)
#     print('Delta generation complete!')
#
#     # Getting the data from TMDb
#     print('Gathering data from TMDb...')
#     df_all_data = get_tmdb_data(df_reviews, tmdb_key)
#     print('Data collection from TMDb complete!')
#
#     # Getting the data from IMDb
#     print('Gathering data from IMDb...')
#     df_all_data = get_tmdb_data(df_all_data)