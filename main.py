from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.api import users


app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
async def health_check():
    """
    Verifica si el microservicio está en un estado saludable.
    """
    return {"status": "ok"}