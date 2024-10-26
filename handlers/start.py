from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, BotCommandScopeChat
from aiogram.types.input_file import FSInputFile
from aiogram.utils.deep_linking import decode_payload
import datetime

from utils.filter import is_admin, is_moder # PayloadFilter, CubePayloadFilter
import keyboards.all_keyboards as kb
from create_bot import bot
from db_handler import db
from handlers.quiz_handler import QuizMiddleware

router = Router()
router.message.middleware(QuizMiddleware())

async def view_event_program(msg: Message):
    photo = FSInputFile("img/event_program.jpg")
    await bot.send_photo(chat_id=msg.chat.id, photo=photo)

# TODO Объяснение использования
async def user_register(msg: Message, cube_id: int):
    try:
        connected_at = datetime.datetime.now()
        await db.add_user_to_cube(cube_id, msg.from_user.username, msg.from_user.id, connected_at)
        await msg.answer("Добро пожаловать на квиз!")
    except Exception as e:
        await msg.answer("Произошла ошибка при подключении к кубу.")
        print(e)

# Старт для QR
@router.message(CommandStart(deep_link=True))
async def cmd_start(msg: Message, command: CommandObject):
    args = command.args
    reference = decode_payload(args)
    
    if(reference == 'program'):
        await view_event_program(msg)
        return
    
    try:
        cube_id = int(reference.split('_')[-1])
    except:
        return
    
    if await db.is_cube_empty(cube_id):
        await user_register(msg, cube_id)
    else:
        await msg.answer("Куб уже занят другим пользователем.")

# Старт для модератора
# TODO добавить удаление из проверки ответов квиза
@router.message(is_moder, Command("start"))
async def cmd_start_mod(msg: Message):
    msg_bot = await msg.answer("Привет, модератор!\n\nВыберите действие", reply_markup=kb.get_management_kb())
    await bot.delete_messages(msg.from_user.id, [msg_bot.message_id - i for i in range(2, 100)])