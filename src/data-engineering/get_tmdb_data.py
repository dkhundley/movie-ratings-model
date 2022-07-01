import numpy as np
import pandas as pd
import tmdbv3api



def get_tmdb_data(df_new_data, tmdb_key):
    """
    Retrieving the appropriate data from The Movies Database (TMDb)

    Args:
        - df_new_data (Pandas DataFrame): A DataFrame containing the movies that need new data collected
        - tmdb_key (str): A string representing our API key for interacting with TMDb's API

    Returns:
        - df_new_data (Pandas DataFrame): A DataFrame containing all the data from before plus the TMDb data
    """
    
    # Printing the starting statement
    print('Gathering data from TMDb...')

    # Instantiating the TMDb objects and setting the API key
    tmdb = tmdbv3api.TMDb()
    tmdb_search = tmdbv3api.Search()
    tmdb_movies = tmdbv3api.Movie()
    tmdb.api_key = tmdb_key

    # Defining which features we need to keep from tmdb_details
    TMDB_FEATS = ['movie_name', 'biehn_scale_rating', 'biehn_yes_or_no', 'tmdb_id', 'imdb_id', 'budget', 'primary_genre', 'secondary_genre', 'popularity', 'revenue', 'runtime', 'vote_average', 'vote_count']

    # Creating a new DataFrame to hold all the TMDb data
    df_tmdb = pd.DataFrame(columns = TMDB_FEATS)

    # Iterating through the df_ratings DataFrame to get the names for extracting detailed info from TMDb
    for index, row in df_new_data.iterrows():
        # Extracting info from df_ratings
        movie_name = row['movie_name']
        biehn_scale_rating = row['biehn_scale_rating']
        biehn_yes_or_no = row['biehn_yes_or_no']

        # Performing the preliminary search
        search_results = tmdb_search.movies({'query': movie_name})

        # Extracting tmdb_id if search results exist
        if len(search_results) != 0:
            tmdb_id = search_results[0]['id']
        else:
            print(f'Results not found for title: {movie_name}.')
            continue

        # Getting the details of the movie using the tmdb_id
        tmdb_details = dict(tmdb_movies.details(tmdb_id))

        # Adding the df_ratings info and tmdb_id to the tmdb_details dictionary
        tmdb_details['movie_name'] = movie_name
        tmdb_details['biehn_scale_rating'] = biehn_scale_rating
        tmdb_details['biehn_yes_or_no'] = biehn_yes_or_no
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

        # Slimming down tmdb_details with only the features we want to keep
        tmdb_details = {key: value for key, value in tmdb_details.items() if key in TMDB_FEATS}

        # Converting the tmdb_details dictionary to a Pandas DataFrame
        new_tmdb_entry = pd.DataFrame.from_dict([tmdb_details])

        # Appending the new movie entry to the overall df_tmdb DataFrame
        df_tmdb = df_tmdb.append(new_tmdb_entry, ignore_index = True)

    # Renaming some of the columns to avoid ambiguity later
    TMDB_NEW_COL_NAMES = {
        'popularity': 'tmdb_popularity',
        'vote_average': 'tmdb_vote_average',
        'vote_count': 'tmdb_vote_count'
    }

    # Applying the new column names appropriately
    df_tmdb.rename(columns = TMDB_NEW_COL_NAMES, inplace = True)

    # Using df_tmdb as source for all new data in a single DataFrame
    df_new_data = df_tmdb
    
    # Printing the completion statement
    print('Data collection from TMDb complete!')

    return df_new_data