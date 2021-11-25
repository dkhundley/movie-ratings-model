import numpy as np
import pandas as pd
from imdb import IMDb

def get_imdb_data(df_all_data):
    """
    Retrieving the appropriate data from the Internet Movie Database (IMDb)

    Args:
        - df_all_data (Pandas DataFrame): A DataFrame containing the movies that need new data collected

    Returns:
        - df_all_data (Pandas DataFrame): A DataFrame containing all the data from before plus the IMDb data
    """
    
    # Printing the starting statement
    print('Gathering data from IMDb...')
    
    # Instantiating the IMDbPY search object
    imdb_search = IMDb()
    
    # Iterating through each entry in df_tmdb, using the IMDb ID to extract relevant movie information
    for index, row in df_all_data.iterrows():
        # Extracting the movie title from the row
        movie_name = row['movie_name']
        
        # Extracting the IMDb ID from the TMDb search results and removing first two "tt" characters
        imdb_id = row['imdb_id']
        imdb_id = imdb_id[2:]
        
        # Using IMDbPY to get movie details using the IMDb ID
        imdb_details = dict(imdb_search.get_movie(imdb_id))
        
        # Adding imdb_rating and imdb_votes to movie's row if available
        if 'rating' not in imdb_details.keys():
            print(f'The following movie has no IMDb rating: {movie_name}.')
            df_all_data.loc[index, 'imdb_rating'] = np.nan
        else:
            df_all_data.loc[index, 'imdb_rating'] = imdb_details['rating']
        if 'votes' not in imdb_details.keys():
            df_all_data.loc[index, 'imdb_rating'] = np.nan
        else:
            df_all_data.loc[index, 'imdb_votes'] = imdb_details['votes']
        
        # Adding the year the movie debuted
        df_all_data.loc[index, 'year'] = imdb_details['year']
    
    # Printing the completion statement
    print('Data collection from IMDb complete!')
    
    return df_all_data