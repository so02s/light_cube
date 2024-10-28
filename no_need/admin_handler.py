import random, re, asyncio

from aiogram import Router
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.types import Message, BotCommandScopeChat
from aiogram.utils.deep_linking import create_start_link
from aiogram.fsm.context import FSMContext

from create_bot import bot
import keyboards.all_keyboards as kb
from utils.filter import is_admin, refresh_moders, moders
from fms.admin_fms import DelModer
from db_handler import db
from mqtt.mqtt_handler import wled_publish
from handlers.quiz_handler import QuizMiddleware

router = Router()
router.message.middleware(QuizMiddleware())

# ------ Помощь

@router.message(is_admin, Command("help"))
async def help_admin(msg: Message):
    await msg.answer('''= Команды модератора =
/change_program - изменить сообщение о программе мероприятия. Еще не работает
/all_quiz - вывести все квизы
/start_quiz {name} - начать квиз name, без аргумента перекидывает в выбор квиза
/add_quiz {name} - добавить квиз name с началом в time, без аргумента спрашивает и про название, и про время
/del_quiz {name} - удаляет квиз name (с подтверждением), если нет аргумента, то дает выбрать квиз для удаления
/change_quiz {name} - изменить квиз name, если нет аргумента, то дает выбрать квиз
/cancel - отмена действия
''')
    await msg.answer('''= Команды администратора =
/start - стартовое сообщение
/help - помощь, выводит это сообщение
/moder - переключиться в режим модератора
/user - переключиться в режим юзера (тебе приходят вопросы с квиза)
/on {group} - включает группу, если нет аргумента, то все группы
/off {group} - выключает группу, если нет аргумента, то все группы
/color {HEX} {group} - изменяет цвет группы на выставленный, если нет аргумента, то на рандомный
/random {group} - изменяет цвет группы на рандомный, если нет аргумента, то все группы
/deep_link - генерирует 120 реферальных ссылок на кубы (специально на мероприятие)
/deep_link_program - генерирует реферальную ссылу на программу (специально на мероприятие)
/all_moder - выводит всех модераторов
/add_moder {name} - добавляет модератора name
/del_moder - дает удалить модератора на выбор
/cancel - отмена действия
''')

# ------ Отмена действия 

@router.message(Command("cancel"),
                StateFilter(DelModer.ch_name,
                            DelModer.confirm))
async def cancel_chosen(msg: Message, state: FSMContext):
    await msg.answer('Вы отменили действие')
    await bot.set_my_commands(kb.commands_admin(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await state.clear()

# ----- Режим модератора

@router.message(is_admin, StateFilter(None), Command("moder"))
async def cmd_start(msg: Message):
    await msg.answer('Включен режим модератора. Для возвращения напишите /start')
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))

# ---- Режим юзера
@router.message(is_admin, StateFilter(None), Command("user"))
async def cmd_start(msg: Message):
    await bot.set_my_commands(kb.commands_user(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await msg.answer('Включен режим юзера. Для возвращения напишите /start')

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
        
# ------ Добавление модератора

@router.message(is_admin, StateFilter(None), Command("add_moder"))
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


# ------ Включение ламп


@router.message(is_admin, StateFilter(None), Command("on"))
async def group_chosen(msg: Message, command: CommandObject):
    args: str = command.args
    if args:
        group_name = args.split(' ')[0]
        await wled_publish(group_name, "ON")
        await msg.answer(text=f"Свет в группе {group_name} включен")
        return
    
    await wled_publish("cubes", "ON")
    await wled_publish("lamps", "ON")
    await msg.answer('Все включено')


# ------ Выключение ламп

@router.message(is_admin, StateFilter(None), Command("off"))
async def cmd_start(msg: Message, command: CommandObject):
    args: str = command.args
    if args:
        group_name = args.split(' ')[0]
        await wled_publish(group_name, "OFF")
        await msg.answer(f'Группа {group_name} выключена')
        return
    
    await wled_publish("cubes", "OFF")
    await wled_publish("lamps", "OFF")
    await msg.answer('Все выключено')


# ------- Рандом цвет всего

@router.message(is_admin, StateFilter(None), Command("random"))
async def random_color(msg: Message, command: CommandObject):
    r = lambda: random.randint(150,255)
    group_name: str = command.args
    if group_name:
        await wled_publish(group_name + "/col", '#%02X%02X%02X' % (r(),r(),r()))
        await msg.answer(f'Цвет в группе {group_name} зарандомлен')
        return
    
    await wled_publish("cubes/col", '#%02X%02X%02X' % (r(),r(),r()))
    await wled_publish("lamps/col", '#%02X%02X%02X' % (r(),r(),r()))
    await msg.answer('Цвет зарандомлен')

# ------- Цвет всего

@router.message(is_admin, StateFilter(None), Command("color"))
async def cmd_start(msg: Message, command: CommandObject):
    args: str = command.args
    if not args:
        await random_color(msg, command)
        return
    args_list = args.split(' ')
    color = args_list[0]
    hex_color_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    if not hex_color_pattern.match(color):
        await msg.answer('Возможно, вы ввели команду не в том порядке.\n/color {HEX} {group}\nЛибо неверный формат цвета. Пожалуйста, используйте HEX формат (например, #FF5733).')
        return
    
    if len(args_list) >= 2:
        group_name = args_list[1]
        await wled_publish(group_name + "/col", color)
        await msg.answer(f'Цвет в группу {group_name} добавлен')
        return
    
    await wled_publish("cubes/col", color)
    await wled_publish("lamps/col", color)
    await msg.answer('Цвет добавлен')

# ------ Генерация реферальных ссылок для кубов от 1 до 120

@router.message(is_admin, StateFilter(None), Command("deep_link"))
async def cmd_start(msg: Message):
    end = 121
    for i in range(1, end):
        if(i % 30 == 0):
            await asyncio.sleep(30)
        link = await create_start_link(bot, f'cube_{i}', encode=True)
        await msg.answer(link)
        
@router.message(is_admin, StateFilter(None), Command("deep_link_program"))
async def cmd_start(msg: Message):
    link = await create_start_link(bot, f'program', encode=True)
    await msg.answer(link)