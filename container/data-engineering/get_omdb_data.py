import numpy as np
import pandas as pd
from omdb import OMDBClient

def get_omdb_data(df_new_data, omdb_key):
    """
    Retrieving the appropriate data from the Open Movie Database (OMDb)

    Args:
        - df_new_data (Pandas DataFrame): A DataFrame containing the movies that need new data collected
        - omdb_key (str): A string representing the API key for OMDb

    Returns:
        - df_new_data (Pandas DataFrame): A DataFrame containing all the data from before plus the OMDb data
    """
    
    # Printing the starting statement
    print('Gathering data from OMDb...')
    
    # Instantiating the OMDb client
    omdb_client = OMDBClient(apikey = omdb_key)
    
    # Iterating through all the movies to extract the proper OMDb information
    for index, row in df_new_data.iterrows():
        # Extracting movie name from the row
        movie_name = row['movie_name']
        
        # Using the OMDb client to search for the movie results using the IMDb ID
        omdb_details = omdb_client.imdbid(row['imdb_id'])
        
        # Resetting the Rotten Tomatoes critic score variable
        rt_critic_score = None
        
        # Checking if the movie has any ratings populated under 'ratings'
        omdb_ratings_len = len(omdb_details['ratings'])
        
        if omdb_ratings_len == 0:
            print(f'{movie_name} has no Rotten Tomatoes critic score.')
        elif omdb_ratings_len >= 0:
            # Extracting out the Rotten Tomatoes score if available
            for rater in omdb_details['ratings']:
                if rater['source'] == 'Rotten Tomatoes':
                    rt_critic_score = rater['value']
                    
        # Populating Rotten Tomatoes critic score appropriately
        if rt_critic_score:
            df_new_data.loc[index, 'rt_critic_score'] = rt_critic_score
        else:
            df_new_data.loc[index, 'rt_critic_score'] = np.nan
            
        # Populating the Metacritic metascore appropriately
        df_new_data.loc[index, 'metascore'] = omdb_details['metascore']
    
    # Printing the completion statement
    print('Data collection from OMDb complete!')
    
    return df_new_data