from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from app.models import * 
from sqlmodel import SQLModel

from app.core.config import settings

# -------------------------
# DATABASE URL
# -------------------------
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI


# -------------------------
# ENGINE
# -------------------------
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)


# -------------------------
# SESSION
# -------------------------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# We use SQLModel.metadata directly to handle table registration and creation.


# -------------------------
# DB DEPENDENCY
# -------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session



# -------------------------
# INIT DB
# -------------------------
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)