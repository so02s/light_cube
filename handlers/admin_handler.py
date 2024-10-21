from aiogram import Router, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.types import Message, BotCommandScopeChat
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram.fsm.context import FSMContext
import asyncio

from utils.filter import is_admin, refresh_moders, moders
import keyboards.all_keyboards as kb
from mqtt.mqtt_handler import wled_publish
from fms.admin_fms import Group, AddModer, DelModer
import random
from create_bot import bot
from db_handler import db
from handlers.quiz_handler import QuizMiddleware

router = Router()
router.message.middleware(QuizMiddleware())

# ------ Отмена действия 
# TODO добавить списки переходов

@router.message(is_admin, Command("cancel"))
async def cancel_chosen(msg: Message, state: FSMContext):
    await msg.answer('Вы отменили действие')
    await bot.set_my_commands(kb.commands_admin(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await state.clear()

# ------ Добавление модератора

@router.message(is_admin, StateFilter(None), Command("add_moder"))
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

@router.message(is_admin, StateFilter(None), Command("all_moder"))
async def cmd_start(msg: Message):
    result = moders()
    if(result != []):
        await msg.answer('Модераторы:')
        for i, el in enumerate(result):
            await msg.answer(f'{i + 1}. {el}')
    else:
        await msg.answer('Нет модераторов')


# ------- Удаление модератора

@router.message(is_admin, StateFilter(None), Command("del_moder"))
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

@router.message(is_admin, Command("moder"))
async def cmd_start(msg: Message, state: FSMContext):
    await msg.answer('Включен режим модератора. Для возвращения напишите /cancel')
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await state.clear()


# ---- Режим юзера

@router.message(is_admin, Command("user"))
async def cmd_start(msg: Message, state: FSMContext):
    await bot.set_my_commands(kb.commands_user(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await msg.answer('Включен режим юзера. Для возвращения напишите /cancel')
    await state.clear()


# ------ Включение ламп


@router.message(is_admin, StateFilter(None), Command("on"))
async def group_chosen(msg: Message, command: CommandObject):
    args: str = command.args
    if args:
        group_name = args[0]
        await wled_publish(group_name, "ON")
        await msg.answer(text=f"Свет в группе {group_name} включен")
        return
    
    await wled_publish("cubes", "ON")
    await wled_publish("lamps", "ON")
    await msg.answer('Все включено')


# ------ Выключение ламп

@router.message(is_admin, Command("off"))
async def cmd_start(msg: Message, command: CommandObject):
    args: str = command.args
    if args:
        group_name = args[0]
        await wled_publish(group_name, "OFF")
        await msg.answer(f'Группа {group_name} выключена')
        return
    
    await wled_publish("cubes", "OFF")
    await wled_publish("lamps", "OFF")
    await msg.answer('Все выключено')


# ------- Рандом цвет всего

@router.message(is_admin, Command("random"))
async def random_color(msg: Message, command: CommandObject):
    r = lambda: random.randint(150,255)
    args: str = command.args
    if args:
        group_name = args[0]
        await wled_publish("cubes/" + group_name, '#%02X%02X%02X' % (r(),r(),r()))
        return
    
    await wled_publish("cubes/col", '#%02X%02X%02X' % (r(),r(),r()))
    await wled_publish("lamps/col", '#%02X%02X%02X' % (r(),r(),r()))
    await msg.answer('Цвет зарандомлен')

# ------- Цвет всего

@router.message(is_admin, Command("color"))
async def cmd_start(msg: Message, command: CommandObject):
    args: str = command.args
    if not args:
        await random_color(msg)
        return
    
    color = args[0]
    hex_color_pattern = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
    if not hex_color_pattern.match(color):
        await msg.answer('Неверный формат цвета. Пожалуйста, используйте HEX формат (например, #FF5733).')
        return
    
    # TODO группа
    await wled_publish("cubes/col", color)
    await wled_publish("lamps/col", color)
    await msg.answer('Цвет добавлен')

# ------ Генерация реферальных ссылок для кубов от 1 до 120

@router.message(is_admin, Command("deep_link"))
async def cmd_start(msg: Message):
    refs='Реферальные ссылки:\n'
    end = 121
    for i in range(1, end):
        if(i % 30 == 0):
            asyncio.sleep(30)
        link = await create_start_link(bot, f'cube_{i}', encode=True)
        await msg.answer(link)