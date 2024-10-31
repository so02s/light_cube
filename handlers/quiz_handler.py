import asyncio

import aioschedule
from aiogram import Router, BaseMiddleware
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, CallbackQuery
from create_bot import bot
from db_handler import db
from db_handler.models import Quiz
from keyboards import all_keyboards as kb
from keyboards.callback_handler import UserCallbackFactory
from mqtt import mqtt_handler as mqtt
from utils.filter import is_moder

quiz_active = False
quiz_id = -1
current_question = None

def is_quiz_active():
    global quiz_active
    return quiz_active

router = Router()

@router.callback_query(UserCallbackFactory.filter())
async def handle_user_answ(callback: CallbackQuery, callback_data: UserCallbackFactory):
    await callback.message.delete_reply_markup()
    await db.add_user_answ(
        cube_id=callback_data.cube_id,
        answer_id=callback_data.answer_id,
    )
    await callback.message.edit_text(text='Ответ принят')


async def start_quiz(selected_quiz_id = None):
    global quiz_active, quiz_id, current_question
    
    quiz_active = True
    quiz_id = selected_quiz_id
    
    await db.del_test_quiz(quiz_id)
    
    cubes = await db.get_cubes()
    questions = await db.get_questions_by_id(quiz_id)
    

    for question in questions:
        
        current_question = question
        answers = await db.get_answers(question)
        
        sent_messages = []
        # Отправка юзерам
        for cube in cubes:
            try:
                msg_bot = await bot.send_message(
                    cube.user_id,
                    question.text,
                    reply_markup=kb.reply_answers(cube.id, question.id, answers)
                )
                
                sent_messages.append((cube.user_id, msg_bot.message_id))
            except:
                pass
        
        # Отправка в канал
        correct_answers = [id for id, answer in enumerate(answers) if answer.is_correct]
        poll_options = [answer.text for answer in answers]
        type_poll = 'regular'
        if len(correct_answers) == 1:
            type_poll = 'quiz'
        
        poll_message = await bot.send_poll(
            chat_id=-1002481450341,
            question=question.text,
            options=[answer.text for answer in answers],
            is_anonymous=True,
            type=type_poll,
            correct_option_id=correct_answers[0],
            disable_notification=False
        )
        
        # Ждем окончания вопроса
        
        await asyncio.sleep(question.time_limit_seconds)
        
        # Остановка вопроса в канале
        try:
            await bot.stop_poll(chat_id=-1002481450341, message_id=poll_message.message_id)
        except:
            pass
        
        # Остановка вопросов в целом
        for user_id, message_id in sent_messages:
            try:
                await bot.delete_message(user_id, message_id)
            except:
                pass
        
        # Вывод ответов на кубы
        cube_answers = await db.get_users_answ(question.id)
        try:
            for cube in cubes:
                await mqtt.cube_publish_by_id(cube.id, '#808080')
            
            for cube_answer in cube_answers:
                await mqtt.cube_publish_by_id(cube_answer.cube_id, cube_answer.answer.color)
            
            # Красиво посветились
            await mqtt.cube_on()
            await asyncio.sleep(10)
            await mqtt.cube_off()
        except:
            print('Welp, MQTT not connect to bot')
    
    quiz_active = False
    wins = await db.win_users(quiz_id)
    # for win in wins:
        