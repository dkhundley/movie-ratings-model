# Importing the necessary Python libraries
import os
import pandas as pd



def generate_delta(df_reviews, df_previous_run, OUTPUT_PATH):
    """
    Generating a delta Pandas DataFrame so as not to duplicate any data we have already gathered

    Args:
        - df_reviews (Pandas DataFrame): A DataFrame containing all the reviews of movies that Caelan has rated
        - df_previous_run (Pandas DataFrame): A DataFrame containing all the data from the previous run
        - OUTPUT_PATH (str): The string location of where to place the data output

    Returns:
        - df_new_data (Pandas DataFrame): A DataFrame containing only the reviews where we have not yet gathered the data
    """
    
    # Printing the starting statement
    print('Slimming down data to delta...')
    
    # Printing how many movies have already collected data
    print(f'Number of movies with already populated data: {len(df_previous_run)}')
    
    # Extracting the movie names from df_previous_run
    movie_names = df_previous_run[['movie_name']]
    
    # Performing a merge to indicate which movies need new data collected
    df_new_data = df_reviews.merge(right = movie_names, how = 'outer', on = 'movie_name', indicator = True)
    
    # Filtering out movies where data has already been collected
    df_new_data = df_new_data[df_new_data['_merge'] == 'left_only']
    
    # Dropping the "_merge" column
    df_new_data.drop(columns = ['_merge'], inplace = True)
    
    # Exiting data engineering process if no data is available
    if len(df_new_data) == 0:
        
        # Saving the output as the former run
        df_previous_run.to_csv(os.path.join(OUTPUT_PATH, 'all_data.csv'), index = False)
        
        # Printing exit message
        print('No new movies are present. Exiting script.')
        
        # Stopping the Python script
        exit(0)
    
    # Printing how many new movies will need additional data
    print(f'Number of new movies needing data: {len(df_new_data)}')
    
    # Printing the completion statement
    print('Delta generation complete!')
    
    return df_new_data