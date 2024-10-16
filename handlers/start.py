from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommandScopeChat
from aiogram.utils.deep_linking import decode_payload

from utils.filter import is_admin, is_moder
import keyboards.all_keyboards as kb
from create_bot import bot
import db_handler.db

router = Router()

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
async def cmd_start(msg: Message):
    args = msg.get_args()
    reference = decode_payload(args)
    cube_id = int(reference.split('_')[-1])
    # TODO проверка на есть пользователь у куба - стоит ли
    try:
        await db.add_user_to_cube(cube_id, msg.from_user.username, msg.from_user.id, reference)
        await msg.answer(f"Добро пожаловать на квиз!")
    except:
        pass
    
# TODO 
# @router.message(lambda msg: msg.from_user.username in users(), CommandStart())
# async def cmd_start(msg: Message):
# #     # args = msg.get_args()
# #     # reference = decode_payload(args)
# #     # await add_user_to_cube(msg.from_user.id, reference)
#     await msg.answer(f"Привет, {msg.from_user.username}")