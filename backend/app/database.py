from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
