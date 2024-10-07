from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, BotCommandScopeChat

from create_bot import admins, moders, bot
import keyboards.all_keyboards as kb

moder_router = Router()

@moder_router.message((F.from_user.id.in_(admins) | F.from_user.id.in_(moders)) & F.text, \
    Command("add_quiz"))
async def cmd_start(message: Message):
    # TODO несколько настроек квиза -> добавление
    await message.answer('Добавлен квиз')

@moder_router.message((F.from_user.id.in_(admins) | F.from_user.id.in_(moders)) & F.text, \
    Command("del_quiz"))
async def cmd_start(message: Message):
    # TODO выбор квиза из списка существующих, двойное подтверждение
    await message.answer('Квиз удален')

@moder_router.message((F.from_user.id.in_(admins) | F.from_user.id.in_(moders)) & F.text, \
    Command("change_quiz"))
async def cmd_start(message: Message):
    # TODO выбор квиза, потом команд из списка
    await message.answer('Изменение принято')

@moder_router.message((F.from_user.id.in_(admins) | F.from_user.id.in_(moders)) & F.text, \
    Command("start_quiz"))
async def cmd_start(message: Message):
    # TODO запуск квиза при этой команде
    await message.answer('Квиз начат')

@moder_router.message(F.from_user.id.in_(moders) & F.text, Command("user"))
async def cmd_start(message: Message):
    await bot.set_my_commands(kb.commands_user(), BotCommandScopeChat(chat_id=message.from_user.id))
    await message.answer('Включен режим юзера. Для возвращения напишите /start')