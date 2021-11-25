#!/bin/bash

# Changing directory to root level of the repository
cd ../../

# Moving data from data directory into sagemaker_dir
echo 'Moving the data into the input directory...'
cp data/raw/all_data.csv tests/sagemaker_dir/input/data/all_data.csv

# Building the Docker image from the Dockerfile
echo 'Rebuilding the Docker image...'
docker build -t movie-ratings-model:dev .

# Running the Docker container while mounting the sagemaker_dir
echo 'Running the Docker image for data engineering...'
docker run -v $(pwd)/tests/sagemaker_dir:/opt/ml movie-ratings-model:dev preprocess

# Moving outputs on job completion into appropriate data directory
echo 'Moving the outputs into appropriate final directory...'
mv tests/sagemaker_dir/output/caelan_reviews.csv data/raw/caelan_reviews.csv
mv tests/sagemaker_dir/output/all_data.csv data/raw/all_data.csv
mv tests/sagemaker_dir/output/train.csv data/clean/train.csv

# Deleting data from sagemaker_dir
echo 'Deleting data from sagemaker_dir'
rm tests/sagemaker_dir/input/data/all_data.csv

echo 'Data engineering local test complete!'