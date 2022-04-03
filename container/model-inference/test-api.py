from fastapi import FastAPI
import os

## API INSTANTIATION
## ----------------------------------------------------------------
# Instantiating FastAPI
api = FastAPI()

# Getting Heroku secret value
SECRET_VAL = os.getenv('SECRET_VAL')

## API ENDPOINTS
## ----------------------------------------------------------------
@api.get('/')
async def mainpage():
    return f'You made it to the page, my friend! Here is the secret value: {SECRET_VAL}'