import aioschedule
from db_handler import db
from db_handler.models import Quiz
from create_bot import bot

async def start_quiz(quiz_obj: Quiz):
    cubes = await db.get_cubes()
    questions = await db.get_questions(quiz_obj)
    time_list = [quest.time_limit_seconds for quest in questions]

    for question in questions:
        answers = db.get_answers(question)
        for cube in cubes:
            await bot.send_message(cube.user_id, question.text)
            for i, answer in enumerate(answers):
                await bot.send_message(cube.user_id, f"{i+1}. {answer.text}")
                
        await asyncio.sleep(time_list[i])
