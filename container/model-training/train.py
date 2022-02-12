# Importing the necessary Python libraries
import os
import pandas as pd

# Importing the helper functions from other adjacent files
from helpers import *



## PROJECT SUPPORT
## ---------------------------------------------------------------------------------------------------------------------
# Pointing to the primary directory where data will be loaded and saved
PRIMARY_DIRECTORY = "/opt/ml/"

# Noting the subdirectories underneath the primary directory
INPUT_PATH = os.path.join(PRIMARY_DIRECTORY, 'input/data')
MODEL_PATH = os.path.join(PRIMARY_DIRECTORY, 'models')
OUTPUT_PATH = os.path.join(PRIMARY_DIRECTORY, 'output')

# Loading in the CSV from the output of the data collection
df_all_data = pd.read_csv(os.path.join(INPUT_PATH, 'all_data.csv'))



## SCRIPT INSTANTIATION
## ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Performing feature engineering on the raw dataset
    df_clean = perform_feature_engineering(df_all_data, OUTPUT_PATH)
    
    print(df_clean.head())
    print(df_clean.info())