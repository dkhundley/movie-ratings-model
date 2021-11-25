# Importing the necessary Python libaries
import os
import pandas as pd



def save_and_join_raw_data(df_previous_run, df_new_data, OUTPUT_PATH):
    """
    Retrieving the appropriate data from the Open Movie Database (OMDb)

    Args:
        - df_previous_run (Pandas DataFrame): A DataFrame containing data from previous runs
        - df_new_data (Pandas DataFrame): A DataFrame containing the movies that need new data collected
        - OUTPUT_PATH (str): The string location of where to place the data output

    Returns:
        - df_all_data (Pandas DataFrame): A DataFrame containing all joined data
    """
    
    # Concatenating the new data with data from the previous run
    df_all_data = pd.concat([df_previous_run, df_new_data], axis = 0)
    
    # Saving the data to the appropriate output path
    df_all_data.to_csv(os.path.join(OUTPUT_PATH, 'all_data.csv'), index = False)
    
    return df_all_data