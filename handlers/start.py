from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from filters.is_admin import IsAdmin
from create_bot import admins

start_router = Router()

# проверка на бан

# Старт для админа
@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()')

# Старт для модератора

# Старт для QR

# Все остальные отправляются в бан