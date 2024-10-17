import aioschedule
from db_handler import db
from db_handler.models import Quiz
from aiogram.types import Message
from create_bot import bot
import asyncio

current_question = None


async def handle_user_response(message: Message):
    """
    Handles user responses to quiz questions
    """
    
    cube_id = message.from_user.id

    global current_question
    answers = await db.get_answers(current_question)
    user_response = message.text
    
    # TODO проверка ответа по индексу
    
    for i, answer in enumerate(answers):
        if user_response == f"{i+1}. {answer.text}" or user_response == answer.text:
            await db.update_quiz_state(cube_id, current_question, True)
            await bot.send_message(cube_id, "Correct!")
            break
    else:
        # User's response is incorrect, update the quiz state
        await db.update_quiz_state(cube_id, current_question, False)
        await bot.send_message(cube_id, "Incorrect. Try again!")

    # Check if the quiz is complete
    if await db.is_quiz_complete(cube_id):
        await bot.send_message(cube_id, "Quiz complete! Your score is ...")
        # Calculate and send the user's final score
        score = await db.get_quiz_score(cube_id)
        await bot.send_message(cube_id, f"Your score is {score} out of {len(questions)}")



async def start_quiz(quiz_obj: Quiz):
    cubes = await db.get_cubes()
    questions = await db.get_questions(quiz_obj)

    for question in questions:
        global current_question
        current_question = question
        answers = await db.get_answers(question)
        for cube in cubes:
            await bot.send_message(cube.user_id, question.text)
            for i, answer in enumerate(answers):
                await bot.send_message(cube.user_id, f"{i+1}. {answer.text}")
                
        await asyncio.sleep(question.time_limit_seconds)
