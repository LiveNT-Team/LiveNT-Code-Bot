"""
Module contains `engine` and `session_factory` objects to connect and execute queries in database
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .configuration import PROD_SQLALCHEMY_URL, DEV_SQLALCHEMY_URL, IS_DEV_MODE


engine = create_async_engine(DEV_SQLALCHEMY_URL if IS_DEV_MODE else PROD_SQLALCHEMY_URL)
session_factory = async_sessionmaker(
    bind=engine,
    autoflush=True,
)
__all__ = (
    "engine",
    "session_factory",
)
