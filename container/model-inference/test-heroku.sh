#!/bin/bash

# Starting up FastAPI using the Uvicorn ASGI service
uvicorn --host 0.0.0.0 --port 8080 test-api:api