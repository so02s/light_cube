from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from db_handler import db
from keyboards.callback_handler import QuizCallbackFactory

def get_no_buttons():
    return InlineKeyboardMarkup()

def get_management_kb():
    buttons = [
        [   InlineKeyboardButton(text="Управление кубами", callback_data="cube_management")],
        [   InlineKeyboardButton(text="Квизы и мероприятие", callback_data="quiz_management")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def get_cube_kb():
    buttons = [
        [   InlineKeyboardButton(text="Назад", callback_data="moder_panel")],
        [
            InlineKeyboardButton(text="Вкл", callback_data="cube_on"),
            InlineKeyboardButton(text="Выкл", callback_data="cube_off")
        ],
        [   InlineKeyboardButton(text="Пресеты", callback_data="cube_presets")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def get_color_blink_kb():
    buttons = [
        [   InlineKeyboardButton(text="Назад", callback_data="cube_management")],
        [
            InlineKeyboardButton(text="Красный", callback_data="color_#FF0000"),
            InlineKeyboardButton(text="Синий", callback_data="color_#0000CD"),
        ],
        [
            InlineKeyboardButton(text="Медленное мигание", callback_data="blink"),
            InlineKeyboardButton(text="Быстрое мигание", callback_data="fast_blink"),
            InlineKeyboardButton(text="Выкл мигание", callback_data="blink_off")
        ],
        [
            InlineKeyboardButton(text="Все", callback_data="one_color"),
            InlineKeyboardButton(text="Половина", callback_data="two_color"),
            InlineKeyboardButton(text="Рандомная половина", callback_data="two_color_random")
        ]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def get_quiz_kb():
    buttons = [
        [   InlineKeyboardButton(text="Назад", callback_data="moder_panel")],
        [   InlineKeyboardButton(text="Начать квиз", callback_data="start_quiz")],
        [   InlineKeyboardButton(text="Программа", callback_data="event_program")],
        [
            InlineKeyboardButton(text="Добавить квиз", callback_data="add_quiz"),
            InlineKeyboardButton(text="Изменить квиз", callback_data="edit_quiz")
        ],
        [   InlineKeyboardButton(text="Удалить квиз", callback_data="delete_quiz")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

async def get_all_quizs_kb(action: str):
    builder = InlineKeyboardBuilder()
    
    try:
        quizs = await db.get_quizs()
    except:
        return get_quiz_kb()
    
    if not quizs:
        builder.button(text='Нет квизов', callback_data='no_data')
    else:
        for quiz in quizs:
            builder.button(
                text=quiz.name,
                callback_data=QuizCallbackFactory(quiz_id=quiz.id, action=action)
            )
    builder.button(text="Назад", callback_data="quiz_management")
    builder.adjust(1)

    return builder.as_markup()

def get_edit_quiz_kb():
    buttons = [
        [InlineKeyboardButton(text="Изменить время начала", callback_data="change_start_time")],
        [InlineKeyboardButton(text="Изменить вопрос", callback_data="change_question")],
        [InlineKeyboardButton(text="Добавить вопрос", callback_data="add_question")],
        [InlineKeyboardButton(text="Удалить вопрос", callback_data="delete_question")],
        [InlineKeyboardButton(text="Назад", callback_data="quiz_management")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def get_confirm_delete_kb(quiz_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data=QuizCallbackFactory(quiz_id=quiz_id, action='confirm delete'))
    builder.button(text="Назад", callback_data="quiz_management")
    builder.adjust(1)
    return builder.as_markup()

def get_delete_done_kb():
    buttons = [[InlineKeyboardButton(text="Хорошо", callback_data='quiz_management')]]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

# TODO хэндлер для удаления этого сообщения и возврета на quiz_manadger
def get_event_program_kb():
    buttons = [
        [InlineKeyboardButton(text="Изменить программу", callback_data="edit_program")],
        [InlineKeyboardButton(text="Назад", callback_data="back_from_event_program")], 
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb



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
