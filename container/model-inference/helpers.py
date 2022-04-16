# Importing the necessary Python libraries
import numpy as np
import pandas as pd
from datetime import datetime
import tmdbv3api
from imdb import IMDb
from omdb import OMDBClient
from rotten_tomatoes_scraper.rt_scraper import MovieScraper



## FEATURE ENGINEERING FUNCTIONS
## ---------------------------------------------------------------------------------------------------------------------
def generate_movie_age(df):
    """
    Generating a movie age relative to the current year and the year that the movie was released

    Args:
        - df (Pandas DataFrame): A DataFrame containing the raw data for which year the movie was released

    Returns:
        - df (Pandas DataFrame): A DataFrame containing newly engineered feature of relative "year"
    """

    # Extracting current year
    currentYear = datetime.now().year

    # Engineering the "year" column to be a relative "movie_age" column based on number of years since original release
    for index, row in df.iterrows():
        year_released = row['year']
        movie_age = currentYear - year_released
        df.loc[index, 'movie_age'] = movie_age

    return df



def engineer_rt_critic_score(df):
    """
    Feature engineering the Rotten Tomatoes critic score

    Args:
        - df (Pandas DataFrame): A DataFrame containing the raw data RT critic score

    Returns:
        - df (Pandas DataFrame): A DataFrame containing an updated version of RT critic score
    """

    # Removing percentage sign from RT critic score
    for index, row in df.iterrows():
        if pd.notnull(row['rt_critic_score']):
            df.loc[index, 'rt_critic_score'] = int(row['rt_critic_score'][:2])

    # Filling rt_critic_score nulls with critic average of 59%
    df['rt_critic_score'].fillna(59, inplace = True)

    # Transforming RT critic score into an integer datatype
    df['rt_critic_score'] = df['rt_critic_score'].astype(int)

    return df



def handle_nulls_for_metascore(df):
    """
    Handling the nulls associated to the metascore feature

    Args:
        - df (Pandas DataFrame): A DataFrame containing the raw data metascore feature

    Returns:
        - df (Pandas DataFrame): A DataFrame containing an updated version of the metascore
    """

    # Filling metascore nulls with 50.0
    df['metascore'].fillna(50.0, inplace = True)

    return df



def handle_nulls_for_rt_audience_score(df):
    """
    Handling the nulls associated to the RT audience score feature

    Args:
        - df (Pandas DataFrame): A DataFrame containing the raw data RT audience score feature

    Returns:
        - df (Pandas DataFrame): A DataFrame containing an updated version of the RT audience score
    """

    # Filling rt_audience_score with audience average of 59%
    df['rt_audience_score'].fillna(59.0, inplace = True)

    return df



## MODEL INFERENCE FUNCTIONS
## ---------------------------------------------------------------------------------------------------------------------
def get_movie_prediction(movie_name, tmdb_key, omdb_key, binary_classification_pipeline, regression_pipeline):
    """
    Getting the movie review prediction from the input data

    Args:
        - movie_name (str): A string containing the name of the movie to infer for predictions
        - tmdb_key (str): A string representing the API key to get data from the TMDb API
        - omdb_key (str): A string representing the API key to get data from the OMDb API
        - binary_classification_pipeline (obj): The model representing the binary classification pipeline to obtain the Biehn binary yes / no approval score
        - regression_pipeline (obj): The model representing the regression pipeline to obtain the Biehn Scale score

    Returns:
        - final_scores (dict): A dictionary containing the movie name and final scores
    """

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

    # Getting JSON from the body of the request and loading as Pandas DataFrame
    df = pd.DataFrame(data = [movie_name], columns = ['movie_name'])

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

    # Establishing final output as a dictionary
    final_scores = {'movie_name': df['movie_name'][0],
                    'biehn_yes_or_no': df['biehn_yes_or_no'][0],
                    'biehn_scale_score': df['biehn_scale_score'][0]
                   }

    return final_scores