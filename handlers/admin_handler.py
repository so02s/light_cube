from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, BotCommandScopeChat

from aiogram.fsm.context import FSMContext

from utils.filter import admins
import keyboards.all_keyboards as kb
from mqtt.mqtt_handler import wled_publish
from fms.admin_fms import Group, AddModer, DelModer
import random
from create_bot import bot
from db_hanler import db

router = Router()

@router.message(F.from_user.id.in_(admins), Command("cancel"))
async def cancel_chosen(message: Message, state: FSMContext):
    await message.answer('Вы отменили действие')
    await bot.set_my_commands(kb.commands_admin(), BotCommandScopeChat(chat_id=message.from_user.id))
    await state.clear()



@router.message(F.from_user.id.in_(admins), StateFilter(None), Command("add_moder"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Отмена на /cancel')
    await message.answer('Добавьте имя:')
    await state.set_state(AddModer.ch_name)

@router.message(AddModer.ch_name)
async def addmoder_chosen(message: Message, state: FSMContext):
    await db.add_moder(message.text)
    await message.answer(f'Добавлен модератор {message.text}')
    await state.clear()


@router.message(F.from_user.id.in_(admins), StateFilter(None), Command("del_moder"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Отмена на /cancel')
    moders = await db.get_moders()
    await message.answer('Выберете модератора:')
    for i, moder in enumerate(moders):
        await message.answer(f'{i + 1}. {moder}')
    await state.set_state(DelModer.ch_name)

@router.message(DelModer.ch_name)
async def delmoder_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen=message.text)
    await message.answer(message.text)
    await message.answer('Этого модератора вы хотите удалить? Введите "да" или "нет"')
    await state.set_state(DelModer.confirm)

@router.message(DelModer.confirm)
async def confirm_delmoder(message: Message, state: FSMContext):
    if(message.text.lower() == 'да'):
        data = await state.get_data()
        await db.del_moder(data["chosen"])
        await message.answer(f'Модератор {data["chosen"]} удален')
        await state.clear()
    elif(message.text.lower() == 'нет'):
        await message.answer('Напишите имя модератора, которого хотите удалить:')
        await state.set_state(DelModer.ch_name)
    else:
        await message.answer('Я не понимаю. Напишите "да" или "нет"')


@router.message(F.from_user.id.in_(admins), Command("moder"))
async def cmd_start(message: Message, state: FSMContext):
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=message.from_user.id))
    await message.answer('Включен режим модератора. Для возвращения напишите /cancel')
    await state.clear()

@router.message(F.from_user.id.in_(admins), Command("user"))
async def cmd_start(message: Message, state: FSMContext):
    await bot.set_my_commands(kb.commands_user(), BotCommandScopeChat(chat_id=message.from_user.id))
    await message.answer('Включен режим юзера. Для возвращения напишите /cancel')
    await state.clear()

# ------ Включение ламп

@router.message(F.from_user.id.in_(admins), StateFilter(None), Command("on"))
async def cmd_start(message: Message, state: FSMContext):
    # TODO добавить клаву для удобства
    await message.answer('Отмена на /cancel')
    await message.answer('Введите название группы:')
    await state.set_state(Group.ch_name)

@router.message(Group.ch_name)
async def group_chosen(message: Message, state: FSMContext):
    # TODO проверка на существование группы
    if(message.text == 'all'):
        await wled_publish("cubes", "ON")
        await wled_publish("lamps", "ON")
        await message.answer(text=f"Отлично! Свет во всех группах включен.")
    else:
        await wled_publish(message.text, "ON")
        await message.answer(text=f"Отлично! Свет в группе {message.text} включен.")
    await state.clear()


# ------ Выключение ламп

@router.message(F.from_user.id.in_(admins), Command("off"))
async def cmd_start(message: Message):
    # TODO написать название группы ламп
    await wled_publish("cubes", "OFF")
    await wled_publish("lamps", "OFF")
    await message.answer('Все выключено')





@router.message(F.from_user.id.in_(admins), Command("random"))
async def cmd_start(message: Message):
    r = lambda: random.randint(150,255)
    # TODO написать название группы ламп
    # TODO выбор из "рандомить для каждого" или "рандомить для группы"
    await wled_publish("cubes/col", '#%02X%02X%02X' % (r(),r(),r()))
    await wled_publish("lamps/col", '#%02X%02X%02X' % (r(),r(),r()))
    await message.answer('Цвет зарандомлен')






@router.message(F.from_user.id.in_(admins), Command("deep_link"))
async def cmd_start(message: Message):
    # TODO добавление payload
    await message.answer('Реферальная ссылка:')