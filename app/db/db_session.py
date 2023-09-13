"""Connection to the Postgres database."""
import logging
from sqlalchemy import MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config import get_api_settings 

logger = logging.getLogger(__name__)

metadata = MetaData()

def get_async_engine() -> AsyncEngine:
    """Return async database engine."""
    try:
        async_engine: AsyncEngine = create_async_engine(
            get_api_settings().database_url,
            echo=True,
            future=True,
        )
    except SQLAlchemyError as e:
        logger.warning("Unable to establish db engine, database might not exist yet")
        logger.warning(e)
        raise e

    return async_engine

async def initialize_database() -> None:
    """
    Initialize database.
    Using the `reflect` method of metadata,
    we can consume the entire base of a database,
    and create its models based on these parameters
    """
    async_engine = get_async_engine()
    async with async_engine.begin() as async_conn:
        await async_conn.run_sync(metadata.reflect)

        logger.info("Initializing database was successfull.")
