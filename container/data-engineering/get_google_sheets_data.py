# Importing the required libraries
import os
import pandas as pd



# Defining the ID of the Google Sheet
SHEET_ID = '1-8tdDUtm0iBrCdCRAsYCw2KOimecrHcmsnL-aqG-l0E'

# Defining the new column names for the review fields
NEW_COL_NAMES = {'Name': 'movie_name',
                 'Rating': 'biehn_scale_rating',
                 'Flickable': 'biehn_yes_or_no'}



def load_google_sheet(sheet_id, sheet_name):
    """
    Takes in the Google sheet ID and sheet name and loads Google sheet data as Pandas DataFrame
    
    Args:
        - sheet_id (str): ID number of the Google sheet
        - sheet_name (str): Name of the desired Google tab / sheet
    
    Returns:
        - df: A Pandas DataFrame containing the Google sheet information
    """
    
    # Formatting the URL with the inputted sheet_id and sheet_name
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    
    # Loading the data as a Pandas Dataframe
    df = pd.read_csv(url)
    
    return df
    
    
    
def get_google_sheets_data():
    """
    Gets data from the Google spreadsheet containing Caelan's reviews
    
    Args:
        - N/A
    Returns:
        - A saved CSV to the raw data directory
        - df_reviews: A Pandas DataFrame containing Caelan's reviews
    """
    
    # Getting the respective sheet data
    df_main = load_google_sheet(SHEET_ID, 'main')
    df_patreon = load_google_sheet(SHEET_ID, 'patreon')
    df_mnight = load_google_sheet(SHEET_ID, 'movie_night')
    
    # Concatenating the reviews across the three sheets
    df_reviews = pd.concat([df_main, df_patreon, df_mnight], axis = 0)
    
    # Filtering down DataFrame to show only movies
    df_reviews = df_reviews[df_reviews['Category'] == 'Movie']
    
    # Dropping the unneeded columns
    df_reviews.drop(columns = ['Category', 'Episode Number', 'Notes'], inplace = True)
    
    # Renaming the columns appropriately
    df_reviews.rename(columns = NEW_COL_NAMES, inplace = True)
    
    # Saving Caelan's reviews to a CSV file
    df_reviews.to_csv('../data/raw/caelan-reviews.csv', index = False)
    
    return df_reviews
