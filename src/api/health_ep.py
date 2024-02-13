from fastapi import Depends, status, APIRouter
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from contextlib import contextmanager

from src.db_config import database
from src.utils.utils import send_confirmation_email
from src.models import models



router = APIRouter(
    prefix="/api",
    tags=['Health Check']
)


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Verify the health of services.
    """
    class UserRepository:
        @staticmethod
        @contextmanager
        def get_db() -> Session:
            db = database.SessionLocal()
            try:
                yield db
            finally:
                db.close()

    async def test():
        with UserRepository.get_db() as db:
            try:
                db.query(models.Users).first()
                try:
                    await send_confirmation_email("test@example.com", "confirmation_token")
                    return {"status": "ok", "message": "Database connection is healthy, email service is healthy"}
                except Exception as e:
                    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                        detail="Email service is not healthy")
            except Exception as e:
                return e

    return await test()

@router.get("/sentry-debug", status_code=status.HTTP_200_OK)
async def trigger_error():
    """
    Verify the Sentry error tracking.
    """
    division_by_zero = 1 / 0
