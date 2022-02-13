#!/bin/bash

# Changing to the root directory of the repository
cd ../../

# Copying the data into the proper SageMaker test directory
echo 'Moving the training data to proper directory...'
cp data/raw/all_data.csv tests/sagemaker_test_dir/input/data/all_data.csv

# Building the Docker container
echo 'Building the Docker container...'
docker build -t movie-ratings-model:dev .

# Running the training container
echo 'Starting the model training job...'
docker run -v $(pwd)/tests/sagemaker_test_dir/:/opt/ml/ movie-ratings-model:dev train

# Moving the trained artifacts into the "models" directory
echo 'Moving the model artifacts...'
mv tests/sagemaker_test_dir/models/binary_classification_pipeline.pkl models/binary_classification_pipeline.pkl
mv tests/sagemaker_test_dir/models/regression_pipeline.pkl models/regression_pipeline.pkl

# Removing the training data from the SageMaker test directory
echo 'Cleaning up training data...'
#rm tests/sagemaker_test_dir/input/data/all_data.csv

# Printing statement to note train job completion
echo 'Model training complete!'