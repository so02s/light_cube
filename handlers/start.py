from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommandScopeChat
from aiogram.utils.deep_linking import decode_payload

from utils.filter import admins, moders
import keyboards.all_keyboards as kb
from create_bot import bot

router = Router()

# Старт для админа
@router.message(F.from_user.id.in_(admins) & F.text, Command("start"))
async def cmd_start_adm(message: Message):
    await bot.set_my_commands(kb.commands_admin(), BotCommandScopeChat(chat_id=message.from_user.id))
    await message.answer('Привет админ! Открой меню для взаимодействия с ботом. Там есть все команды')

# Старт для модератора
@router.message(F.from_user.id.in_(moders) & F.text, Command("start"))
async def cmd_start_mod(message: Message):
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=message.from_user.id))
    await message.answer('Привет!\nВы - модератор! Вы можете открыть меню с доступными вам командами.')

# Старт для QR
@router.message(CommandStart(deep_link=True))
async def cmd_start(message: Message):
    args = message.get_args()
    reference = decode_payload(args)
    # await add_user_to_cube(message.from_user.id, reference)
    await message.answer(f"Добро пожаловать на квиз!")