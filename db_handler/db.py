from create_bot import Session
from db_handler.models import Moder, Quiz, Question, Answer
from sqlalchemy import select

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
    async with Session() as session:
        moder = (await session.scalars(select(Moder).where(Moder.name == name))).first()
        if moder:
            await session.delete(moder)
            await session.commit()


# -----модерские

async def get_quizs():
    session = Session()
    try:
        async with session:
            result = await session.scalars(select(Quiz))
            return [quiz.name for quiz in result]
    finally:
        await session.close()

async def add_quiz(quiz):
    async with Session() as session:
        quiz_obj = Quiz(name=quiz)
        session.add(quiz_obj)
        await session.commit()

async def del_quiz(quiz):
    async with Session() as session:
        quiz_obj = await session.scalars(Quiz.select().where(Quiz.name == quiz)).first()
        if quiz_obj:
            await session.delete(quiz_obj)
            await session.commit()

async def add_question(question, quiz):
    async with Session() as session:
        quiz_obj = await session.scalars(Quiz.select().where(Quiz.name == quiz)).first()
        if quiz_obj:
            question_obj = Question(text=question, quiz=quiz_obj)
            session.add(question_obj)
            await session.commit()

async def add_question_time(time, question, quiz):
    async with Session() as session:
        quiz_obj = await session.scalars(Quiz.select().where(Quiz.name == quiz)).first()
        if quiz_obj:
            question_obj = await session.scalars(Question.select().where(Question.text == question)).first()
            if question_obj:
                question_obj.time = time
                await session.commit()

async def add_answ(answer, question, quiz):
    async with Session() as session:
        quiz_obj = await session.scalars(Quiz.select().where(Quiz.name == quiz)).first()
        if quiz_obj:
            question_obj = await session.scalars(Question.select().where(Question.text == question, Question.quiz == quiz_obj)).first()
            if question_obj:
                answer_obj = Answer(text=answer, question=question_obj)
                session.add(answer_obj)
                await session.commit()

async def add_answ_col(color, answer, question, quiz):
    async with Session() as session:
        quiz_obj = await session.scalars(Quiz.select().where(Quiz.name == quiz)).first()
        if quiz_obj:
            question_obj = await session.scalars(Question.select().where(Question.text == question, Question.quiz == quiz_obj)).first()
            if question_obj:
                answer_obj = await session.scalars(Answer.select().where(Answer.text == answer, Answer.question == question_obj)).first()
                if answer_obj:
                    answer_obj.color = color
                    await session.commit()

async def get_question(quiz):
    async with Session() as session:
        quiz_obj = await session.scalars(Quiz.select().where(Quiz.name == quiz)).first()
        if quiz_obj:
            return [question.text async for question in session.scalars(Question.select().where(Question.quiz == quiz_obj))]

async def del_question(question, quiz):
    async with Session() as session:
        quiz_obj = await session.scalars(Quiz.select ().where(Quiz.name == quiz)).first()
        if quiz_obj:
            question_obj = await session.scalars(Question.select().where(Question.text == question, Question.quiz == quiz_obj)).first()
            if question_obj:
                await session.delete(question_obj)
                await session.commit()

async def set_quiz_time(time, quiz):
    async with Session() as session:
        quiz_obj = await session.scalars(Quiz.select().where(Quiz.name == quiz)).first()
        if quiz_obj:
            quiz_obj.time = time
            await session.commit()
            

# юзерские

async def add_user_to_cube(id, cube):
    pass