# Importing the required libraries
import os
import pandas as pd

# Defining the ID of the Google Sheet
sheet_id = '1-8tdDUtm0iBrCdCRAsYCw2KOimecrHcmsnL-aqG-l0E'

# Creating a small function to load the data sheet by ID and sheet name
def load_google_sheet(sheet_id, sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url)
    return df
    
# Loading all the sheets and joining them together
def load_raw():
    df_main = load_google_sheet(sheet_id, 'main')
    df_patreon = load_google_sheet(sheet_id, 'patreon')
    df_mnight = load_google_sheet(sheet_id, 'movie_night')
    df = pd.concat([df_main, df_patreon, df_mnight], axis = 0)
    df.to_csv('../data/raw.csv', index = False)
    

if __name__ == '__main__':
    load_raw()

# Comment!