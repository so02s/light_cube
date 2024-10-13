from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, BotCommandScopeChat

from aiogram.fsm.context import FSMContext

from utils.filter import admins, moders, refresh_moders
import keyboards.all_keyboards as kb
from mqtt.mqtt_handler import wled_publish
from fms.admin_fms import Group, AddModer, DelModer
import random
from create_bot import bot
from db_handler import db

router = Router()

# ------ Отмена действия 
# TODO добавить списки переходов

@router.message(lambda msg: msg.from_user.username in admins(), Command("cancel"))
async def cancel_chosen(msg: Message, state: FSMContext):
    await msg.answer('Вы отменили действие')
    await bot.set_my_commands(kb.commands_admin(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await state.clear()

# ------ Добавление модератора

@router.message(lambda msg: msg.from_user.username in admins(), StateFilter(None), Command("add_moder"))
async def cmd_start(msg: Message, state: FSMContext):
    await msg.answer('Отмена на /cancel')
    await msg.answer('Добавьте имя:')
    await state.set_state(AddModer.ch_name)

@router.message(AddModer.ch_name)
async def addmoder_chosen(msg: Message, state: FSMContext):
    try:
        await db.add_moder(str(msg.text))
        await msg.answer(f'Добавлен модератор {msg.text}')
        await refresh_moders()
    except Exception as e:
        await msg.answer(f'Error: {str(e)}')
    finally:
        await state.clear()

# -------- Вывод всех модераторов

@router.message(lambda msg: msg.from_user.username in admins(), StateFilter(None), Command("all_moder"))
async def cmd_start(msg: Message):
    result = moders()
    if(result != []):
        await msg.answer('Модераторы:')
        for i, el in enumerate(result):
            await msg.answer(f'{i + 1}. {el}')
    else:
        await msg.answer('Нет модераторов')


# ------- Удаление модератора

@router.message(lambda msg: msg.from_user.username in admins(), StateFilter(None), Command("del_moder"))
async def cmd_start(msg: Message, state: FSMContext):
    await msg.answer('Отмена на /cancel')
    await msg.answer('Выберете модератора (индекс):')
    for i, moder in enumerate(moders()):
        await msg.answer(f'{i + 1}. {moder}')
    await state.set_state(DelModer.ch_name)

@router.message(DelModer.ch_name)
async def delmoder_chosen(msg: Message, state: FSMContext):
    try:
        index = int(msg.text) - 1
        if 0 <= index < len(moders()):
            chosen_moder = moders()[index]
            await state.update_data(chosen=chosen_moder)
            await msg.answer(f'Вы выбрали модератора {chosen_moder}')
            await msg.answer('Этого модератора вы хотите удалить? Введите "да" или "нет"')
            await state.set_state(DelModer.confirm)
        else:
            await msg.answer('Некорректный индекс. Пожалуйста, введите номер модератора снова.')
    except ValueError:
        await msg.answer('Некорректный ввод. Пожалуйста, введите номер модератора.')

@router.message(DelModer.confirm)
async def confirm_delmoder(msg: Message, state: FSMContext):
    if(msg.text.lower() == 'да'):
        data = await state.get_data()
        try:
            await db.del_moder(data["chosen"])
            await msg.answer(f'Модератор {data["chosen"]} удален')
        except Exception as e:
            await msg.answer(f'Произошла ошибка: {e}, попробуйте снова')
        finally:
            await refresh_moders()
            await state.clear()
    elif(msg.text.lower() == 'нет'):
        await msg.answer('Напишите индекс модератора, которого хотите удалить:')
        await state.set_state(DelModer.ch_name)
    else:
        await msg.answer('Я не понимаю. Напишите "да" или "нет"')


# ----- Режим модератора

@router.message(lambda msg: msg.from_user.username in admins(), Command("moder"))
async def cmd_start(msg: Message, state: FSMContext):
    await msg.answer('Включен режим модератора. Для возвращения напишите /cancel')
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await state.clear()


# ---- Режим юзера

@router.message(lambda msg: msg.from_user.username in admins(), Command("user"))
async def cmd_start(msg: Message, state: FSMContext):
    await bot.set_my_commands(kb.commands_user(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await msg.answer('Включен режим юзера. Для возвращения напишите /cancel')
    await state.clear()


# ------ Включение ламп

@router.message(lambda msg: msg.from_user.username in admins(), StateFilter(None), Command("on"))
async def cmd_start(msg: Message, state: FSMContext):
    # TODO добавить клаву для удобства
    await msg.answer('Отмена на /cancel')
    await msg.answer('Введите название группы:')
    await state.set_state(Group.ch_name)

@router.message(Group.ch_name)
async def group_chosen(msg: Message, state: FSMContext):
    # TODO проверка на существование группы
    if(msg.text == 'all'):
        await wled_publish("cubes", "ON")
        await wled_publish("lamps", "ON")
        await msg.answer(text=f"Отлично! Свет во всех группах включен.")
    else:
        await wled_publish(msg.text, "ON")
        await msg.answer(text=f"Отлично! Свет в группе {msg.text} включен.")
    await state.clear()


# ------ Выключение ламп

@router.message(lambda msg: msg.from_user.username in admins(), Command("off"))
async def cmd_start(msg: Message):
    # TODO написать название группы ламп
    await wled_publish("cubes", "OFF")
    await wled_publish("lamps", "OFF")
    await msg.answer('Все выключено')





@router.message(lambda msg: msg.from_user.username in admins(), Command("random"))
async def cmd_start(msg: Message):
    r = lambda: random.randint(150,255)
    # TODO написать название группы ламп
    # TODO выбор из "рандомить для каждого" или "рандомить для группы"
    await wled_publish("cubes/col", '#%02X%02X%02X' % (r(),r(),r()))
    await wled_publish("lamps/col", '#%02X%02X%02X' % (r(),r(),r()))
    await msg.answer('Цвет зарандомлен')






@router.message(lambda msg: msg.from_user.username in admins(), Command("deep_link"))
async def cmd_start(msg: Message):
    # TODO добавление payload
    await msg.answer('Реферальная ссылка:')