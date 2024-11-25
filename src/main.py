from fastapi import FastAPI

from src.api import users_ep, health_ep
from src.config import configure_cors

app = FastAPI()

configure_cors(app)

app.include_router(users_ep.router)
app.include_router(health_ep.router)



