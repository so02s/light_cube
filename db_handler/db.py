from create_bot import Session
from db_handler.models import Moder, Quiz, Question, Answer, Cube, Testing
from sqlalchemy import select, func, update
import datetime

# ----админские

async def add_moder(name) -> None:
    async with Session() as session, session.begin():
        session.add(Moder(name=name))

async def get_moders():
    async with Session() as session:
        result = await session.scalars(select(Moder))
        return [moder.name for moder in result]

async def del_moder(name):
    async with Session() as session, session.begin():
        moder = (await session.scalars(
                    select(Moder)
                    .where(Moder.name == name))
                    ).first()
        if moder:
            await session.delete(moder)

# -----модерские

async def get_quizs():
    async with Session() as session:
        result = await session.scalars(select(Quiz))
        return result.all()

async def get_quiz(name: str) -> Quiz:
    async with Session() as session:
        quiz_obj = await session.scalars(select(Quiz)
                                         .where(Quiz.name == name))
        return quiz_obj.first()

async def add_quiz(name: str, time: str = '01.01.2026 00:00') -> None:
    start_datetime = datetime.datetime.strptime(time, '%d.%m.%Y %H:%M')
    async with Session() as session, session.begin():
        quiz_obj = Quiz(name=name,
                        start_datetime=start_datetime)
        session.add(quiz_obj)

async def del_quiz(quiz_obj: Quiz) -> None:
    async with Session() as session, session.begin():
        await session.delete(quiz_obj)

async def add_question(time: str, question: str, quiz_obj: Quiz) -> Question:
    async with Session() as session, session.begin():
        time_limit_minutes, time_limit_seconds = map(int, time.split(':'))
        max_question_number = await session.execute(
            select(func.max(Question.question_number))
            .where(Question.quiz == quiz_obj)
        )
        max_question_number = max_question_number.scalar() or 0
        question_obj = Question(
            text=question,
            quiz=quiz_obj,
            time_limit_seconds=time_limit_minutes * 60 + time_limit_seconds,
            question_number=max_question_number + 1
        )
        session.add(question_obj)
        question_obj = await session.execute(
            select(Question)
            .where(
                Question.quiz == quiz_obj,
                Question.text == question)
        )
        return question_obj.scalars().first()

async def add_answ(col: str, answer: str, is_correct: bool, question_obj: Question) -> Answer:
    async with Session() as session, session.begin():
        answer_obj = Answer(
            text=answer,
            question=question_obj,
            color=col,
            is_correct=is_correct
        )
        session.add(answer_obj)
        question_obj = await session.execute(
            select(Answer)
            .where(
                Answer.question == question_obj,
                Answer.text == answer
            )
        )
        return question_obj.scalars().first()

async def get_questions(quiz_obj: Quiz):
    async with Session() as session:
        result = await session.execute(
            select(Question)
            .where(Question.quiz == quiz_obj)
            .order_by(Question.question_number)
        )
        return result.scalars().all()

async def update_question_time(question_obj: Question, time: int) -> None:
    async with Session() as session, session.begin():
        await session.execute(
            update(Question)
            .where(Question.id == question_obj.id)
            .values({'time_limit_seconds': time})
        )

async def del_question(question_obj: Question) -> None:
    async with Session() as session, session.begin():
        await session.delete(question_obj)

async def get_answers(question_obj: Question):
    async with Session() as session:
        answer_list = await session.execute(
            select(Answer)
            .where(Answer.question == question_obj)
        )
        return answer_list.scalars().all()

async def set_quiz_time(time: str, quiz_obj: Quiz) -> Quiz:
    time = datetime.datetime.strptime(time, "%d.%m.%Y %H:%M:%S")
    async with Session() as session, session.begin():
        await session.execute(
            update(Quiz)
            .where(Quiz.id == quiz_obj.id)
            .values({'start_datetime': time})
        )
            
async def get_users_answ(question_obj: Question):
    async with Session() as session:
        answer_list = await session.execute(
            select(Testing)
            .where(Testing.question == question_obj)
        )
        return answer_list.scalars().all()

# юзерские

async def is_cube_empty(cube_id) -> bool:
    async with Session() as session:
        result = await session.execute(
            select(Cube)
            .filter(
                Cube.id == cube_id,
                Cube.user_id.isnot(None)
            )
        )
        return result.scalars().first() is None

async def get_cubes():
    async with Session() as session:
        cubes_list = await session.execute(select(Cube))
        return cubes_list.scalars().all()
        
async def add_user_to_cube(cube_id, username, user_id, connected_at, color='#808080') -> None:
    async with Session() as session, session.begin():
        cube_obj = Cube(
            id=cube_id,
            username=username,
            user_id=user_id,
            connected_at=connected_at,
            status=color
        )
        session.add(cube_obj)

async def add_user_answ(cube_id, question_obj: Question, answer_obj: Answer) -> None:
    async with Session() as session, session.begin():
        testing_obj = Testing(
            cube_id=cube_id,
            question_id=question_obj.id,
            answer_id=answer_obj.id,
            time_add_answer=datetime.datetime.utcnow()
        )
        session.add(testing_obj)
        
            
async def get_user_answ(cube_id, current_question: Question):
    async with Session() as session:
        result = await session.execute(
            select(Testing)
            .where(
                Testing.cube_id == cube_id,
                Testing.question_id == current_question.id
            )
        )
        return result.scalars().first()