from create_bot import Session
from db_handler.models import Moder, Quiz, Question, Answer
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import datetime

# ----админские

async def add_moder(name) -> None:
    async with Session() as session:
        async with session.begin():
            session.add(Moder(name=name))

async def get_moders():
    session = Session()
    try:
        async with session:
            result = await session.scalars(select(Moder))
            return [moder.name for moder in result]
    finally:
        await session.close()

async def del_moder(name):
    session = Session()
    try:
        async with session:
            moder = (await session.scalars(select(Moder).where(Moder.name == name))).first()
            if moder:
                await session.delete(moder)
                await session.commit()
    finally:
        await session.close()


# -----модерские

async def get_quizs():
    async with Session() as session:
        result = await session.scalars(select(Quiz))
        await session.close()
        return result.all()

async def get_quiz(name: str) -> Quiz:
    async with Session() as session:
        quiz_obj = await session.scalars(select(Quiz).where(Quiz.name == name))
        await session.close()
        return quiz_obj.first()

async def add_quiz(name: str) -> None:
    async with Session() as session:
        async with session.begin():
            quiz_obj = Quiz(name=name, start_datetime=datetime.datetime.utcnow())
            session.add(quiz_obj)

async def del_quiz(quiz_obj: Quiz) -> None:
    async with Session() as session:
        async with session.begin():
            await session.delete(quiz_obj)

async def add_question(time: str, question: str, quiz_obj: Quiz) -> Question:
    async with Session() as session:
        async with session.begin():
            time_limit_minutes, time_limit_seconds = map(int, time.split(':'))
            question_obj = Question(text=question, quiz=quiz_obj, time_limit_seconds=time_limit_minutes * 60 + time_limit_seconds)
            session.add(question_obj)
            question_obj = await session.execute(select(Question).where(Question.quiz == quiz_obj, Question.text == question))
            return question_obj.scalars().first()

async def add_answ(col: str, answer: str, question_obj: Question):
    async with Session() as session:
        async with session.begin():
            answer_obj = Answer(text=answer, question=question_obj, color=col)
            session.add(answer_obj)

async def get_questions(quiz_obj: Quiz):
    async with Session() as session:
        result = await session.execute(select(Question).where(Question.quiz == quiz_obj).order_by(id))
        session.close()
        return result.scalars().all()

async def del_question(question_obj: Question):
    async with Session() as session:
        async with session.begin():
            await session.delete(question_obj)

async def get_answers(question_obj: Question):
    async with Session() as session:
        answer_list = await session.execute(select(Answer).where(Answer.question == question_obj))
        session.close()
        return answer_list.scalars().all()

async def set_quiz_time(time: str, quiz:Quiz):
    time = datetime.datetime.strptime(time, "%d.%m.%Y %H:%M:%S")
    async with Session() as session:
        async with session.begin():
            quiz_obj.time = time

# юзерские

async def get_cubes():
    async with Session() as session:
        cubes_list = await session.execute(select(Cubes))
        session.close()
        return cubes_list.scalars().all()
        
async def add_user_to_cube(id, cube):
    pass