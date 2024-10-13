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
    session = Session()
    try:
        async with session:
            result = await session.scalars(select(Quiz))
            return [quiz.name for quiz in result]
    finally:
        await session.close()


async def add_quiz(quiz):
    async with Session() as session:
        async with session.begin():
            quiz_obj = Quiz(name=quiz)
            session.add(quiz_obj)
            await session.commit()

async def del_quiz(quiz):
    session = Session()
    try:
        async with session:
            quiz_obj = (await session.scalars(select(Quiz).where(Quiz.name == quiz))).first()
            if quiz_obj:
                await session.delete(quiz_obj)
                await session.commit()
    finally:
        await session.close()

async def add_question(time, question, quiz):
    async with Session() as session:
        quiz_obj = (await session.scalars(select(Quiz).where(Quiz.name == quiz))).first()
        if quiz_obj:
            time_limit_minutes, time_limit_seconds = map(int, time.split(':'))
            question_obj = Question(text=question, quiz=quiz_obj, time_limit_seconds=time_limit_minutes * 60 + time_limit_seconds)
            session.add(question_obj)
            await session.commit()

# async def add_question_time(time, question, quiz):
#     async with Session() as session:
#         quiz_obj = await session.scalars(Quiz.select().where(Quiz.name == quiz)).first()
#         if quiz_obj:
#             question_obj = await session.scalars(Question.select().where(Question.text == question)).first()
#             if question_obj:
#                 question_obj.time = time
#                 await session.commit()

async def add_answ(col, answer, question, quiz):
    async with Session() as session:
        quiz_obj = (await session.scalars(select(Quiz).where(Quiz.name == quiz))).first()
        if quiz_obj:
            question_obj = (await session.scalars(select(Question).where(Question.text == question, Question.quiz == quiz_obj))).first()
            if question_obj:
                answer_obj = Answer(text=answer, question=question_obj, color=col)
                session.add(answer_obj)
                await session.commit()

# async def add_answ_col(color, answer, question, quiz):
#     async with Session() as session:
#         quiz_obj = await session.scalars(Quiz.select().where(Quiz.name == quiz)).first()
#         if quiz_obj:
#             question_obj = await session.scalars(Question.select().where(Question.text == question, Question.quiz == quiz_obj)).first()
#             if question_obj:
#                 answer_obj = await session.scalars(Answer.select().where(Answer.text == answer, Answer.question == question_obj)).first()
#                 if answer_obj:
#                     answer_obj.color = color
#                     await session.commit()

async def get_questions(quiz):
    async with Session() as session:
        quiz_obj = (await session.scalars(select(Quiz).where(Quiz.name == quiz))).subquery()
        quests_list = await session.scalars(Question.quiz_id.in_(quiz_obj))
        return [question.text for question in quests_list]

async def del_question(question, quiz):
    async with Session() as session:
        quiz_obj = (await session.scalars(select(Quiz).where(Quiz.name == quiz))).first()
        if quiz_obj:
            question_obj = (await session.scalars(select(Question).where(Question.text == question, Question.quiz == quiz_obj))).first()
            if question_obj:
                await session.delete(question_obj)
                await session.commit()

async def set_quiz_time(time, quiz):
    async with Session() as session:
        quiz_obj = (await session.scalars(select(Quiz).where(Quiz.name == quiz))).first()
        if quiz_obj:
            quiz_obj.time = time
            await session.commit()

async def get_quiz_time(quiz):
    async with Session() as session:
        quiz_obj = (await session.scalars(select(Quiz).where(Quiz.name == quiz))).first()
        if quiz_obj:
            return 'время квиза тип'
            # return quiz_obj.start_datetime

# юзерские

async def add_user_to_cube(id, cube):
    pass