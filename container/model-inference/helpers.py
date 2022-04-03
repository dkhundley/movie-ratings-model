# Importing the necessary Python libraries
import numpy as np
import pandas as pd
from datetime import datetime



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