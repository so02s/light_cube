import aioschedule
from db_handler import db
from db_handler.models import Quiz
from aiogram.types import Message, CallbackQuery
from aiogram import Router, BaseMiddleware
from aiogram.filters import StateFilter, Command
from create_bot import bot
import asyncio
import mqtt.mqtt_handler as mqtt
from utils.filter import is_moder
from keyboards import all_keyboards as kb
from keyboards.callback_handler import UserCallbackFactory

quiz_active = False
quiz_id = -1
current_question = None
    
router = Router()

@router.callback_query(UserCallbackFactory)
async def handle_user_answ(callback: CallbackQuery, callback_data: UserCallbackFactory):
    await db.add_user_answ(callback.message.chat.id, callback_data.answer_id)
    await callback.message.edit(text='Ответ принят')
    await callback.message.delete_reply_markup()


async def start_quiz(selected_quiz_id = None):
    global quiz_active, quiz_id, current_question
    
    if selected_quiz_id is None:
        if quiz_active:
            quiz_active = False
            return
        else:
            return
    
    cubes = await db.get_cubes()
    questions = await db.get_questions(quiz_obj)
    
    global quiz_active
    quiz_active = True

    for question in questions:
        global current_question
        current_question = question
        answers = await db.get_answers(question)
        
        # Отправка юзерам
        for cube in cubes:
            try:
                msg_bot = await bot.send_message(
                    cube.user_id,
                    question.text,
                    reply_markup=kb.reply_answers(answers)
                )
                await bot.delete_message(msg_bot.id - 1)
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
        
        # Вывод ответов на кубы
        cube_answers = await db.get_users_answ(current_question)
        try:
            for cube in cubes:
                await mqtt.cube_publish_by_id(cube.id, '#808080')
            
            for cube_answer in cube_answers:
                # TODO Может быть ошибка в обращении к объекту, проверить
                await mqtt.cube_publish_by_id(cube_answer.cube_id, cube_answer.cube_id.status)
            
            # Красиво посветились
            await mqtt.cube_on()
            await asyncio.sleep(30)
            await mqtt.cube_off()
        except:
            print('Welp, MQTT not connect to bot')
    
    quiz_active = False
    quiz_id = -1