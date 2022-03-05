# Importing the necessary Python libraries
import os
import sys
import cloudpickle
import pandas as pd
from category_encoders.one_hot import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# Importing the helper functions from other adjacent files
from helpers import *



## PROJECT SUPPORT
## ---------------------------------------------------------------------------------------------------------------------
# Pointing to the primary directory where data will be loaded and saved
PRIMARY_DIRECTORY = '/opt/ml/'

# Noting the subdirectories underneath the primary directory
INPUT_PATH = os.path.join(PRIMARY_DIRECTORY, 'input/data/train')
MODEL_PATH = os.path.join(PRIMARY_DIRECTORY, 'model')
OUTPUT_PATH = os.path.join(PRIMARY_DIRECTORY, 'output')



## MODEL TRAINING
## ---------------------------------------------------------------------------------------------------------------------
def train(df_raw):
    """
    Takes in the raw data for the movie rating model and trains the respective binary classfication and regression algorithms

    Args:
        - df_raw (Pandas DataFrame): A Pandas DataFrame containing the data that will be trained upon

    Returns:
        - binary_classification_pipeline (object): The trained version of the binary classification pipeline
        - regression_pipeline (object): The trained version of the regression pipeline
    """

    # Instantiating a StandardScaler object for feature scaling
    feature_scaler = StandardScaler()

    # Creating the data preprocessor that will perform our feature engineering
    data_preprocessor = ColumnTransformer(transformers = [
        ('ohe_engineering', OneHotEncoder(use_cat_names = True, handle_unknown = 'ignore'), ['primary_genre', 'secondary_genre']),
        ('movie_age_engineering', FunctionTransformer(generate_movie_age, validate = False), ['year']),
        ('rt_critic_score_engineering', FunctionTransformer(engineer_rt_critic_score, validate = False), ['rt_critic_score']),
        ('rt_audience_score_engineering', FunctionTransformer(handle_nulls_for_rt_audience_score, validate = False), ['rt_audience_score']),
        ('metascore_engineering', FunctionTransformer(handle_nulls_for_metascore, validate = False), ['metascore']),
        ('columns_to_drop', 'drop', ['movie_name', 'tmdb_id', 'imdb_id', 'tmdb_popularity'])
    ],
        remainder = 'passthrough'
    )

    # Creating the full inference pipeline for the binary classification model
    binary_classification_pipeline = Pipeline(steps = [
        ('feature_engineering', data_preprocessor),
        ('predictive_modeling', RandomForestClassifier(n_estimators = 50,
                                                       max_depth = 20,
                                                       min_samples_split = 5,
                                                       min_samples_leaf = 2))
    ])

    # Creating the full inference pipeline for the binary classification model
    regression_pipeline = Pipeline(steps = [
        ('feature_engineering', data_preprocessor),
        ('feature_scaling', feature_scaler),
        ('predictive_modeling', Lasso(alpha = 0.275))
    ])

    # Formally training the binary classification pipeline
    binary_classification_pipeline.fit(df_raw.drop(columns = ['biehn_yes_or_no', 'biehn_scale_rating']),
                                       df_raw[['biehn_yes_or_no']])

    # Formally training the regression pipeline
    regression_pipeline.fit(df_raw.drop(columns = ['biehn_yes_or_no', 'biehn_scale_rating']),
                            df_raw[['biehn_scale_rating']])

    # Returning the trained pipelines
    return binary_classification_pipeline, regression_pipeline



## SCRIPT INSTANTIATION
## ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Loading in the CSV from the output of the data collection
    df_raw = pd.read_csv(os.path.join(INPUT_PATH, 'all_data.csv'))

    # Training the binary classification and regression algorithms
    binary_classification_pipeline, regression_pipeline = train(df_raw)

    # Saving the binary classification pipeline to a serialized pickle file
    with open(os.path.join(MODEL_PATH, 'binary_classification_pipeline.pkl'), 'wb') as f:
        cloudpickle.dump(binary_classification_pipeline, f)

    # Saving the regression pipeline to a serialized pickle file
    with open(os.path.join(MODEL_PATH, 'regression_pipeline.pkl'), 'wb') as f:
        cloudpickle.dump(regression_pipeline, f)

    # Exiting with a zero code to let SageMaker know training job's success
    sys.exit(0)