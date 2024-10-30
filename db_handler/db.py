from create_bot import Session
from db_handler.models import Moder, Quiz, Question, Answer, Cube, Testing
from sqlalchemy import select, func, update, case
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

async def top_ten(quiz_id: int):
    async with Session() as session:
        query = (
            select(
                Cube.username,
                UserTesting.cube_id,
                func.count(UserTesting.id).label('correct_count'),
                func.min(UserTesting.time_add_answer).label('fastest_time')
            )
            .join(UserTesting, UserTesting.cube_id == Cube.id)
            .join(Answer, UserTesting.answer_id == Answer.id)
            .filter(Answer.is_correct == True, UserTesting.quiz_id == quiz_id)  # Filter by quiz_id
            .group_by(Cube.username, UserTesting.cube_id)
            .order_by(desc('correct_count'), 'fastest_time')
            .limit(10)  
        )
        
        result = await session.execute(query)
        
        return result.all()

async def get_quizs():
    async with Session() as session:
        result = await session.scalars(select(Quiz))
        return result.all()

async def get_quiz(name: str) -> Quiz:
    async with Session() as session:
        quiz_obj = await session.scalars(select(Quiz)
                                         .where(Quiz.name == name))
        return quiz_obj.first()

async def get_quiz_by_id(quiz_id: int) -> Quiz:
    async with Session() as session:
        quiz_obj = await session.scalars(select(Quiz)
                                         .where(Quiz.id == quiz_id))
        return quiz_obj.first()

# возвращает id добавленного квиза
async def add_quiz(name: str, time: str = '01.01.2026 00:00') -> int:
    start_datetime = datetime.datetime.strptime(time, '%d.%m.%Y %H:%M')
    async with Session() as session, session.begin():
        quiz_obj = Quiz(name=name,
                        start_datetime=start_datetime)
        session.add(quiz_obj)
        quiz_obj = await session.execute(
            select(Quiz)
            .where(
                Quiz.name == name,
                Quiz.start_datetime == start_datetime
            )
        )
        return (quiz_obj.scalars().first()).id

async def del_quiz(quiz_obj: Quiz) -> None:
    async with Session() as session, session.begin():
        await session.delete(quiz_obj)
        
async def del_quiz_by_id(quiz_id: int) -> None:
    async with Session() as session, session.begin():
        quiz_obj = (await session.scalars(select(Quiz)
                                         .where(Quiz.id == quiz_id))).first()
        await session.delete(quiz_obj)

# возвращает id добавленного вопроса
async def add_question(question: str, quiz_id: int, time=0) -> int:
    async with Session() as session, session.begin():
        max_question_number = await session.execute(
            select(func.max(Question.question_number))
            .where(Question.quiz_id == quiz_id)
        )
        max_question_number = max_question_number.scalar() or 0
        question_obj = Question(
            text=question,
            quiz_id=quiz_id,
            time_limit_seconds=time,
            question_number=max_question_number + 1
        )
        session.add(question_obj)
        question_obj = await session.execute(
            select(Question)
            .where(
                Question.quiz_id == quiz_id,
                Question.text == question
            )
        )
        return (question_obj.scalars().first()).id

# возвращает id добавленного ответа
async def add_answ(answer: str, question_id: int, is_correct=False, col='#FF0000') -> int:
    async with Session() as session, session.begin():
        answer_obj = Answer(
            text=answer,
            question_id=question_id,
            color=col,
            is_correct=is_correct
        )
        session.add(answer_obj)
        question_obj = await session.execute(
            select(Answer)
            .where(
                Answer.question_id == question_id,
                Answer.text == answer
            )
        )
        return (question_obj.scalars().first()).id

async def get_questions(quiz_obj: Quiz):
    async with Session() as session:
        result = await session.execute(
            select(Question)
            .where(Question.quiz == quiz_obj)
            .order_by(Question.question_number)
        )
        return result.scalars().all()

async def get_questions_by_id(quiz_id: int):
    async with Session() as session:
        result = await session.execute(
            select(Question)
            .where(Question.quiz_id == quiz_id)
            .order_by(Question.question_number)
        )
        return result.scalars().all()

async def get_question_by_id(question_id: int) -> Question:
    async with Session() as session:
        result = await session.execute(
            select(Question)
            .where(Question.id == question_id)
        )
        return result.scalars().first()

async def get_answer_by_id(answer_id: int) -> Answer:
    async with Session() as session:
        result = await session.execute(
            select(Answer)
            .where(Answer.id == answer_id)
        )
        return result.scalars().first()

async def update_question_time(question_id: int, time: int) -> None:
    async with Session() as session, session.begin():
        await session.execute(
            update(Question)
            .where(Question.id == question_id)
            .values({'time_limit_seconds': time})
        )

async def update_question_text(question_id: int, text: str) -> None:
    async with Session() as session, session.begin():
        await session.execute(
            update(Question)
            .where(Question.id == question_id)
            .values({'text': text})
        )

async def update_answer_text(answer_id: int, text: str) -> None:
    async with Session() as session, session.begin():
        await session.execute(
            update(Answer)
            .where(Answer.id == answer_id)
            .values({'text': text})
        )

async def update_answer_color(answer_id: int, color: str) -> None:
    async with Session() as session, session.begin():
        await session.execute(
            update(Answer)
            .where(Answer.id == answer_id)
            .values({'color': color})
        )

async def update_answer_cor(answer_id: int) -> None:
    async with Session() as session, session.begin():
        result = await session.execute(
            select(Answer)
            .where(Answer.id == answer_id)
        )
        answer = result.scalar_one_or_none()
        if answer is not None:
            answer.is_correct = not answer.is_correct
            session.add(answer)

async def del_question(question_obj: Question) -> None:
    async with Session() as session, session.begin():
        await session.delete(question_obj)

async def del_answer(answer_obj: Answer) -> None:
    async with Session() as session, session.begin():
        await session.delete(answer_obj)

async def get_answers(question_obj: Question):
    async with Session() as session:
        answer_list = await session.execute(
            select(Answer)
            .where(Answer.question == question_obj)
            .order_by(Answer.id)
        )
        return answer_list.scalars().all()

async def get_answers_by_id(question_id: int):
    async with Session() as session:
        answer_list = await session.execute(
            select(Answer)
            .where(Answer.question_id == question_id)
            .order_by(Answer.id)
        )
        return answer_list.scalars().all()

async def set_quiz_time(time: str, quiz_id: int) -> None:
    time = datetime.datetime.strptime(time, "%d.%m.%Y %H:%M")
    async with Session() as session, session.begin():
        await session.execute(
            update(Quiz)
            .where(Quiz.id == quiz_id)
            .values({'start_datetime': time})
        )
            
async def get_users_answ(question_obj: Question):
    async with Session() as session:
        answer_list = await session.execute(
            select(Testing)
            .where(Testing.question == question_obj)
        )
        return answer_list.scalars().all()

async def shuffle_quest(question_id: int, shuffle_to: int) -> None:
    async with Session() as session, session.begin():
        # Получаем текущий вопрос и его номер
        result = await session.execute(
            select(Question)
            .where(Question.id == question_id)
        )
        question = result.scalar_one_or_none()

        if question is None:
            return

        current_number = question.question_number

        if current_number == shuffle_to:
            return

        # Перемещаем все вопросы между current_number и shuffle_to
        if current_number < shuffle_to:
            # Сдвиг вопросов вниз
            await session.execute(
                update(Question)
                .where(Question.quiz_id == question.quiz_id,
                        Question.question_number > current_number,
                        Question.question_number <= shuffle_to)
                .values(question_number=case(
                        {Question.question_number: None}, 
                        else_=Question.question_number - 1
                    ))
            )
        else:
            # Сдвиг вопросов вверх
            await session.execute(
                update(Question)
                .where(Question.quiz_id == question.quiz_id,
                        Question.question_number >= shuffle_to,
                        Question.question_number < current_number)
                .values(question_number==case(
                        {Question.question_number: None}, 
                        else_=Question.question_number + 1
                    ))
            )

        # Обновляем номер текущего вопроса
        question.question_number = shuffle_to
        session.add(question)  # Добавляем вопрос обратно в сессию для обновления



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
        
async def add_user_to_cube(cube_id, username, user_id, connected_at, color='#808080') -> bool:
    async with Session() as session, session.begin():
        stmt = select(Cube).where(Cube.user_id == user_id, Cube.id == cube_id)
        result = await session.execute(stmt)
        existing_cube = result.scalars().first()

        if existing_cube:
            time_difference = connected_at - existing_cube.connected_at
            if time_difference.total_seconds() <= 15 * 60:
                return False
            existing_cube.username = username
            existing_cube.connected_at = connected_at
            existing_cube.status = color
        else:
            cube_obj = Cube(
                id=cube_id,
                username=username,
                user_id=user_id,
                connected_at=connected_at,
                status=color
            )
            session.add(cube_obj)
        return True

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