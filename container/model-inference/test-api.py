from fastapi import FastAPI

## API INSTANTIATION
## ----------------------------------------------------------------
# Instantiating FastAPI
api = FastAPI()



## API ENDPOINTS
## ----------------------------------------------------------------
@api.get('/')
async def mainpage():
    return 'You made it to the page, my friend!'