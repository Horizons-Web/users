from fastapi import FastAPI, status

from app.api import users_ep
from app.config import configure_cors, configure_sentry

app = FastAPI()

configure_cors(app)
configure_sentry(app)

app.include_router(users_ep.router)


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
async def health_check():
    """
    Verifica si el microservicio está en un estado saludable.
    """
    return {"status": "ok"}


@app.get("/sentry-debug", status_code=status.HTTP_200_OK, tags=["Sentry"])
async def trigger_error():
    """
    Endpoint para probar la integración de Sentry.
    """
    division_by_zero = 1 / 0
