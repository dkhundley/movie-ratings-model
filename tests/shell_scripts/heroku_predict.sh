#curl --request POST --header 'Content-Type: application/json' --data @../test_json/single_movie.json --url https://caelan-api.herokuapp.com/predict
curl --request POST --header "Content-Type: application/json" --data "The Batman" --url https://caelan-api.herokuapp.com/predict
