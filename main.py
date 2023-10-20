from fastapi import FastAPI

from app.api import endpoint


app = FastAPI()

app.include_router(endpoint.router)
