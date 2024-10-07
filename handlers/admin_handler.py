from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, BotCommandScopeChat

from aiogram.fsm.context import FSMContext
# from aiogram.contrib.fsm_storage.memory import MemoryStorage

from create_bot import admins, bot
import keyboards.all_keyboards as kb
from mqtt.mqtt_handler import wled_publish
from fms.admin_fms import Group
import random

admin_router = Router()

@admin_router.message(F.from_user.id.in_(admins), Command("add_moder"))
async def cmd_start(message: Message):
    # TODO добавление в бд модеров
    
    await message.answer('Добавлен модератор')



@admin_router.message(F.from_user.id.in_(admins), Command("moder"))
async def cmd_start(message: Message):
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=message.from_user.id))
    await message.answer('Включен режим модератора. Для возвращения напишите /start')

@admin_router.message(F.from_user.id.in_(admins), Command("user"))
async def cmd_start(message: Message):
    await bot.set_my_commands(kb.commands_user(), BotCommandScopeChat(chat_id=message.from_user.id))
    await message.answer('Включен режим юзера. Для возвращения напишите /start')


@admin_router.message(F.from_user.id.in_(admins), StateFilter(None), Command("on"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Введите название группы:')
    await state.set_state(Group.ch_group_name)
    # TODO написать название группы ламп
    # await wled_publish(topic, "ON")

@admin_router.message(Group.ch_group_name)
async def food_chosen(message: Message, state: FSMContext):
    # TODO проверка на существование группы
    if(message.text == 'all'):
        await wled_publish("cubes", "ON")
        await wled_publish("lamps", "ON")
        await message.answer(text=f"Отлично! Свет во всех группах включен.")
    else:
        await wled_publish(message.text, "ON")
        await message.answer(text=f"Отлично! Свет в группе {message.text} включен.")
    await state.clear()

@admin_router.message(F.from_user.id.in_(admins), Command("off"))
async def cmd_start(message: Message):
    # TODO написать название группы ламп
    await wled_publish("cubes", "OFF")
    await wled_publish("lamps", "OFF")
    await message.answer('Все выключено')





@admin_router.message(F.from_user.id.in_(admins), Command("random"))
async def cmd_start(message: Message):
    r = lambda: random.randint(150,255)
    # TODO написать название группы ламп
    # TODO выбор из "рандомить для каждого" или "рандомить для группы"
    await wled_publish("cubes/col", '#%02X%02X%02X' % (r(),r(),r()))
    await wled_publish("lamps/col", '#%02X%02X%02X' % (r(),r(),r()))
    await message.answer('Цвет зарандомлен')






@admin_router.message(F.from_user.id.in_(admins), Command("deep_link"))
async def cmd_start(message: Message):
    # TODO добавление payload
    await message.answer('Реферальная ссылка:')