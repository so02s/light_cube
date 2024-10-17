from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime, TypeDecorator, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
import datetime
import asyncio
from create_bot import engine, Session

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
    start_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

class Question(Base):
    __tablename__ = 'questions'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    time_limit_seconds: Mapped[int] = mapped_column()
    quiz_id: Mapped[int] = mapped_column(ForeignKey('quizs.id'))
    
    quiz = relationship('Quiz', backref=backref('questions', cascade="all,delete"))

    @property
    def time_limit(self):
        minutes, seconds = divmod(self.time_limit_seconds, 60)
        return minutes * 60 + seconds

class Answer(Base):
    __tablename__ = 'answers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    color: Mapped[str]
    is_correct: Mapped[bool]
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    question = relationship('Question', backref=backref('answers', cascade="all,delete"))

class Cube(Base):
    __tablename__ = "cubes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(nullable=True)
    connected_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column()


class Testing(Base):
    __tablename__ = "testing"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    cube_id: Mapped[int] = mapped_column(ForeignKey('cubes.id'))
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    answer_id: Mapped[int] = mapped_column(ForeignKey('answers.id'))
    time_add_answer: Mapped[datetime.datetime] = mapped_column(DateTime)

    cube = relationship('Cube', backref='testings')
    question = relationship('Question', backref='testings')
    answer = relationship('Answer', backref='testings')

    @property
    def is_correct(self):
        return self.answer.is_correct

async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)