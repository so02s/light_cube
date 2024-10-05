from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, BotCommandScopeChat

from create_bot import admins, moders, bot
import keyboards.all_keyboards as kb

start_router = Router()

# Старт для админа
@start_router.message(F.from_user.id.in_(admins) & F.text, Command("start"))
async def cmd_start(message: Message):
    await bot.set_my_commands(kb.commands_admin(), BotCommandScopeChat(chat_id=message.from_user.id))
    await message.answer(f'Запуск сообщения по команде /start используя фильтр CommandStart(), твой id = {message.from_user.id}')

# Старт для модератора
@start_router.message(F.from_user.id.in_(moders) & F.text, Command("start"))
async def cmd_start(message: Message):
    await message.answer(f'Привет!')

# Старт для QR
