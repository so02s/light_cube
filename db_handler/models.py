from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
import datetime
import asyncio
from create_bot import engine, Session

class HexColor(TypeDecorator):
    impl = String
    def process_bind_param(self, value, dialect):
        if value and not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value):
            raise ValueError("Invalid hex color")
        return value


class Base(AsyncAttrs, DeclarativeBase):
    pass

class Moder(Base):
    __tablename__ = 'moders'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

class Quiz(Base):
    __tablename__ = 'quizs'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

class Question(Base):
    __tablename__ = 'questions'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    quiz_id: Mapped[int] = mapped_column(ForeignKey('quizs.id'))
    quiz = relationship('Quiz', backref='questions')

class Answer(Base):
    __tablename__ = 'answers'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    color: Mapped[str] = mapped_column(HexColor()) # мб ошибка
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    question = relationship('Question', backref='answers')
    
# class User(Base):
#     __tablename__ = "users"
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]

class Cube(Base):
    __tablename__ = "cubes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=True)
    connected_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(HexColor())
    
async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# asyncio.run(create_all_tables())