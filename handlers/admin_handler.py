from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, BotCommandScopeChat

from create_bot import admins, bot
import keyboards.all_keyboards as kb
from mqtt.mqtt_handler import publish
import random

admin_router = Router()

@admin_router.message(F.from_user.id.in_(admins) & F.text, Command("add_moder"))
async def cmd_start(message: Message):
    await message.answer('Добавлен модератор')

@admin_router.message(F.from_user.id.in_(admins) & F.text, Command("moder"))
async def cmd_start(message: Message):
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=message.from_user.id))
    await message.answer('Включен режим модератора. Для возвращения напишите /start')

@admin_router.message(F.from_user.id.in_(admins) & F.text, Command("user"))
async def cmd_start(message: Message):
    await bot.set_my_commands(kb.commands_user(), BotCommandScopeChat(chat_id=message.from_user.id))
    await message.answer('Включен режим юзера. Для возвращения напишите /start')

@admin_router.message(F.from_user.id.in_(admins) & F.text, Command("on"))
async def cmd_start(message: Message):
    await publish("cubes", "ON")
    await publish("lamps", "ON")
    await message.answer('Все включено')
    
@admin_router.message(F.from_user.id.in_(admins) & F.text, Command("off"))
async def cmd_start(message: Message):
    await publish("cubes", "OFF")
    await publish("lamps", "OFF")
    await message.answer('Все выключено')
    
@admin_router.message(F.from_user.id.in_(admins) & F.text, Command("random"))
async def cmd_start(message: Message):
    r = lambda: random.randint(150,255)
    await publish("cubes/col", '#%02X%02X%02X' % (r(),r(),r()))
    await publish("lamps/col", '#%02X%02X%02X' % (r(),r(),r()))
    await message.answer('Цвет зарандомлен')