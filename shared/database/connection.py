from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# fix asyncpg
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+asyncpg://"
    )

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
