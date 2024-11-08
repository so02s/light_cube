import asyncio
import subprocess

from aiogram import Router
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.fsm.context import FSMContext

from create_bot import bot
from utils.filter import is_admin, refresh_moders, moders
from db_handler import db
from mqtt.mqtt_handler import wled_publish


router = Router()

@router.message(is_admin, Command("help"))
async def help_admin(msg: Message):
    await msg.answer('''= Команды администратора =
/help - помощь, выводит это сообщение
/brigh {value} - установление яркости (от 0 до 255)
/restart_network - перезагружает подключение
/reboot - перезагрузка raspberry
/deep_link - генерирует 120 реферальных ссылок на кубы (специально на мероприятие)
/deep_link_program - генерирует реферальную ссылу на программу (специально на мероприятие)
/all_moder - выводит всех модераторов
/add_moder {name} - добавляет модератора name
/del_moder - дает удалить модератора на выбор
/cancel - отмена действия, удаление прошлых сообщений
''')

# -------- FSM

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class DelModer(StatesGroup):
    ch_name = State()
    confirm = State()

@router.message(
    is_admin,
    StateFilter(
        DelModer.ch_name,
        DelModer.confirm,
        None
    ),
    Command("cancel")
)
async def edit_answer_repl(
    msg: Message,
    state: FSMContext
):
    await bot.delete_messages(msg.from_user.id, [msg.message_id - i for i in range(100)])
    await bot.delete_messages(msg.from_user.id, [msg.message_id - i for i in range(100, 200)])
    await state.clear()

# Яркость
@router.message(
    is_admin,
    StateFilter(None),
    Command("brigh")
)
async def cmd_start(msg: Message, command: CommandObject):
    args: str = command.args
    if not args:
        await msg.answer('Вы забыли добавить значение\n/brigh {value}')
        return
    brigh = args.split(' ')[0]
    await wled_publish('cubes/api', f'{{"bri": {brigh}}}')

# Все админы
@router.message(
    is_admin,
    StateFilter(None),
    Command("all_moder")
)
async def cmd_start(msg: Message):
    result = moders()
    if(result != []):
        text = 'Модераторы:\n'
        for i, el in enumerate(result):
            text = text + f'{i + 1}. {el}\n'
    else:
        text = 'Нет модераторов'
    await msg.answer(text)

# ---- Добавление модера
@router.message(
    is_admin,
    StateFilter(None),
    Command("add_moder")
)
async def cmd_start(msg: Message, command: CommandObject):
    args: str = command.args
    if not args:
        await msg.answer('Вы забыли добавить имя\n/add_moder {name}')
        return
    
    moder_name = args.split(' ')[0]
    try:
        await db.add_moder(moder_name)
        await msg.answer(f'Добавлен модератор {moder_name}')
        await refresh_moders()
    except Exception as e:
        await msg.answer(f'Error: {str(e)}')
        
# ---- Удаление админа
@router.message(
    is_admin,
    StateFilter(None),
    Command("del_moder")
)
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

# Генерация реферальных ссылок

@router.message(is_admin, StateFilter(None), Command("deep_link"))
async def cmd_start(msg: Message):
    for i in [109]:
        link = await create_start_link(bot, f'cube_{i}', encode=True)
        await msg.answer(link)
        
@router.message(is_admin, StateFilter(None), Command("deep_link_program"))
async def cmd_start(msg: Message):
    link = await create_start_link(bot, f'program', encode=True)
    await msg.answer(link)
    
# emqx
@router.message(
    is_admin,
    StateFilter(None),
    Command("restart_network")
)
async def cmd_restart_network(msg: Message):
    try:
        subprocess.run(["systemctl", "restart", "NetworkManager"], check=True)
        await msg.answer("Служба NetworkManager успешно перезагружена.")
    except subprocess.CalledProcessError as e:
        await msg.answer(f"Ошибка при перезагрузке службы NetworkManager: {e}")
    except Exception as e:
        await msg.answer(f"Произошла непредвиденная ошибка: {e}")
        
        
@router.message(
    is_admin,
    StateFilter(None),
    Command("reboot")
)
async def cmd_reboot(msg: Message):
    try:
        # Перезагрузка системы
        subprocess.run(["sudo", "reboot"], check=True)
        await msg.answer("Система будет перезагружена.")
    except subprocess.CalledProcessError as e:
        await msg.answer(f"Ошибка при перезагрузке системы: {e}")
    except Exception as e:
        await msg.answer(f"Произошла непредвиденная ошибка: {e}")