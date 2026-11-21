from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.authentication_controller import router as authentication_router
from app.api.v1.authorization_controller import router as authorization_router
from app.core.config import Settings
from app.core.errors.domain_errors import DomainErrors
from app.core.exception_config import ExceptionConfig
from app.core.logging.logger import get_logger
from app.core.logging.logging_config import logging_config
from app.database import database
from app.middleware.logging_middleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute these lines when the application is starting

    # Add authentication endpoints
    my_app.include_router(authentication_router)

    # Initialize logging
    logging_config()

    logger = get_logger("startup")
    logger.info("Starting authentication API")
    logger.info(f"Environment: {Settings.ENV}")

    # Database initialization
    await database.init_database(logger, my_app)

    # Authorization endpoints are accessible only when authorization interface is enabled
    if Settings.ACTIVATE_AUTHORIZATION_INTERFACE:
        my_app.include_router(authorization_router)
        logger.info("Authorization interface routes added")
    else:
        logger.info("Authorization interface disabled. To enable it check Settings(app/core/config.py)")

    # SMTP variables must be defined if email validation is enabled
    if Settings.EMAIL_VALIDATION:
        if (not Settings.SMTP_HOST
                or not Settings.SMTP_PORT
                or not Settings.SMTP_USER
                or not Settings.SMTP_PASSWORD
                or not Settings.SMTP_FROM):
            logger.error("SMTP variables are not initialized. Check .env")
            raise

    logger.info(f"Application Running at http://{Settings.APP_HOST}:{Settings.APP_PORT}")

    yield
    # Execute these lines when the application is stopping
    logger.info("Shutting down authentication API")


my_app = FastAPI(lifespan=lifespan)

# Cannot add middleware after an application has started
ExceptionConfig(my_app)
my_app.add_middleware(LoggingMiddleware)


@my_app.exception_handler(DomainErrors)
async def domain_error_handler(request, exc: DomainErrors):
    return exc.http()


@my_app.get("/")
def root():
    return {"status": "ok"}
