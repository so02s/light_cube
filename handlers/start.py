from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, BotCommandScopeChat
from aiogram.utils.deep_linking import decode_payload
import datetime

from utils.filter import is_admin, is_moder
import keyboards.all_keyboards as kb
from create_bot import bot
from db_handler import db
from handlers.quiz_handler import QuizMiddleware

router = Router()
router.message.middleware(QuizMiddleware())

# Старт для админа
@router.message(is_admin, Command("start"))
async def cmd_start_adm(msg: Message):
    await bot.set_my_commands(kb.commands_admin(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await msg.answer('Привет админ! Открой меню для взаимодействия с ботом. Там есть все команды')

# Старт для модератора
@router.message(is_moder, Command("start"))
async def cmd_start_mod(msg: Message):
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await msg.answer('Привет!\nВы - модератор! Вы можете открыть меню с доступными вам командами.')

# Старт для QR
@router.message(CommandStart(deep_link=True))
async def cmd_start(msg: Message, command: CommandObject):
    args = command.args
    reference = decode_payload(args)
    cube_id = int(reference.split('_')[-1])
    
    if await db.is_cube_empty(cube_id):
        try:
            connected_at = datetime.datetime.now()
            await db.add_user_to_cube(cube_id, msg.from_user.username, msg.from_user.id, connected_at)
            await msg.answer("Добро пожаловать на квиз!")
        except Exception as e:
            await msg.answer("Произошла ошибка при подключении к кубу.")
            print(e)
    else:
        await msg.answer("Куб уже занят другим пользователем.")
    
@router.message(CommandStart())
async def cmd_start():
    pass