import numpy as np
import pandas as pd
from rotten_tomatoes_scraper.rt_scraper import MovieScraper

def get_rt_data(df_new_data):
    """
    Retrieving the appropriate data from Rotten Tomatoes

    Args:
        - df_new_data (Pandas DataFrame): A DataFrame containing the movies that need new data collected

    Returns:
        - df_new_data (Pandas DataFrame): A DataFrame containing all the data from before plus the Rotten Tomatoes data
    """
    
    # Printing the starting statement
    print('Gathering data from Rotten Tomatoes...')
    
    # Iterating through the DataFrame to collect the appropriate RT data
    for index, row in df_new_data.iterrows():
      
        # Extracting movie name from row
        movie_name = row['movie_name']
        
        # Checking to see if the movie has a critic score from the OMDb run
        rt_critic_score_string = str(row['rt_critic_score'])
        if rt_critic_score_string == 'nan':
            df_new_data.loc[index, 'rt_audience_score'] = np.nan
            continue
        
        # Instantiating scraper object with movie title
        try:
            movie_scraper = MovieScraper(movie_title = movie_name)
        except:
            df_new_data.loc[index, 'rt_audience_score'] = np.nan
            continue
        
        # Extracting the metadata about the movie
        try:
            movie_scraper.extract_metadata()
        except:
            df_new_data.loc[index, 'rt_audience_score'] = np.nan
            continue
        
        # Extracting the critic and audience scores from the metadata
        rt_critic_score = movie_scraper.metadata['Score_Rotten']
        rt_audience_score = movie_scraper.metadata['Score_Audience']
        
        # Comparing the RT critic score to OMDb and saving audience score if the same
        if rt_critic_score == row['rt_critic_score'][:2]:
            df_new_data.loc[index, 'rt_audience_score'] = rt_audience_score
        else:
          df_new_data.loc[index, 'rt_audience_score'] = np.nan
    
    # Printing the completion statement
    print('Data collection from OMDb complete!')
    
    return df_new_data