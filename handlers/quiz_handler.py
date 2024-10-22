import aioschedule
from db_handler import db
from db_handler.models import Quiz
from aiogram.types import Message
from aiogram import Router, BaseMiddleware
from aiogram.filters import StateFilter, Command
from create_bot import bot
import asyncio
import mqtt.mqtt_handler as mqtt
from utils.filter import is_admin_or_moder, is_quiz_user

quiz_active = False
current_question = None

class QuizMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if quiz_active:
            await event.answer("Сейчас идет квиз")
            # await event.answer("Вы можете его остановить на /stop_quiz")
            return
        return await handler(event, data)

class QuizMiddlewareAnsware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if not quiz_active:
            # await event.answer("Квиз еще не начался")
            return
        return await handler(event, data)
    
router = Router()

router.message.middleware(QuizMiddlewareAnsware())

# TODO как остановить квиз
@router.message(is_admin_or_moder, StateFilter(None), Command("stop_quiz"))
async def handle_stop(message: Message):
    pass


@router.message(is_quiz_user, StateFilter(None))
async def handle_user_response(message: Message):
    cube_id = message.from_user.id
    
    global current_question
    answers = await db.get_answers(current_question)
    
    # Проверка на давал ответ или нет
    
    # Если да, остановить выполнение хэндлера
    
    try:
        index_answ = int(message.text)
        if 0 <= index_answ < len(answers):
            user_answer = answers[index_answ]
            await db.add_user_answ(cube_id, current_question, user_answer)
            await bot.send_message(cube_id, f"Вы ответили:\n{user_answer.text}\nСкоро выведут правильные ответы, подождите")
        else:
            await bot.send_message(cube_id, "Пожалуйста, напишите номер ответа")
    except ValueError:
        await bot.send_message(cube_id, "Пожалуйста, напишите номер ответа")
    except Exception as e:
        await bot.send_message(cube_id, f"Что-то пошло не так. Error: {e}")


async def start_quiz(quiz_obj: Quiz):
    cubes = await db.get_cubes()
    questions = await db.get_questions(quiz_obj)
    
    global quiz_active
    quiz_active = True

    for question in questions:
        global current_question
        current_question = question
        answers = await db.get_answers(question)
        
        text = question.text + '\n\n'
        for i, answer in enumerate(answers):
            text += f"{i+1}. {answer.text}\n"
            
        for cube in cubes:
            await bot.send_message(cube.user_id, text)
        
        correct_answers = [id for id, answer in enumerate(answers) if answer.is_correct]
        poll_options = [answer.text for answer in answers]
        type_poll = 'regular'
        if len(correct_answers) == 1:
            type_poll = 'quiz'
            
        await bot.send_poll(
            chat_id=-1002481450341,
            question=question.text,
            options=[answer.text for answer in answers],
            is_anonymous=True,
            type=type_poll,
            correct_option_id=correct_answers[0],
            disable_notification=False
        )
        
        await asyncio.sleep(question.time_limit_seconds)
        
        cube_answers = await db.get_users_answ(current_question)
        try:
            for cube in cubes:
                await mqtt.cube_publish_by_id(cube.id, '#808080')
            
            for cube_answer in cube_answers:
                # TODO Может быть ошибка в обращении к объекту, проверить
                await mqtt.cube_publish_by_id(cube_answer.cube_id, cube_answer.cube_id.status)
            
            await mqtt.cube_on()
            await asyncio.sleep(10)
            await mqtt.cube_off()
        except:
            print('Welp, MQTT not connect to bot')
    
    quiz_active = False
    # TODO возможно вывод в канал результата сидящих в зале?
    # Либо конкретному модератору
