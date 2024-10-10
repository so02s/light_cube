from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime
import datetime

class Base(AsyncAttrs, DeclarativeBase):
    pass

# class Quiz(Base):
#     __tablename__ = "quiz"
    
#     id_quiz: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
#     quiz_name: Mapped[str] = mapped_column(String, nullable=False)
#     num_corrections: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
#     time_start: Mapped[str] = mapped_column(String)

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Cube(Base):
    __tablename__ = "cubes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    connected_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(6))
    
async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_all_tables())