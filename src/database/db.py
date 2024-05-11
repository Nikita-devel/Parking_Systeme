import contextlib

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from src.conf.config import config
from src.database.models import Base


class DatabaseSessionManager:
    def __init__(self, url: str):
        """
        DatabaseSessionManager constructor.

        Parameters:
        - url (str): The URL of the database.
        """
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker | None = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        """
        Async context manager for providing a database session.

        Yields:
        - AsyncSession: A new database session.

        Raises:
        - Exception: If the session maker is not initialized.
        """
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session
            await session.commit()
        except Exception as err:
            await session.rollback()
            raise err
        finally:
            await session.close()

    async def create_tables(self):
        """
        Create database tables asynchronously.

        Raises:
        - Exception: If an error occurs during table creation.
        """
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


sessionmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    """
    Async generator function to provide a database session.

    Yields:
    - AsyncSession: A database session.

    Raises:
    - Exception: If an error occurs during table creation.
    """
    await sessionmanager.create_tables()
    async with sessionmanager.session() as session:
        print("ok")
        yield session
