# Importing the necessary Python libraries
import os
import warnings
import pandas as pd
from datetime import datetime
from category_encoders.one_hot import OneHotEncoder



def perform_feature_engineering(df_all_data, OUTPUT_PATH):
    """
    Generating a delta Pandas DataFrame so as not to duplicate any data we have already gathered

    Args:
        - df_all_data (Pandas DataFrame): A DataFrame containing all data ready for feature engineering
        - OUTPUT_PATH (str): The string location of where to place the data output

    Returns:
        - df_clean (Pandas DataFrame): A DataFrame containing the cleaned data
    """
    
    # Printing the starting statement
    print('Starting feature engineering...')
    
    # Removing any entries without a score
    df_all_data.dropna(subset = ['biehn_scale_rating'], axis = 'rows', inplace = True)
    
    # Dropping columns that are not required
    df_all_data.drop(columns = ['tmdb_id', 'imdb_id', 'tmdb_popularity'], inplace = True)
    
    # Performing the encoding of the "biehn_yes_or_no" feature
    for index, row in df_all_data.iterrows():
        movie_name = row['movie_name']
        if row['biehn_yes_or_no'] == 'Yes':
            df_all_data.loc[index, 'biehn_yes_or_no'] = 1
        elif row['biehn_yes_or_no'] == 'No':
            df_all_data.loc[index, 'biehn_yes_or_no'] = 0
            
    # Changing the datatype of the "biehn_yes_or_no" to int
    df_all_data['biehn_yes_or_no'] = df_all_data['biehn_yes_or_no'].astype(int)
    
    # Defining the OneHotEncoders for the genre columns
    primary_genre_encoder = OneHotEncoder(use_cat_names = True, handle_unknown = 'ignore')
    secondary_genre_encoder = OneHotEncoder(use_cat_names = True, handle_unknown = 'ignore')
    
    # Getting the one-hot encoded dummies for each of the genre columns
    primary_genre_dummies = primary_genre_encoder.fit_transform(df_all_data['primary_genre'])
    secondary_genre_dummies = secondary_genre_encoder.fit_transform(df_all_data['secondary_genre'])
    
    # Concatenating the genre dummies to the original dataframe
    df_all_data = pd.concat([df_all_data, primary_genre_dummies, secondary_genre_dummies], axis = 1)
    
    # Dropping the original genre columns
    df_all_data.drop(columns = ['primary_genre', 'secondary_genre'], inplace = True)
    
    # Extracting current year
    currentYear = datetime.now().year
    
    # Engineering the "year" column to be a relative "movie_age" column based on number of years since original release
    for index, row in df_all_data.iterrows():
        movie_name = row['movie_name']
        year_released = row['year']
        movie_age = currentYear - year_released
        df_all_data.loc[index, 'movie_age'] = movie_age
        
    # Removing percentage sign from RT critic score
    for index, row in df_all_data.iterrows():
        if pd.notnull(row['rt_critic_score']):
          df_all_data.loc[index, 'rt_critic_score'] = int(row['rt_critic_score'][:2])
          
    # Filling rt_critic_score nulls with critic average of 59%
    df_all_data['rt_critic_score'].fillna(59, inplace = True)
    
    # Transforming RT critic score into an integer datatype
    df_all_data['rt_critic_score'] = df_all_data['rt_critic_score'].astype(int)
    
    # Filling metascore nulls with 50.0
    df_all_data['metascore'].fillna(50.0, inplace = True)
    
    # Filling rt_audience_score with audience average of 59%
    df_all_data['rt_audience_score'].fillna(59.0, inplace = True)
    
    # Copying the DataFrame appropriately
    df_clean = df_all_data
    
    # Saving the DataFrame to a CSV
    df_clean.to_csv(os.path.join(OUTPUT_PATH, 'train.csv'), index = False)
    
    # Printing completion statement
    print('Feature engineering complete!')
    
    return df_clean