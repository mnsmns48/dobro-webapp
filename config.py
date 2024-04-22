from asyncio import current_task
from contextlib import asynccontextmanager

from pydantic import SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session


class Settings(BaseSettings):
    db_username: str
    db_password: SecretStr
    db_port: int
    dobrotsen_db_name: str


hv = Settings(_env_file=".env")


class CoreConfig():
    def __init__(self, db):
        self.db = db
        self.base: str = (
            f"postgresql+asyncpg://{hv.db_username}:{hv.db_password.get_secret_value()}"
            f"@localhost:{hv.db_port}/{db}"
        )
        self.db_echo: bool = False


dobrotsen_config = CoreConfig(db=hv.dobrotsen_db_name)


class AsyncDataBase:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url.replace('driver', 'asyncpg'),
            echo=echo,
            poolclass=NullPool
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def scoped_session(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        try:
            async with session() as s:
                yield s
        finally:
            await session.remove()

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = await self.scoped_session()
        yield session
        await session.close()


dobro_engine = AsyncDataBase(dobrotsen_config.base, dobrotsen_config.db_echo)
