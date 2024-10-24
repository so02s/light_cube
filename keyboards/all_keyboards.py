from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from db_handler import db

def get_management_keyboard():
    buttons = [
        [   InlineKeyboardButton(text="Управление кубами", callback_data="cube_management")],
        [   InlineKeyboardButton(text="Управление квизом", callback_data="quiz_management")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_cube_keyboard():
    buttons = [
        [   InlineKeyboardButton(text="Назад", callback_data="moder_panel")],
        [
            InlineKeyboardButton(text="Вкл", callback_data="cube_on"),
            InlineKeyboardButton(text="Выкл", callback_data="cube_off")
        ],
        [   InlineKeyboardButton(text="Пресеты", callback_data="cube_presets")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_color_blink_keyboard():
    buttons = [
        [   InlineKeyboardButton(text="Назад", callback_data="cube_management")],
        [
            InlineKeyboardButton(text="Вкл мигание", callback_data="blink_on"),
            InlineKeyboardButton(text="Выкл мигание", callback_data="blink_off")
        ],
        [
            InlineKeyboardButton(text="Красный", callback_data="color_#FF0000"),
            InlineKeyboardButton(text="Синий", callback_data="color_#0000CD"),
            InlineKeyboardButton(text="Желтый", callback_data="color_#FFFF00")
        ],
        [
            InlineKeyboardButton(text="Оранжевый", callback_data="color_#FF4500"),
            InlineKeyboardButton(text="Зеленый", callback_data="color_#00FF00"),
            InlineKeyboardButton(text="Фиолетовый", callback_data="color_#800080")
        ],
        [
            InlineKeyboardButton(text="Голубой", callback_data="color_#20B2AA"),
            InlineKeyboardButton(text="Розовый", callback_data="color_#FF00FF"),
            InlineKeyboardButton(text="Песочный", callback_data="color_#F0E68C")
        ],
        [
            InlineKeyboardButton(text="Черный", callback_data="color_#000000"),
            InlineKeyboardButton(text="Белый", callback_data="color_#FFFFFF")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_quiz_keyboard():
    buttons = [
        [   InlineKeyboardButton(text="Назад", callback_data="moder_panel")],
        [   InlineKeyboardButton(text="Начать квиз", callback_data="start_quiz")],
        [   InlineKeyboardButton(text="Изменить программу", callback_data="change_program")],
        [
            InlineKeyboardButton(text="Добавить квиз", callback_data="add_quiz"),
            InlineKeyboardButton(text="Изменить квиз", callback_data="edit_quiz")
        ],
        [   InlineKeyboardButton(text="Удалить квиз", callback_data="delete_quiz")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_all_quizs_keyboard(action: str):
    try:
        quizs = await db.get_quizs()
    except:
        return get_quiz_keyboard()

    buttons = []
    if not quizs:
        buttons.append([InlineKeyboardButton(text='Нет квизов', callback_data='no_data')])
    else:
        for quiz in quizs:
            buttons.append([InlineKeyboardButton(text=quiz.name, callback_data=f"quiz_{quiz.id}")])

    buttons.append([InlineKeyboardButton(text="Назад", callback_data="quiz_management")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard





# Старое

def commands_admin():
    return [
                BotCommand(command='start', description='Старт'),
                BotCommand(command='help', description='Помощь'),
                BotCommand(command='moder', description='Режим модератора'),
                BotCommand(command='user', description='Режим юзера'),
                BotCommand(command='on', description='Включить свет'),
                BotCommand(command='off', description='Выключить свет'),
                BotCommand(command='color', description='Установка цвета'),
                BotCommand(command='random', description='Поменять на рандомный цвет'),
                BotCommand(command='deep_link', description='Создать реферальную ссылку для кубов'),
                BotCommand(command='deep_link_program', description='Создать реферальную ссылку для программы мероприятия'),
                BotCommand(command='all_moder', description='Все модераторы'),
                BotCommand(command='add_moder', description='Добавить модератора'),
                BotCommand(command='del_moder', description='Удалить модератора'),
                BotCommand(command='cancel', description='Отмена действия')
            ]


def commands_moder():
    return [
                BotCommand(command='start', description='Старт'), 
                BotCommand(command='help', description='Помощь'),
                BotCommand(command='change_program', description='Изменить сообщение о программе мероприятия. Еще не работает'),
                BotCommand(command='all_quiz', description='Вывести все квизы'),
                BotCommand(command='start_quiz', description='Начать квиз'),
                BotCommand(command='add_quiz', description='Добавить квиз'),
                BotCommand(command='del_quiz', description='Удалить квиз'),
                BotCommand(command='change_quiz', description='Изменить квиз'),
                # BotCommand(command='user', description='Режим юзера'),
                BotCommand(command='cancel', description='Отмена действия')
            ]

def commands_change_quiz():
    return [
                BotCommand(command='cancel', description='Выход из изменения квиза'),
                BotCommand(command='help', description='Помощь'),
                BotCommand(command='all_info', description='Информация о квизе'),
                BotCommand(command='add_question', description='Добавить вопрос'), 
                BotCommand(command='del_question', description='Удалить вопрос'),
                # BotCommand(command='change_question', description='Изменить вопрос'),
                BotCommand(command='change_start_time', description='Изменить время начала квиза')
            ]
    
def commands_change_question():
    return [
                BotCommand(command='cancel', description='Выход из изменения вопроса'),
                BotCommand(command='help', description='Помощь'),
                BotCommand(command='question_info', description='Вывод информации о вопросе'),
                BotCommand(command='change_time', description='Изменить время на вопрос'),
                BotCommand(command='add_answer', description='Добавить ответ к вопросу'),
                BotCommand(command='del_answer', description='Удалить ответ с подтверждением'),
                BotCommand(command='change_answer', description='Изменить ответ на вопрос')
            ]

def commands_change_answer():
    return [
                BotCommand(command='cancel', description='Выход из изменения ответа'),
                BotCommand(command='help', description='Помощь'),
                BotCommand(command='answer_info', description='Вывод информации о ответе'),
                BotCommand(command='change_correctness', description='Изменить правильность ответа'),
                BotCommand(command='change_text', description='Изменить текст ответа'),
                BotCommand(command='change_color', description='Изменить цвет ответа')
            ]

def commands_user():
    return [BotCommand(command='start', description='Старт')]