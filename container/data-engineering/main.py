# Importing the necessary Python Libraries
import os
import yaml
import numpy as np
import pandas as pd
import tmdbv3api
from imdb import IMDb
from omdb import OMDBClient
from rotten_tomatoes_scraper.rt_scraper import MovieScraper

# Importing the helper functions from other adjacent files
from get_google_sheets_data import *



## SCRIPT INSTANTIATION
## ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Getting the raw data from the Google Spreadsheet
    get_google_sheets_data()
